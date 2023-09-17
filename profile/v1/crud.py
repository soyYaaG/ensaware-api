from sqlalchemy.orm import Session
from sqlalchemy.future import select

from profile.v1.models import ProfileModel
from profile.v1.schema import Profile


class DBProfile:
    def __init__(self, session: Session) -> None:
        self.__session = session


    async def get_all(self) -> list[Profile]:
        select_profile = (
            select(ProfileModel)
            .filter(ProfileModel.is_active)
            .order_by(ProfileModel.created)
        )

        result = await self.__session.execute(select_profile)
        return result.scalars().all()