from uuid import UUID

from pydantic import BaseModel, Field, EmailStr, ConfigDict


class BaseUser(BaseModel):
    email: EmailStr = Field(max_length=100)
    username: str = Field(max_length=25)


class User(BaseUser):
    id: int = Field(gt=0)
    user_code: UUID
    password: str = Field()
    session_version: int = Field(gt=0)

    model_config = ConfigDict(from_attributes=True)


# Input user
class UserIn(BaseUser):
    username: str = Field(max_length=25, pattern=r"^[a-zA-z0-9]*$")
    password: str = Field(max_length=50)


class UserInDB(UserIn):
    password: str
    session_version: int = Field(default=1)


class UpdatedUser(BaseUser):
    user_code: UUID
    password: str = Field(max_length=50)


class UpdatedUserDB(BaseUser):
    user_code: UUID
    password: str
    session_version: int = Field(gt=0)


# Output user
class PublicMinUser(BaseUser):
    pass


class PublicUser(BaseUser):
    user_code: UUID
