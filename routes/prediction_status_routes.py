from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from security.hashing import verify_password
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine
from schemas.user_schema import UserData, UserId
from services import user_crud
from security.token import create_access_token  
from pydantic import BaseModel
from db.database import get_db
from schemas.token_schema import Token
from services.prediction_status_service import get_prediction_status_by_class
from schemas.predictionstatus_schema import PredictionStatusResponse
from security.dependencies import get_current_user
from services.prediction_status_service import generate_prediction_backupresponses  # Asegúrate que esté bien importado
from schemas.predicctionbackup_schema import PredictionBackupResponse, PredictionBackupRequest
from services.prediction_status_service import (
    get_prediction_status_by_class,
    generate_prediction_backupresponses,
    check_prediction_backup_exists,
    register_prediction_generated
)

router = APIRouter(prefix="/statusprediction", tags=["statusprediction"])      


@router.get("/classes/{class_id}/predictions-status", response_model=PredictionStatusResponse)
def get_predictions_status(class_id: int, db: Session = Depends(get_db), current_user: UserData = Depends(get_current_user)):
    
    return get_prediction_status_by_class(db, class_id)



@router.post("/backup", response_model=PredictionBackupResponse)
def create_prediction_backuprespomses(
    data: PredictionBackupRequest,
    db: Session = Depends(get_db),
    current_user: UserData = Depends(get_current_user)
):
    if current_user.role != "docente":
        raise HTTPException(status_code=403, detail="Acceso denegado")

    return generate_prediction_backupresponses(db, data.class_id, data.prediction_stage)


@router.get("/backup-exists/{class_id}/{prediction_stage}", response_model=bool)
def prediction_backupresponses_exists(
    class_id: int,
    prediction_stage: int,
    db: Session = Depends(get_db),
    current_user: UserData = Depends(get_current_user)
):
    if current_user.role != "docente":
        raise HTTPException(status_code=403, detail="Acceso denegado")

    return check_prediction_backup_exists(db, class_id, prediction_stage)

