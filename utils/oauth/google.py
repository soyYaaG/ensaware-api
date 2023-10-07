from fastapi import Request, status
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
import requests as api_requests
from sqlalchemy.orm import Session

from authorization.v1.schema import Token
from profiles import ProfileType
from profiles.v1.crud import DBProfile
from profiles.v1.schema import Profile
from utils import Message, TypeMessage
from utils.exception.ensaware import EnsawareException
from utils.oauth.security import Security
from user.v1.crud import DBUser
from user.v1.schema import User, UserBase

from . import OAuth20


SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email'
]


class GoogleProvider(OAuth20):
    def __init__(self, url_callback: str, db: Session) -> None:
        super().__init__(url_callback)

        self.__base_url = 'https://oauth2.googleapis.com'
        self.__db_user = DBUser(db)
        self.__db_profile = DBProfile(db)
        self.__settings = self.encryption._settings
        self.__security = Security()

    async def __create_user(self, token: dict, credentials) -> User:
        profile: Profile = await self.__db_profile.get_name(ProfileType.STUDENT)

        user_base = UserBase(
            provider_id=token.get('sub', None),
            provider='google',
            display_name=str(token.get('name', None)).title(),
            email=token.get('email', None),
            picture=token.get('picture', None),
            profile_id=profile.id,
            refresh_token=self.encryption.encrypt(credentials._refresh_token),
        )

        return await self.__db_user.add_user(user_base)

    def __get_config(self) -> Flow:
        flow = Flow.from_client_config(
            client_config={
                'web': {
                    'client_id': self.__settings.client_id_google,
                    'client_secret': self.__settings.client_secret_google,
                    'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                    'token_uri': f'{self.__base_url}/token',
                    'redirect_uris': ['urn:ietf:wg:oauth:2.0:oob']
                }
            },
            scopes=SCOPES
        )

        flow.redirect_uri = self.url_callback

        return flow

    async def __get_token(self, token: str) -> tuple[dict, User | None]:
        try:
            new_token = id_token.verify_token(
                id_token=token,
                request=requests.Request(),
                audience=self.__settings.client_id_google,
                clock_skew_in_seconds=10
            )

            email: str = new_token.get('email', None)
            user: User = await self.__db_user.get_user_email(email)

            return new_token, user
        except Exception as ex:
            raise EnsawareException(
                status.HTTP_400_BAD_REQUEST, TypeMessage.ERROR.value, str(ex))

    def authentication(self) -> tuple[str, str]:
        try:
            flow = self.__get_config()

            return flow.authorization_url(
                access_type='offline',
                prompt='consent',
                include_granted_scopes='true',
            )
        except Exception as ex:
            raise EnsawareException(
                status.HTTP_400_BAD_REQUEST, TypeMessage.ERROR.value, str(ex))

    async def get_data(self, request: Request) -> str:
        try:
            flow = self.__get_config()
            flow.fetch_token(
                authorization_response=str(request.url),
            )

            credentials = flow.credentials

            token, get_user = await self.__get_token(credentials.id_token)

            if not get_user:
                get_user = await self.__create_user(token, credentials)

            get_user.refresh_token = self.encryption.encrypt(
                credentials._refresh_token)
            get_user.picture = token.get('picture', None)
            get_user: User = await self.__db_user.update_user_id(get_user.id, get_user)

            token_data: Token = self.__security.jwt_encode(get_user)
            params: str = ''

            for key, value in token_data.model_dump().items():
                params += f'&{key}={value}'

            return f'{self.__settings.callback_url_front}?proyect=ensaware{params}'
        except EnsawareException as enw:
            raise enw
        except Exception as ex:
            raise EnsawareException(
                status.HTTP_400_BAD_REQUEST, TypeMessage.ERROR.value, str(ex))

    async def refresh_token(self, token: str) -> Token:
        refresh_token = ''

        try:
            refresh_token = self.encryption.decrypt(token)
        except _:
            raise EnsawareException(
                status.HTTP_400_BAD_REQUEST, TypeMessage.VALIDATION.value, Message.INVALID_REFRESH_TOKEN.value)

        body = {
            'client_id': self.__settings.client_id_google,
            'client_secret': self.__settings.client_secret_google,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

        response = api_requests.post(
            f'{self.__base_url}/token',
            data=body
        )

        try:
            json_response = response.json()
            _, get_user = await self.__get_token(json_response['id_token'])

            return self.__security.jwt_encode(get_user)
        except EnsawareException as enw:
            raise enw
        except Exception:
            raise EnsawareException(
                status.HTTP_400_BAD_REQUEST, TypeMessage.ERROR.value, Message.REFRESH_TOKEN_FAILED.value)
