import logging
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from utils.database import get_db

from career.v1.crud import DBCareer
from career.v1.schema import Career


router = APIRouter(
    dependencies=[
        Depends(get_db)
    ]
)

get_db = router.dependencies[0]
db_career = DBCareer


@router.get(
    '/all',
    response_model=list[Career],
    status_code=status.HTTP_200_OK,
)
async def all_career(
    db: Session = get_db
):
    '''
    Obtener la información de todas las carreras de la CUA.

    ### Return
    - `list[Career]` Respuesta con las carreras de la CUA.
    '''
    return await db_career(db).get_all()
