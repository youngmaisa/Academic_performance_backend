from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.real_grade_schema import RealGradeFlexibleList
from services.real_grade_service import insert_real_grade_list_dynamic, are_all_real_grades_filled_for_nota
from security.dependencies import get_current_user
from db.database import get_db

router = APIRouter(prefix="/real-grades", tags=["Real Grades"])

@router.post("/register")
def create_real_grades(payload: RealGradeFlexibleList, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    if current_user.role != "docente":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    try:
        insert_real_grade_list_dynamic(db, payload.grades)
        return {"message": "Notas registradas correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{target_nota}/{class_id}")
def check_real_grades_status(class_id: int, target_nota: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "docente":
        raise HTTPException(status_code=403, detail="Acceso denegado")

    try:
        filled = are_all_real_grades_filled_for_nota(db, class_id, target_nota)
        return {"allFilled": filled}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
