from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date

class Settings(BaseModel):
    authjwt_secret_key:str = 'c17c08f66cd85f310e227aee7213dee3eb8042a3d8fddb12e5d70f33961837a4'
    # authjwtalgorithm:str = 'HS256'


class SignUpModel(BaseModel):
    username: str
    email:str
    password:str

    class Config:
        from_attributes  = True
        json_schema_extra = {
            'example': {
                "username":"Munira",
                "email": "a@gmail.com",
                "password":"password1234",
            }
        }

class UserOutModel(BaseModel):
    email: EmailStr
    username: str
    password: str

    class Config:
        from_attributes  = True

class LoginModel(BaseModel):
    username_or_email: str
    password: str

    class Config:
        from_attributes  = True
        json_schema_extra = {
            'example': {
                "username": "john",
                "password": "password1234",
            }
        }


class DebtModel(BaseModel):
    debt_type:str='OWED_TO'
    debt_valyuta:str="UZS"
    amount: float=0
    due_date:datetime
    first_name:str
    phone:Optional[str]=None




