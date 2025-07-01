import os
from dotenv import load_dotenv


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()

DIALECT_DB = os.getenv("DIALECT_DB")
SECRET = os.getenv("SECRET")
PORT = os.getenv("PORT")
POSTGRES_HOST = os.getenv("POSTGRESQL_HOST")
POSTGRES_DATA_BASE = os.getenv("POSTGRESQL_DATA_BASE")
POSTGRES_USER = os.getenv("POSTGRESQL_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRESQL_PORT")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

ALGORITHM = "HS256"
API_V1_STR: str = "/api/v1"

SQLALCHEMY_POSTGRES_URL = f"{DIALECT_DB}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATA_BASE}"
postgres_engine = create_engine(
    SQLALCHEMY_POSTGRES_URL, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=postgres_engine)
Base = declarative_base()
