from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from schemas.user_schema import UserData
from schemas.formstatus_schema import StudentFormStatus, ClassFormStatus
from schemas.formassignment_schema import (
    FormAssignmentCreate, FormAssignmentRead
)
from schemas.formresponse_schema import FormResponseCreate, FormResponseRead
from services.form_service import (
    assign_form_to_class,
    get_form_assignments_by_class,
    create_form_response,
    get_form_responses_by_student,
    get_form_assignments_by_student,
    get_form_status_for_students,
    get_assignments_by_student_and_class,
    get_form_status_by_student,
    get_form_responses_by_student_and_class,
    delete_form_response_by_student_and_class,
    delete_all_form_responses_by_class
)
from security.dependencies import get_current_user



router = APIRouter(prefix="/forms", tags=["Forms"])


@router.post("/assign", response_model=FormAssignmentRead)
def assign_form_class_(class_assignment: FormAssignmentCreate, db: Session = Depends(get_db), current_user: UserData = Depends(get_current_user)):
    if current_user.role != "docente":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    return assign_form_to_class(db, class_assignment.class_id)



@router.get("/assignments/class/{class_id}", response_model=List[FormAssignmentRead])
def get_assignments_by_class(class_id: int, db: Session = Depends(get_db), current_user: UserData = Depends(get_current_user)):
    if current_user.role != "docente":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    return get_form_assignments_by_class(db, class_id)



@router.post("/responses", response_model=FormResponseRead)
def create_form_response_student(response_data: FormResponseCreate, db: Session = Depends(get_db), current_user: UserData = Depends(get_current_user)):
    if current_user.role != "estudiante" or current_user.id != response_data.student_id:
        raise HTTPException(status_code=403, detail="No autorizado para responder este formulario")
    return create_form_response(db, response_data)
  
  
  
@router.get("/status/class/{class_id}", response_model=List[StudentFormStatus])
def get_form_status_by_class(class_id: int, db: Session = Depends(get_db), current_user: UserData = Depends(get_current_user)):
    if current_user.role != "docente":
        raise HTTPException(status_code=403, detail="Acceso denegado")

    return get_form_status_for_students(db, class_id)



@router.get("/responses/student/{student_id}", response_model=List[FormResponseRead])
def get_responses_by_student(student_id: int, db: Session = Depends(get_db)):
    return get_form_responses_by_student(db, student_id)




@router.get("/assignments/student/{student_id}", response_model=List[FormAssignmentRead])
def get_assignments_by_student(student_id: int, db: Session = Depends(get_db), current_user: UserData = Depends(get_current_user)):
    if current_user.role != "estudiante":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    return get_form_assignments_by_student(db, student_id)




@router.get("/assignments/student/{student_id}/class/{class_id}", response_model=list[FormAssignmentRead])
def get_assignments_student_class(student_id: int, class_id: int, db: Session = Depends(get_db), current_user: UserData = Depends(get_current_user)):
    if current_user.role != "estudiante":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    return get_assignments_by_student_and_class(db, student_id, class_id)




@router.get("/status/student/{student_id}", response_model=List[ClassFormStatus])
def get_form_status_by_student_route(student_id: int, db: Session = Depends(get_db), current_user: UserData = Depends(get_current_user)):
    if current_user.role != "estudiante" or current_user.id != student_id:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    return get_form_status_by_student(db, student_id)




@router.get("/respuestas/{class_id}/{student_id}")
def obtener_respuestas(class_id: int, student_id: int, db: Session = Depends(get_db), current_user: UserData = Depends(get_current_user)):
    if current_user.role != "docente":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    return get_form_responses_by_student_and_class(db, student_id, class_id)



    
@router.delete("/responses/class/{class_id}", status_code=204)
def delete_responses_by_class(class_id: int, db: Session = Depends(get_db), current_user: UserData = Depends(get_current_user)):
    if current_user.role != "docente":
        raise HTTPException(status_code=403, detail="Acceso denegado")

    success = delete_all_form_responses_by_class(db, class_id)

    if not success:
        raise HTTPException(status_code=404, detail="No se encontraron respuestas para eliminar en esta clase")



@router.delete("/responses/student/{student_id}/class/{class_id}", status_code=204)
def delete_response(student_id: int, class_id: int, db: Session = Depends(get_db), current_user: UserData = Depends(get_current_user)):
    success = delete_form_response_by_student_and_class(db, student_id, class_id)
    if current_user.role != "docente":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    if not success:
        raise HTTPException(status_code=404, detail="Respuesta no encontrada")
    
    
