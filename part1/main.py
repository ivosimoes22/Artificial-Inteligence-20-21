from solution import PDMAProblem
import sys

def main():
    #file_name = input("Please enter problem file name:\n")   
    file_name = sys.argv[1]
    problem = PDMAProblem()
    problem.load(file_name)
    x = problem.getPatientDict()["001"]
    print(x.getCode())
    print(x.getTimePassed())
    print(x.getLabel())
    #print(PDMAProblem.medic_list[0])
    #print(PDMAProblem.label_list)
    #print(PDMAProblem.patient_list)
    #actions = PDMAProblem.actions(PDMAProblem, status)
    #print(actions)
    #print(status)
    #status = PDMAProblem.result(PDMAProblem,status,actions[0])
    #print(status)
    #status = PDMAProblem.result(PDMAProblem,status,actions[1])
    #print(status)
    #actions = PDMAProblem.actions(PDMAProblem, status)
    #print(actions)

if __name__ == "__main__":
    main()