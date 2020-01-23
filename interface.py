from tkinter import *

class App(Frame):
    def __init__(self, master):
        super(App, self).__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        Label(self,text="Select assignment to grade:").grid(row=0,column=0,sticky=W)
        Label(self,text="Select one.").grid(row=1,column=0,sticky=W)
        self.anum=StringVar()
        Radiobutton(self,text='1', variable=self.anum, value="test 1", command=self.update_text).grid(row=2,column=0,sticky=W)
        Radiobutton(self,text='2', variable=self.anum, value="test 2", command=self.update_text).grid(row=3,column=0,sticky=W)
        self.results_txt = Text(self, width = 40, height = 5, wrap = WORD)
        self.results_txt.grid(row = 5, column = 0, columnspan = 3)

        self.grade = Button(self)
        self.grade["text"]="Grade!"
        self.grade["command"]=self.run
        self.grade.grid()

    def run(self):
        self.results_txt.delete(0.0,END)
        self.results_txt.insert(0.0, "GRADING!")

    def update_text(self):
        message = f"You selected assignment {self.anum.get()} to grade."
        self.results_txt.delete(0.0, END)
        self.results_txt.insert(0.0, message)

root = Tk()
root.title("1030 Python AutoGrader")
app = App(root)
#run the app
root.mainloop()
