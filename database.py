from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base,Session

DATABASE_URL="postgresql://fastapi_user:123@localhost:5433/teachers_student_assignment_4"
engine=create_engine(DATABASE_URL)
Sessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()