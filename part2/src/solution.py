from part2.src.probability import BayesNet, elimination_ask
import probability
from itertools import product

class Exam():
    def __init__(self, name, disease, TPR, FPR):
        self.name = name
        self.disease = disease
        self.TPR = TPR
        self.FPR = FPR

class Measurement():
    def __init__(self, name, testResult):
        self.name = name
        self.result = testResult

class Disease():
    def __init__(self, name):
        self.name = name
        self.symptoms = []
        self.related = []
        
class MDProblem():  

    def __init__(self, fh):
        self.diseaseDict = {}
        self.symptomDict = {}
        self.examDict = {}
        self.measDict = {}
        self.p = 0
        self.load(fh)
        self.BayesNet = probability.BayesNet()
        self.createBayesNetwork()


#######Print Methods###########
    def printDisease(self):
        for disease in self.diseaseDict.keys():
            print(self.diseaseDict[disease].name)
            print(self.diseaseDict[disease].symptoms)
            print("\n")

    def printExam(self):
        for exam in self.examDict.keys():
            print(self.examDict[exam].name)
            print(self.examDict[exam].disease)
            print(self.examDict[exam].TPR)
            print(self.examDict[exam].FPR)
            print("\n")

    def printMeas(self):
        for meas in self.measDict.keys():
            for i in self.measDict[meas]:
                print(i.name)
                print(i.result)
            print("\n")
####################################

    def get_related_diseases(self):
        for d in self.diseaseDict:
            for s in d.symptom:
                for f in self.diseaseDict:
                    if s in f.symptom:
                        d.related.append(f.name)

    def assert_parents(self, name,timestamp): 
        parents = ""
        for x in self.diseaseDict[name].related:
            parents += x + "__" + str(timestamp-1) + " "
        return parents

    def createBayesNetwork(self):
        #The time corresponds to the measures taken
        for t in self.measDict.keys():
            #Go through all the diseases
            for d in self.diseaseDict.keys():
        
                #Create a unique name for the current time step
                D = self.diseaseDict[d].name + "__" + str(t)

                #If in initial time step
                if t == 1:                                
                    #Add disease with 0.5 prob because we dont know and no parents
                    self.BayesNet.add([D,'', 0.5])
                else:
                    #Look for the parents - disease that are on t-1 with the sharing symptom
                    
                    self.BayesNet.add([D,assert_parents(d, t), get_prob_table(len(self.diseaseDict[d].related), t)])

            D = self.examDict[self.measDict[t].name].name
            parent = self.examDict[self.measDict[t].name].disease + "__" + str(t)
            self.BayesNet.add(D, parent, get_prob_table(1, t ,"Exam", D)) 


    def get_prob_table(self, nParents, t, nodeType="Disease", examName=None):
        
        if nParents == 1:
            if nodeType == "Disease":
                return {True: 1, False: 0}

            elif nodeType == "Exam":
                tpr = self.examDict[examName].tpr
                fpr = self.examDict[examName].fpr
                return {True: tpr, False: fpr}

        else:
            cpt = {}
            combinations = list(product([True, False], repeat=nParents))
            for i in range(len(combinations)/2):
                cpt[combinations[i]] = 1
            for i in range(len(combinations)/2, len(combinations)-1):
                cpt[combinations[i]] = self.p
            cpt[combinations[-1]] = 0
            return cpt


    def solve(self):

        measures = {}
        for t in self.measDict.keys():
            m = self.measDict[t].name + '__' + str(t)

            if self.measDict[t].result == 'T':
                measures[m] = True
            elif self.measDict[t].result == 'F':
                measures[m] = False

        for disease in self.diseaseDict.keys():
            d = disease + '__' + str(len(self.measDict))
            prob = probability.elimination_ask(d, measures, self.BayesNet).show_approx()
            print(str(prob))
            diseaseProb[disease] = prob


        # max_prob = max(diseaseProb)
        # disease, likelihood = [max_prob, ]
        
        return(disease, likelihood)

    
    def load(self, f):
        
        
        line_info = f.readlines()
        c = 1
        i = 0
        for line in line_info:
            if ("D " in line):
                k = 0
                temp = line.split()
                for k in range(1, len(temp)):
                    self.diseaseDict[str(temp[k])] = Disease(temp[k])
            elif("S " in line):
                temp = line.split()
                #self.symptomDict[str(temp[1])] = Symptom(temp[1], temp[2], temp[3])
                for k in range(2, len(temp)):
                    self.diseaseDict[temp[k]].symptoms.append(temp[1])

            elif("E " in line):
                temp = line.split()
                self.examDict[str(temp[1])] = Exam(temp[1], temp[2], float(temp[3]), float(temp[4]))
            elif("M " in line):
                temp = line.split()
                self.measDict[c] = []
                for i in range(1, len(temp), 2):
                    self.measDict[c].append(Measurement(temp[i], temp[i+1]))
                c += 1

            elif("P " in line):
                temp = line.split()
                self.p = float(temp[1])

        get_related_diseases()
        
        
    
                            


                
