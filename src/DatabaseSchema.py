tables = {
    "Classes": {
        "classID": "integer primary key",
        "classTitle": "text",
        "classCode": "text",
        "classSession": "int",
        "classSemester": "text",
        "startTime": "text",
        "endTime": "text"
    },
    "Students": {
        "studentID": "integer primary key",
        "classID": "integer",
        "studentName": "text",
        "foreign key (classID)": "references Classes(classID)"
    }
}
