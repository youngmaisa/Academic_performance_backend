from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base


from models.class_student_model import class_student


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    name = Column(String(30),index=True)
    password = Column(String(100), index=True)
    role = Column(String(30), index=True)

    classes_created = relationship("Class", back_populates="teacher")

    enrolled_classes = relationship(
        "Class",
        secondary=class_student,
        back_populates="students",
        passive_deletes=True
    )
    
     
    form_responses = relationship("FormResponse", back_populates="student", cascade="all, delete-orphan")


    form_response_backups = relationship(
        "FormResponseBackup",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    real_grades = relationship(
        "RealGrade",
        back_populates="student",
        cascade="all, delete-orphan"
    )
    
    predicted_risks = relationship("PredictedRisk", back_populates="student", cascade="all, delete-orphan")
