from cryptography.fernet import Fernet

from utils.settings import Settings


class Encryption:
    def __init__(self) -> None:
        self._settings: Settings = Settings()
        self._fernet: Fernet = Fernet(self._settings.fernet_pass)


    def encrypt(self, message: str) -> str:
        return self._fernet.encrypt(message.encode(self._settings.encode)).decode(self._settings.encode)


    def decrypt(self, token: str) -> str:
        return self._fernet.decrypt(token).decode(self._settings.encode)
