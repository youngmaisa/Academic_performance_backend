from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.formassignment_model import FormAssignment
from models.formresponse_model import FormResponse
from models.class_model import Class
from models.user_model import User
from schemas.formassignment_schema import FormAssignmentCreate
from schemas.formresponse_schema import FormResponseCreate
from models.predictionstatus_model import PredictionStatus
from models.formresponsebackup import FormResponseBackup  
from models.formresponse_model import FormResponse
from schemas.predictionstatus_schema import PredictionStatusResponse



def get_prediction_status_by_class(db: Session, class_id: int) -> PredictionStatusResponse:
    prediction = db.query(PredictionStatus).filter(PredictionStatus.class_id == class_id).first()
    
    if not prediction:
        return PredictionStatusResponse(
            class_id=class_id,
            has_prediction1=False,
            has_prediction2=False,
            has_prediction3=False
        )
    
    return PredictionStatusResponse(
        class_id=prediction.class_id,
        has_prediction1=prediction.has_prediction1,
        has_prediction2=prediction.has_prediction2,
        has_prediction3=prediction.has_prediction3
    )



def generate_prediction_backupresponses(db: Session, class_id: int, prediction_stage: int):

    class_instance = db.query(Class).filter(Class.id == class_id).first()
    if not class_instance:
        raise HTTPException(status_code=404, detail="Clase no encontrada")


    existing_backups = db.query(FormResponseBackup).filter(
        FormResponseBackup.class_id == class_id,
        FormResponseBackup.prediction_stage == prediction_stage
    ).all()
    if existing_backups:
        raise HTTPException(status_code=400, detail="Ya existe un backup para esta predicción")

    responses = (
        db.query(FormResponse)
        .join(FormAssignment)
        .filter(FormAssignment.class_id == class_id)
        .all()
    )

    if not responses:
        raise HTTPException(status_code=404, detail="No hay respuestas para esta clase")

    for response in responses:
        backup = FormResponseBackup(
            student_id=response.student_id,
            class_id=class_id,
            prediction_stage=prediction_stage,
            answer_1=response.answer_1,
            answer_2=response.answer_2,
            answer_3=response.answer_3,
            answer_4=response.answer_4,
            answer_5=response.answer_5,
            answer_6 = response.answer_6,
            answer_7= response.answer_7,
            answer_8 = response.answer_8,
            answer_9 = response.answer_9,
            answer_10 = response.answer_10,
            answer_11 = response.answer_11,
            answer_12 = response.answer_12,
            answer_13 = response.answer_13,
            answer_14 = response.answer_14,
            answer_15 = response.answer_15,
            answer_16 = response.answer_16,
            answer_17 = response.answer_17,
            answer_18 = response.answer_18,
            answer_19 = response.answer_19,
            answer_20 = response.answer_20
            
        )
        db.add(backup)

    db.commit()
    return {"total_backups": len(responses), "class_id": class_id, "prediction_stage": prediction_stage}





def check_prediction_backup_exists(db: Session, class_id: int, prediction_stage: int) -> bool:
    return db.query(FormResponseBackup).filter_by(
        class_id=class_id,
        prediction_stage=prediction_stage
    ).first() is not None
    
    
    
 
def register_prediction_generated(db: Session, class_id: int, prediction_stage: int) -> PredictionStatusResponse:
    if prediction_stage not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="prediction_stage debe ser 1, 2 o 3")

    prediction_status = db.query(PredictionStatus).filter_by(class_id=class_id).first()
    if not prediction_status:
        prediction_status = PredictionStatus(class_id=class_id)
        db.add(prediction_status)
        db.flush()  

    if prediction_stage == 1:
        prediction_status.has_prediction1 = True
    elif prediction_stage == 2:
        prediction_status.has_prediction2 = True
    elif prediction_stage == 3:
        prediction_status.has_prediction3 = True

    db.commit()
    db.refresh(prediction_status)  

    return prediction_status



