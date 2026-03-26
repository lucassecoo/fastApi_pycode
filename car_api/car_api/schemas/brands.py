from typing import Optional
from datetime import datetime

from pydantic import BaseModel, field_validator, ConfigDict

class BrandSchema(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True

    @field_validator("name")
    def validar_name(cls, value):
        if len(value) <= 2:
            raise ValueError("O nome da marca deve ter pelo menos 3 caracteres")
        return value

class BrandUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = True
    update_at: datetime
    created_at: datetime

    @field_validator("name")
    def validar_name(cls, value):
        if len(value) <= 2:
            raise ValueError("O nome da marca deve ter pelo menos 3 caracteres")
        return value
    
class BrandPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    description: Optional[str] = None
    is_active: Optional[bool] = True
    update_at: datetime
    created_at: datetime

class BrandListPublicSchema(BaseModel):
    brands: list[BrandPublicSchema]
    limit: int    

class BrandUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None