# -*- coding: utf-8 -*-
import search
import sys
import time
from itertools import permutations
from collections import defaultdict
from copy import deepcopy, copy



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
    
    def updateCost(self, patient):
        self.cost += patient
    # def computeCost(self):
    #     for i in self.patientDict.keys():
    #         self.cost += self.patientDict[i].timePassed**2



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
#->> THIS SHIT DOOMED, BRAIN HURTS        
        # #Check for redundant pairs
        # for x in combinations(list(s.remainingPatients.keys()),2):
        #     if s.remainingPatient[x[0]].labelCode == s.remainingPatient[x[1]].labelCode:
        #         if s.remainingPatient[x[0]].timePassed == s.remainingPatient[x[1]].timePassed:
        #             same_gang.append(list(x)) #-> list of redundant pairs (not sure if working properly)

#psuedo code for same gang
# if x1,...,xn are same state(label and waited time same)
# check actions with x1,...,xn for their position and erase all actions that are redundant
# example: if x1,x2 same gang
# detect actions with x1,x2, ex: [003,x1,004,x2]
# erase all actions that change x1 and x2 between themselves, as they are redundant
# how? idk lol   

        
# [[002,006],[001,003]]

# [002,006,x],[002,x,006],[x,002,006]

# [002,004,005,006,001]->[006,004,005,002,001]

# [002,003,006]
       
       
       
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

            if not invalid: 
                #print("CRL")
                   actapp(list(zip(list(self.medicDict.keys()),i))) 
        #print("Actions\n")
        
        #print(actions)
        return actions

    #returns the obtained state after applying the action a to state s
    def result(self,s,a):

        #Create a new state, by copying state s
        new_s = deepcopy(s)

        #List with the pacients who are currently in a consultation
        patients_attended = []
        #Considering 1 action as number of medics singleActions
        for singleAction in a:
            if singleAction[1] is not "empty":
                #Increase patient's passed  time in a consultation
                medic_rate = self.medicDict[singleAction[0]].getRate()
                new_s.patientDict[str(singleAction[1])].incPassedTime(float(medic_rate),1)

                #Remove the patient from the patient's dictionary if he has reached the total Consultation Time
                if new_s.patientDict[str(singleAction[1])].getTimePassedConsult() >= self.getLabelDict()[new_s.patientDict[str(singleAction[1])].getLabel()].getConsultationTime():
                    del new_s.remainingPatients[str(singleAction[1])]

                #Store patients who are in a consultation 
                patients_attended.append(singleAction[1])
            #Add the new consultation to the new_s consultations dictionary
            new_s.consultations[str(singleAction[0])].append(str(singleAction[1]))
         
        #Increase the waiting time in every patient who is not in a consultation at this moment in new_s
        for x in new_s.remainingPatients.keys():
            if x not in patients_attended:
                new_s.patientDict[str(x)].incPassedTime()

            ##Actions não deve deixar isto acontecer!
            # Check if any patient has exceeded the Maximum Waiting Time 
            # if new_s.getPatientDict()[str(x)].getTimePassed() > self.getLabelDict()[new_s.getPatientDict()[str(x)].getLabel()].getMaxWaitingTime():
            #        new_s.deadend = 1
        
        
        return new_s

    #receives a state and checks if it is a goal state 
    def goal_test(self,s):
        return not bool(s.remainingPatients)



    #receives 2 states and the cost of the 1st one; returns the cost of the 2nd 
    def path_cost(self,c,s1,a,s2):

        state2_cost = 0

        for key in s2.patientDict.keys():
            state2_cost += s2.patientDict[key].getTimePassed()**2    

        s2.cost = state2_cost
        s2.getStatus()
        print("\nDiff:" + str(state2_cost - c) + "\n")
        return (state2_cost - c)




    def load(self,f):
        initialCost = 0
        if(".txt" in f):
                prob_file = open(f,"r")
                line_info = prob_file.readlines()
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
        else:
            sys.exit("Wrong file format, exiting...\n")

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
        f.close()

    def search(self, p):
        self.solution = search.astar_search(p, p.heuristic)
        #self.solution = search.uniform_cost_search(p)
        if self.solution  is not None:
            print("Found Solution")
            return True
        else: 
            print("Infeas")
            return False

    def heuristic(self, n):
        attenuation = 0.0
        bias =  1 - (len(n.state.remainingPatients.keys())/len(n.state.patientDict.keys()))
        weight = n.state.cost*bias
        return -weight
        