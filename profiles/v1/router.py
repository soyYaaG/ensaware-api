from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from profiles.v1.crud import DBProfile
from profiles.v1.schema import Profile

from utils.database import get_db


router = APIRouter(
    dependencies=[
        Depends(get_db)
    ]
)

get_db = router.dependencies[0]
db_profile = DBProfile


@router.get(
    '/',
    response_model=list[Profile],
    status_code=status.HTTP_200_OK
)
async def all(
    db: Session = get_db
):
    '''
    Obtener todos los perfiles de la aplicación.

    ### Return
    - `list[Profile]` Respuesta con los perfiles.
    '''
    return await db_profile(db).get_all()
