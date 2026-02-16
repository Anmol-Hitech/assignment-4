from pydantic import BaseModel,EmailStr,field_validator,model_validator
from typing import Optional,List
from datetime import datetime

class DepRes(BaseModel):
    id:int
    name:str
class TeacherProfileRes(BaseModel):
    qualification: str
    exp_years: int

    class Config:
        from_attributes = True


class TeacherRes(BaseModel):
    id: int
    name: str
    email: EmailStr
    department_id: Optional[int]
    teacher_profile: Optional[TeacherProfileRes]

class StudentRes(BaseModel):
    id:int
    name:str
    email:EmailStr
class CourseRes(BaseModel):
    id:int
    title:str
    credits:int
class EnrollRes(BaseModel):
    id:int
    student_id:int
    course_id:int
    sem:int
    enrolled_at:datetime
class CustomCourseres(BaseModel):
    title:str
    semester:int
class CustomStudentRes(BaseModel):

    student:str
    courses:List[CustomCourseres]=[]

class Custometeacher(BaseModel):
    name: str
    department_name: Optional[str]
    teacher_profile: Optional[TeacherProfileRes]
class CustomLazyStudent(BaseModel):
    name:str
class CustomLazyCourse(BaseModel):
    course:str
    students:List[CustomLazyStudent]

class StudentInSemester(BaseModel):
    id: int
    name: str
    email: str

class BonusCustomTeacher(BaseModel):
    id: int
    name: str
    email: str
    department_id: Optional[int]

class BonusDepartmentWithTeachers(BaseModel):
    id: int
    name: str
    teachers: List[BonusCustomTeacher] = []