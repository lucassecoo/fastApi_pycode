from typing import Optional

from fastapi import APIRouter, Depends
from fastapi import APIRouter, Depends, HTTPException, Query, status

from car_api.schemas.cars import (CarPublicSchema, CarListPublicSchema, CarSchema, CarUpdateSchema)
from car_api.core.database import get_session
from car_api.models.cars import Car
from car_api.models.cars import Car
from sqlalchemy import func, select, exists
from sqlalchemy.orm import selectinload

router = APIRouter()

from fastapi import Depends, HTTPException, status
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=CarSchema,
    summary="Criar um novo veiculo",
)
async def create_car(car: CarSchema, db: AsyncSession = Depends(get_session)):
    db_car = Car(
        model=car.model,
        factory_year=car.factory_year,
        model_year = car.model_year,
        color = car.color,
        plate = car.plate,
        fuel_type = car.fuel_type,
        transmission_type = car.transmission_type,
        price = car.price,
        description = car.description,
        is_available = car.is_available,
        brand_id = car.brand_id,
        owner_id = car.owner_id,
    )
    db.add(db_car)
    await db.commit()
    await db.refresh(db_car)

    result = await db.execute(
        select(Car).options(selectinload(Car.brand), selectinload(Car.owner)).where(Car.id == db_car.id)
    )
    car_with_relations = result.scalar_one()

    return car_with_relations

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=CarListPublicSchema,
    summary="Lista todos os carros",
)
async def list_brands(
    limit: int = Query(100, ge=1, le=100, description="Limite de registros"),
    db: AsyncSession = Depends(get_session),
    search: Optional[str] = Query(None, description="Busca por nome"),
    is_available: Optional[bool] = Query(None, description="Busca por status"),
):
    query = select(Car)

    if search:
        search_filter = f"%{search}%"
        query = query.where(
            (Car.name.ilike(search_filter)))
    
    if is_available is not None:
        search_filter = f"%{is_available}%"
        query = query.where(
            (Car.is_active == is_available))
    
    query = query.limit(limit)
    result = await db.execute(query)
    cars = result.scalars().all()

    return {
        "cars": cars,
        "limit": limit,
    }