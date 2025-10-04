from sqlalchemy import Table, Column, Integer, ForeignKey
from db.database import Base

class_student = Table(
    "class_student",
    Base.metadata,
    Column("class_id", Integer, ForeignKey("classes.id", ondelete="CASCADE"), primary_key=True),
    Column("student_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)
