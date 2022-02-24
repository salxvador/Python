"""
    Creating parent class 'Student' and child classes
    'SpecialNeeds' and 'Graduated'
"""

class Student:
    #attributes for the parent class with placeholders
    name = "No Name Provided"
    grade = ""
    email = ""
    studentID = "00000"

class SpecialNeeds(Student):
    #attributes specific to special needs students with placeholders.
    disabilityCode = "no code entered"
    IEPDate = "mm/dd/yyyy"

class Graduated(Student):
    #attributes for graduated students.
    graduationDate: "mm/dd/yyyy"
    finalGPA = 0.00
