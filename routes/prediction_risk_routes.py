from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from security.dependencies import get_current_user
from db.database import get_db
from services.prediction_risk_service import predict_by_stage
from services.prediction_status_service import register_prediction_generated
from services.prediction_risk_service import get_predictions_by_class_and_stage
from services.prediction_risk_service import get_detailed_prediction_explanation_for_student


router = APIRouter(prefix="/mlpredictions", tags=["Predicciones"])

@router.post("/{stage}/{class_id}")
def generate_prediction(stage: int, class_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "docente":
        raise HTTPException(status_code=403, detail="Acceso denegado")

    predictions = predict_by_stage(stage, class_id, db)
    register_prediction_generated(db, class_id, stage)

    return {
        "message": f"Predicción {stage} generada y almacenada correctamente.",
        "result":predictions
    }



@router.get("/class/{class_id}/{stage}")
def get_predicted_risks(class_id: int, stage: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    
    return get_predictions_by_class_and_stage(class_id, stage, db)


@router.get("/student/{class_id}/{stage}/{student_id}")
def get_detailed_prediction_explanation_for_student_route(
    class_id: int,
    stage: int,
    student_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    
    if current_user.role == "estudiante" and current_user.id != student_id:
        raise HTTPException(status_code=403, detail="No puedes ver la predicción de otro estudiante.")

    return get_detailed_prediction_explanation_for_student(class_id, stage, student_id, db)



