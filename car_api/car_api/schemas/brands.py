from typing import Optional
from datetime import datetime

from pydentic import BaseModel, field_validator

class BrandSchema(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    update_at: datetime
    created_at: datetime

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
    brands: List[BrandPublicSchema]
    offset: int
    limit: int    