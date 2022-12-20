from sqlalchemy import select, delete

__all__ = (
    'BaseDBService',
)


class BaseDBService:
    def __init__(self, session, model):
        self.session = session
        self.model = model

    async def get_by_id(self, idx):
        result = await self.session.execute(
            select(self.model)
            .where(self.model.id == idx)
        )
        result = result.one_or_none()

        if result:
            return result[0]

        return

    async def get_all(self):
        result = await self.session.execute(
            select(self.model)
            .order_by(
                self.model.id
            )
        )
        return result.scalars().all()

    async def add(self, model_instance):
        self.session.add(model_instance)

    async def remove(self, idx):

        result = await self.session.execute(
            select(self.model)
            .where(self.model.id == idx)
        )
        if result:
            await self.session.execute(
                delete(self.model)
                .where(self.model.id == idx)
            )

            return result.one_or_none()
