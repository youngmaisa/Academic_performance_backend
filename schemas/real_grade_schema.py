
from pydantic import BaseModel, Field
from typing import Literal

class RealGradeFlexible(BaseModel):
    student_id: int
    class_id: int
    nota: float = Field(..., ge=0, le=20)
    target_nota: Literal['nota_1', 'nota_2', 'nota_3']


from typing import List
class RealGradeFlexibleList(BaseModel):
    grades: List[RealGradeFlexible]
    
    
    