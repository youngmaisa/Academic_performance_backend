from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware


from sqlalchemy.orm import Session
from services import user_crud
from db.database import SessionLocal, engine
from schemas.user_schema import UserData, UserId
from models.user_model import User
from models.user_model import Base
from routes import prediction_risk_routes, prediction_status_routes, user_routes, login_routes, class_routes, forms_routes, real_grade_routes
        
        
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_routes.router)
app.include_router(login_routes.router)
app.include_router(class_routes.router)
app.include_router(forms_routes.router)
app.include_router(prediction_status_routes.router)
app.include_router(real_grade_routes.router)
app.include_router(prediction_risk_routes.router)

origins = [
    "http://localhost:5173"  # dirección donde corre tu frontend
    #"https://tusitiofrontend.com"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)


@app.get("/")
def root():
    return {"message": "Hello World"}
        

