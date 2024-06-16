from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas import DomainRead, ScanRead, DomainReadWithLastScan
from app.controllers import domain_controller, scan_controller

router = APIRouter()


# Get all domains (without scans)
@router.get("/", response_model=List[DomainRead], summary="Get all domains without scans")
async def get_all_domains(db: AsyncSession = Depends(get_db)):
    domains = await domain_controller.get_all_domains(db)
    return [DomainRead.from_orm(domain) for domain in domains]


# Get all domains (with the last scan)
@router.get("/with-last-scan", response_model=List[DomainReadWithLastScan],
            summary="Get all domains with the latest scan")
async def get_all_domains_with_last_scan(db: AsyncSession = Depends(get_db)):
    domains = await domain_controller.get_all_domains_with_scans(db)
    domains_with_last_scan = []
    for domain in domains:
        domain_data = DomainRead.from_orm(domain)
        last_scan = domain.scans[0] if domain.scans else None
        last_scan_data = ScanRead.from_orm(last_scan) if last_scan else None
        domains_with_last_scan.append(DomainReadWithLastScan(domain=domain_data, last_scan=last_scan_data))
    return domains_with_last_scan


# Endpoint to delete a scan by ID
@router.delete("/scan/{scan_id}", status_code=204, summary="Delete a scan by ID")
async def delete_scan(scan_id: str, db: AsyncSession = Depends(get_db)):
    await scan_controller.delete_scan(scan_id, db)
    return None
