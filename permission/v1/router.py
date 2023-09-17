from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from permission.v1.crud import DBPermission
from permission.v1.schema import ReadPermissionProfile

from utils.database import get_db


router = APIRouter(
    dependencies=[
        Depends(get_db)
    ]
)

get_db = router.dependencies[0]
db_permission = DBPermission


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
