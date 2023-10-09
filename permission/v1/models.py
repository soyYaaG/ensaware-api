from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, text
from sqlalchemy.orm import relationship

from utils import UTC, UUID_4
from utils.database import Base


class ContentTypeModel(Base):
    __tablename__ = 'content_type'

    id = Column(String(60), primary_key=True,
                index=True, default=UUID_4)
    model = Column(String(100), index=True, unique=True)
    created = Column(TIMESTAMP, default=UTC)
    modified = Column(TIMESTAMP, default=None)

    permission = relationship('PermissionModel', back_populates='content_type')


class PermissionModel(Base):
    __tablename__ = 'permission'

    id = Column(String(60), primary_key=True,
                index=True, default=UUID_4)
    content_type_id = Column(String(60), ForeignKey(
        'content_type.id'), nullable=False)
    code_name = Column(String(255), index=True, unique=True)
    description = Column(String(1000), nullable=True)
    created = Column(TIMESTAMP, default=UTC)
    modified = Column(TIMESTAMP, default=None)

    content_type = relationship(
        'ContentTypeModel', back_populates='permission')
    permission_profile = relationship(
        'PermissionProfileModel', back_populates='permission')


class PermissionProfileModel(Base):
    __tablename__ = 'permission_profile'

    id = Column(String(60), primary_key=True,
                index=True, default=UUID_4)
    permission_id = Column(String(60), ForeignKey(
        'permission.id'), nullable=False)
    profile_id = Column(String(60), ForeignKey(
        'profile.id'), nullable=False)
    created = Column(TIMESTAMP, default=UTC)
    modified = Column(TIMESTAMP, default=None)

    permission = relationship(
        'PermissionModel', back_populates='permission_profile')
    profile = relationship('ProfileModel', back_populates='permission_profile')
