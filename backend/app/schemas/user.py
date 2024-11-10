from uuid import UUID

from pydantic import EmailStr
from fastapi_users import schemas


class UserRead(schemas.BaseUser[UUID]):
    email: EmailStr
    is_superuser: bool


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str


class UserUpdate(schemas.BaseUserUpdate):
    password: str
