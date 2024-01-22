from os import path, remove
from uuid import uuid4
import cv2
import json
from fastapi import status
from io import BytesIO
from PIL import Image
import pyqrcode

from utils import Message, TypeMessage
from utils.encryption import Encryption
from utils.exception.ensaware import EnsawareException
from utils.quick_response_code import CreateQuickResponseCode, ReadQuickResponseCode


class QRCode(CreateQuickResponseCode, ReadQuickResponseCode):
    def __init__(self, value: dict = None) -> None:
        self.__encryption = Encryption()
        self.__value = value

    def create(self) -> bytes:
        try:
            if not self.__value:
                raise EnsawareException(status.HTTP_400_BAD_REQUEST, TypeMessage.VALIDATION.value, Message.QR_VALIDATION_VALUE.value)

            json_object: str = json.dumps(self.__value, default=str, indent=4)
            token: str = self.__encryption.encrypt(json_object)
            qr = pyqrcode.create(token)

            buffered = BytesIO()
            qr.png(file=buffered, scale=10)

            return buffered.getvalue()
        except:
            raise EnsawareException(status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, Message.QR_ERROR_CREATE.value)


    def read(self, image: bytes) -> dict:
        code_detector = cv2.QRCodeDetector()
        filename = f'{str(uuid4())}.png'

        try:
            qr = Image.open(BytesIO(image)).convert('L')
            qr.save(filename)
            data = cv2.imread(filename)

            token, _, _ = code_detector.detectAndDecode(data)
            decrypt: str = self.__encryption.decrypt(token)
            data: dict = json.loads(decrypt)

            return data
        except Exception as ex:
            print(ex)
            raise EnsawareException(status.HTTP_500_INTERNAL_SERVER_ERROR, TypeMessage.ERROR.value, Message.QR_ERROR_READ.value)
        finally:
            if path.exists(filename):
                remove(filename)
