import os, shutil, importlib.util, csv, subprocess, datetime, shelve
from data_maker import Assignment,Student
from data_maker import main as setup

def intro():
    print("Python Grader")
    print("This program needs to be ran from the parent directory of the collection of student repos")
    print()
    setup()
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

def gather(a):
    root = os.getcwd()
    try:
        shutil.rmtree('testing')
    except:
        pass#old testing folder already removed
    data = shelve.open('grading_data')
    students = data['students']
    os.mkdir("testing")
    PIPE = subprocess.PIPE
    for s in students:
        shutil.copyfile(os.path.join(root,s.github,a.folder,a.file), os.path.join(root,'testing',s.github+'_'+a.file))
        os.chdir(s.github)
        p = subprocess.Popen(["git","log","-1","--format=%ci"],stdout=PIPE)
        out = p.communicate()[0].decode()
        os.chdir(root)
        time = format_date(out)
        s.submit = time
    data['students']=students
    data.close()

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

def grade(a):
    data = shelve.open('grading_data')
    s = data['students']
    root = os.getcwd()
    os.chdir('testing')
    with open('report.csv','w',newline='') as f:
        w = csv.writer(f,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Student Name','assignment name','points earned','is late?'])
    test_name = "test_"+a.file
    spec = importlib.util.spec_from_file_location(test_name,os.path.join(root,test_name))
    tests = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tests)
    files = [f.name for f in os.scandir() if f.is_file()]
    files.remove('report.csv')
    for i in files:
        try:
            print(f"Grading: {i}")
            out = tests.tests(i)
        except:
            #python error running tests - probably because they didn't merge
            points = 0#so they failed
        else:
            points = string_to_math(out)
        #seperate github username from 'github_file.py'
        name = name = i[:-(1+len(a.file))]
        for student in s:
            if student.github == name:
                student.set_grade(a, points)
    f = open('report.csv','a',newline='')
    w = csv.writer(f,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in s:
        w.writerow([i.name,i.assignment.folder,i.score,i.late])
    f.close()
    os.chdir(root)
    data['students'] = s
    data.close()
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
    gather(assign_obj)
    print('files gatherd, moving to grading')
    grade(assign_obj)
    print("Testing complete")
    #input("Press enter to exit...")

if __name__ == '__main__':
    main()
