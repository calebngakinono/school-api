
from fastapi import Depends, FastAPI, status, HTTPException
from sqlmodel import Session, select

from database import get_db
from models import Instructor, Student
from schemas import CreateStudentRequest, CreateStudentResponse, CreateInstructorRequest, CreateInstructorResponse, CreateCourseRequest, CreateCourseResponse
from models import Course

app = FastAPI()


@app.get("/students")
async def get_students(db: Session = Depends(get_db)) -> list[Student]:
    return db.exec(select(Student)).all()


@app.post("/students")
async def create_student(new_student: CreateStudentRequest, db: Session = Depends(get_db)) -> CreateStudentResponse:
    student = Student(**new_student.model_dump())
    db.add(student)
    db.commit()
    return CreateStudentResponse(student_id=student.student_id)


@app.delete("/students/{student_id}")
async def delete_student(student_id: int, db: Session = Depends(get_db)) -> None:
    student: Student | None = db.get(Student, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail=f"Student with ID {
                            student_id} not found")

    db.delete(student)
    db.commit()


@app.post("/courses")
async def create_course(new_course: CreateCourseRequest, db: Session = Depends(get_db)) -> CreateCourseResponse:
    course = Course(**new_course.model_dump())
    db.add(course)
    db.commit()
    return CreateCourseResponse(course_id=course.course_id)


@app.get("/courses")
async def get_courses(db: Session = Depends(get_db)) -> list[Course]:
    return db.exec(select(Course)).all()


@app.delete("/courses/{course_id}")
async def delete_course(course_id: int, db: Session = Depends(get_db)) -> None:
    course: Course | None = db.get(Course, course_id)

    if course is None:
        raise HTTPException(status_code=404, detail=f"Course with ID {
                            course_id} not found")

    db.delete(course)
    db.commit()


@app.post("/instructors")
async def create_instructor(new_instructor: CreateInstructorRequest, db: Session = Depends(get_db)) -> CreateInstructorResponse:
    instructor = Instructor(**new_instructor.model_dump())
    db.add(instructor)
    db.commit()
    return CreateInstructorResponse(instructor_id=instructor.id)


@app.get("/instructors")
async def get_instructors(db: Session = Depends(get_db)) -> list[Instructor]:
    return db.exec(select(Instructor)).all()


@app.get("/instructors/{id}")
async def get_instructor_courses(id: int, db: Session = Depends(get_db)) -> list[str]:
    instructor: Instructor | None = db.get(Instructor, id)

    if instructor is None:
        raise HTTPException(
            status_code=404, detail=f"Instructor with ID {id} not found ")

    course_names: list[str] = []

    for course in instructor.courses:
        course_names.append(course.course_number)
    return course_names


@app.delete("/instructors/{instructor_id}")
async def delete_instructor(instructor_id: int, db: Session = Depends(get_db)) -> None:
    instructor: Instructor | None = db.get(Instructor, instructor_id)

    if instructor is None:
        raise HTTPException(status_code=404, detail=f"Instructor with ID {
                            instructor_id} not found")

    db.delete(instructor)
    db.commit()
