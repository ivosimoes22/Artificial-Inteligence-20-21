from solution import PDMAProblem
from search import breadth_first_tree_search
import sys
import copy

def main():  
    file_name = sys.argv[1]
    problem = PDMAProblem()
    problem.load(file_name)
    x = breadth_first_tree_search(problem)
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
    #f = open("solution.txt", "a")
    #problem.save(f)


if __name__ == "__main__":
    main()