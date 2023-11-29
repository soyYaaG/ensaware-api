from datetime import datetime
from enum import Enum, unique
from uuid import uuid4
from urllib.parse import ParseResult, urlparse


def replace_url_scheme(url: str):
    _urlparse: "ParseResult" = urlparse(url)
    scheme: str = _urlparse.scheme.lower()
    hostname: str = _urlparse.hostname.lower()

    if hostname == 'localhost':
        return url

    if scheme == 'http':
        return url.replace('http', 'https')

    return url


@unique
class Message(Enum):
    EXPIRED_TOKEN = 'Token expirado.'
    FAILED_CREATE_JWT = 'Error al crear el token.'
    INVALID_AUTH = 'No esta autorizado para realizar esta solicitud.'
    INVALID_JWT = 'Token no valido.'
    NVALID_PROVIDER = 'Proveedor no valido.'
    INVALID_REFRESH_TOKEN = 'refresh token no válido.'
    NO_INFORMATION = 'Información no encontrada.'
    REFRESH_TOKEN_FAILED = 'No se puedo actulizar el token. Asegúrese de enviar el refresh token correcto.'

    ERROR_ADD_CAREER = "Ha ocurrido un error al crear la carrera."
    ERROR_NOT_FOUND_CAREER = "Ha ocurrido un error al obtener la información de la cerrera."

    ERROR_ADD_USER = "Ha ocurrido un error al crear el usuario."
    ERROR_GET_USER = "Ha ocorrido un error al obtener la información del usuario."
    ERROR_UPDATE_USER = "Ha ocorrido un error al actualizar la información del usuario."
    ERROR_UPDATE_USER_CAREER = "Ha ocorrido un error al actualizar la carrera del usuario."


@unique
class TypeMessage(Enum):
    ERROR = 'error'
    INFORMATION = 'information'
    WARNING = 'warning'
    VALIDATION = 'validation'
