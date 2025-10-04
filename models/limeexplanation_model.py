from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.database import Base

class LIMEExplanation(Base):
    __tablename__ = "lime_explanations"

    id = Column(Integer, primary_key=True)
    predicted_risk_id = Column(Integer, ForeignKey("predicted_risks.id", ondelete="CASCADE"), nullable=False)
    explanation_json = Column(Text, nullable=False)

    predicted_risk = relationship("PredictedRisk", back_populates="lime_explanation")