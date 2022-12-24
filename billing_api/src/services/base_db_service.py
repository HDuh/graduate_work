from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

__all__ = (
    'BaseDBService',
)


class BaseDBService:
    def __init__(self, session: AsyncSession, model):
        self.session = session
        self.model = model

    async def get_by_id(self, **kwargs):
        result = await self.session.execute(
            select(self.model)
            .filter_by(**kwargs)
        )
        return result.scalar()

    async def get_all(self, **kwargs):
        result = await self.session.execute(
            select(self.model)
            .filter_by(**kwargs)
            .order_by(self.model.id)
        )
        return result.scalars().all()

    async def save(self, model_instance):
        self.session.add(model_instance)
        await self.session.commit()

    async def check_and_delete(self, **kwargs):
        if result := await self.get_by_id(**kwargs):
            await self.session.delete(result)
            await self.session.commit()
