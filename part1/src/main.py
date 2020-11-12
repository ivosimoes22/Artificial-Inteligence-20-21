from solution import PDMAProblem
import search
import sys
import copy

def main():  
    file_name = sys.argv[1]
    #file_name = "PUB4.txt"
    
    problem = PDMAProblem()
    problem.load(file_name)
    #problem.initial.getStatus()
    x = problem.search(problem)
    if x:
        print("Final Cost:" + str(problem.solution.state.cost))
    
    #x = problem.getPatientDict()
    #ac = problem.actions(x)
    #s1 = problem.result(x, ac[0])
    #problem.getStatus(s1)
    #s1t = copy.deepcopy(s1)
    ##print("\n")
    #2 = problem.result(s1t, ac[0])
    #problem.getStatus(s1)
    #problem.getStatus(s2)
    #print(problem.path_cost(0,s1,0,s2))
    f = open("\\solution_files\\solution.txt", "a")
    #print("final cost " + str(problem.solution.state.cost))
    #problem.save(f)


if __name__ == "__main__":
    main()