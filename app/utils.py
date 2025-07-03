from datetime import timedelta, datetime, timezone, date

from zoneinfo import ZoneInfo
import jwt
from passlib.context import CryptContext

from app.config import ALGORITHM, SECRET

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(subject: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = subject.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def obtener_fecha_actual() -> date:
    zona = ZoneInfo("America/Guatemala")
    return datetime.now(zona).date()
