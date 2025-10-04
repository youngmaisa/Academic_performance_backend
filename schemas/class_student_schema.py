# schemas/class_student_model.py
from pydantic import BaseModel, EmailStr
from typing import List


class AddStudentsRequest(BaseModel):
    student_emails: List[EmailStr]