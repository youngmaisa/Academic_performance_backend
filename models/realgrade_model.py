from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class RealGrade(Base):
    __tablename__ = "real_grades"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)

    nota_1 = Column(Float, nullable=True)
    nota_2 = Column(Float, nullable=True)
    nota_3 = Column(Float, nullable=True)  


    student = relationship("User", back_populates="real_grades")
    class_ = relationship("Class", back_populates="real_grades")