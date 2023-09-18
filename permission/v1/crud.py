from fastapi import status
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, Session

from permission.v1.models import ContentTypeModel, PermissionModel, PermissionProfileModel
from permission.v1.schema import CUDPermission, PermissionProfile, ReadContentTypePermission, ReadPermissionProfile

from utils import TypeMessage
from utils.exception.ensaware import EnsawareException


class DBPermission:
    def __init__(self, session: Session) -> None:
        self.__session = session

    async def add_permission(self, permission: CUDPermission) -> PermissionProfile:
        try:
            add_permission = PermissionProfileModel(
                permission_id=permission.permission_id,
                profile_id=permission.profile_id
            )

            self.__session.add(add_permission)
            await self.__session.commit()
            await self.__session.refresh(add_permission)
        except Exception as ex:
            raise EnsawareException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, str(ex))

    async def get_permission(self, code_name: str, profile_id: str) -> ReadPermissionProfile:
        try:
            select_permission = (
                select(PermissionProfileModel).join(PermissionModel)
                .filter(PermissionModel.code_name == code_name, PermissionProfileModel.profile_id == profile_id)
            )

            result = await self.__session.execute(select_permission)
            return result.scalars().first()
        except Exception as ex:
            raise EnsawareException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, str(ex))

    async def get_permission_profile(self, profile_id: str) -> list[ReadPermissionProfile]:
        try:
            select_permission = (
                select(PermissionProfileModel).options(
                    selectinload(PermissionProfileModel.permission),
                    selectinload(PermissionProfileModel.profile)
                )
                .filter(PermissionProfileModel.profile_id == profile_id)
            )

            result = await self.__session.execute(select_permission)
            return result.scalars().all()
        except Exception as ex:
            raise EnsawareException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, str(ex))

    async def get_content_type_permission(self) -> list[ReadContentTypePermission]:
        try:
            select_content_type_permission = (
                select(ContentTypeModel).options(
                    selectinload(ContentTypeModel.permission))
            )

            result = await self.__session.scalars(select_content_type_permission)
            return result.all()
        except Exception as ex:
            raise EnsawareException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, str(ex))
