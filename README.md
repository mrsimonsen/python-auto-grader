support tool for my python programming class.

was trying to run premade pytest tests but 1) pytest doesn't like running the same test file in different directories 2) multiple copies of pytest (renamed) require to import specific student's module (and since all student code is using the same dir structure & file names, they have to be renamed)<br>
It's easier to modify the testing code to run it on multiple files

outline of the program:

* Display reminder to run (this) program from the parent directory of all student repos
* ask for the path of the student assignment (all students should be using the same directory structure and file name)
* ask for the name of the test file (not the one given to students to ensure testing integrity)
* run the grading
* save a file with the results of the tests per student


Additional features:
* create a files of all assignment paths and make a menu to choose assignment, able to run multiple grading files. GUI 2.0
* create a file that is a collection of student object that link grades to assignment, student names to usernames, and class period, 3.0
* add testing when typing in files to make sure they exist before running grading
