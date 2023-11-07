from datetime import datetime, timedelta, timezone

from authlib.jose import jwt
from fastapi import Depends, status
from fastapi.security import HTTPBearer
from typing import Annotated

from authorization.v1.schema import Token, TokenData
from utils import Message, TypeMessage
from utils.exception.ensaware import EnsawareException
from utils.settings import Settings
from user.v1.schema import User

oauth2_token = HTTPBearer(auto_error=False)


class Security:
    def __init__(self) -> None:
        self.__settings: Settings = Settings()
        self.__algorithm = 'HS512'
        self.__utc = datetime.now(timezone.utc)

    def jwt_encode(self, user: User) -> Token:
        header = {
            'alg': self.__algorithm,
            'typ': 'JWT'
        }

        now: datetime = self.__utc.now()
        exp: datetime = now + timedelta(minutes=self.__settings.jwt_expire_minutes)

        payload: dict = {
            'email': user.email,
            'exp': int(exp.timestamp()),
            'iat': int(now.timestamp()),
            'profile': str(user.profile_id),
            'sub': str(user.id)
        }

        try:
            token: str = jwt.encode(
                header, payload, self.__settings.jwt_secret_key).decode(self.__settings.encode)

            return Token(
                token=token,
                refresh_token=user.refresh_token
            )
        except Exception:
            raise EnsawareException(
                status.HTTP_400_BAD_REQUEST, TypeMessage.VALIDATION.value, Message.FAILED_CREATE_JWT.value)

    def jwt_decode(self, token: str) -> TokenData:
        try:
            payload: dict = jwt.decode(token, self.__settings.jwt_secret_key)
            unix = int(self.__utc.now().timestamp())

            if unix > payload['exp']:
                raise EnsawareException(
                    status.HTTP_401_UNAUTHORIZED, TypeMessage.ERROR.value, Message.EXPIRED_TOKEN.value)

            return TokenData(**payload)
        except EnsawareException as enw:
            raise enw
        except Exception:
            raise EnsawareException(
                status.HTTP_403_FORBIDDEN, TypeMessage.VALIDATION.value, Message.INVALID_JWT.value)

    @staticmethod
    def get_token(token: Annotated[str, Depends(oauth2_token)]) -> TokenData:
        if not token:
            raise EnsawareException(
                status.HTTP_403_FORBIDDEN, TypeMessage.VALIDATION.value, Message.INVALID_JWT.value)

        security = Security()
        return security.jwt_decode(token.credentials)
