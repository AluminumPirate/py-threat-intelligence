from pydantic import BaseModel
import uuid
from datetime import datetime


class DomainBase(BaseModel):
    name: str


class DomainCreate(DomainBase):
    pass


class DomainRead(DomainBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ScanBase(BaseModel):
    status: str
    data: dict


class ScanCreate(ScanBase):
    pass


class ScanRead(ScanBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
