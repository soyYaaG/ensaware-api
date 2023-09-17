from datetime import datetime, timezone
from enum import Enum, unique
from uuid import uuid4
from urllib.parse import ParseResult, urlparse


UTC: datetime = datetime.now(timezone.utc)
UUID_4: uuid4 = uuid4


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
    NO_INFORMATION = 'Información no encontrada.'


@unique
class TypeMessage(Enum):
    ERROR = 'error'
    INFORMATION = 'information'
    WARNING = 'warning'
    VALIDATION = 'validation'