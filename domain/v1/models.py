from sqlalchemy import TIMESTAMP, Column, String

from utils.database import Base
from utils.settings import DefaultValuesModels


class DomainModel(Base, DefaultValuesModels):
    __tablename__ = 'domain'

    id = Column(String(60), primary_key=True, index=True, default=DefaultValuesModels.uuid4())
    value = Column(String(100), nullable=False, unique=True)
    created = Column(TIMESTAMP, default=DefaultValuesModels.utc())
    modified = Column(TIMESTAMP, default=None)
