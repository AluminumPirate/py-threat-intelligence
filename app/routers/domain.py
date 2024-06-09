from app.utils.domain_utils import validate_domain_name
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.controllers import domain_controller
from app.database import get_db
from app.schemas import DomainRead, DomainCreate, ScanRead
from starlette import status

router = APIRouter()


@router.get("/", response_model=DomainRead)
async def get_domain(domain_name: str = Query(..., alias="domain_name"), db: Session = Depends(get_db)):
    domain_name = validate_domain_name(domain_name)
    if domain_name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid domain.")

    domain, last_scan = domain_controller.get_domain_with_latest_scan(domain_name, db)
    if not domain:
        domain = domain_controller.create_domain(DomainCreate(name=domain_name), db)

    return {
        "id": domain.id,
        "name": domain.name,
        "status": domain.status.value,
        "created_at": domain.created_at,
        "updated_at": domain.updated_at,
        "last_scan": last_scan or {}
    }


@router.post("/", response_model=DomainRead)
async def create_domain(domain_data: DomainCreate, db: Session = Depends(get_db)):
    domain_name = validate_domain_name(domain_data.name)
    if domain_name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid domain.")

    return domain_controller.create_domain(domain_data, db)


@router.get("/all", response_model=List[DomainRead])
async def get_all_domains(db: Session = Depends(get_db)):
    return domain_controller.get_all_domains(db)


@router.post("/scan", response_model=ScanRead)
async def scan_domain(domain_name: str = Query(..., alias="domain_name"), db: Session = Depends(get_db)):
    domain_name = validate_domain_name(domain_name)
    if domain_name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid domain.")

    scan_result = domain_controller.scan_domain(domain_name, db)
    if not scan_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Domain not found or scan failed")
    return scan_result
