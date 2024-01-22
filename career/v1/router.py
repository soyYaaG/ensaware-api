from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from authorization.v1.schema import TokenData

from utils.database import get_db
from utils.oauth.security import Security

from career.v1.crud import DBCareer
from career.v1.schema import Career, CareerBase


router = APIRouter(
    dependencies=[
        Depends(get_db),
        Depends(Security.get_token)
    ]
)

get_db = router.dependencies[0]
get_token = router.dependencies[1]
db_career = DBCareer


@router.delete(
    '/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_career(
    id: str,
    token: TokenData = get_token,
    db: Session = get_db
):
    '''
    Eliminar la carrera del usuario que inicio sesión.
    '''
    return await db_career(db).delete_id(id)


@router.get(
    '/all',
    response_model=list[Career],
    status_code=status.HTTP_200_OK,
)
async def all_career(
    token: TokenData = get_token,
    db: Session = get_db
):
    '''
    Obtener la información de todas las carreras de la CUA.

    ### Return
    - `list[Career]` Respuesta con las carreras de la CUA.
    '''
    return await db_career(db).get_all()


@router.post(
    '',
    response_model=Career,
    status_code=status.HTTP_201_CREATED,
)
async def create_career(
    career: CareerBase,
    token: TokenData = get_token,
    db: Session = get_db
):
    '''
    Crear una carrera de la CUA.

    ### Return
    - `Career` Respuesta con la carrera creada.
    '''
    return await db_career(db).add(career)
