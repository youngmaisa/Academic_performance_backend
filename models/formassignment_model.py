from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

   
class FormAssignment(Base):
    __tablename__ = "form_assignments"
    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)


    class_ = relationship("Class", back_populates="form_assignments")
    form_responses = relationship("FormResponse", back_populates="form_assignment", 
                                  cascade="all, delete-orphan")