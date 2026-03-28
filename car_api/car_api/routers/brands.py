from typing import Optional

from fastapi import APIRouter, Depends
from fastapi import APIRouter, Depends, HTTPException, Query, status

from car_api.schemas.brands import (BrandListPublicSchema, BrandPublicSchema, BrandSchema, BrandUpdateSchema)
from car_api.core.database import get_session
from car_api.models.cars import Car
from car_api.models.cars import Brand
from sqlalchemy import func, select, exists

router = APIRouter()

from fastapi import Depends, HTTPException, status
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

async def validar_nome_unico(nome: str, db: AsyncSession):
    nome_exists = await db.scalar(select(exists().where(Brand.name == nome)))
    if nome_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Nome já está em uso"
        )
    return True

@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=BrandSchema,
    summary="Criar uma nova marca",
)
async def create_brand(brand: BrandSchema, db: AsyncSession = Depends(get_session)):
    # validacao de username unico
    await validar_nome_unico(brand.name, db)

    db_brand = Brand(
        name=brand.name,
        description = brand.description,
        is_active = brand.is_active,
    )
    db.add(db_brand)
    await db.commit()
    await db.refresh(db_brand)

    return db_brand

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=BrandListPublicSchema,
    summary="Lista todos as marcas",
)
async def list_brands(
    limit: int = Query(100, ge=1, le=100, description="Limite de registros"),
    db: AsyncSession = Depends(get_session),
    search: Optional[str] = Query(None, description="Busca por nome"),
    is_active: Optional[bool] = Query(None, description="Busca por status"),
):
    query = select(Brand)

    if search:
        search_filter = f"%{search}%"
        query = query.where(
            (Brand.name.ilike(search_filter)))
    
    if is_active is not None:
        search_filter = f"%{is_active}%"
        query = query.where(
            (Brand.is_active == is_active))
    
    query = query.limit(limit)
    result = await db.execute(query)
    brands = result.scalars().all()

    return {
        "brands": brands,
        "limit": limit,
    }

@router.get(
    "/brand/{brand_id}",
    status_code=status.HTTP_200_OK,
    response_model=BrandPublicSchema,
    summary="Procura usuário por ID",
)
async def get_user(
    brand_id: int,
    db: AsyncSession = Depends(get_session),
):
    brand = await db.get(Car, brand_id)
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Marca não encontrado"
        )
    return brand

@router.put(
    path="/{brand_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=BrandUpdateSchema,
)
async def update_brand(
    brand_id:int, brand_update:BrandSchema, db: AsyncSession = Depends(get_session)
):
    brand = await db.get(Car, brand_id)

    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Marca não encontrado"
        )

    update_data = brand_update.model_dump(exclude_unset=True)

    if "name" in update_data and update_data["name"] != brand.name:
        await validar_nome_unico(update_data["name"], db)

    for field, value in update_data.items():
        setattr(brand, field, value)

    await db.commit()
    await db.refresh(brand)
    return brand

@router.delete(
    path="/{brand_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    brand_id: int,
    db: AsyncSession = Depends(get_session),
):
    brand = await db.get(Car, brand_id)
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Marca não encontrada"
        )

    cars_count = await db.scalar(select(func.count()).select_from(Car).where(Car.brand_id == brand_id))
    if cars_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Não é possível excluir a marca, existem carros associados a ela"
        )

    await db.delete(brand)
    await db.commit()
    return