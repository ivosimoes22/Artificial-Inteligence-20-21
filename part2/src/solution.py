from probability import JointProbDist

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
        
class MDProblem():  

    def __init__(self, fh):
        self.diseaseDict = {}
        self.symptomDict = {}
        self.examDict = {}
        self.measDict = {}
        self.p = 0
        self.load(fh)
        
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

    def solve(self):
        return(disease, likelihood)

    
    def load(self, f):
        
        
        line_info = f.readlines()
        c = 0
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
                
