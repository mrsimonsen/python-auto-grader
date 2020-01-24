from tkinter import *

class App(Frame):
    def __init__(self, master):
        super(App, self).__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        Label(self,text="Select assignment to grade:").grid(row=0,column=0,sticky=W, columnspan = 2)
        self.anum=StringVar()
        Radiobutton(self,text='1', variable=self.anum, value="test 1", command=self.update_text).grid(row=2,column=0,sticky=W)
        Radiobutton(self,text='2', variable=self.anum, value="test 2", command=self.update_text).grid(row=2,column=1,sticky=W)
        Radiobutton(self,text='00', variable=self.anum, value="00 Hello World", command=self.update_text).grid(row=2,column=2,sticky=W)
        Radiobutton(self,text='01', variable=self.anum, value="01 Calculator", command=self.update_text).grid(row=3,column=0,sticky=W)
        Radiobutton(self,text='02', variable=self.anum, value="02 Fortune Cookie", command=self.update_text).grid(row=3,column=1,sticky=W)
        Radiobutton(self,text='03', variable=self.anum, value="03 Coin Flipper", command=self.update_text).grid(row=3,column=2,sticky=W)
        Radiobutton(self,text='04', variable=self.anum, value="04 Guess My Number 2", command=self.update_text).grid(row=4,column=0,sticky=W)
        Radiobutton(self,text='05', variable=self.anum, value="05 Dice Roller", command=self.update_text).grid(row=4,column=1,sticky=W)
        Radiobutton(self,text='06', variable=self.anum, value="06 Counter", command=self.update_text).grid(row=4,column=2,sticky=W)
        Radiobutton(self,text='07', variable=self.anum, value="07 Reverse Message", command=self.update_text).grid(row=5,column=0,sticky=W)
        Radiobutton(self,text='08', variable=self.anum, value="08 Right Triangle", command=self.update_text).grid(row=5,column=1,sticky=W)
        Radiobutton(self,text='09', variable=self.anum, value="09 Word Jumble 2", command=self.update_text).grid(row=5,column=2,sticky=W)
        Radiobutton(self,text='10', variable=self.anum, value="10 Scrambler", command=self.update_text).grid(row=6,column=0,sticky=W)
        Radiobutton(self,text='11', variable=self.anum, value="11 Character Creator", command=self.update_text).grid(row=6,column=1,sticky=W)
        Radiobutton(self,text='12', variable=self.anum, value="12 Guess Your Number", command=self.update_text).grid(row=6,column=2,sticky=W)
        Radiobutton(self,text='13', variable=self.anum, value="13 Pig Latin", command=self.update_text).grid(row=7,column=0,sticky=W)
        Radiobutton(self,text='14', variable=self.anum, value="14 Critter Caretaker 2", command=self.update_text).grid(row=7,column=1,sticky=W)
        Radiobutton(self,text='15', variable=self.anum, value="15 Trivia Challenge 2", command=self.update_text).grid(row=7,column=2,sticky=W)

        self.results_txt = Text(self, width = 40, height = 5, wrap = WORD)
        self.results_txt.grid(row = 8, column = 0, columnspan = 3)

        self.grade = Button(self)
        self.grade["text"]="Grade!"
        self.grade["command"]=self.run
        self.grade.grid()

    def run(self):
        self.results_txt.delete(0.0,END)
        self.results_txt.insert(0.0, "GRADING!")
        message = gather()
        self.results_txt.delete(0.0,END)
        self.results_txt.insert(0.0, message)
        feedback = grade()
        if feedback:
            self.results_txt.delete(0.0,END)
            self.results_txt.insert(0.0, feedback)

    def update_text(self):
        message = f"You selected assignment \"{self.anum.get()}\" to grade."
        self.results_txt.delete(0.0, END)
        self.results_txt.insert(0.0, message)

root = Tk()
root.title("1030 Python AutoGrader")
app = App(root)
#run the app
root.mainloop()
