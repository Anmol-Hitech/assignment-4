from pydantic import BaseModel,EmailStr,field_validator,model_validator
from typing import Optional
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

