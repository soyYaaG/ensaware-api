from fastapi import status
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from utils import TypeMessage
from utils.exception.ensaware import EnsawareException

from career.v1.models import CareerModel
from career.v1.schema import Career


class DBCareer:
    def __init__(self, session: Session) -> None:
        self.__session = session

    async def get_all(self) -> list[Career]:
        try:
            select_profile = (
                select(CareerModel)
                .filter(CareerModel.is_active)
                .order_by(CareerModel.name)
            )

            result = await self.__session.execute(select_profile)
            return result.scalars().all()
        except Exception as ex:
            raise EnsawareException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, str(ex))
