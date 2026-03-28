
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List

from car_api.models.cars import FuelType, TransmissionType
from car_api.schemas.brands import BrandPublicSchema
from car_api.schemas.users import UserPublicSchema


class CarSchema(BaseModel):
    model: str
    factory_year: int
    model_year: int
    color: str
    plate: str
    fuel_type: FuelType
    transmission_type: TransmissionType
    price: Decimal
    description: str
    is_available: bool
    brand_id: int
    owner_id: int

    @field_validator("model")
    def model_min_length(cls, value):
        if len(value.strip()) <= 2:
            raise ValueError("O modelo deve ter pelo menos 2 caracteres")
        return value.strip()
    
    @field_validator("color")
    def color_min_length(cls, value):
        if len(value.strip()) <= 2:
            raise ValueError("Cor deve ter pelo menos 2 caracteres")
        return value.strip()
    
    @field_validator("plate")
    def plate_min_length(cls, value):
        plate = value.strip().upper()
        if len(plate) < 7 or len(plate) > 10:
            raise ValueError("Placa deve ter pelo menos 7 caracteres")
        return plate

    @field_validator("factory_year", "model_year")
    def year_validation(cls, value):
        if value < 1900 or value > 2028:
            raise ValueError("Ano deve estar entre 1900 e 2028")
        return value

    @field_validator("factory_year", "model_year")
    def price_validation(cls, value):
        if value <= 0:
            raise ValueError("Preco deve ser positivo")
        return value

class CarUpdateSchema(BaseModel):
    model: Optional[str] = None
    factory_year: Optional[int] = None
    model_year: Optional[int] = None
    color: Optional[str] = None
    plate: Optional[str] = None
    fuel_type: Optional[FuelType] = None
    transmission_type: Optional[TransmissionType] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None
    is_available: Optional[bool] = None
    brand_id: Optional[int] = None
    owner_id: Optional[int] = None

    @field_validator("model")
    def model_min_length(cls, value):
        if len(value.strip()) <= 2:
            raise ValueError("O modelo deve ter pelo menos 2 caracteres")
        return value.strip()
    
    @field_validator("color")
    def color_min_length(cls, value):
        if len(value.strip()) <= 2:
            raise ValueError("Cor deve ter pelo menos 2 caracteres")
        return value.strip()
    
    @field_validator("plate")
    def plate_min_length(cls, value):
        plate = value.strip().upper()
        if len(plate) < 7 or len(plate) > 10:
            raise ValueError("Placa deve ter pelo menos 7 caracteres")
        return plate

    @field_validator("factory_year", "model_year")
    def year_validation(cls, value):
        if value < 1900 or value > 2028:
            raise ValueError("Ano deve estar entre 1900 e 2028")
        return value

    @field_validator("factory_year", "model_year")
    def price_validation(cls, value):
        if value <= 0:
            raise ValueError("Preco deve ser positivo")
        return value

class CarPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    model: str
    factory_year: int
    model_year: int
    color: str
    plate: str
    fuel_type: FuelType
    transmission_type: TransmissionType
    price: Decimal
    description: str
    is_available: bool
    brand_id: int
    owner_id: int
    update_at: datetime
    created_at: datetime
    brand: BrandPublicSchema
    user: UserPublicSchema

class CarListPublicSchema(BaseModel):
    cars: List[CarPublicSchema]
    offset: int
    limit: int