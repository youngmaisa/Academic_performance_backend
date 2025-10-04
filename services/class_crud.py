from sqlalchemy.orm import Session
from models.class_model import Class
from schemas.class_schema import ClassData, ClassInput
from fastapi import HTTPException


def get_classes_by_teacher(db: Session, teacher_id: int):
    return db.query(Class).filter(Class.teacher_id == teacher_id).all()

def create_class(db: Session, class_data: ClassInput, teacher_id: int):
    new_class = Class(
        subject=class_data.subject,
        section=class_data.section,
        grade=class_data.grade,
        year=class_data.year,
        teacher_id=teacher_id  
    )
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class


def get_class_by_id(db: Session, class_id: int):
    class_ = db.query(Class).filter(Class.id == class_id).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Clase no encontrada")
    return class_


def delete_class(db: Session, class_id: int):
    class_ = db.query(Class).filter(Class.id == class_id).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Clase no encontrada")
    
    db.delete(class_)
    db.commit()
    return {"message": "Clase eliminada correctamente"}

