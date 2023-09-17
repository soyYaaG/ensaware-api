from sqlalchemy.orm import Session

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
        self.__db = db
        self.__settings = self.encryption._settings
        self.__security = Security()