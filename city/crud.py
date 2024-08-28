from fastapi import HTTPException
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import DBCity
from city.schemas import City, CityCreate, CityUpdate


async def get_all_cities(db: AsyncSession) -> list[City] | None:
    query = select(DBCity).order_by(DBCity.name)
    result: Result = await db.execute(query)
    cities = result.scalars().all()
    return cities if cities else []


async def get_one_city(db: AsyncSession, city_id: int) -> City | None:
    return await db.get(DBCity, city_id)


async def upgrade_city(
        db: AsyncSession,
        city: City,
        city_to_update: CityUpdate
) -> City:
    for name, value in city_to_update.model_dump().items():
        if hasattr(city, name):
            setattr(city, name, value)
    await db.commit()
    await db.refresh(city)
    return city


async def create_city(db: AsyncSession, city: CityCreate):
    existing_city_query = select(DBCity).filter_by(name=city.name)
    res = await db.execute(existing_city_query)
    existing_city = res.scalars().first()

    if existing_city:
        raise HTTPException(
            status_code=400,
            detail="City with this name already exists."
        )

    city = DBCity(**city.model_dump())
    db.add(city)
    await db.commit()
    await db.refresh(city)
    return city


async def delete_city_from_db(db: AsyncSession, city: City):
    await db.delete(city)
    await db.commit()
