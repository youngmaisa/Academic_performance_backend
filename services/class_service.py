
from sqlalchemy.orm import Session
from sqlalchemy import and_

from fastapi import HTTPException
from models.class_model import Class
from models.user_model import User
from models.formresponse_model import FormResponse
from models.formresponsebackup import FormResponseBackup
from models.realgrade_model import RealGrade



def add_students_to_class(db: Session, class_id: int, student_emails: list[str]):
    
    class_obj = db.query(Class).filter(Class.id == class_id).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Clase no encontrada")

    not_found_emails = []
    
    for email in student_emails:
        student = db.query(User).filter(User.email == email, User.role == "estudiante").first()
        if not student:
            not_found_emails.append(email)
            continue

        if student not in class_obj.students:
            class_obj.students.append(student)

    db.commit()
    return {
        "message": "Estudiantes añadidos correctamente",
        "no_encontrados": not_found_emails
    }




def get_students_by_class(db: Session, class_id: int):
    class_obj = db.query(Class).filter(Class.id == class_id).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Clase no encontrada")

    return class_obj.students



def remove_student_from_class(db: Session, class_id: int, student_id: int):
    class_obj = db.query(Class).filter(Class.id == class_id).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Clase no encontrada")

    student = db.query(User).filter(User.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    if student in class_obj.students:
        class_obj.students.remove(student)
        
        db.commit()

    return {"message": f"Estudiante {student.email} removido de la clase"}



def get_classes_by_student(db: Session, student_id: int):
    student = db.query(User).filter(User.id == student_id, User.role == "estudiante").first()
    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

   
    return student.enrolled_classes




