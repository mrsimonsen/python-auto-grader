import os, shutil, importlib.util, csv

assignments = {'00':'00-hello-world','01':'01-calculator','02':'02-fortune-cookie',
'03':'03-coin-flipper','04':'04-guess-my-number-2.0','05':'05-dice-roller',
'06':'06-counter','07':'07-reverse-message','08':'08-right-triangle',
'09':'09-word-jumble-2.0','10':'10-sentence-scrambler','11':'11-character-creator',
'12':'12-guess-your-number','13':'13-pig-latin','14':'14-critter-caretaker-2.0',
'15':'15-trivia-challenge-2.0','1':'test1'}
file_names = {'00':'hello_world.py','01':'calculator.py','02':'fortune_cookie.py',
'03':'coin_flipper.py','04':'GMN2.py','05':'dice_roller.py',
'06':'counter.py','07':'reverse_message.py','08':'right_triangle.py',
'09':'WJ2.py','10':'scrambler.py','11':'character_creator.py',
'12':'guess_AI.py','13':'pig_latin.py','14':'CC2.py',
'15':'TC2.py','1':'hi.py'}

def intro():
    print("Python Grader")
    print("This program needs to be ran from the parent directory of the collection of student repos")
    print()
    n = True
    while n:
        assign = input("What is the number of the assignment folder?\n")
        try:
            assign_name = assignments[assign]
            file = file_names[assign]
            n = False
        except:
            print("That wasn't a valid assignment number!")
    return assign_name, file

def gather(assignment, file):
    root = os.getcwd()
    try:
        shutil.rmtree('testing')
    except:
        pass#old testing folder already removed
    subfolders = [f.name for f in os.scandir(root) if f.is_dir()]
    try:
        subfolders.remove('.git')
    except ValueError:
        pass#folder doesn't exist
    try:
        subfolders.remove('__pycache__')
    except ValueError:
        pass#folder doesn't exist

    os.mkdir("testing")
    for folder in subfolders:
        shutil.copyfile(os.path.join(root,folder,assignment,file), os.path.join(root,'testing',folder+'_'+file))


def grade(file):
    root = os.getcwd()
    os.chdir('testing')
    with open('report.csv','w',newline='') as f:
        w = csv.writer(f,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Repo name','tests passed','points earned'])
    file = "test_"+file
    spec = importlib.util.spec_from_file_location(file,os.path.join(root,file))
    master = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(master)
    files = [f.name for f in os.scandir() if f.is_file()]
    files.remove('report.csv')
    for i in files:
        out = master.tests(i)
        points = string_to_math(out)
        with open('report.csv','a',newline='') as f:
            w = csv.writer(f,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            w.writerow([i,out,points])
    os.chdir(root)
    shutil.copyfile(os.path.join(root,'testing','report.csv'), os.path.join(root,'report.csv'))
    shutil.rmtree('testing')

def string_to_math(thing):
    if len(thing)%3==0:
        #single digit values
        total = int(thing[-1])
        score = int(thing[0])
    if len(thing)%5==0:
        #double digit values
        total = int(thing[-2:])
        score = int(thing[:2])
    if len(thing)%2==0:
        #single digit score with 2 digit total
        total = int(thing[-2:])
        score = int(thing[0])
    return round(score/total * 10,2)

def main():
    assignment, file = intro()
    print()
    gather(assignment, file)
    print('files gatherd, moving to grading')
    grade(file)
    print("Testing complete")
    #input("Press enter to exit...")

if __name__ == '__main__':
    main()
