import os

def intro():
    print("Python Grader")
    print("This program needs to be ran from the parent directory of the collection of student repos")
    print()
    assignment = input("What is the path of the assignment?\n")
    test = input("What is the name of the test file?\n")
    return test, assignment

def outro(errors):
    print("Testing complete")
    if errors:
        print(f"There were {len(errors)} errors:")
        for i in errors:
            print(i)

def grade(test, path):
    errors = []
    
    #for each folder in the directory
        #change working directory to folder/assignment
        #set collection of output
        #run tests
        #save output to file under folder name
        #if can't run tests
            #add folder name to errors
    #close file
    #return name list
    return errors




def main():
    test, assignment = intro()
    errors = grade(test, assignment)
    outro(errors)
    input("Press enter to exit...")

if __name__ == '__main__':
    main()
