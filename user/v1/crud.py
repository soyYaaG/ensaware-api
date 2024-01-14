from fastapi import status
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, Session

from user.v1.models import UserModel
from user.v1.schema import UserBase, User, UserRead, UserUpdate

from utils import Message, TypeMessage
from utils.exception.ensaware import EnsawareException
from utils.settings import DefaultValuesModels


class DBUser:
    def __init__(self, session: Session) -> None:
        self.__session = session


    def __select(self, return_user_read_model: bool):
        if return_user_read_model:
            return select(UserModel).options(
                selectinload(UserModel.profile),
                selectinload(UserModel.career)
            )
        else:
            return select(UserModel)


    def __validate(self, user):
        if not user:
            raise EnsawareException(
                status.HTTP_404_NOT_FOUND, TypeMessage.VALIDATION.value, Message.NO_INFORMATION.value)

        return user


    async def add_user(self, user: UserBase, return_user_read_model: bool = False) -> UserRead | User:
        try:
            add_user = UserModel(**user.model_dump())
            add_user.id = DefaultValuesModels.uuid4()

            self.__session.add(add_user)
            await self.__session.commit()
            await self.__session.refresh(add_user)

            if return_user_read_model:
                return UserRead.model_validate(add_user)
            else:
                return User.model_validate(add_user)
        except:
            raise EnsawareException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, Message.ERROR_ADD_USER.value)


    async def delete_id(self, id: str) -> None:
        try:
            select_user = (
                select(UserModel)
                .filter(UserModel.id == id, UserModel.is_active)
            )

            result = await self.__session.execute(select_user)
            select_user = result.scalar()

            if not select_user:
                raise EnsawareException(
                    status.HTTP_404_NOT_FOUND, TypeMessage.ERROR.value, Message.ERROR_GET_USER.value)

            await self.__session.delete(select_user)
            await self.__session.commit()
        except EnsawareException as enw:
            raise enw
        except:
            raise EnsawareException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, Message.ERROR_GET_USER.value)


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
        except:
            raise EnsawareException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, Message.ERROR_GET_USER.value)


    async def get_user_email(self, email: str, return_user_read_model: bool = False) -> UserRead | User | None:
        try:
            select_user = self.__select(return_user_read_model).filter(
                UserModel.email == email, UserModel.is_active)

            execute = await self.__session.execute(select_user)
            result = execute.scalars().first()
            self.__validate(result)

            if return_user_read_model:
                return UserRead.model_validate(result)
            else:
                return User.model_validate(result)
        except EnsawareException as enw:
            raise enw
        except:
            raise EnsawareException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, Message.ERROR_GET_USER.value)


    async def get_all(self, return_user_read_model: bool = False):
        try:
            select_user = self.__select(return_user_read_model).filter(UserModel.is_active).order_by(UserModel.created.desc())

            return select_user
        except:
            raise EnsawareException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, Message.ERROR_GET_USER.value)


    async def update_user_id(self, id: str, update_user: User, return_user_read_model: bool = False) -> UserRead | User:
        try:
            select_user = await self.get_user_id(id)
            self.__validate(select_user)

            update_user.modified = DefaultValuesModels.utc()

            query_update = update(UserModel).execution_options(synchronize_session=False).filter(
                UserModel.id == id, UserModel.is_active).values(update_user.model_dump())

            await self.__session.execute(query_update)
            await self.__session.commit()

            return await self.get_user_id(id, return_user_read_model)
        except EnsawareException as enw:
            raise enw
        except:
            raise EnsawareException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, Message.ERROR_UPDATE_USER.value)


    async def update_career_id(self, id: str, update_user: UserUpdate, return_user_read_model: bool = False) -> UserRead | User:
        try:
            select_user = await self.get_user_id(id)
            self.__validate(select_user)

            select_user.modified = DefaultValuesModels.utc()
            if update_user.career_id:
                select_user.career_id = update_user.career_id

            if update_user.profile_id:
                select_user.profile_id = update_user.profile_id

            query_update = update(UserModel).execution_options(synchronize_session=False).filter(
                UserModel.id == id, UserModel.is_active).values(select_user.model_dump())

            await self.__session.execute(query_update)
            await self.__session.commit()

            return await self.get_user_id(id, return_user_read_model)
        except EnsawareException as enw:
            raise enw
        except:
            raise EnsawareException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, Message.ERROR_UPDATE_USER_CAREER.value)
