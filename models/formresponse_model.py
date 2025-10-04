from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class FormResponse(Base):
    __tablename__ = "form_responses"
    id = Column(Integer, primary_key=True)
    form_assignment_id = Column(Integer, ForeignKey("form_assignments.id",  ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    answer_1 = Column(String)
    answer_2 = Column(String)
    answer_3 = Column(String)
    answer_4 = Column(String)
    answer_5 = Column(String)
    answer_6 = Column(String)
    answer_7 = Column(String)
    answer_8 = Column(String)
    answer_9 = Column(String)
    answer_10 = Column(String)
    answer_11 = Column(String)
    answer_12 = Column(String)
    answer_13 = Column(String)
    answer_14 = Column(String)
    answer_15 = Column(String)
    answer_16 = Column(String)
    answer_17 = Column(String)
    answer_18 = Column(String)
    answer_19 = Column(String)
    answer_20 = Column(String)
   
   
    form_assignment = relationship("FormAssignment", back_populates="form_responses")
    student = relationship("User", back_populates="form_responses")

