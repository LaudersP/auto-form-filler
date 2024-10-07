import os
import re
import sqlite3
from tkinter import messagebox
import DatabaseSchema as DatabaseSchema

class Database:
    # Path to the database
    DBPATH = os.path.join(os.path.dirname(__file__),"..","database.db")

    def __init__(self):
        haveIt = os.path.exists(Database.DBPATH)
        self.conn = sqlite3.connect(Database.DBPATH)
        if not haveIt:
            self.createTables()

    def createTables(self):
        '''Create tables based on the set schema'''
        with self.conn:
            for tableName in DatabaseSchema.tables:
                table = DatabaseSchema.tables[tableName]
                L=[]

                for columnName in table:
                    L.append(f"{columnName} {table[columnName]}")
                
                self.conn.execute(
                    f"create table {tableName} ({','.join(L)})"
                )

    def addClass(self, classTitle, classCode, classSession, classSemester, startTime, endTime):
        '''Create a class in the database.'''
        
        # Check if the class title is valid (allowing letters, numbers, spaces, and parentheses)
        pattern = r'^[a-z0-9 ()]+$'
        if not re.match(pattern, classTitle, re.IGNORECASE):
            raise Exception(f"Invalid class title '{classTitle}'!")
        
        # Validate and format the classCode
        department = classCode[:4]
        courseNum = classCode[4:]
        classCode = department.upper() + courseNum  # Make the department part uppercase
        
        # Check if department is alphabetic and courseNum is numeric
        if not (department.isalpha() and courseNum.isdigit()):
            raise Exception(f"Invalid class code '{classCode}'!")
        
        # Check if the session ID is numeric
        if not classSession.isdigit():  # Use isdigit to ensure it's an integer
            raise Exception(f"Invalid session id '{classSession}'!")
        
        # Check if the semester was entered
        if classSemester == '':
            raise Exception(f"Invalid class semester '{classSemester}'!")
        
        # Check if startTime and endTime are in the correct format (e.g., "9:30 am")
        time_pattern = r'^(1[0-2]|0?[1-9]):[0-5][0-9] (am|pm)$'
        
        if not re.match(time_pattern, startTime, re.IGNORECASE):
            raise Exception(f"Invalid start time '{startTime}'!")
        
        if not re.match(time_pattern, endTime, re.IGNORECASE):
            raise Exception(f"Invalid end time '{endTime}'!")
        
        # Insert into the database
        with self.conn:
            self.conn.execute("""
                INSERT INTO Classes (classTitle, classCode, classSession, classSemester, startTime, endTime)
                VALUES (?, ?, ?, ?, ?, ?)""", (classTitle, classCode, classSession, classSemester, startTime, endTime))
            
    def getClassList(self):
        '''Creates a list of classes in the format <classTitle>[<classSession>] (<classSemester>)'''
        classes = []

        # Get class titles, class sessions, class semester
        classTitles = self.getDatabaseFields("classTitle", "Classes")
        classSessions = self.getDatabaseFields("classSession", "Classes")
        classSemesters = self.getDatabaseFields("classSemester", "Classes")

        # Loop through the data and format each class string
        for i in range(len(classTitles)):
            classes.append(f"{classTitles[i]}[{classSessions[i]}] ({classSemesters[i]})")

        return classes

    def addStudent(self, studentName, studentID, studentClass):
        '''Create a student in the database'''

        # Check if student name is correct
        pattern = r"^[A-Za-z\s'-]+$"

        if not re.match(pattern, studentName, re.IGNORECASE):
            raise Exception(f"Invalid student name '{studentName}'!")
        
        # Check if student id is correct
        if not studentID.isdigit() and len(studentID) != 6:
            raise Exception(f"Invalid student id '{studentID}'!")
        
        # Check if the class was selected
        if studentClass == '':
            raise Exception(f"Invalid student class '{studentClass}'!")
        
        # Get the students class title
        classTitle = studentClass.split('[')[0]

        # Get the students class session
        classSession = studentClass.split('[')[1].split(']')[0]
        
        # Insert student into database
        with self.conn:
            try:
                # Get the class ID
                cur = self.conn.execute(
                    f'''SELECT classID
                        FROM Classes
                        WHERE classTitle = "{classTitle}"
                        AND classSession = '{classSession}'
                    '''
                )
                classId = cur.fetchall()
                classId = classId[0][0]
            except Exception as ea:
                messagebox.showerror("ERROR", ea)

            # Add the student
            self.conn.execute(
                f'''INSERT INTO Students
                    VALUES (?,?,?)''', (studentID, classId, studentName)
            )

    def getClassID(self, className, classSession, classSemester):
        '''Gets the ID for a class'''
        try:
            with self.conn:
                cur = self.conn.execute(
                    f'''SELECT classID
                        FROM Classes
                        WHERE classTitle = '{className}'
                        AND classSession = {classSession}
                        AND classSemester = '{classSemester}\''''
                )

                classID = cur.fetchall()
                classID = classID[0][0]
        except Exception as ea:
            messagebox.showerror("ERROR", ea)

        return classID

    def getStudentList(self, classID):
        '''Creates a list of students'''
        students = []

        try:
            with self.conn:
                cur = self.conn.execute(
                    f'''SELECT studentName
                        FROM Students
                        WHERE classID = '{classID}' 
                        ORDER BY studentName'''
                )

                studentList = cur.fetchall()

                for student in studentList:
                    students.append(student[0])

        except Exception as ea:
            messagebox.showerror("ERROR", ea)

        return students

        
        
    def getDatabaseFields(self, fieldName, tableName):
        with self.conn:
            cur = self.conn.execute(
                f'''SELECT {fieldName}
                    FROM {tableName}'''
            )
            
            results = cur.fetchall()
            L = [result[0] for result in results]

            return L
        
    def getTableLength(self, tableName):
        with self.conn:
            cur = self.conn.execute(
                f"""SELECT *
                    FROM {tableName}"""
            )
            return len(cur.fetchall())