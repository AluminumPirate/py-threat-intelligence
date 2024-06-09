from pydantic import BaseModel, Field, field_validator
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from app.models import ScanStatus
from app.utils.domain_utils import clean_domain_name, is_valid_domain


class DomainBase(BaseModel):
    name: str = Field(..., example="example.com")

    @field_validator('name', mode='before')
    def validate_domain_name(cls, value):
        cleaned_value = clean_domain_name(value)
        if not is_valid_domain(cleaned_value):
            raise ValueError('Invalid domain name format')
        return cleaned_value


class DomainCreate(DomainBase):
    pass


class DomainRead(DomainBase):
    id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime
    last_scan: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


class ScanBase(BaseModel):
    status: ScanStatus
    data: dict


class ScanCreate(ScanBase):
    pass


class ScanRead(ScanBase):
    id: uuid.UUID
    status: ScanStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
