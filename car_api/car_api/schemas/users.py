from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from typing import Optional, List

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("username")
    def validar_username(cls, value):
        if len(value) <= 3:
            raise ValueError("O nome de usuário deve ter pelo menos 4 caracteres")
        return value

    @field_validator("password")
    def validar_password(cls, value):
        if len(value) <= 6:
            raise ValueError("A senha deve ter pelo menos 7 caracteres")
        return value
    
    @field_validator("email")
    def validar_email(cls, value):
        if "@" not in value:
            raise ValueError("O email deve conter um '@'")
        return value

class UserPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    update_at: datetime

class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserListPublicSchema(BaseModel):
    users: List[UserPublicSchema]
    offset: int
    limit: int