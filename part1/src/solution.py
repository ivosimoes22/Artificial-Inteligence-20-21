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
        #Code of the doctor
        self.code = code
        #Rate of the doctor
        self.rate = efficiencyRate

class Patient():
    def __init__(self, code, timePassed, labelCode):
        #Code of the patient
        self.code = code
        #Time passed before the consultation
        self.timePassed = float(timePassed)
        #Code of the label associated
        self.labelCode = labelCode
        #Time spent in a consultation
        self.timePassedConsult = 0

    #Returns the the time passed
    def incPassedTime(self, rateDoc=1, isConsult=0):
        #if the patient is in a consultation, the time multiplies with the rate of the doctor
        if isConsult:
            self.timePassedConsult += 5*rateDoc
        #if not, increases five minutes to waiting time of the patient
        else:
            self.timePassed += 5


class Label():
    def __init__(self, code, maxWaitingTime, consultationTime):
        #Code of the label
        self.code = code
        #Maximum wating time a patient can wait
        self.maxWaitingTime = int(maxWaitingTime)
        #Time needed for a consultation
        self.consultationTime = int(consultationTime)


class State():
    def __init__(self, patientDict=None, remainingPatients=None, consultations=None, mediclistkeys = None, c=0):
        #Dictionary with the patients
        self.patientDict = {}
        #Dictionary with patients that have not finished their consultation
        self.remainingPatients = {}
        #Dictionary that keeps track of the executed consultations
        self.consultations = defaultdict(list)
        
        if patientDict is not None:
            self.patientDict = deepcopy(patientDict)        
        if consultations is not None:
            self.consultations = deepcopy(consultations)
        if remainingPatients is not None:
            self.remainingPatients = deepcopy(remainingPatients)
        self.cost = c

    def __lt__(self, other):
        return self.cost < other.cost

    #Debugging function
    def getStatus(self):
        for x in self.patientDict.keys():
            print("Code " + str(self.patientDict[x].code))
            print("Time Waiting " + str(self.patientDict[x].timePassed))
            print("Time Consultation " + str(self.patientDict[x].timePassedConsult))
            print("Consultations: " + str(self.consultations))
            print("Cost: " + str(self.cost))
            print("\n")


class PDMAProblem(search.Problem):
    
    #Constructor
    def __init__(self):
        self.medicDict = {}
        self.labelDict = {}
        self.patientDict = {}
        self.initial = State()
        self.solution = 0


    #returns a list with the actions that can be applied to state s
    def actions(self,s):
        #list with each action using the following correspondence[destination_doctor,patient]
        actions = []
         
        #list with patients that have reached the maximum waiting time
        urgent_patients = []
        
        #list with patients that have stats that make some combinations actions involving them redundant
        redundant_patients = []

        #enunciation of append methods for more performance
        redunapp = redundant_patients.append
        actapp = actions.append
        urgapp = urgent_patients.append

        #variable associated with computed actions that must not be used/are redundant
        invalid = 0

        #compute all patients that have reached maximum waiting time
        for patient in s.remainingPatients.keys():
            if(s.patientDict[patient].timePassed >= self.labelDict[s.patientDict[patient].labelCode].maxWaitingTime):
                urgapp(patient)
        
        #if there are more urgent patients that available doctors, node is to be pruned
        if len(urgent_patients) > len(list(self.medicDict.keys())):
            return actions
       
        # #Check for redundant pairs of patients(same label, same waited time, same total consultation time)
        for x in combinations(list(s.remainingPatients.keys()),2):
            if s.remainingPatients[x[0]].labelCode == s.remainingPatients[x[1]].labelCode:
                if s.patientDict[x[0]].timePassed == s.patientDict[x[1]].timePassed:
                    if s.patientDict[x[0]].timePassedConsult == s.patientDict[x[1]].timePassedConsult:
                        redunapp(list(x)) 

        
        new_patient_list = list(s.remainingPatients.keys())
        new_p_app = new_patient_list.append
        
        #if there are more doctors than remaining patients available, actions must now be computed with "empty" consultations
        if len(list(s.remainingPatients.keys())) <  len(list(self.medicDict.keys())):
            diff = len(list(self.medicDict.keys())) - len(list(s.remainingPatients.keys())) 
            for _ in range(diff):
                new_p_app("empty")

        #create all permutations of patients with size equal to amount of doctors available       
        permuts = permutations(new_patient_list, len(list(self.medicDict.keys())))       
        actapp = actions.append
        
        #this loop evaluates each action in order to remove undesirable or redundant ones
        for i in permuts:
            invalid = 0
            
            #if action does not contain all of the urgent patients, it is invalid
            for urg in urgent_patients:
                if urg not in i:
                    invalid = 1
                    break         

            #check every redundant pair of patients: prioritizing actions with redundant patients in ascending order
            # e.g. for redundant pair [002,003], eliminate every action with patient 003 coming first in the action than patient 002
            # action [004,003,001,002] is deleted, action [004,002,001,003] is maintained     
            for redun in redundant_patients:
                
                try:                  
                    index0 = i.index(redun[0]) 
                except ValueError:
                    try: 
                        index1 = i.index(redun[1]) 
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

            #if action is valid, append the action mixed with doctors available according to index
            #e.g: index 0 in action goes to first doctor in the doctor dictionary
            if not invalid: 
                actapp(list(zip(list(self.medicDict.keys()),i)))
                
        return actions


    #returns the obtained state after applying the action a to state s
    def result(self,s,a):

        #Create a new state, by copying state s
        new_s = deepcopy(s)

        #New state's cost
        new_cost = 0

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

        #Calculate the new state's cost and store it
        for key, p in new_s.patientDict.items():
            new_cost += p.timePassed**2    
        new_s.cost = new_cost 
        
        #return the new state
        return new_s


    #receives a state and checks if it is a goal state 
    def goal_test(self,s):
        return not bool(s.remainingPatients)


    #receives 2 states and the cost of the 1st one; returns the cost of the 2nd 
    def path_cost(self,c,s1,a,s2):
        return (s2.cost - c)


    #Loads the problem from an input file to an initial state
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
            initialCost += self.patientDict[key].timePassed**2

        self.initial = State(self.patientDict,self.patientDict, None, self.medicDict.keys(), initialCost)


    # Saves the solution to an output file    
    def save(self, f):
        consultations = self.solution.state.consultations
        for key, medicConsultations in consultations.items():
            f.write("MD " + key + " ")
            for singleConsultation in medicConsultations:
                f.write(singleConsultation + " ")
            f.write("\n")

    #Returns true if the algorithm find a solution and returns false otherwise
    def search(self):
        self.solution = search.astar_search(self, self.heuristic)
        if self.solution  is not None:
            return True
        else:
            return False


    def heuristic(self, n):
        #Simplify n.state call
        s=n.state
        
        #Variable for calculating the cost of the final state seen by the heuristic
        my_cost = 0
        
        #List with the time remaining to complete the consultation for each remaining patient  
        time_to_complete = []
        
        #List with the time every remaining patient has waited so far 
        time_waited = []
    
        complete_app = time_to_complete.append
        waited_app = time_waited.append
        
        #Check if all patients can be in a consultation
        if len(s.remainingPatients) <= len(self.medicDict):
            return 0

        #Calculate the cost of the pacients who have finished the consultaion
        for patient in s.patientDict:
            if (self.labelDict[s.patientDict[patient].labelCode].consultationTime - s.patientDict[patient].timePassedConsult) <= 0:
                my_cost += s.patientDict[patient].timePassed**2

        #Create lists with the passed time and the time to complete the consultation of every pacient
        for patient in s.remainingPatients:
            complete_app(self.labelDict[s.patientDict[patient].labelCode].consultationTime - n.state.patientDict[patient].timePassedConsult)
            waited_app(n.state.patientDict[patient].timePassed)

        #sort the times to complete consultation (smallest to biggest)
        time_to_complete.sort(key=int)

        #sort the waited times (biggest to smallest)
        time_waited.sort(key=int, reverse=True)


        '''
        Let's assume that the patient who has waited for the longest time is also the patient with the shortest time to complete
        the consultion. 
        '''
        
        #Keep this loop running untill we can assign a consultaton to every remaining patient
        while len(self.medicDict) < len(time_to_complete):

            #Go through all patients
            for i in range(0, len(time_to_complete)):
                #Assign a consultation to the first n patients (n=number of medical doctors)
                if i < len(self.medicDict):
                    time_to_complete[i] -= 5

                #Increment the waited time for every patient who not in a consultation
                else:
                    time_waited[i] += 5

            #variable to avoid index -1 of the next loop
            j=0 

            #Go through the patients who were assigned a consultation 
            for i in range(0, len(self.medicDict)):

                #Check if the consultation has finished
                if time_to_complete[j] <= 0:
                    
                    #Add the patient's cost to the state's cost
                    my_cost += time_waited[j]**2

                    #Remove the patient from both lists
                    del time_to_complete[j]
                    del time_waited[j]

                    #Decrement the iterator's value since we removed one index
                    j -= 1

                #Since time_to_complete is sorted, if we find a patient who hasn't finished the consultation we can break the loop    
                else: 
                    break

                j += 1

        #Add the cost of every last patient to the state's cost
        for i in range(0, len(time_waited)):
            my_cost += time_waited[i]**2

        #Return the cost of the path from the given state (inside the node) to the goal state computed by the heuristic
        return (my_cost - n.state.cost)