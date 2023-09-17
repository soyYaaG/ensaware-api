from fastapi import status
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from profile.v1.models import ProfileModel
from profile.v1.schema import Profile

from utils import TypeMessage
from utils.exception.ensaware import EnsawareException


class DBProfile:
    def __init__(self, session: Session) -> None:
        self.__session = session

    async def get_all(self) -> list[Profile]:
        try:
            select_profile = (
                select(ProfileModel)
                .filter(ProfileModel.is_active)
                .order_by(ProfileModel.name)
            )

            result = await self.__session.execute(select_profile)
            return result.scalars().all()
        except Exception as ex:
            raise EnsawareException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, str(ex))
