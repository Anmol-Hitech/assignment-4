from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from response_schemas import DepRes,TeacherRes,CourseRes,EnrollRes,StudentRes,CustomStudentRes,CustomCourseres,Custometeacher,CustomLazyCourse,CustomLazyStudent,StudentInSemester,BonusDepartmentWithTeachers,BonusCustomTeacher
from input_schemas import DepartmentCreate,TeacherCreate,StudentCreate,CourseCreate,EnrollmentCreate
from models import get_db,Department,Teacher,Student,Course,Enrollment,TeacherProfile
from typing import List
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


@app.get("/lazy/teachers/{id}", response_model=Custometeacher)
def get_teacher(id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    return {
        "name": teacher.name,
        "department_name": teacher.department.name if teacher.department else None,
        "teacher_profile": {
            "qualification": teacher.teacher_profile.qualification if teacher.teacher_profile else None,
            "exp_years": teacher.teacher_profile.exp_years if teacher.teacher_profile else None
        } if teacher.teacher_profile else None
    }



@app.get("/lazy/students/{id}", response_model=CustomStudentRes)
def get_student(id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    courses = [
        CustomCourseres(
            title=enrollment.course.title,
            semester=enrollment.sem
        )
        for enrollment in student.enrollments
    ]

    return {
        "student": student.name,
        "courses": courses
    }
@app.get("/lazy/courses/{id}", response_model=CustomLazyCourse)
def get_course(id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == id).first()
    if not course:
        raise HTTPException(status_code=404, detail={"message": "Course not found"})

    students = [
        CustomLazyStudent(name=enrollment.student.name)
        for enrollment in course.enrollments
    ]

    return {
        "course": course.title,
        "students": students
    }
@app.get("/bonus/departments/{id}", response_model=BonusDepartmentWithTeachers)
def get_department(id: int, db: Session = Depends(get_db)):
    department = db.query(Department).filter(Department.id == id).first()
    if not department:
        raise HTTPException(status_code=404, detail={"message": "Department not found"})

    teachers = [
        BonusCustomTeacher(
            id=teacher.id,
            name=teacher.name,
            email=teacher.email,
            department_id=teacher.department_id
        )
        for teacher in department.teacher  
    ]

    return {
        "id": department.id,
        "name": department.name,
        "teachers": teachers
    }

@app.get("/bonus/students", response_model=List[StudentInSemester])
def get_students_by_semester(semester: int, db: Session = Depends(get_db)):
    enrollments = db.query(Enrollment).filter(Enrollment.sem == semester).all()
    students_set = {enrollment.student for enrollment in enrollments}

    students = [
        StudentInSemester(
            id=student.id,
            name=student.name,
            email=student.email
        ) for student in students_set
    ]

    return students