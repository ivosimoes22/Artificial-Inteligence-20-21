# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from search import Problem
import sys


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
        self.timePassed = timePassed
        self.labelCode = labelCode

    #Gettters
    def getCode(self):
        return self.code
    def getTimePassed(self):
        return self.timePassed
    def getLabel(self):
        return self.labelCode

class Label():
    def __init__(self, code, maxWaitingTime, consultationTime):
        self.code = code
        self.maxWaitingTime = maxWaitingTime
        self.consultationTime = consultationTime

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
        
    #medic_list and patient_list are used as status
    #medic_list = []             #[[medic_code,efficiency,avalability],...]
    #label_list = []             #[[label_code,max_wait_time,consult_time],...]
    #patient_list = []           #[[patient_code,current_wait,label_code,bool_sent_to_consultation],...]
    #solution = []               #[[medic_code,[patient_order]],...]
    #medics_ocupied = 0

    
    #Getters
    def getMedicDict(self):
        return self.medicDict
    def getLabelDict(self):
        return self.labelDict
    def getPatientDict(self):
        return self.patientDict


    def actions(self,s):
        actions = [] #[destination_doctor,patient]
        for medic in s[0]:
            if medic[2] == 0:
                for patient in s[1]:
                    if patient[3]:
                        pass
                    else:
                        #print("Move patient", patient[0], "to doctor", medic[0], "\n")
                        actions.append([medic[0],patient[0]])
        return actions
        
    def result(self,status,a):
        # num_medics_processed = 0
        # for medic in self.medic_list:
        #     if medic[0] == a[0]:
        #         if len(self.solution[num_medics_processed]) == 2:
        #             self.solution[num_medics_processed][1].append(a[1])
        #         else:
        #             self.solution[num_medics_processed].append([a[1]])
        #         self.medic_list[num_medics_processed][2] = a[1]
        #         num_patients_processed = 0
        #         for patient in self.patient_list:
        #             if patient[0] == a[1]:
        #                 status[1][num_patients_processed][3] = 1
        #             num_patients_processed += 1 
        #     else: pass
        #     num_medics_processed += 1 
        # medics_occupied += 1
        # if medics_occupied == len(self.medic_list):
        #     for medic in self.medic_list:
        #         for patient in self.patient_list.index:
        #                 if (medic[2] == patient[0]):
        #                     for label in self.label_list:
        #                         if (label[0] == patient[2]):
        pass
                                    

        return status

    def goal_test(self,s):
        pass

    def path_cost(self,c,status1,a,status2):
        pass

    def load(self,f):
        if(".txt" in f):
                prob_file = open(f,"r")
                line_info = prob_file.readlines()
                for line in line_info:
                    #print(line)
                    if ("MD" in line):
                        temp = line.split()
                        temp.append(0)
                        self.medicDict[str(temp[1])] = Doctor(temp[1], temp[2])
                        #self.medic_list.append(temp[1:])
                        #self.solution.append([temp[1]])
                    elif("PL" in line):
                        temp = line.split()
                        #self.label_list.append(temp[1:])
                        self.labelDict[str(temp[1])] = Label(temp[1], temp[2], temp[3])
                    elif("P " in line):
                        temp = line.split()
                        temp.append(0)
                        self.patientDict[str(temp[1])] = Patient(temp[1], temp[2], temp[3])
                        #self.patient_list.append(temp[1:])
        else:
            sys.exit("Wrong file format, exiting...\n")
            
        #status = [self.medic_list, self.patient_list]

        
        
    def save(self,f,s):
        
        pass
    def search(self):
        pass
    
