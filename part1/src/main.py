from solution import PDMAProblem
import search
import sys
import time
import copy

def main():  
    start = time.time()
    file_name = sys.argv[1]
    #file_name = "PUB4.txt"
    
    problem = PDMAProblem()
    problem.load(file_name)
    #problem.initial.getStatus()
    x = problem.search(problem)
    if x:
        print("Final Cost:" + str(problem.solution.state.cost))
    
    f = open("solution.txt", "w")
    problem.save(f)
    end = time.time()
    print(end-start)


if __name__ == "__main__":
    main()