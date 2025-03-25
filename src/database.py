from src import Config
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    db = DBSession()
    try:
        yield db
    finally:
        await db.close()


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseDBModel.metadata.create_all)


database_name = Config.database_name
database_path = f"sqlite+aiosqlite:///{database_name}"

engine = create_async_engine(database_path, echo=False)
BaseDBModel = declarative_base()

DBSession = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
