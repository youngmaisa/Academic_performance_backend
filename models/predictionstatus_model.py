from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base




class PredictionStatus(Base):
    __tablename__ = "prediction_status"

    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), unique=True, nullable=False)

    has_prediction1 = Column(Boolean, default=False)
    has_prediction2 = Column(Boolean, default=False)
    has_prediction3 = Column(Boolean, default=False)

   
    class_ = relationship("Class", back_populates="prediction_status")
