from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import settings

engine = create_async_engine(settings.postgres_config.database_uri)

Base = declarative_base()


def async_session_generator() -> sessionmaker:
    return sessionmaker(
        engine, class_=AsyncSession
    )


async def get_session() -> AsyncSession:
    """
    Получить сессию БД.
    """
    try:
        async_session = async_session_generator()
        async with async_session() as session:
            yield session
            await session.commit()
    except Exception as error:
        await session.rollback()
        raise error
    finally:
        await session.close()
