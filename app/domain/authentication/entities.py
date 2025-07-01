from uuid import UUID

from pydantic import BaseModel, Field, EmailStr, ConfigDict


class User(BaseModel):
    id: int = Field(gt=0)
    user_code: UUID
    email: EmailStr = Field(max_length=100)
    username: str = Field(max_length=25)
    password: str = Field()
    session_version: int = Field(gt=0)

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPlayload(BaseModel):
    sub: str
    sv: int


class RefreshTokenPayload(BaseModel):
    sub: str
