from pydantic import BaseModel

class UserData(BaseModel):
    id: int
    email: str
    name: str
    password: str
    role: str
    

class UserId(UserData):
    id: int

class UserCreateRequest(BaseModel):
    email: str
    name: str
    password: str
    role: str


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
   