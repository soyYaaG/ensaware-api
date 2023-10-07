from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from utils.settings import Settings


settings = Settings()


SQLALCHEMY_DATABASE_URL: str = f'{settings.database_api}://{settings.database_username}:{settings.database_pass}@{settings.database_host}:{settings.database_port}/{settings.database_name}'

ENGINE = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=ENGINE)

Base = declarative_base()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
