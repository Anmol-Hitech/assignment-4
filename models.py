from database import engine,Base,Sessionlocal
from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Date
from sqlalchemy.orm import relationship
from datetime import date,datetime

class Teacher(Base):
    __tablename__="teachers"
    id=Column(Integer,primary_key=True,nullable=False,unique=True,index=True)
    name=Column(String,nullable=False)
    email=Column(String,unique=True,nullable=False)
    department_id=Column(Integer,ForeignKey("departments.id",ondelete="SET NULL"),nullable=True)
    teacher_profile=relationship("TeacherProfile",back_populates="teacher",uselist=False,cascade="all, delete-orphan")
    department=relationship("Department",back_populates="teacher")

class TeacherProfile(Base):
    __tablename__="teachers_profile"
    id=Column(Integer,primary_key=True,index=True,nullable=False)
    qualification=Column(String,nullable=False)
    exp_years=Column(Integer)
    teacher_id=Column(Integer,ForeignKey("teachers.id",ondelete="CASCADE"),unique=True)
    teacher=relationship("Teacher",back_populates="teacher_profile")

class Department(Base):
    __tablename__="departments"
    id=Column(Integer,index=True,unique=True,nullable=False,primary_key=True)
    name=Column(String,unique=True,nullable=False)
    teacher=relationship("Teacher",back_populates="department")

class Course(Base):
    __tablename__="courses"
    id=Column(Integer,index=True,unique=True,nullable=False,primary_key=True)
    title=Column(String,nullable=False)
    credits=Column(Integer,nullable=False)
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")


class Student(Base):
    __tablename__="students"
    id=Column(Integer,index=True,unique=True,nullable=False,primary_key=True)
    name=Column(String,nullable=False)
    email=Column(String,unique=True,nullable=False)
    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")

class Enrollment(Base):
    __tablename__="enrollments"
    id=Column(Integer,index=True,unique=True,nullable=False,primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id",ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey("courses.id",ondelete="CASCADE"))
    sem=Column(Integer,nullable=False)
    enrolled_at=Column(DateTime,default=datetime.now,nullable=False)
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
Base.metadata.create_all(bind=engine)

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
