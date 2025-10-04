from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.formassignment_model import FormAssignment
from models.formresponse_model import FormResponse
from models.class_model import Class
from models.user_model import User
from schemas.formassignment_schema import FormAssignmentCreate
from schemas.formresponse_schema import FormResponseCreate


def assign_form_to_class(db: Session, class_id: int):
    existing = db.query(FormAssignment).filter(FormAssignment.class_id == class_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un formulario asignado a esta clase")

    assignment = FormAssignment(class_id=class_id)
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


def get_form_assignments_by_class(db: Session, class_id: int):
    assignments = db.query(FormAssignment).filter(FormAssignment.class_id == class_id).all()
    return assignments


def create_form_response(db: Session, response_data: FormResponseCreate):

    assignment = db.query(FormAssignment).filter(FormAssignment.id == response_data.form_assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Asignación de formulario no encontrada")

    class_obj = db.query(Class).filter(Class.id == assignment.class_id).first()
    student = db.query(User).filter(User.id == response_data.student_id).first()
    if not student or student not in class_obj.students:
        raise HTTPException(status_code=400, detail="El estudiante no está matriculado en esta clase")

    response = FormResponse(
        form_assignment_id=response_data.form_assignment_id,
        student_id=response_data.student_id,
        answer_1=response_data.answer_1,
        answer_2=response_data.answer_2,
        answer_3=response_data.answer_3,
        answer_4=response_data.answer_4,
        answer_5=response_data.answer_5,
        answer_6=response_data.answer_6,
        answer_7=response_data.answer_7,
        answer_8=response_data.answer_8,
        answer_9=response_data.answer_9,
        answer_10=response_data.answer_10,
        answer_11=response_data.answer_11,
        answer_12=response_data.answer_12,
        answer_13=response_data.answer_13,
        answer_14=response_data.answer_14,
        answer_15=response_data.answer_15,
        answer_16=response_data.answer_16,
        answer_17=response_data.answer_17,
        answer_18=response_data.answer_18,
        answer_19=response_data.answer_19,
        answer_20=response_data.answer_20,
       
    )
    db.add(response)
    db.commit()
    db.refresh(response)
    return response


def get_form_responses_by_student(db: Session, student_id: int):
    responses = (
        db.query(FormResponse)
        .filter(FormResponse.student_id == student_id)
        .all()
    )
    return responses



def get_form_responses_by_student_and_class(db: Session, student_id: int, class_id: int):
    return (
        db.query(FormResponse)
        .join(FormAssignment, FormResponse.form_assignment_id == FormAssignment.id)
        .filter(FormResponse.student_id == student_id)
        .filter(FormAssignment.class_id == class_id)
        .all()
    )
    


def get_form_assignments_by_student(db: Session, student_id: int):
    student = db.query(User).filter(User.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    class_ids = [c.id for c in student.enrolled_classes]

    assignments = db.query(FormAssignment).filter(FormAssignment.class_id.in_(class_ids)).all()
    return assignments



def get_form_status_for_students(db: Session, class_id: int):
    class_obj = db.query(Class).filter(Class.id == class_id).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Clase no encontrada")

    assignment = db.query(FormAssignment).filter(FormAssignment.class_id == class_id).one_or_none()
    assignment_id = assignment.id if assignment else None

    results = []
    for student in class_obj.students:
        if not assignment_id:
            form_status = "no asignado"
        else:
            response = (
                db.query(FormResponse)
                .filter(
                    FormResponse.form_assignment_id == assignment_id,
                    FormResponse.student_id == student.id,
                )
                .first()
            )
            form_status = "respondido" if response else "asignado"

        results.append({
            "student_id": student.id,
            "student_name": student.name,
            "email": student.email,
            "form_status": form_status,
        })

    return results




def get_assignments_by_student_and_class(db: Session, student_id: int, class_id: int):
    student = db.query(User).filter(User.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    enrolled_class_ids = [c.id for c in student.enrolled_classes]
    if class_id not in enrolled_class_ids:
        raise HTTPException(status_code=403, detail="El estudiante no está inscrito en esta clase")

    assignments = db.query(FormAssignment).filter(FormAssignment.class_id == class_id).all()
    return assignments



def get_form_status_by_student(db: Session, student_id: int):
    student = db.query(User).filter(User.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    results = []

    for class_ in student.enrolled_classes:
        assignment = class_.form_assignments[0] if class_.form_assignments else None
        has_form = assignment is not None

        answered = False
        if has_form:
            response = (
                db.query(FormResponse)
                .filter(
                    FormResponse.form_assignment_id == assignment.id,
                    FormResponse.student_id == student_id
                )
                .first()
            )
            answered = response is not None

        results.append({
            "class_id": class_.id,
            "subject": class_.subject,
            "section": class_.section,
            "grade": class_.grade,
            "year": class_.year,
            "has_form": has_form,
            "answered": answered,
        })

    return results



def delete_form_response_by_student_and_class(db: Session, student_id: int, class_id: int):
    response = (
        db.query(FormResponse)
        .join(FormAssignment, FormResponse.form_assignment_id == FormAssignment.id)
        .filter(FormResponse.student_id == student_id)
        .filter(FormAssignment.class_id == class_id)
        .first()
    )

    if response:
        db.delete(response)
        db.commit()
        return True
    return False



def delete_all_form_responses_by_class(db: Session, class_id: int):
    responses = (
        db.query(FormResponse)
        .join(FormAssignment, FormResponse.form_assignment_id == FormAssignment.id)
        .filter(FormAssignment.class_id == class_id)
        .all()
    )

    if not responses:
        return False  

    for response in responses:
        db.delete(response)
    db.commit()
    return True
