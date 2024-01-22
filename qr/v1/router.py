
from fastapi import APIRouter, Depends, Response, UploadFile, status
from sqlalchemy.orm import Session

from authorization.v1.schema import TokenData
from user.v1.crud import DBUser
from utils.database import get_db
from utils.oauth.security import Security
from utils.quick_response_code.qr import QRCode


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
    '/user',
    status_code=status.HTTP_200_OK
)
async def get_qr_user(
    token: TokenData = get_token,
    db: Session = get_db
):
    '''
    Obtener el código QR del usuario que inicio sesión.
    '''
    user = await db_user(db).get_user_id(token.sub, True)
    result = QRCode(user.model_dump())
    img = result.create()

    return Response(content=img, media_type='image/png')


@router.get(
    '/user/{id}',
    status_code=status.HTTP_200_OK
)
async def get_qr_user_id(
    id: str,
    token: TokenData = get_token,
    db: Session = get_db
):
    '''
    Obtener el código QR del usuario.
    '''
    user = await db_user(db).get_user_id(id, True)
    result = QRCode(user.model_dump())
    img = result.create()

    return Response(content=img, media_type='image/png')


@router.post(
    '/read/image',
    status_code=status.HTTP_200_OK
)
async def read_imagen(
    image: UploadFile,
    token: TokenData = get_token,
    db: Session = get_db
):
    contents = await image.read()
    result = QRCode()

    return result.read(contents)
