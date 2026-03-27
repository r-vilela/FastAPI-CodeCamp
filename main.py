from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {
        "name": "Jonh",
        "age": 15,
        "year": "year 10"
    }
}


class Student(BaseModel):
    name: str
    age: int
    year: str


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


@app.get('/')
def index():
    return {"name": "First API"}


@app.get('/get-students')
def getStudents():
    return students

# Path parameters
@app.get('/get-student/{id}')
def getStudentById(id: int = Path(description="The ID of the student you want to view", gt=0, lt=3)):
    if id in students:
        return students[id]
    return {"message": "ID not valid"}


# Query Parameters
@app.get('/get-by-year')
def getSudentByYear(student_year: str):
    students_in_year = []
    for student_id in students:
        if students[student_id]['year'] == student_year:
            students_in_year.append(students[student_id])

    return students_in_year


# Path combining with Query Parameters
@app.get('/get-by-name/{student_id}')
def getStudentByName(*, student_id: int, name: Optional[str] = None, test: int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Date": "Not found"}


# Request Body
@app.post('/create-student/{student_id}')
def createStudent(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student already exists!"}

    students[student_id] = student
    return students[student_id]


# PUT method make BaseModel atributes optional
@app.put('/update-student/{student_id}')
def updateStudent(student_id: int, update_student: UpdateStudent):
    if student_id not in students:
        return {"Error": "This Student does not exists!"}

    if update_student.name is not None:
        students[student_id].name = update_student.name

    if update_student.age is not None:
        students[student_id].age = update_student.age

    if update_student.year is not None:
        students[student_id].year = update_student.year

    return students[student_id]


# DELETE method
@app.delete('/delete-student/{student_id}')
def deleteStudent(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exists!"}

    del students[student_id]
    return {"Message": "Student deleted successfully"}

