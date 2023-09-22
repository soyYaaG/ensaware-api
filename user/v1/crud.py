from fastapi import status
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, Session

from user.v1.models import UserModel
from user.v1.schema import UserBase, User, UserRead

from utils import Message, TypeMessage, UTC
from utils.exception.ensaware import EnsawareException


class DBUser:
    def __init__(self, session: Session) -> None:
        self.__session = session

    def __select(self, return_user_read_model):
        if return_user_read_model:
            return select(UserModel).options(
                selectinload(UserModel.profile),
                selectinload(UserModel.career)
            )
        else:
            return select(UserModel)

    async def add_user(self, user: UserBase, return_user_read_model: bool = False) -> UserRead | User:
        try:
            add_user = UserModel(**user.model_dump())

            self.__session.add(add_user)
            await self.__session.commit()
            await self.__session.refresh(add_user)

            if return_user_read_model:
                return UserRead.model_validate(add_user)
            else:
                return User.model_validate(add_user)
        except Exception as ex:
            raise EnsawareException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, str(ex))

    async def get_user_id(self, id: str, return_user_read_model: bool = False) -> UserRead | User | None:
        try:
            select_user = self.__select(return_user_read_model).filter(
                UserModel.id == id, UserModel.is_active)

            execute = await self.__session.execute(select_user)
            result = execute.scalars().first()

            if not result:
                return None

            if return_user_read_model:
                return UserRead.model_validate(result)
            else:
                return User.model_validate(result)
        except Exception as ex:
            raise EnsawareException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, str(ex))

    async def get_user_email(self, email: str, return_user_read_model: bool = False) -> UserRead | User | None:
        try:
            select_user = self.__select(return_user_read_model).filter(
                UserModel.email == email, UserModel.is_active)

            execute = await self.__session.execute(select_user)
            result = execute.scalars().first()

            if not result:
                return None

            if return_user_read_model:
                return UserRead.model_validate(result)
            else:
                return User.model_validate(result)
        except Exception as ex:
            raise EnsawareException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, str(ex))

    async def update_user_id(self, id: str, update_user: User, return_user_read_model: bool = False) -> UserRead | User:
        try:
            select_user = await self.get_user_id(id)

            if not (select_user):
                raise EnsawareException(
                    status.HTTP_404_NOT_FOUND, TypeMessage.VALIDATION.value, Message.NO_INFORMATION.value)

            update_user.modified = UTC

            query_update = update(UserModel).execution_options(synchronize_session=False).filter(
                UserModel.id == id, UserModel.is_active).values(update_user.model_dump())

            await self.__session.execute(query_update)
            await self.__session.commit()

            return await self.get_user_id(id, return_user_read_model)
        except Exception as ex:
            raise EnsawareException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, str(ex))
