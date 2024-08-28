from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from database import Base


class DBCity(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(65), nullable=False, unique=True)
    additional_info = Column(String(255), nullable=True)

    temperatures = relationship("DBTemperature", back_populates="city")
