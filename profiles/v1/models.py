from sqlalchemy import Boolean, Column, String, TIMESTAMP, text
from sqlalchemy.orm import relationship

from permission.v1.models import PermissionProfileModel

from utils import UTC
from utils.database import Base


class ProfileModel(Base):
    __tablename__ = 'profile'

    id = Column(String(60), primary_key=True,
                index=True, server_default=text('UUID()'))
    name = Column(String(100), index=True, unique=True)
    is_active = Column(Boolean, default=True)
    created = Column(TIMESTAMP, default=UTC)
    modified = Column(TIMESTAMP, default=None)

    permission_profile = relationship(
        'PermissionProfileModel', back_populates='profile')
