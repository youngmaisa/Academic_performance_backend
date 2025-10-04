
from pydantic import BaseModel
from typing import List, Optional


class FormResponseCreate(BaseModel):
    form_assignment_id: int
    student_id: int   
    answer_1: Optional[str]
    answer_2: Optional[str]
    answer_3: Optional[str]
    answer_4: Optional[str]
    answer_5: Optional[str]
    answer_6: Optional[str]
    answer_7: Optional[str]
    answer_8: Optional[str]
    answer_9: Optional[str]
    answer_10: Optional[str]
    answer_11: Optional[str]
    answer_12: Optional[str]
    answer_13: Optional[str]
    answer_14: Optional[str]
    answer_15: Optional[str]
    answer_16: Optional[str]
    answer_17: Optional[str]
    answer_18: Optional[str]
    answer_19: Optional[str]
    answer_20: Optional[str]
  

class FormResponseRead(BaseModel):
    id: int
    form_assignment_id: int
    student_id: int
    answer_1: Optional[str]
    answer_2: Optional[str]
    answer_3: Optional[str]
    answer_4: Optional[str]
    answer_5: Optional[str]
    answer_6: Optional[str]
    answer_7: Optional[str]
    answer_8: Optional[str]
    answer_9: Optional[str]
    answer_10: Optional[str]
    answer_11: Optional[str]
    answer_12: Optional[str]
    answer_13: Optional[str]
    answer_14: Optional[str]
    answer_15: Optional[str]
    answer_16: Optional[str]
    answer_17: Optional[str]
    answer_18: Optional[str]
    answer_19: Optional[str]
    answer_20: Optional[str]



class FormAssignmentWithResponses(BaseModel):
    id: int
    class_id: int
    responses: List[FormResponseRead] = []