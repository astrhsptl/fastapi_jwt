from pydantic import BaseModel
from pydantic import Field

class User(BaseModel):
    id: int = Field(...)
    username: str
    email: str | None = None
    is_active: bool | None = True
    is_admin: bool | None = False

    class Config:
        orm_mode = True


class UserCreateSchema(BaseModel):
    username: str
    email: str | None = None
    password: str
    is_active: bool | None = True
    is_admin: bool | None = False

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None