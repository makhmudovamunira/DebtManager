from datetime import datetime, date
from fastapi.exceptions import HTTPException
from sqlalchemy import func
from fastapi import APIRouter, Depends
from another_fastapi_jwt_auth import AuthJWT
from sqlalchemy.exc import NoResultFound
from models import User, Debt
from database import session, engine, Base
from schemas import DebtModel
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder



debt_router=APIRouter(
    prefix="/debt",
    tags=["debt"]
)

session = session(bind=engine)
@debt_router.get("/debt")
async def debt():
    pass

@debt_router.post("/create")
async def create( request: DebtModel,Authorize: AuthJWT = Depends()):
    try:
        auth = Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Not authenticated")

    current_user = Authorize.get_jwt_subject()
    print(current_user)
    request_user = session.query(User).filter(User.username == current_user).first()
    if request_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    debt=Debt(
        amount=request.amount,
        debt_type=request.debt_type,
        debt_valyuta=request.debt_valyuta,
        given_date=datetime.now().date(),
        due_date=request.due_date,
        first_name=request.first_name,
        phone=request.phone,
        user_id=request_user.id
    )
    session.add(debt)
    session.commit()
    data = {
        "first_name": request.first_name,
        "phone": request.phone,
        "amount": request.amount,
        "debt_type": request.debt_type,
        "debt_valyuta": request.debt_valyuta,

    }
    response = {
        "success": True,
        "message": "Created Debt Successfully",
        "data": data
    }
    return response


@debt_router.get("/list")
async def list(Authorize: AuthJWT = Depends()):
    try:
        auth = Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Not authenticated")
    # current_user = Authorize.get_jwt_subject()
    debts = session.query(Debt).all()
    return jsonable_encoder(debts)



@debt_router.put("/{id}/update")
async def update(id:int, request: DebtModel,Authorize: AuthJWT = Depends()):
    try:
        auth = Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Not authenticated")

    current_user = Authorize.get_jwt_subject()
    request_user = session.query(User).filter(User.username == current_user).first()
    if request_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    debts = session.query(Debt).filter(Debt.user_id == request_user.id).all()
    for debt in debts:
        if id==debt.id:
            for k,v in request.dict(exclude_unset=True).items():
                setattr(debt, k, v)
            session.commit()
            data = {
                "id":debt.id,
                "first_name": request.first_name,
                "amount": request.amount,
                "debt_type": request.debt_type,
                "debt_valyuta": request.debt_valyuta,
            }
            response = {
                "success": True,
                "message": "Updated Debt Successfully",
                "data": data
            }
            return response

    raise HTTPException(status_code=404, detail="Not found debt")

@debt_router.delete("/{id}/delete")
async def delete(id:int, Authorize: AuthJWT = Depends()):
    try:
        auth = Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Not authenticated")

    current_user = Authorize.get_jwt_subject()
    user=session.query(User).filter(User.username == current_user).first()
    if user is None:
        raise HTTPException(status_code=404 ,detail='Not found user')
    debt=session.query(Debt).filter(Debt.id == id).first()
    if debt in user.debt:
        session.delete(debt)
        session.commit()
        data = {
            'success': True,
            'message': 'Deleted Debt Successfully',
        }
        return data
    data = {
        'success': True,
        'message': 'Deleted Debt Successfully',
    }
    return data


@debt_router.get("/owed_to_me")
async def owed_to_me(Authorize: AuthJWT = Depends()):
    try:
        auth = Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Not authenticated")

    current_user = Authorize.get_jwt_subject()
    user=session.query(User).filter(User.username == current_user).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    debts=session.query(Debt).filter(Debt.user_id == user.id, Debt.debt_type=="OWED_TO").all()
    s=0
    for debt in debts:
        if debt.debt_valyuta=="UZS":
            s+=debt.amount
        elif debt.debt_valyuta=="USD":
            usd_amount=debt.amount*12070
            s+=usd_amount
        elif debt.debt_valyuta=="EUR":
            eur_amount=debt.amount*13700
            s+=eur_amount
        elif debt.debt_valyuta=="RUB":
            rub_amount=debt.amount*155
            s+=rub_amount
        else:
            s+=0

        response = {
            "success": True,
            "debts":debts,
            "Total amount": s
        }



    return response


@debt_router.get("/owed_by_me")
async def owed_by_me(Authorize: AuthJWT = Depends()):
    try:
        auth = Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Not authenticated")

    current_user = Authorize.get_jwt_subject()
    user=session.query(User).filter(User.username == current_user).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    debts=session.query(Debt).filter(Debt.user_id == user.id, Debt.debt_type=="OWED_BY").all()
    s = 0
    for debt in debts:
        if debt.debt_valyuta == "UZS":
            s += debt.amount
        elif debt.debt_valyuta == "USD":
            usd_amount = debt.amount * 12070
            s += usd_amount
        elif debt.debt_valyuta == "EUR":
            eur_amount = debt.amount * 13700
            s += eur_amount
        elif debt.debt_valyuta == "RUB":
            rub_amount = debt.amount * 155
            s += rub_amount
        else:
            s += 0

        response = {
            "success": True,
            "debts": debts,
            "Total amount": s
        }

    return response

@debt_router.get("/indivudal")
async def indivudal(Authorize: AuthJWT = Depends()):

    try:
        auth = Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Not authenticated")


    contacts = session.query(Debt.first_name).distinct().all()

    rates = {
        "UZS": 1,
        "USD": 12070,
        "EUR": 13700,
        "RUB": 155
    }

    response = {}

    for contact in contacts:
        name = contact[0]

        debts = session.query(Debt).filter(
            Debt.first_name == name
        ).all()

        debt_to = 0
        debt_by = 0

        for debt in debts:

            amount_uzs = debt.amount * rates.get(
                debt.debt_valyuta,
                1
            )

            if debt.debt_type == "OWED_TO":
                debt_to += amount_uzs

            elif debt.debt_type == "OWED_BY":
                debt_by += amount_uzs

        total = debt_to - debt_by

        response[name] = {
            "debt_to": debt_to,
            "debt_by": -debt_by,
            "total": total
        }

    return {
        "success": True,
        "data": response
    }

