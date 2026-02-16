from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from response_schemas import DepRes,TeacherRes,CourseRes,EnrollRes,StudentRes
from input_schemas import DepartmentCreate,TeacherCreate,StudentCreate,CourseCreate,EnrollmentCreate
from models import get_db,Department,Teacher,Student,Course,Enrollment,TeacherProfile

app=FastAPI()

@app.post("/departments/",response_model=DepRes)
def create_department(department:DepartmentCreate,db:Session=Depends(get_db)):
    db_dep=Department(**department.model_dump())
    db.add(db_dep)
    db.commit()
    db.refresh(db_dep)
    return db_dep

@app.post("/teachers/", response_model=TeacherRes)
def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):

    db_teacher = Teacher(
        name=teacher.name,
        email=teacher.email,
        department_id=teacher.department_id,
        teacher_profile=TeacherProfile(
            qualification=teacher.qualification,
            exp_years=teacher.exp_years
        )
    )

    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)

    return db_teacher

@app.post("/student/",response_model=StudentRes)
def create_student(student:StudentCreate,db:Session=Depends(get_db)):
    db_student=Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.post("/courses/",response_model=CourseRes)
def create_course(course:CourseCreate,db:Session=Depends(get_db)):
    db_course=Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@app.post("/enroll/",response_model=EnrollRes)
def create_enrollment(enroll:EnrollmentCreate,db:Session=Depends(get_db)):
    db_enroll=Enrollment(**enroll.model_dump())
    db.add(db_enroll)
    db.commit()
    db.refresh(db_enroll)
    return db_enroll
