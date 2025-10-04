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

  
router = APIRouter(prefix="/login", tags=["login"])      


@router.post("", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, form_data.username)  # ahora username será el email
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }