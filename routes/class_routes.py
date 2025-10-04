from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user_schema import UserData, UserId
from schemas.class_schema import ClassData, ClassId , ClassInput
from schemas.class_student_schema import AddStudentsRequest
from services import class_crud
from services import user_crud
from db.database import SessionLocal, engine
from security.dependencies import get_current_user
from security.has_role import get_has_role
from db.database import get_db
from services import class_service
from schemas.user_schema import UserResponse  


router = APIRouter(prefix="/classes", tags=["classes"])


@router.get("/my", response_model=list[ClassData])
def get_classes(db: Session = Depends(get_db), current_user: UserData = Depends(get_current_user)):
    
    if current_user.role != "docente":
        raise HTTPException(status_code=403, detail="Acceso denegado")

  
    classes = class_crud.get_classes_by_teacher(db, current_user.id)
    return classes



@router.post("/create", response_model=ClassData)
def create_class(class_data: ClassInput, db: Session = Depends(get_db), current_user: UserData = Depends(get_current_user)):
    if current_user.role != "docente":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    new_class = class_crud.create_class(db, class_data, teacher_id=current_user.id)
    return new_class



@router.post("/students/add/{class_id}")
def add_students_to_class(
    class_id: int,
    request: AddStudentsRequest,
    db: Session = Depends(get_db),
    current_user: UserData = Depends(get_current_user)
):
    if current_user.role != "docente":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    return class_service.add_students_to_class(db, class_id, request.student_emails)




@router.get("/students/{class_id}", response_model=list[UserResponse])
def get_students_by_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: UserData = Depends(get_current_user)
):
    if current_user.role != "docente":
        raise HTTPException(status_code=403, detail="Acceso denegado")

    return class_service.get_students_by_class(db, class_id)



@router.get("/{class_id}", response_model=ClassData)
def get_class_by_id(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: UserData = Depends(get_current_user)
):
    if current_user.role != "docente":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    return class_crud.get_class_by_id(db, class_id)



@router.delete("/{class_id}/students/{student_id}")
def remove_student_from_class(
    class_id: int,
    student_id: int,
    db: Session = Depends(get_db),
    current_user: UserData = Depends(get_current_user)
):
    if current_user.role != "docente":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    return class_service.remove_student_from_class(db, class_id, student_id)


@router.delete("/{class_id}")
def delete_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: UserData = Depends(get_current_user)
):
    if current_user.role != "docente":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    return class_crud.delete_class(db, class_id)



@router.get("/students/{student_id}/classes", response_model=list[ClassData])
def read_student_classes(student_id: int, db: Session = Depends(get_db), current_user: UserData = Depends(get_current_user)):
    if current_user.role != "estudiante":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    return class_service.get_classes_by_student(db, student_id)