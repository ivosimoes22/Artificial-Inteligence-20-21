from solution import PDMAProblem
import sys

def main():
    #file_name = input("Please enter problem file name:\n")   
    file_name = sys.argv[1]
    status = PDMAProblem.load(PDMAProblem, file_name)
    print(PDMAProblem.medic_list)
    print(PDMAProblem.label_list)
    print(PDMAProblem.patient_list)
    PDMAProblem.actions(PDMAProblem, status)
    print(status[1][2][3])

if __name__ == "__main__":
    main()