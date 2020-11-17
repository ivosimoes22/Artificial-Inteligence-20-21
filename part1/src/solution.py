# -*- coding: utf-8 -*-
import search
import sys
import time
from itertools import permutations, combinations
from collections import defaultdict
from copy import deepcopy, copy

from utils import print_table

class Doctor():
    def __init__(self, code, efficiencyRate):
        self.code = code
        self.rate = efficiencyRate

    #getters
    def getCode(self):
        return self.code
    def getRate(self):
        return self.rate

class Patient():
    def __init__(self, code, timePassed, labelCode):
        self.code = code
        self.timePassed = float(timePassed)
        self.labelCode = labelCode
        self.timePassedConsult = 0

    #gettters
    def getCode(self):
        return self.code
    def getTimePassed(self):
        return self.timePassed
    def getLabel(self):
        return self.labelCode
    def getTimePassedConsult(self):
        return self.timePassedConsult

    def incPassedTime(self, rateDoc=1, isConsult=0):
        if isConsult:
            self.timePassedConsult += 5*rateDoc
        else:
            self.timePassed += 5


class Label():
    def __init__(self, code, maxWaitingTime, consultationTime):
        self.code = code
        self.maxWaitingTime = int(maxWaitingTime)
        self.consultationTime = int(consultationTime)

    #getters
    def getCode(self):
        return self.code
    def getMaxWaitingTime(self):
        return self.maxWaitingTime
    def getConsultationTime(self):
        return self.consultationTime

class State():
    def __init__(self, patientDict=None, remainingPatients=None, consultations=None, mediclistkeys = None, c=0):
        self.patientDict = {}
        self.remainingPatients = {}
        self.consultations = defaultdict(list)
        if patientDict is not None:
            self.patientDict = deepcopy(patientDict)        
        if consultations is not None:
            self.consultations = deepcopy(consultations)
        if remainingPatients is not None:
            self.remainingPatients = deepcopy(remainingPatients)
        # if mediclistkeys is not None:
        #     self.consultations = dict.fromkeys(mediclistkeys, [])
        self.cost = c

    def __lt__(self, other):
        return self.cost < other.cost

    def getPatientDict(self):
        return self.patientDict

    def getConsultations(self):
        return self.consultations

    def getStatus(self):
        for x in self.patientDict.keys():
            print("Code " + str(self.patientDict[x].getCode()))
            print("Time Waiting " + str(self.patientDict[x].getTimePassed()))
            print("Time Consultation " + str(self.patientDict[x].getTimePassedConsult()))
            print("Consultations: " + str(self.consultations))
            print("Cost: " + str(self.cost))
            print("\n")

    def setPatientDict(self, patientDict):
        self.patientDict = patientDict


class PDMAProblem(search.Problem):
    
    #Constructor
    def __init__(self):
        self.medicDict = {}
        self.labelDict = {}
        self.patientDict = {}
        self.initial = State()
        self.solution = 0
    
    #Getters
    def getMedicDict(self):
        return self.medicDict
    def getLabelDict(self):
        return self.labelDict
    def getPatientDict(self):
        return self.patientDict

    #returns a list with the actions that can be applied to state s
    def actions(self,s):
        actions = [] #[destination_doctor,patient]
        urgent_patients = []
        same_gang = []
        actapp = actions.append
        urgapp = urgent_patients.append

        invalid = 0
        for patient in s.remainingPatients.keys():
            if(s.patientDict[patient].timePassed >= self.labelDict[s.patientDict[patient].labelCode].maxWaitingTime):
                urgapp(patient)
        if len(urgent_patients) > len(list(self.medicDict.keys())):
            return actions
       
        # #Check for redundant pairs
        for x in combinations(list(s.remainingPatients.keys()),2):
            if s.remainingPatients[x[0]].labelCode == s.remainingPatients[x[1]].labelCode:
                if s.patientDict[x[0]].timePassed == s.patientDict[x[1]].timePassed:
                    if s.patientDict[x[0]].timePassedConsult == s.patientDict[x[1]].timePassedConsult: #maybe they need to have same total time in consultation, cause of goal state i guess
                    #maybe try with this:
                    #if (s.labelDict[patientDict[x[0]].labelCode].consultationTime - s.patientDict[x[0]].timePassedConsult) == (s.labelDict[patientDict[x[1]].labelCode].consultationTime) - s.patientDict[x[1]].timePassedConsult:
                    #CAN WE CONSIDER 2 PATIENTS WITH SAME TIME REMAINING IN CONSULTATION AND SAME TIME WAITING AS REDUNDANT????? THEORY CRAFT ON THIS
                        same_gang.append(list(x)) #-> list of redundant patients (not sure if working properly)
        #print("Redundant Lads")              
        #print(same_gang)
        # for x in s.remainingPatients.keys():
        #     for notx in s.remainingPatients.keys():
        #         if x is not notx:
        #             if s.remain


        # print("ugernt guys\n")
        # print(urgent_patients)    
        new_patient_list = list(s.remainingPatients.keys())
        new_p_app = new_patient_list.append
        if len(list(s.remainingPatients.keys())) <  len(list(self.medicDict.keys())):
            diff = len(list(self.medicDict.keys())) - len(list(s.remainingPatients.keys())) 
            for _ in range(diff):
                new_p_app("empty")
                
        permuts = permutations(new_patient_list, len(list(self.medicDict.keys())))       
        actapp = actions.append
        for i in permuts:
            invalid = 0
            #print(i)
            for urg in urgent_patients:
                if urg not in i:
                    invalid = 1
                    #print("bruh moment")
                    break         
            #[x,x,x,x,2,x]->[x,x,x,3,x]       
            for redun in same_gang: #ex.[2,3]
                try: 
                    index0 = i.index(redun[0]) 
                except ValueError:
                    try: 
                        index0 = i.index(redun[1]) 
                        invalid = 1
                        break
                    except ValueError:
                        continue
                try: 
                    index1 = i.index(redun[1])
                    if(index0 > index1):
                        invalid = 1
                        break
                except ValueError:
                    continue

            if not invalid: 
                #print("CRL")
                   actapp(list(zip(list(self.medicDict.keys()),i))) 
        #print("Actions\n")
        return actions


    #returns the obtained state after applying the action a to state s
    def result(self,s,a):

        #Create a new state, by copying state s
        new_s = deepcopy(s)

        #List with the pacients who are currently in a consultation
        patients_attended = []
        #Considering 1 action as number of medics singleActions
        for singleAction in a:
            if singleAction[1] != "empty":
                #Increase patient's passed  time in a consultation
                medic_rate = self.medicDict[singleAction[0]].rate
                new_s.patientDict[str(singleAction[1])].incPassedTime(float(medic_rate),1)

                #Remove the patient from the patient's dictionary if he has reached the total Consultation Time
                if new_s.patientDict[str(singleAction[1])].timePassedConsult >= self.labelDict[new_s.patientDict[str(singleAction[1])].labelCode].consultationTime:
                    del new_s.remainingPatients[str(singleAction[1])]

                #Store patients who are in a consultation 
                patients_attended.append(singleAction[1])
            #Add the new consultation to the new_s consultations dictionary
            new_s.consultations[str(singleAction[0])].append(str(singleAction[1]))
         
        #Increase the waiting time in every patient who is not in a consultation at this moment in new_s
        for x in new_s.remainingPatients.keys():
            if x not in patients_attended:
                new_s.patientDict[str(x)].incPassedTime()
        
        
        return new_s


    #receives a state and checks if it is a goal state 
    def goal_test(self,s):
        return not bool(s.remainingPatients)


    #receives 2 states and the cost of the 1st one; returns the cost of the 2nd 
    def path_cost(self,c,s1,a,s2):

        state2_cost = 0

        for key, p in s2.patientDict.items():
            state2_cost += p.timePassed**2    

        s2.cost = state2_cost
        #s2.getStatus()
        #print("\nDiff:" + str(state2_cost - c) + "\n")
        return (state2_cost - c)


    def load(self,f):
        initialCost = 0
        line_info = f.readlines()
        for line in line_info:
            if ("MD" in line):
                temp = line.split()
                temp.append(0)
                self.medicDict[str(temp[1])] = Doctor(temp[1], temp[2])
            elif("PL" in line):
                temp = line.split()
                self.labelDict[str(temp[1])] = Label(temp[1], temp[2], temp[3])
            elif("P " in line):
                temp = line.split()
                temp.append(0)
                self.patientDict[str(temp[1])] = Patient(temp[1], temp[2], temp[3])

        for key in self.patientDict:
            initialCost += self.patientDict[key].getTimePassed()**2

        self.initial = State(self.patientDict,self.patientDict, None, self.medicDict.keys(), initialCost)

        
    def save(self, f):
        consultations = self.solution.state.consultations
        for key, medicConsultations in consultations.items():
            f.write("MD " + key + " ")
            for singleConsultation in medicConsultations:
                f.write(singleConsultation + " ")
            f.write("\n")


    def search(self):
        self.solution = search.astar_search(self, self.heuristic)
        #self.solution = search.uniform_cost_search(p)
        if self.solution  is not None:
            return True
        else:
            return False

    '''
    def heuristic(self, n):
        ns = deepcopy(n.state)

        my_cost = 0
        
        #Perform this operation number of doctors times
        for i in range(len(self.medicDict)):

            #Check if there are any patients left
            if bool(ns.remainingPatients) == True:

                max_val = 0
                max_key = 0

                #Find the patient who has been waiting for the longest time 
                for patient in ns.remainingPatients:
                    if ns.remainingPatients[patient].timePassed >= max_val:
                        max_val = ns.remainingPatients[patient].timePassed
                        max_key = patient

                #Remove the patient from the remaing patients dictionary
                del ns.remainingPatients[max_key]


        #Increment every remaining patient's waiting time
        for x in ns.remainingPatients:
                ns.patientDict[str(x)].incPassedTime()

        #Calculate this state's cost
        for key in ns.patientDict:
            my_cost += ns.patientDict[key].getTimePassed()**2

        
        return (my_cost - n.state.cost)
    
    '''
    def heuristic(self, n):
        s=n.state
        my_cost = 0
        i = 0
        time_to_complete = []
        time_waited = []
        complete_app = time_to_complete.append
        waited_app = time_waited.append

        if len(s.remainingPatients) <= len(self.medicDict):
            return 0

        for patient in s.patientDict:
            if (self.labelDict[s.patientDict[patient].labelCode].consultationTime - s.patientDict[patient].timePassedConsult) <= 0:
                my_cost += s.patientDict[patient].timePassed**2

        for patient in s.remainingPatients:
            complete_app(self.labelDict[s.patientDict[patient].labelCode].consultationTime - n.state.patientDict[patient].timePassedConsult)
            waited_app(n.state.patientDict[patient].timePassed)

        time_to_complete.sort(key=int)
        time_waited.sort(key=int, reverse=True)

        while len(self.medicDict) < len(time_to_complete):
            #print(tuple(time_to_complete))
            #print(tuple(time_waited))
            #input()
            for i in range(len(time_to_complete)):
                if i < len(self.medicDict):
                    time_to_complete[i] -= 5
                else:
                    time_waited[i] += 5
            j=0 #avoid index -1
            for i in range(len(self.medicDict)):
                if time_to_complete[j] <= 0:
                    del time_to_complete[j]
                    my_cost += time_waited[j]**2
                    del time_waited[j]
                    j -= 1
                else: 
                    break
                j += 1

        for i in range(len(time_waited)):
            my_cost += time_waited[i]**2

        if (my_cost - n.state.cost) < 0:
            print(my_cost - n.state.cost)
            input()
        return (my_cost - n.state.cost)
        