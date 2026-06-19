import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base


load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")
print(DB_USER)
print(DB_PASSWORD)
print(DB_HOST)
print(DB_PORT)
print(DB_NAME)
DATABASES_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASES_URL, echo=True)

Base = declarative_base()

session = sessionmaker(bind=engine, autocommit=False, autoflush=False)