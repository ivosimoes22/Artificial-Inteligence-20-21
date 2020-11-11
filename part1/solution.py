# -*- coding: utf-8 -*-
from search import Problem, depth_first_tree_search, depth_first_graph_search, bidirectional_search, breadth_first_tree_search, Node
import sys
from itertools import permutations
from collections import defaultdict
from copy import deepcopy, copy


class Doctor():
    def __init__(self, code, efficiencyRate):
        self.code = code
        self.rate = efficiencyRate
        self.patientList = []

    #getters
    def getCode(self):
        return self.code
    def getRate(self):
        return self.rate
    def getPatientList(self):
        return self.patientList

    #setter
    def setNewPatient(self, patientCode):
        self.patientList.append(patientCode)


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
    def __init__(self, patientDict=None, consultations=None, mediclistkeys = None, c=0):
        self.patientDict = {}
        self.consultations = defaultdict(list)
        self.deadend = 0
        if patientDict is not None:
            self.patientDict = deepcopy(patientDict)        
        if consultations is not None:
            self.consultations = deepcopy(consultations)
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

    def setNewConsultation(self, medic_code, patient_code):
        self.consultations[str(medic_code)].append(str(patient_code))

    def setPatientDict(self, patientDict):
        self.patientDict = patientDict
    
    def updateCost(self, patient):
        self.cost += patient
    # def computeCost(self):
    #     for i in self.patientDict.keys():
    #         self.cost += self.patientDict[i].timePassed**2



class PDMAProblem(Problem):
    
    #Constructor
    def __init__(self):
        self.medicDict = {}
        self.labelDict = {}
        self.patientDict = {}
        self.initial = State()
        self.solution = Node(self.initial)
    
    #Getters
    def getMedicDict(self):
        return self.medicDict
    def getLabelDict(self):
        return self.labelDict
    def getPatientDict(self):
        return self.patientDict

    # def getStatus(self):
    #     patientDict = self.getPatientDict()
    #     for x in patientDict.keys():
    #         print("Code " + str(patientDict[x].getCode()))
    #         print("Time Waiting " + str(patientDict[x].getTimePassed()))
    #         print("Time Consultation " + str(patientDict[x].getTimePassedConsult()))
    #         print("\n")


    #returns a list with the actions that can be applied to state s
    def actions(self,s):
        actions = [] #[destination_doctor,patient]
        if not s.deadend:
            permuts = permutations(list(s.getPatientDict().keys()), len(list(self.medicDict.keys())))
            actapp = actions.append
            for i in permuts:
                actapp(list(zip(list(self.medicDict.keys()),i)))
            print(actions)
            return actions
        else:
            return []

    #returns the obtained state after applying the action a to state s
    def result(self,s,a):

        #Create a new state, by copying state s
        new_s = deepcopy(s)
        new_s.cost = 0
        #List with the pacients who are currently in a consultation
        patients_attended = []
        #Considering 1 action as 3 singleActions
        for singleAction in a:

            #Increase patient's passed  time in a consultation
            medic_rate = self.medicDict[singleAction[0]].getRate()
            new_s.getPatientDict()[str(singleAction[1])].incPassedTime(float(medic_rate),1)

            #Remove the patient from the patient's dictionary if he has reached the total Consultation Time
            if new_s.getPatientDict()[str(singleAction[1])].getTimePassedConsult() >= self.getLabelDict()[new_s.getPatientDict()[str(singleAction[1])].getLabel()].getConsultationTime() :
                del new_s.getPatientDict()[str(singleAction[1])]


            #Add the new consultation to the new_s consultations dictionary
            #new_s.setNewConsultation(singleAction[0], singleAction[1])
            new_s.consultations[str(singleAction[0])].append(str(singleAction[1]))

            #Store patients who are in a consultation 
            patients_attended.append(singleAction[1])
         
        #Increase the waiting time in every patient who is not in a consultation at this moment in new_s
        for x in new_s.getPatientDict().keys():
            if x not in patients_attended:
                new_s.getPatientDict()[str(x)].incPassedTime()

            #Check if any patient has exceeded the Maximum Waiting Time 
            if new_s.getPatientDict()[str(x)].getTimePassed() > self.getLabelDict()[new_s.getPatientDict()[str(x)].getLabel()].getMaxWaitingTime():
                    new_s.deadend = 1
        
        #print("After action\n")
        new_s.getStatus()
        return new_s

    #receives a state and checks if it is a goal state 
    def goal_test(self,s):
        # aqui nao assumes nada ô rapazinho
        #___________________________________________________________________________________________________________#
        # for x in s.patientDict.keys():
        #    consul_target_time = self.labelDict[s.patientDict[x].labelCode].consultationTime
        #    if  s.patientDict[x].timePassedConsult < consul_target_time:
        #        return False
        return not bool(s.patientDict)
        #___________________________________________________________________________________________________________#



    #receives 2 states and the cost of the 1st one; returns the cost of the 2nd 
    #só é necessário caluclar o custo de a e somar a c
    def path_cost(self,c,s1,a,s2):

        action_cost = 0

        for singleAction in a:
            #Check if the patient is in state 2's dictionary; If he is, no cost is added (max consultation time not reached)
            if str(singleAction[1]) not in s2.getPatientDict():
                #Check in state 1's patient dictionary how much time the paitient waited and compute the cost 
                action_cost += s1.getPatientDict()[str(singleAction[1])].getTimePassed()**2
        
        #s2.updateCost(action_cost) 
        s2.cost += action_cost
        s2.getStatus()
        return (c + action_cost)


        #c1 = 0 
        #c2 = 0
        #for x in status1.keys():
        #    c1 += status1[x].getTimePassed()**2
        #    #print(status1[x].getTimePassed())
        #for x in status2.keys():
        #    c2 += (status2[x].getTimePassed()**2)
        #print("c1 " + str(c1) + " c2 " + str(c2))
        #return (c2 - c1)


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

        self.initial = State(self.patientDict,None,self.medicDict.keys(), initialCost)
        self.initial.getStatus()
        
    def save(self, f):

        consultations = self.solution.state.getConsultations()
        for key, medic in consultations:
            print("MD " + key + " ")
            f.write("MD " + key + " ")
            for p in consultations[key]:
                print(p + " ")
                f.write(p + " ")
            print("\n")
            f.write("\n")
        f.close()

        if consultations == None:
            f.write("Infeasible")

    def search(self, p):
        if breadth_first_tree_search(p) == True:
            print("Found Solution")

    
