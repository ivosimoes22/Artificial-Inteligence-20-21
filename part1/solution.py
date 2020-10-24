# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from search import Problem
import sys


# class search_prob(ABC):
#     pass

class PDMAProblem(Problem):
    
    #Constructor
    def __init__(self):
        
        #medic_list and patient_list are used as status
        self.medic_list = []             #[[medic_code,efficiency,[patient_order]],...]
        self.label_list = []             #[[label_code,max_wait_time,consult_time],...]
        self.patient_list = []           #[[patient_code,current_wait,label_code,bool_sent_to_consultation],...]
    
    def actions(self,s):
        self.action = [] #[destination_doctor,patient]
        for medic in s[0]:
            for patient in s[1]:
                if patient[3]:
                    pass
                else:
                    print("Move patient", patient[0], "to doctor", medic[0], "\n")
        pass
    def result(self,status,a):
        
        pass
    def goal_test(self,s):
        pass
    def path_cost(self,c,status1,a,status2):
        pass
    def load(self,f):
        if(".txt" in f):
                prob_file = open(f,"r")
                line_info = prob_file.readlines()
                for line in line_info:
                    print(line)
                    if ("MD" in line):
                        temp = line.split()
                        self.medic_list.append(temp[1:])
                    elif("PL" in line):
                        temp = line.split()
                        self.label_list.append(temp[1:])
                    elif("P " in line):
                        temp = line.split()
                        temp.append(0)
                        self.patient_list.append(temp[1:])
        else:
            sys.exit("Wrong file format, exiting...\n")
            
        status = [self.medic_list, self.patient_list]

        return status
        
    def save(self,f,s):
        pass
    def search(self):
        pass
    
