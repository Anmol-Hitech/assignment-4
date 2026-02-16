from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator, model_validator, Field

class TeacherCreate(BaseModel):
    name: str
    email: EmailStr
    department_id: int | None = None
    qualification: str
    exp_years: int

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Name required")
        return v

    @field_validator("exp_years")
    @classmethod
    def experience_positive(cls, v):
        if v < 0:
            raise ValueError("Experience cannot be negative")
        return v

class DepartmentCreate(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v):
        if not v.strip():
            raise ValueError("Department name req")
        return v

class StudentCreate(BaseModel):
    name: str
    email: EmailStr

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v):
        if not v.strip():
            raise ValueError("Name req")
        return v


class CourseCreate(BaseModel):
    title: str
    credits: int = Field(gt=0)

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v):
        if not v.strip():
            raise ValueError("Title req")
        return v


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    sem: int = Field(gt=0)

    @model_validator(mode="after")
    def check_ids(self):
        if self.student_id <= 0 or self.course_id <= 0:
            raise ValueError("Atleast one student or course id req")
        return self
    
