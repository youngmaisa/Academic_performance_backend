from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user_schema import UserData, UserId, UserCreateRequest
from services import user_crud
from db.database import SessionLocal, engine
from security.dependencies import get_current_user
from db.database import get_db


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def read_me(current_user = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "role": current_user.role
    }
    
    
@router.get("", response_model=list[UserId])
def get_users(db: Session = Depends(get_db)):
    users = user_crud.get_users(db)
    return users


@router.post("/create", response_model=UserId)
def crear_user(user: UserCreateRequest, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Usuario ya existente")
    return user_crud.create_user(db=db, user=user)



@router.get("/users/by-email/{email}", response_model=UserId)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.get("/{user_id}", response_model=UserId)     
def get_user_by_id(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    user = user_crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.delete("/{user_id}", response_model=UserId)  
def delete_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_user = user_crud.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user_crud.delete_user(db=db, user_id=user_id)


@router.put("/{user_id}", response_model=UserId)
def update_user(user_id: int, user: UserData, db: Session = Depends(get_db) , current_user = Depends(get_current_user)):
    db_user = user_crud.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user_crud.update_user(db=db, user_id=user_id, user=user)

