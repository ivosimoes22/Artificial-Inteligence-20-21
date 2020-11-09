from solution import PDMAProblem
import sys
import copy

def main():
    #file_name = input("Please enter problem file name:\n")   
    file_name = sys.argv[1]
    problem = PDMAProblem()
    problem.load(file_name)
    x = problem.getPatientDict()
    ac = problem.actions(x)
    for i in ac:
        print(tuple(i))
    wait = input("Press Enter to continue")
    
    s1 = problem.result(x, ac[0])
    problem.getStatus(s1)
    s1t = copy.deepcopy(s1)
    print("\n")
    s2 = problem.result(s1t, ac[0])
    problem.getStatus(s1)
    problem.getStatus(s2)
    print(problem.path_cost(0,s1,0,s2))
    f = open("solution.txt", "a")
    y = problem.getMedicDict()
    problem.save(f)
    #print(x[0][0][0])
    #x = problem.getPatientDict()["001"]
    # print(x.getCode())
    # print(x.getTimePassed())
    # print(x.getLabel())
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