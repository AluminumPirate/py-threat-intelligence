from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, String, ForeignKey, JSON, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum
import uuid


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class DomainStatus(enum.Enum):
    pending = "pending"
    scanned = "scanned"


class ScanStatus(enum.Enum):
    scanning = "scanning"
    completed = "completed"
    failed = "failed"
    partially_succeeded = "partially succeeded"


class Domain(Base):
    __tablename__ = 'domains'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    status = Column(Enum(DomainStatus), default=DomainStatus.pending, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    scans = relationship("Scan", back_populates="domain")


class Scan(Base):
    __tablename__ = 'scans'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    domain_id = Column(UUID(as_uuid=True), ForeignKey('domains.id'), nullable=False)
    data = Column(JSON, nullable=False)
    status = Column(Enum(ScanStatus), default=ScanStatus.scanning, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    domain = relationship("Domain", back_populates="scans")
