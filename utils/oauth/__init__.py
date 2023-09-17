from abc import ABC, abstractmethod

from fastapi import Depends, Request, status
from sqlalchemy.orm import Session

# from permission.v1.crud import get_permission

from authorization.v1.schema import TokenData
from utils.database import get_db
from utils.encryption import Encryption
from utils.exception import TypeMessage, Validate
from utils.exception.ensaware import EnsawareException
from utils.oauth.security import Security


class OAuth20(ABC):
    def __init__(self, url_callback: str) -> None:
        self.url_callback: str = url_callback
        self.encryption: Encryption = Encryption()

    @abstractmethod
    def authentication(self):
        pass


    @abstractmethod
    def get_data(self, request: Request):
        pass


    @abstractmethod
    def refresh_token(self, token: str):
        pass