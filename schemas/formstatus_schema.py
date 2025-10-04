
from pydantic import BaseModel
from typing import List, Optional


class StudentFormStatus(BaseModel):
    student_id: int
    student_name: str
    email: str
    form_status: str
    
    
class ClassFormStatus(BaseModel):
    class_id: int
    subject: str
    section: str
    grade: str
    year: int
    has_form: bool
    answered: bool
