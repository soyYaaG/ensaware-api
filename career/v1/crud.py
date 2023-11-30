from fastapi import status
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from utils import Message, TypeMessage
from utils.exception.ensaware import EnsawareException

from career.v1.models import CareerModel
from career.v1.schema import Career, CareerBase
from utils.settings import DefaultValuesModels


class DBCareer:
    def __init__(self, session: Session) -> None:
        self.__session = session

    async def add(self, career: CareerBase) -> Career:
        try:
            add_career = CareerModel(**career.model_dump())
            add_career.id = DefaultValuesModels.uuid4()

            self.__session.add(add_career)
            await self.__session.commit()
            await self.__session.refresh(add_career)

            return Career.model_validate(add_career)
        except:
            raise EnsawareException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, Message.ERROR_ADD_CAREER.value)


    async def delete_id(self, id: str) -> None:
        try:
            select_career = (
                select(CareerModel)
                .filter(CareerModel.id == id, CareerModel.is_active)
            )

            result = await self.__session.execute(select_career)
            select_career = result.scalar()
            select_career = Career.model_validate(select_career)

            if not select_career:
                raise EnsawareException(
                    status.HTTP_404_NOT_FOUND, TypeMessage.ERROR.value, Message.ERROR_NOT_FOUND_CAREER.value)

            select_career.is_active = False
            select_career.modified = DefaultValuesModels.utc()

            query_update = (
                update(CareerModel)
                .execution_options(synchronize_session=False)
                .filter(CareerModel.id == id, CareerModel.is_active)
                .values(select_career.model_dump())
            )

            await self.__session.execute(query_update)
            await self.__session.commit()
        except EnsawareException as enw:
            raise enw
        except:
            raise EnsawareException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, Message.ERROR_NOT_FOUND_CAREER.value)


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
