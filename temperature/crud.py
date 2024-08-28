from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from temperature.models import DBTemperature
from temperature.schemas import Temperature, TemperatureCreate


async def get_all_temperatures(db: AsyncSession):
    query = select(DBTemperature).options(selectinload(DBTemperature.city))
    result = await db.execute(query)
    temperatures = result.scalars().all()
    return temperatures


async def get_temperatures_for_city(
        db: AsyncSession,
        city_id: int
) -> list[Temperature]:
    query = (select(DBTemperature).
             options(selectinload(DBTemperature.city)).
             filter(DBTemperature.city_id == city_id))
    result = await db.execute(query)
    db_temperatures = result.scalars().all()
    temperatures = [Temperature.model_validate(db_temp)
                    for db_temp in db_temperatures]
    return temperatures


async def create_temperature(db: AsyncSession, temperature: TemperatureCreate):
    db_temp = DBTemperature(**temperature.model_dump())
    db.add(db_temp)
    await db.commit()
    await db.refresh(db_temp)
    return db_temp
