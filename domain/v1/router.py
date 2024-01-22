from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from authorization.v1.schema import TokenData
from domain.v1.crud import DBDomain
from domain.v1.schema import Domain, DomainBase
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
db_domain = DBDomain


@router.get(
    '',
    response_model=list[Domain],
    status_code=status.HTTP_200_OK
)
async def get_all(
    token: TokenData = get_token,
    db: Session = get_db
):
    '''
    Obtener todos los dominios.

    ### Return
    - `list[Domain]` Respuesta con todos los dominios.
    '''
    return await db_domain(db).get_all()


@router.get(
    '/{domain}',
    response_model=Domain,
    status_code=status.HTTP_200_OK
)
async def get_domain(
    domain: str,
    token: TokenData = get_token,
    db: Session = get_db
):
    '''
    Obtener un dominio.

    ### Return
    - `Domain` Respuesta con el dominio.
    '''
    return await db_domain(db).get_domain(domain)


@router.post(
    '',
    response_model=Domain,
    status_code=status.HTTP_201_CREATED
)
async def set_domain(
    domain: DomainBase,
    token: TokenData = get_token,
    db: Session = get_db
):
    '''
    Crear un dominio.

    ### Return
    - `Domain` Respuesta con el dominio creado.
    '''
    return await db_domain(db).add_domain(domain)
