import csv, shelve, datetime
#support classes
class Assignment(object):
    '''an assignment with a folder, file name, and due date'''

    def __init__(self,folder,file,due):
        self.folder = folder
        self.file = file
        self.due = due

    def __str__(self):
        rep = f"{self.folder}\\{self.file}\n{self.due}"
        return rep
class Student(object):
    '''a student with name, weber username, and github username'''

    def __init__(self, name, weber, github):
        self.name = name
        self.weber = weber
        self.github = github
        self.assignment = Assignment('error','',datetime.datetime.today())
        self.score = 0
        self.late = True
        self.submit = None

    def __str__(self):
        rep = f"{self.name}\n{self.weber}\n{self.github}\n--Current Assignment--\n{self.assignment.folder}\\{self.assignment.file}\n{self.score} points\nSubmitted:{self.submit}\nLate = {self.late}"
        return rep

    def set_grade(self, assign_obj, score):
        self.assignment = assign_obj
        self.score = score
        if assign_obj.due > self.submit:
            self.late = False
def main():
    #create shelve file, overwrite old file if exists
    data = shelve.open('grading_data','n')

    #assignment details
    assignments = ('00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','1')
    folders = {'00':'00-hello-world','01':'01-calculator','02':'02-fortune-cookie',
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
    due_dates = {'00':datetime.datetime(2019, 9, 1, 23, 59,59),
    '01':datetime.datetime(2019, 9, 8, 23, 59,59),'02':datetime.datetime(2019,9,15,23,59,59),
    '03':datetime.datetime(2019,9,15,23,59,59),'04':datetime.datetime(2019,9,22,23,59,59),
    '05':datetime.datetime(2019,9,29,23,59,59),'06':datetime.datetime(2019,9,29,23,59,59),
    '07':datetime.datetime(2019,10,6,23,59,59),'08':datetime.datetime(2019,10,6,23,59,59),
    '09':datetime.datetime(2019,10,13,23,59,59),'10':datetime.datetime(2019,10,20,23,59,59),
    '11':datetime.datetime(2019,10,27,23,59,59),'12':datetime.datetime(2019,11,3,23,59,59),
    '13':datetime.datetime(2019,11,10,23,59,59),'14':datetime.datetime(2019,11,17,23,59,59),
    '15':datetime.datetime(2019,12,1,23,59,59),'1':datetime.datetime.today()}
    for i in assignments:
        data[i]=Assignment(folders[i],file_names[i],due_dates[i])

    #student details
    names = {}
    with open('Weber names.csv','r',newline='') as f:
        #format = NAME,WEBER
        raw = csv.reader(f,delimiter=',',quotechar='"')
        for row in raw:
            names[row[0]]=row[1]
    weber = {}
    with open('1030 usernames - Corrected.csv','r',newline='') as f:
        #format = TIMESTAMP, GITHUB, WEBER
        raw = csv.reader(f, delimiter=',')
        for row in raw:
            weber[row[2]]=row[1]
    students = []
    for i in names.keys():
        students.append(Student(i,names[i],weber[names[i]]))
    data['students'] = students

    #save all the things
    data.close()
