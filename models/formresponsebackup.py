from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class FormResponseBackup(Base):
    __tablename__ = "form_response_backups"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    prediction_stage = Column(Integer, nullable=False)  # 1, 2 o 3

    
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

    
    
    
    student = relationship("User", back_populates="form_response_backups")
    class_ = relationship("Class", back_populates="form_response_backups")
