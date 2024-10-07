from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import Database

# Setup the database
database = Database.Database()
  
# Create the root window
root = Tk() 

# Create the window title
root.title("Student Tracker AutoFiller")

# Create the tab control
tabControl = ttk.Notebook(root)

# Create the tabs
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

# Add the tabs
tabControl.add(tab1, text='Form Filler')
tabControl.add(tab2, text='Add Class')
tabControl.add(tab3, text='Add Student')

# Make the tabs visible
tabControl.pack(expand=1, fill='both')

# Set the windows geometry (width x height)
root.geometry('800x725')



### ==== Form Filler ====
# Add a label for the class selection
optionst1 = database.getClassList()
lbl1t1 = Label(tab1, text="Class: ", font=('Calibri 15 bold'), pady=5)        # Class session
lbl1t1.pack(anchor='w', padx=10)
combot1 = ttk.Combobox(tab1, values=optionst1, width=35)
combot1.pack(anchor='w', padx=10)

btn1t1 = Button(tab1, text="Get Students", command=lambda: getStudents())
btn1t1.pack(anchor='w', padx=10)

# Add a label for the student selection
lbl2t1 = Label(tab1, text="Students: ", font=('Calibri 15 bold'))
lbl2t1.pack(anchor='w', padx=10)

# Create a frame to hold student checkboxes
student_frame = Frame(tab1)
student_frame.pack(anchor='w', padx=10,pady=5)

students = []
checkboxs = []

def getStudents():
    global students, checkboxs

    # Clear any existing student data in the frame
    for widget in student_frame.winfo_children():
        widget.destroy()

    # Get the current class
    classInfo = combot1.get()

    # Ensure that the class was selected
    if not classInfo:
        messagebox.showerror("ERROR", "Please select a class first!")
        return

    # Parse the input string
    class_name, session_semester = classInfo.split('[')

    # Extract class session from the format '1] (Fall)'
    class_session = session_semester.split(']')[0]

    # Extract class semester from the format '(Fall)'
    class_semester = session_semester.split('(')[1].strip(')')

    # Get the list of students
    classID = database.getClassID(class_name, class_session, class_semester)
    students = database.getStudentList(classID)

    # Check that the student list is filled
    if students:
        # Create a checkbox for each student
        checkboxs = []

        # Iterate through each student
        for student in students:
            var = BooleanVar()
            checkboxs.append(var)
            checkbox = Checkbutton(student_frame, text=student, variable=var)
            checkbox.pack(anchor='w')

# Add a label for the notes input
lbl3t1 = Label(tab1, text="Notes: ", font=('Calibri 15 bold'))
lbl3t1.pack(anchor='w', padx=10)

# Adding entry field
txt3t1 = Text(tab1, width="100", height="5")
txt3t1.pack(anchor='w', padx=10, pady=20)

# Function for handling filling the student tracker form
def fillForm():
    # Get the note text
    note = txt3t1.get("1.0", "end-1c")

    # Check if the note is empty
    if note == "":
        messagebox.showerror('ERROR', 'Please insert a note!')
        return
    
    # Check which students are selected
    selected_students = []
    for i, var in enumerate(checkboxs):
        if var.get():
            selected_students.append(students[i])

    # Check if there are student selected
    if not selected_students:
        messagebox.showerror('ERROR', 'Please select at least one student!')
        return
    
    # Print the selected students (for now)
    print(f"Form filled for:{', '.join(selected_students)}")
    print(f"Note: {note}")

    # Uncheck all checkboxes after filling the form
    for var in checkboxs:
        var.set(False)
    
    # Clear the text box
    txt3t1.delete("1.0", "end")

# Btn widget 
btn2t1 = Button(tab1, text="Fill Forms",
             command=fillForm)
btn2t1.pack()



### ==== Add Class Tab ====
# Add labels and entry fields
lbl1t2 = Label(tab2, text="Class title: ", font=('Calibri 12 bold'))                  # Class title
lbl1t2.pack(anchor='w')
txt1t2 = Entry(tab2, width=50)
txt1t2.pack(anchor='w', padx=10)

lbl2t2 = Label(tab2, text="Class code: ", font=('Calibri 12 bold'), pady=5)           # Class code
lbl2t2.pack(anchor='w')
txt2t2 = Entry(tab2, width=25)
txt2t2.pack(anchor='w', padx=10)

lbl3t2 = Label(tab2, text="Class session: ", font=('Calibri 12 bold'), pady=5)        # Class session
lbl3t2.pack(anchor='w')
txt3t2 = Entry(tab2, width=3)
txt3t2.pack(anchor='w', padx=10)

lbl4t2 = Label(tab2, text="Class semester: ", font=('Calibri 12 bold'), pady=5)       # Class semester
lbl4t2.pack(anchor='w')
optionst2 = ["Fall", "Spring", "Summer"]
combot2 = ttk.Combobox(tab2, values=optionst2)
combot2.pack(anchor='w', padx=10)

lbl5t2 = Label(tab2, text="Start Time: ", font=('Calibri 12 bold'), pady=5)           # Class start time
lbl5t2.pack(anchor='w')
txt5t2 = Entry(tab2, width=20)
txt5t2.pack(anchor='w', padx=10)

lbl6t2 = Label(tab2, text="End Time: ", font=('Calibri 12 bold'), pady=5)             # Class end time
lbl6t2.pack(anchor='w')
txt6t2 = Entry(tab2, width=20)
txt6t2.pack(anchor='w', padx=10)

# Call function when class submission button is pressed
def addClassHandler():
    try:
        # Attempt to create the class in the database
        database.addClass(txt1t2.get(),
                          txt2t2.get(),
                          txt3t2.get(),
                          combot2.get(),
                          txt5t2.get(),
                          txt6t2.get())
        
        # Present the user with a completion message
        messagebox.showinfo("COMPLETE", "Class added successfully!")

        # Clear the input fields
        txt1t2.delete(0, END)  # Clear class title
        txt2t2.delete(0, END)  # Clear class code
        txt3t2.delete(0, END)  # Clear class session
        txt5t2.delete(0, END)  # Clear start time
        txt6t2.delete(0, END)  # Clear end time
        combot2.set('')           # Reset the combobox selection
    except Exception as ea:
        messagebox.showerror("ERROR", ea)

# Add the submit button
btnt2 = Button(tab2, text="Add Class", command=addClassHandler )
btnt2.pack()



### ==== Add Student Tab ====
# Add labels and entry fields
lbl1t3 = Label(tab3, text="Student Name: ", font=('Calibri 12 bold'))                  # Class title
lbl1t3.pack(anchor='w')
txt1t3 = Entry(tab3, width=50)
txt1t3.pack(anchor='w', padx=10)

lbl2t3 = Label(tab3, text="Student ID: ", font=('Calibri 12 bold'), pady=5)           # Class code
lbl2t3.pack(anchor='w')
txt2t3 = Entry(tab3, width=25)
txt2t3.pack(anchor='w', padx=10)

optionst3 = database.getClassList()
lbl3t3 = Label(tab3, text="Class: ", font=('Calibri 12 bold'), pady=5)        # Class session
lbl3t3.pack(anchor='w')
combot3 = ttk.Combobox(tab3, values=optionst3, width=35)
combot3.pack(anchor='w', padx=10)

# Function for handling refreshing of class table
def refreshClassTable():
    optionst3 = database.getClassList()
    combot3['values'] = optionst3

refresh_btn_1 = Button(tab3, text="Refresh Class List", command=refreshClassTable)
refresh_btn_1.pack(anchor='w', padx=10)

# Function for handling adding a student
def addStudentHandler():
    try:
        # Attempt to create the student in the database
        database.addStudent(txt1t3.get(),
                            txt2t3.get(),
                            combot3.get())
        
        # Present the user with a completion message
        messagebox.showinfo("COMPLETE", "Student added successfully!")

        # Clear the input fields
        txt1t3.delete(0, END)
        txt2t3.delete(0, END)
        combot3.set('')
    except Exception as ea:
        messagebox.showerror("ERROR", ea)

# Add the submit button
btnt3 = Button(tab3, text="Add Student", command=addStudentHandler)
btnt3.pack()

# Execute the graphic application
root.mainloop() 