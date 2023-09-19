from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from utils.database import get_db

from user.v1.crud import DBUser
from user.v1.schema import UserRead


router = APIRouter(
    dependencies=[
        Depends(get_db)
    ]
)

get_db = router.dependencies[0]
db_user = DBUser


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
    return db_user(db).get_user_id(id)
