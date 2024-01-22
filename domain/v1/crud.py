from fastapi import status
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, Session
from domain import validate_domain

from domain.v1.models import DomainModel
from domain.v1.schema import Domain, DomainBase
from utils import Message, TypeMessage
from utils.exception.ensaware import EnsawareException
from utils.settings import DefaultValuesModels


class DBDomain:
    def __init__(self, session: Session) -> None:
        self.__session = session


    async def add_domain(self, value: DomainBase) -> Domain:
        try:
            domain = DomainModel(**value.model_dump())

            if not validate_domain(domain.value):
                raise EnsawareException(status.HTTP_400_BAD_REQUEST, TypeMessage.VALIDATION.value, Message.DOMAIN_VALIDATION_VALUE.value)

            domain.id = DefaultValuesModels.uuid4()

            self.__session.add(domain)
            await self.__session.commit()
            await self.__session.refresh(domain)

            return Domain.model_validate(domain)
        except EnsawareException as enw:
            raise enw
        except:
            raise EnsawareException(status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, Message.DOMAIN_ERROR_CREATE.value)


    async def delete_id(self, id: str) -> None:
        try:
            select_domain = (
                select(DomainModel)
                .filter(DomainModel.id == id)
            )

            result = await self.__session.execute(select_domain)
            select_domain = result.scalar()

            if not select_domain:
                raise EnsawareException(status.HTTP_404_NOT_FOUND, TypeMessage.ERROR.value, Message.DOMAIN_ERROR_GET.value)

            await self.__session.delete(select_domain)
            await self.__session.commit()
        except EnsawareException as enw:
            raise enw
        except:
            raise EnsawareException(status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, Message.DOMAIN_ERROR_GET.value)


    async def get_all(self):
        try:
            select_domain = select(DomainModel).order_by(DomainModel.created.desc())

            result = await self.__session.execute(select_domain)
            return result.scalars().all()
        except:
            raise EnsawareException(status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, Message.DOMAIN_ERROR_GET.value)


    async def get_domain(self, domain: str) -> Domain:
        try:
            select_domain = (
                select(DomainModel)
                .filter(DomainModel.value == domain)
            )

            execute = await self.__session.execute(select_domain)
            result = execute.scalars().first()

            if not result:
                raise EnsawareException(status.HTTP_404_NOT_FOUND, TypeMessage.ERROR.value, Message.DOMAIN_ERROR_GET.value)

            return Domain.model_validate(result)
        except EnsawareException as enw:
            raise enw
        except:
            raise EnsawareException(status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, Message.DOMAIN_ERROR_GET.value)
