from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.formassignment_model import FormAssignment
from models.class_model import Class
from models.user_model import User
from schemas.formassignment_schema import FormAssignmentCreate
from schemas.formresponse_schema import FormResponseCreate
from models.predictionstatus_model import PredictionStatus
from models.formresponsebackup import FormResponseBackup  
from models.class_model import Class
from models.formresponse_model import FormResponse
from schemas.predictionstatus_schema import PredictionStatusResponse
from models.realgrade_model import RealGrade
from schemas.real_grade_schema import RealGradeFlexible
from typing import List


def insert_real_grade_dynamic(db: Session, data: RealGradeFlexible):
    existing = db.query(RealGrade).filter(
        RealGrade.student_id == data.student_id,
        RealGrade.class_id == data.class_id
    ).first()

    if existing:
       
        setattr(existing, data.target_nota, data.nota)
        db.commit()
        return

    new_grade = RealGrade(
        student_id=data.student_id,
        class_id=data.class_id,
    )
    setattr(new_grade, data.target_nota, data.nota)
    db.add(new_grade)
    db.commit()


def insert_real_grade_list_dynamic(db: Session, grade_list: List[RealGradeFlexible]):
    for grade in grade_list:
        insert_real_grade_dynamic(db, grade)


def are_all_real_grades_filled_for_nota(db: Session, class_id: int, target_nota: str) -> bool:
    from backend.models.user_model import User

    if target_nota not in {"nota_1", "nota_2", "nota_3"}:
        raise ValueError("Campo de nota inválido")

    students_in_class = db.query(User).join(RealGrade).filter(RealGrade.class_id == class_id).all()

    if not students_in_class:
        return False

    student_ids = [s.id for s in students_in_class]

    
    
    column = getattr(RealGrade, target_nota, None)
    if column is None:
        raise ValueError(f"{target_nota} no es un campo válido")

    grades_with_nota = db.query(RealGrade).filter(
        RealGrade.class_id == class_id,
        RealGrade.student_id.in_(student_ids),
        column.isnot(None)
    ).count()

    return grades_with_nota == len(student_ids)


