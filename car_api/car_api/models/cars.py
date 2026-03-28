from typing import Optional, List, TYPE_CHECKING
from decimal import Decimal
from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from car_api.models.base import Base
from datetime import datetime
from sqlalchemy import func, String, Text, Integer, Numeric, ForeignKey

if TYPE_CHECKING:
    from car_api.models.users import User

class TransmissionType(str,Enum):
    MANUAL = 'manual'
    AUTOMATICO = 'automatico'
    SEMI_AUTOMATICO = 'semi_automatic'
    CVT = 'cvt'

class FuelType(str, Enum):
    GASOLINA = 'gasolina'
    DIESEL = 'diesel'
    ETHANOL = 'ethanol'
    FLEX = 'flex'
    ELETRIC = 'eletric'
    HYBRID = 'hybrid'

class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, default=None)
    is_active: Mapped[bool] = mapped_column(default=True)
    update_at: Mapped[datetime] = mapped_column(onupdate=func.now(), server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    cars: Mapped[List['Car']] = relationship("Car", back_populates="brand")

class Car(Base):
    __tablename__ = "cars"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str] = mapped_column(String(100))
    factory_year: Mapped[int] = mapped_column(Integer)
    model_year: Mapped[int] = mapped_column(Integer)
    color: Mapped[str] = mapped_column(String(30))
    plate: Mapped[str] = mapped_column( String(10), unique=True, index=True)
    fuel_type: Mapped[FuelType] = mapped_column(String(20))
    transmission_type: Mapped[TransmissionType] = mapped_column(String(20))
    price: Mapped[Decimal] = mapped_column(Numeric(10,2))
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_available: Mapped[bool] = mapped_column(default=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    update_at: Mapped[datetime] = mapped_column(onupdate=func.now(), server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    brand: Mapped['Car'] = relationship("Brand", back_populates="cars")
    owner: Mapped['User'] = relationship("User", back_populates="cars")