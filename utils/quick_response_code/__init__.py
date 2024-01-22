from abc import ABC, abstractmethod
from enum import Enum, unique

from utils.settings import DefaultValuesModels


class CreateQuickResponseCode(ABC):
    @abstractmethod
    def create(self) -> bytes:
        pass


class ReadQuickResponseCode(ABC):
    @abstractmethod
    def read(self, image: bytes) -> any:
        pass


@unique
class QRType(Enum):
    ELEMENT_ROOM = 'element_room'
    ROOM = 'room'
    USER = 'user'


def set_qr_type(qr_type: QRType, id: str):
    return {
        'qr_type': qr_type.value,
        'id': id,
        'created': DefaultValuesModels.utc()
    }
