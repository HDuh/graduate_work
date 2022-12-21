from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.core import settings
from asyncio import current_task

engine = create_async_engine(settings.db_config.database_uri)

Base = declarative_base()

# def async_session_generator() -> sessionmaker:
#     return sessionmaker(
#         engine,
#         class_=AsyncSession,
#         expire_on_commit=False
#     )
#
#
# async def get_session() -> AsyncSession:
#     """
#     Получить сессию БД.
#     """
#     try:
#         async_session = async_session_generator()
#         async with async_session() as session:
#             yield session
#             await session.commit()
#     except Exception as error:
#         await session.rollback()
#         raise error
#     finally:
#         await session.close()

# async_session = AsyncSession(engine, expire_on_commit=False)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


@asynccontextmanager
async def get_session():
    """
    Получить сессию БД.
    """
    try:
        async with async_session() as session:
            yield session
            await session.commit()
    except Exception as error:
        await session.rollback()
        raise error
    finally:
        await session.close()
