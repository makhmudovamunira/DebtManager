from fastapi.exceptions import HTTPException
import datetime
from fastapi import APIRouter, status, Depends
from another_fastapi_jwt_auth import AuthJWT
from schemas import SignUpModel, LoginModel
from models import User
from database import session, engine
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_

auth_router = APIRouter(
    prefix="/auth"
)
session=session( bind=engine )

@auth_router.post("/")
async def welcome():
    return {"message": "Welcome to Auth router"}

@auth_router.post("/register")
async def register(request: SignUpModel ):
    email = session.query(User).filter(User.email==request.email).first()
    if email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail='User with this username already exists')
    username = session.query(User).filter(User.username==request.username).first()
    if username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail='User with this email already exists')

    user = User(
        email=request.email,
        username=request.username,
        password=generate_password_hash(request.password),
    )

    session.add(user)
    session.commit()
    data = {
        "username": user.username,
        "email": user.email,
    }
    response = {
        "success": True,
        "message": "Registration successful",
        "data": data
    }
    return response

@auth_router.get("/list")
async def list():
    users=session.query(User).all()
    return jsonable_encoder(users)


@auth_router.post("/login")
async def login(request: LoginModel, Authorize: AuthJWT = Depends()):
    user = session.query(User).filter(or_(
        User.username == request.username_or_email,
        User.email == request.username_or_email
    )).first()
    if user is None:
        raise HTTPException(
            status_code=404, detail="Not found username"
        )

    if user and check_password_hash(user.password ,request.password):
        access_token =Authorize.create_access_token(subject=request.username_or_email)
        refresh_token = Authorize.create_refresh_token(subject=request.username_or_email)
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        response = {
            "success": True,
            "code": 200,
            "message": "success",
            "token": data
        }
        return jsonable_encoder(response)
