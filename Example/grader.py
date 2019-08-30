import os, shutil, importlib.util, csv, subprocess, datetime

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
#https://docs.python.org/3.7/library/datetime.html#datetime.datetime
due_dates = {'00':datetime.datetime(2109, 9, 1, 23, 59,59),
'01':datetime.datetime(2019, 9, 8, 23, 59,59),'02':datetime.datetime(2109,9,15,23,59,59),
'03':datetime.datetime(2019,9,15,23,59,59),'04':datetime.datetime(2019,9,22,23,59,59),
'05':datetime.datetime(2019,9,29,23,59,59),'06':datetime.datetime(2019,9,29,23,59,59),
'07':datetime.datetime(2019,10,6,23,59,59),'08':datetime.datetime(2019,10,6,23,59,59),
'09':datetime.datetime(2019,10,13,23,59,59),'10':datetime.datetime(2019,10,20,23,59,59),
'11':datetime.datetime(2019,10,27,23,59,59),'12':datetime.datetime(2019,11,3,23,59,59),
'13':datetime.datetime(2019,11,10,23,59,59),'14':datetime.datetime(2019,11,17,23,59,59),
'15':datetime.datetime(2019,12,1,23,59,59),'1':datetime.datetime.today()}

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
            due = due_dates[assign]
            n = False
        except:
            print("That wasn't a valid assignment number!")
    return assign_name, file, due

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
    days = {}
    PIPE = subprocess.PIPE
    for folder in subfolders:
        name = folder+'_'+file
        shutil.copyfile(os.path.join(root,folder,assignment,file), os.path.join(root,'testing',name))
        os.chdir(folder)
        p = subprocess.Popen(["git","log","-1","--format=%ci"],stdout=PIPE)
        out = p.communicate()[0].decode()
        os.chdir(root)
        time = format_date(out)
        days[name] = time
    return days

def format_date(raw):
    #format '2019-08-28 14:46:11 -0600'
    #index:  0123456789012345678901234
    year = int(raw[:4])
    month = int(raw[5:7])
    day = int(raw[8:10])
    hour = int(raw[11:13])
    minute = int(raw[14:16])
    second = int(raw[17:19])
    date = datetime.datetime(year, month, day, hour, minute, second)
    return date

def late_check(time, due):
    #if the submission is greater than the duedate it is late
    if time > due:
        return True #it is late
    else:
        return False #it is not late

def format_usernames():
    username = {}
    with open('1030 usernames - Form Responses 1.csv','r',newline='') as f:
        #format = TIMESTAMP, GITHUB, WEBER
        raw = csv.reader(f, delimiter=',', quotechar='|')
        for row in raw:
            username[row[1]]=row[2]
    return username

def grade(file,days, due):
    root = os.getcwd()
    username = format_usernames()
    os.chdir('testing')
    with open('report.csv','w',newline='') as f:
        w = csv.writer(f,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['GitHub_File','Weber name','points earned','is late?'])
    tests = "test_"+file
    spec = importlib.util.spec_from_file_location(tests,os.path.join(root,tests))
    master = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(master)
    files = [f.name for f in os.scandir() if f.is_file()]
    files.remove('report.csv')
    for i in files:
        try:
            out = master.tests(i)
            points = string_to_math(out)
            late = late_check(days[i], due)
            name = username.get(i[:-(1+len(file))],'GitHub name Error')
        except:
            points = 0
            late = False
            name = 'Test error'
        with open('report.csv','a',newline='') as f:
            w = csv.writer(f,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            w.writerow([i,name,points,late])
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
    assignment, file, due = intro()
    print("gathering files, please wait")
    days = gather(assignment, file)
    print('files gatherd, moving to grading')
    grade(file, days, due)
    print("Testing complete")
    #input("Press enter to exit...")

if __name__ == '__main__':
    main()
