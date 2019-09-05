import os, shutil, importlib.util, csv, subprocess, datetime, shelve
from data_maker import *

def intro():
    print("Python Grader")
    print("This program needs to be ran from the parent directory of the collection of student repos")
    print()
    n = True
    while n:
        assign = input("What is the number of the assignment folder?\n")
        try:
            data = shelve.open('grading_data')
            assign_obj = data[assign]
            n = False
        except:
            print("That wasn't a valid assignment number!")
        data.close()
    return assign_obj

def gather(assign_obj):
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
    data = shelve.open('grading_data')
    students = data['students']
    os.mkdir("testing")
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
            late = True
            name = 'Student Code Failed - did you merge?'
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
    assign_obj = intro()
    print("gathering files, please wait")
    days = gather(assign_obj)
    print('files gatherd, moving to grading')
    grade(file, days, due)
    print("Testing complete")
    #input("Press enter to exit...")

if __name__ == '__main__':
    main()
