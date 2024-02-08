import os

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

POSTGRES_DB = os.getenv("POSTGRES_DB", "async")
POSTGRES_USER = os.getenv("POSTGRES_USER", "script_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password121")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5431)

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class SwapiPeople(Base):

    __tablename__ = "swapi_people"

    id: Mapped[int] = mapped_column(primary_key=True)
    birth_year: Mapped[str] = mapped_column(nullable=True)
    eye_color: Mapped[str] = mapped_column(nullable=True)
    films: Mapped[ARRAY] = mapped_column(ARRAY(String), nullable=True)
    gender: Mapped[str] = mapped_column(nullable=True)
    hair_color: Mapped[str] = mapped_column(nullable=True)
    height: Mapped[str] = mapped_column(nullable=True)
    homeworld: Mapped[str] = mapped_column(nullable=True)
    mass: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(nullable=True)
    skin_color: Mapped[str] = mapped_column(nullable=True)
    species: Mapped[ARRAY] = mapped_column(ARRAY(String), nullable=True)
    starships: Mapped[ARRAY] = mapped_column(ARRAY(String), nullable=True)
    vehicles: Mapped[ARRAY] = mapped_column(ARRAY(String), nullable=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
