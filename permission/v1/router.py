from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from permission.v1.crud import DBPermission
from permission.v1.schema import CUDPermission, PermissionProfile, ReadContentTypePermission, ReadPermissionProfile

from utils.database import get_db
from utils.oauth.security import Security


router = APIRouter(
    dependencies=[
        Depends(get_db),
        Depends(Security.get_token)
    ]
)

get_db = router.dependencies[0]
get_token = router.dependencies[1]
db_permission = DBPermission


@router.get(
    '/content_type',
    response_model=list[ReadContentTypePermission],
    status_code=status.HTTP_200_OK
)
async def content_type(
    db: Session = get_db
):
    '''
    Obtener los tipos por cada perfil.

    ### Return
    - `list[ReadContentTypePermission]` Respuesta con los permisos por perfil.
    '''
    return await db_permission(db).get_content_type_permission()


@router.get(
    '/{profile_id}',
    response_model=list[ReadPermissionProfile],
    status_code=status.HTTP_200_OK
)
async def permission_profile(
    profile_id: str,
    db: Session = get_db
):
    '''
    Obtener los permisos por cada perfil.

    ### Return
    - `list[ReadPermissionProfile]` Respuesta con los permisos por perfil.
    '''
    return await db_permission(db).get_permission_profile(profile_id)


@router.post(
    '/',
    response_model=PermissionProfile,
    status_code=status.HTTP_201_CREATED
)
async def add_permission_profile(
    permission: CUDPermission,
    db: Session = get_db
):
    '''
    Crear un permiso para un perfil

    ### Return
    `ReadPermissionProfile` Respuesta con el permiso creado.
    '''
    return await db_permission(db).add_permission(permission)
