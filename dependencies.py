from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city.crud import get_one_city
from city.schemas import City
from database import SessionLocal


async def get_db() -> AsyncSession:
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()


async def get_city_by_id(city_id: int, db: AsyncSession = Depends(get_db)) -> City:
    db_city = await get_one_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return City.model_validate(db_city)
