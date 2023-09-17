from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from profile.v1.crud import DBProfile
from profile.v1.schema import Profile

from utils import Message, TypeMessage
from utils.database import get_db
from utils.exception.ensaware import EnsawareException


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
    try:
        return await db_profile(db).get_all()
    except Exception as ex:
        raise EnsawareException(
            status.HTTP_400_BAD_REQUEST,
            TypeMessage.ERROR.value,
            str(ex)
        )