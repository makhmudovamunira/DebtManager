from fastapi import FastAPI
from another_fastapi_jwt_auth import AuthJWT
from schemas import Settings
from database import Base, engine
from auth_routes import auth_router
from debt_routers import debt_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(auth_router)
app.include_router(debt_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Debt Calculator"}