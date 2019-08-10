import os, shutil
import give5_test as master

def intro():
    print("Python Grader")
    print("This program needs to be ran from the parent directory of the collection of student repos")
    print()
    assignment = input("What is the name of the assignment folder?\n")
    file = input("What is the name of the file?\n")
    if file [-3:] != ".py":
        file += ".py"
    return assignment, file

def gather(assignment, file):
    root = os.getcwd()
    subfolders = [f.name for f in os.scandir(root) if f.is_dir()]
    subfolders.remove('.git')
    subfolders.remove('__pycache__')
    os.mkdir("testing")
    for folder in subfolders:
        shutil.copyfile(os.path.join(root,folder,assignment,file), os.path.join(root,'testing',folder+'_'+file))
    print('files gatherd, moveing to grading')

def grade():
    root = os.getcwd()
    file = open('report.txt','w')
    os.chdir('testing')
    files = [f.name for f in os.scandir() if f.is_file()]
    for i in files:
        out = master.tests(i)
        file.write(f"{i}: {out}\n")

    file.close()
    os.chdir(root)
    shutil.rmtree('testing')


def main():
    assignment, file= intro()
    gather(assignment, file)
    grade()
    print("Testing complete")
    #input("Press enter to exit...")

if __name__ == '__main__':
    main()
