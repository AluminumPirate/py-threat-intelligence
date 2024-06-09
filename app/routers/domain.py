from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.controllers import domain_controller
from app.database import get_db
from app.schemas import DomainRead, DomainCreate, ScanRead

router = APIRouter()


@router.get("/{domain_name}", response_model=DomainRead)
async def get_domain(domain_name: str, db: Session = Depends(get_db)):
    domain, last_scan = domain_controller.get_domain_with_latest_scan(domain_name, db)
    if not domain:
        domain_controller.create_domain(DomainCreate(name=domain_name), db)
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="Domain added for analysis. Check back later.")
    return {
        "id": domain.id,
        "name": domain.name,
        "status": domain.status,
        "created_at": domain.created_at,
        "updated_at": domain.updated_at,
        "last_scan": last_scan
    }


@router.post("/", response_model=DomainRead)
async def create_domain(domain_data: DomainCreate, db: Session = Depends(get_db)):
    return domain_controller.create_domain(domain_data, db)


@router.get("/", response_model=List[DomainRead])
async def get_all_domains(db: Session = Depends(get_db)):
    return domain_controller.get_all_domains(db)


@router.post("/scan/{domain_name}", response_model=ScanRead)
async def scan_domain(domain_name: str, db: Session = Depends(get_db)):
    scan_result = domain_controller.scan_domain(domain_name, db)
    if not scan_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Domain not found or scan failed")
    return scan_result
