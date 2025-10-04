from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class PredictedRisk(Base):
    __tablename__ = "predicted_risks"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    prediction_stage = Column(Integer, nullable=False)  
    predicted_risk = Column(String, nullable=False)  

    student = relationship("User", back_populates="predicted_risks")
    class_ = relationship("Class", back_populates="predicted_risks")

    lime_explanation = relationship("LIMEExplanation", back_populates="predicted_risk", uselist=False,  cascade="all, delete-orphan")

