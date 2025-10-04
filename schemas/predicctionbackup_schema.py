# backend/schemas/backup_schema.py
from pydantic import BaseModel

class PredictionBackupResponse(BaseModel):
    total_backups: int
    class_id: int
    prediction_stage: int
    
    
    
class PredictionBackupRequest(BaseModel):
    class_id: int
    prediction_stage: int