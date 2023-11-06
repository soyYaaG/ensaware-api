from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from utils.database import get_db
from utils.oauth.security import Security

from authorization.v1.schema import TokenData
from user.v1.crud import DBUser
from user.v1.schema import UserRead


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
    db: Session = get_db
):
    '''
    Obtener la información de usuario en especifico.

    ### Return
    - `UserRead` Respuesta con la información del usuario
    '''
    return await db_user(db).get_user_id(id, True)
