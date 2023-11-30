from fastapi import APIRouter, Depends, status
from fastapi_pagination.links import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from utils.database import get_db
from utils.oauth.security import Security

from authorization.v1.schema import TokenData
from user.v1.crud import DBUser
from user.v1.schema import UserRead, UserUpdate


router = APIRouter(
    dependencies=[
        Depends(get_db),
        Depends(Security.get_token)
    ]
)

get_db = router.dependencies[0]
get_token = router.dependencies[1]
db_user = DBUser


@router.get(
    '',
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    db: Session = get_db,
    token: TokenData = get_token,
):
    '''
    Obtener la información del usuario que inicio sesión.

    ### Return
    - `UserRead` Respuesta con la información del usuario
    '''
    return await db_user(db).get_user_id(token.sub, True)


@router.get(
    '/{id}',
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
async def get_user_id(
    id: str,
    token: TokenData = get_token,
    db: Session = get_db
):
    '''
    Obtener la información de un usuario en especifico.

    ### Return
    - `UserRead` Respuesta con la información del usuario
    '''
    return await db_user(db).get_user_id(id, True)


@router.get(
    '/see/all',
    response_model=Page[UserRead],
    status_code=status.HTTP_200_OK,
)
async def see_all_users(
    token: TokenData = get_token,
    db: Session = get_db
):
    '''
    Obtener la información de un usuario en especifico.

    ### Return
    - `Page[UserRead]` Respuesta con la información del usuario
    '''
    result = await db_user(db).get_all(True)
    return await paginate(db, result)



@router.patch(
    '',
    response_model=UserRead,
    status_code=status.HTTP_200_OK
)
async def update_career(
    update_career: UserUpdate,
    token: TokenData = get_token,
    db: Session = get_db
):
    '''
    Actualizar la carrera del usuario que inicio sesión.

     ### Return
    - `UserRead` Respuesta con la información del usuario
    '''
    return await db_user(db).update_career_id(token.sub, update_career, True)
