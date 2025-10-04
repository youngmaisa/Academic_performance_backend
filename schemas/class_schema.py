from pydantic import BaseModel

class ClassData(BaseModel):
    id: int
    subject: str
    section: str 
    grade: str
    year: int

class ClassId(ClassData):
    id: int
    
class ClassInput(BaseModel):
    subject: str
    section: str 
    grade: str
    year: int