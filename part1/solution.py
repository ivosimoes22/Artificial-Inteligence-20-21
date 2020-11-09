# -*- coding: utf-8 -*-
from search import Problem
import sys
from itertools import permutations


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

    #Gettters
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


class PDMAProblem(Problem):
    
    #Constructor
    #def __init__(self):
    def __init__(self):
        self.medicDict = {}
        self.labelDict = {}
        self.patientDict = {}
        self.initial = {}
        
    
    #Getters
    def getMedicDict(self):
        return self.medicDict
    def getLabelDict(self):
        return self.labelDict
    def getPatientDict(self):
        return self.patientDict

    def getStatus(self, status):
        for x in status.keys():
            print("Code " + str(status[x].getCode()))
            print("Time Waiting " + str(status[x].getTimePassed()))
            print("Time Consultation " + str(status[x].getTimePassedConsult()))
            print("\n")

    def addAction(self,a):
        for singleAction in a:
            self.medicDict[singleAction[0]].getPatientList().append(singleAction[1])
        
    def actions(self,s):
        actions = [] #[destination_doctor,patient]
        permuts = permutations(list(s.keys()), len(list(self.medicDict.keys())))
        
        for i in permuts:
            actions.append(list(zip(list(self.medicDict.keys()),i)))
        
        return actions
        
    def result(self,status,a):
        patients_attended = []
        for singleAction in a:
            medic_rate = self.medicDict[singleAction[0]].getRate()
            status[str(singleAction[1])].incPassedTime(float(medic_rate),1)
            patients_attended.append(singleAction[1])
          
        for x in status.keys():
            if x not in patients_attended:
                status[str(x)].incPassedTime()
        self.addAction(a)    
        return status

    def goal_test(self,status):
        for x in status.keys():
            max_wait_time = self.labelDict[status[x].getLabel()].getMaxWaitingTime()
            consul_target_time = self.labelDict[status[x].getLabel()].getConsultationTime()
            if status[x].getTimePassed() > max_wait_time or status[x].getTimePassedConsult() < consul_target_time:
                return False
        return True

    def path_cost(self,c,status1,a,status2):
        c1 = 0 
        c2 = 0
        for x in status1.keys():
            c1 += status1[x].getTimePassed()**2
            print(status1[x].getTimePassed())
        for x in status2.keys():
            c2 += (status2[x].getTimePassed()**2)
        print("c1 " + str(c1) + " c2 " + str(c2))
        return (c2 - c1)


    def load(self,f):
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
            self.initial = self.patientDict
        
        
    def save(self,f):

        f = open("solution.txt", "a")
        medicDict = self.medicDict
        for key, medic in medicDict.items():
            #Lista mal criada?
            PatientList = medic.getPatientList()
            f.write("MD " + key + " ")
            for p in PatientList:
                f.write(p + " ")
            f.write("\n")
        f.close()

        if medicDict == None:
            f.write("Infeasible")

        
        pass
    def search(self):
        pass
    
