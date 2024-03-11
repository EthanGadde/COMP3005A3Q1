import psycopg2
from dateutil import parser

#Connecting to database
conn = psycopg2.connect("host='localhost' dbname='Assignment3' user='postgres' password='admin' port=5432")
curr = conn.cursor()

#Console Menu
def print_options():
    print("\nType 1 to execute getAllStudent()")
    print("Type 2 to execute addStudent()")
    print("Type 3 to execute updateStudentEmail()")
    print("Type 4 to execute deleteStudent()")
    print("Type 0 to terminate program")


def getAllStudents():
    curr.execute('SELECT * FROM students')
    result = curr.fetchall()
    #Print formatting
    print("\n----------------------------------------")
    for row in result:
        print(f"student_id = {row[0]}\nfirst_name = {row[1]}\nlast_name = {row[2]}\nemail = {row[3]}\nenrollment_date = {row[4]}\n----------------------------------------")

def addStudent(first_name, last_name, email, enrollment_date):
    #Checking if the enrollment_date parameter was inputted since it is optional
    if not enrollment_date:
        curr.execute(f"INSERT INTO students (first_name, last_name, email) VALUES ('{first_name}','{last_name}','{email}');")
    else:
        curr.execute(f"INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES ('{first_name}','{last_name}','{email}','{enrollment_date}');")
    conn.commit()

def updateStudentEmail(student_id, new_email):
    curr.execute(f"UPDATE students SET email='{new_email}' WHERE student_id={student_id};")
    conn.commit()

def deleteStudent(student_id):
    curr.execute(f"DELETE FROM students WHERE student_id={student_id};")
    conn.commit()


def main():
    while True:
        print_options()
        choice = input("Enter your choice: ")
        if choice == '0':
            break
        elif choice == '1':
            getAllStudents()
        elif choice == '2':
            #getting first_name input
            while True:
                first_name = input("Enter the students first name (Mandatory): ")
                if not first_name:
                    print("Must input first name of student")
                else:
                    break
            #Getting last_name input
            while True:
                last_name = input("Enter the students last name (Mandatory): ")
                if not last_name:
                    print("Must input last name of student")
                else:
                    break
            while True:
                #Getting email input
                email = input("Enter the students email (Mandatory): ")
                if not email:
                    print("Must input email of student")
                else:
                    #Error checking email
                    if email.count('@')!=1:
                        print("Invalid email format. Try again")
                        continue
                    first_half, domain_half = email.split("@")
                    if len(first_half) == 0 or len(domain_half) == 0:
                        print("Invalid email format. Try again")
                        continue
                    if domain_half.find('.') == -1:
                        print("Invalid email format. Try again")
                        continue
                    break
            while True:
                #Getting enrollment_date input
                enrollment_date = input("Enter the students enrollment date in YYYY-MM-DD format (Optional): ")
                if not enrollment_date:
                    addStudent(first_name,last_name,email,enrollment_date)
                    break
                else:
                    #Error checking enrollment date
                    format = "%Y-%m-%d"
                    res = True
                    try:
                        res = bool(parser.parse(enrollment_date))
                    except ValueError:
                        res = False
                    if res == False:
                        print("Invalid date format")
                    else:
                        addStudent(first_name,last_name,email,enrollment_date)
                        break
        elif choice == '3':
            #Getting student_id input
            while True:
                student_id = input("Enter student id of the targeted student: ")
                if not student_id.isdigit():
                    print("Student id must be an integer")
                else:
                    break
            #Getting email input
            while True:
                new_email = input("Enter the new email you wish to change to: ")
                if not new_email:
                    print("Must input email of student")
                else:
                    #Error checking email
                    if new_email.count('@')!=1:
                        print("Invalid email format. Try again")
                        continue
                    first_half, domain_half = new_email.split("@")
                    if len(first_half) == 0 or len(domain_half) == 0:
                        print("Invalid email format. Try again")
                        continue
                    if domain_half.find('.') == -1:
                        print("Invalid email format. Try again")
                        continue
                    break
            updateStudentEmail(student_id,new_email)
        elif choice == '4':
            #Getting student_id input
            while True:
                student_id = input("Enter student id of the targeted student: ")
                if not student_id.isdigit():
                    print("Student id must be an integer")
                else:
                    break
            deleteStudent(student_id)
        else:
            print("Invalid option. Try again")

if __name__ == "__main__":
    main()
    conn.close()
