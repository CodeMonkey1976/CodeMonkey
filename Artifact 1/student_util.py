import csv
import hashlib

#edit Student Information.
#   User can edit student name and / or grade
def editStudent(student, grade):
    while True:
        print("Menu\nChange Name or Grade")
        print("1. " + student)
        print("2.  " + grade)
        print("Press 'C' to Continue")
        try:
            menu = input("Choice: ")
            if menu.upper() == "C":
                break
            menu = int(menu)
            if menu == 1:
                name = input("Enter Name \n <Enter> to cancel: ")
                if name:
                    student = name
            if menu == 2:
                new_grade = input("Enter Grade \n <Enter> to cancel: ")
                if new_grade:
                    grade = new_grade
        except:
            print("\n")
    return student, grade

#adjust spaces in menu to allign grades
def spaces(name, size):
    size = size - len(name)
    space = ""
    for i in range(size):
        space = space + "."
    return space


# Read User Info
def ReadUserInfo():
    userName = input("\nEnter name: ")
    password = input("\nEnter password: ")
    return userName, password


# Check User Permission Access
def CheckUserPermissionAccess(username,password):
    #  Grab usernames and passwords from user.csv file
    access = False
    try:
        with open('user.csv', 'r') as user_info:
            user_reader = csv.reader(user_info, dialect='excel')
            professor = []
            professor_password = []
            for row in user_reader:
                professor.append(row[0])
                professor_password.append(row[1])

    except FileNotFoundError:
        print("\n\nuser.csv file is missing\n... halting!")
        quit()

    for i in range(len(professor)):
        if professor[i] == username:
            break
    password = hashlib.md5(password.encode())
    password = (str(password.hexdigest()))
    if password == professor_password[i]:
        access = True
    else:
        print("Invalid Username or Password")
    return access


#Display Student Information
#def DisplayStudentInformation

def spaces_in_menu(name, maxNameSize):
    if len(name) + 3 > maxNameSize:
        maxNameSize = len(name) + 3
    return maxNameSize


#Load Student Information
maxNameSize = 0  # variable to help allign the menu
try:
    with open('students.csv', 'r') as students_Info:
        student_reader = csv.reader(students_Info, dialect='excel')
        student = []
        grade = []
        for row in student_reader:
           student.append(row[0])
           grade.append(row[1])

except FileNotFoundError:
    print("\n\nStudents.csv file is missing\n... halting!")
    quit()


#System login
access = False
loginAttempts = 0
while not access:
    loginAttempts = loginAttempts + 1
    if loginAttempts > 3:
        print("Login Attmpts Exceeded")
        quit()

    #Get Username and password
    userName, password = ReadUserInfo()

    #verify access
    access = CheckUserPermissionAccess(userName, password)

#menu to edit grades
print("Menu")
while True:
    print("Students  Grades")
    for i in range(len(student)):
        if i != 0:
            maxNameSize = spaces_in_menu(student[i], maxNameSize)
            space = spaces(student[i], maxNameSize)
            print(str(i) + ". " + student[i] + str(space) + grade[i])
    print("\nSelect 1 - " + str(len(student)) + " Or 'Q' to quit")
    menu = input("Choice: ")
    try:
        if menu.upper() == "Q":
            print("Done")
            break

        menu = int(menu)
        student[menu], grade[menu] = editStudent(student[menu], grade[menu])

        maxNameSize = 0 # reset name size var in case the size of the name changes durring edits
    except:
        print("\n")

try:
    #  Write Student information to file
    print("Updating CSV file...")
    with open('students.csv', 'w') as csvfile:
        student_writter = csv.writer(csvfile,lineterminator = '\n', dialect='excel')
        for i in range(len(student)):
            student_writter.writerow([student[i], grade[i]])


except FileNotFoundError:
    print("\n\nError!")
    quit()
