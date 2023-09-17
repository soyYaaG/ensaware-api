from fastapi import status
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from permission.v1.models import PermissionModel, PermissionProfileModel
from permission.v1.schema import ReadPermissionProfile

from utils import TypeMessage
from utils.exception.ensaware import EnsawareException


class DBPermission:
    def __init__(self, session: Session) -> None:
        self.__session = session

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
                select(PermissionProfileModel)
                .filter(PermissionProfileModel.profile_id == profile_id)
            )

            result = await self.__session.execute(select_permission)
            return result.scalars().all()
        except Exception as ex:
            raise EnsawareException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, str(ex))
