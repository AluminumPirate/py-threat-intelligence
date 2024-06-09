from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from app.controllers import domain_controller
from app.database import get_db
from app.schemas import ScanRead, ScanWithDomainRead

router = APIRouter()


@router.post("/", response_model=Union[List[ScanWithDomainRead], Dict], status_code=status.HTTP_200_OK)
async def run_job(db: Session = Depends(get_db)) -> Union[List[ScanWithDomainRead], Dict]:
    scans_with_domains = domain_controller.scan_domains_job(db)

    result = [
        ScanWithDomainRead(domain_name=domain.name, scan=ScanRead.from_orm(scan)) for scan, domain in scans_with_domains
    ]

    return result

