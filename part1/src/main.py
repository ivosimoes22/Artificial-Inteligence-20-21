from solution import PDMAProblem
import search
import sys
import time
import copy

def main():  
    start = time.time()
    file_name = sys.argv[1]
    f = open(file_name, "r")
    
    problem = PDMAProblem()
    problem.load(f)
    x = problem.search()
    if x:
        print("Final Cost:" + str(problem.solution.state.cost))
        f = open("solution.txt", "w")
        problem.save(f)
    else:
        print("Infeasible")
    
    end = time.time()
    print(end-start)


if __name__ == "__main__":
    main()