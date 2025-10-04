from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from models.class_student_model import class_student
from models.predictionstatus_model import PredictionStatus

class Class(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    subject = Column(String, nullable=False)
    section = Column(String, nullable=False)
    grade = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    
    teacher = relationship("User", back_populates="classes_created")

    
    students = relationship(
        "User",
        secondary=class_student,
        back_populates="enrolled_classes",
         passive_deletes=True
    )

   
    form_assignments = relationship("FormAssignment", back_populates="class_",  
                                    cascade="all, delete-orphan")
   
    form_response_backups = relationship(
        "FormResponseBackup",
        back_populates="class_",
        cascade="all, delete-orphan"
    )

    real_grades = relationship(
    "RealGrade",
    back_populates="class_",
    cascade="all, delete-orphan"
    )
    

    prediction_status = relationship("PredictionStatus", back_populates="class_", uselist=False, cascade="all, delete-orphan")

    
    predicted_risks = relationship("PredictedRisk", back_populates="class_", cascade="all, delete-orphan")
