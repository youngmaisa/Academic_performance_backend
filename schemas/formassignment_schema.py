from pydantic import BaseModel, EmailStr
from typing import List


# Para crear una nueva asignación de formulario a una clase (sin student_id)
class FormAssignmentCreate(BaseModel):
    class_id: int


# Para mostrar la asignación en lectura (sin student_id)
class FormAssignmentRead(BaseModel):
    id: int
    class_id: int

