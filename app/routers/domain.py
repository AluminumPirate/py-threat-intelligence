from app.utils.domain_utils import validate_domain_name
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.controllers import domain_controller
from app.database import get_db
from app.schemas import DomainRead, DomainCreate, ScanRead
from starlette import status

router = APIRouter()


# @router.get("/", response_model=DomainRead, status_code=status.HTTP_200_OK)
# async def get_domain(domain_name: str = Query(..., alias="domain_name"), db: Session = Depends(get_db)):
#     domain_name = validate_domain_name(domain_name)
#     if domain_name is None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid domain.")
#
#     domain, last_scan = domain_controller.get_domain_with_latest_scan(domain_name, db)
#     if not domain:
#         domain = domain_controller.create_domain(DomainCreate(name=domain_name), db)
#
#     return {
#         "id": domain.id,
#         "name": domain.name,
#         "status": domain.status.value,
#         "created_at": domain.created_at,
#         "updated_at": domain.updated_at,
#         "last_scan": last_scan or {}
#     }

@router.get("/", response_model=DomainRead, status_code=status.HTTP_200_OK)
async def get_domain(domain_name: str = Query(..., alias="domain_name"), db: Session = Depends(get_db)) -> DomainRead:
    domain_name = validate_domain_name(domain_name)
    if domain_name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid domain.")

    domain, last_scan = domain_controller.get_domain_with_latest_scan(domain_name, db)
    if not domain:
        domain = domain_controller.create_domain(DomainCreate(name=domain_name), db)

    domain_data = DomainRead.from_orm(domain).dict()
    domain_data["last_scan"] = last_scan.to_dict() if last_scan else None

    return DomainRead(**domain_data)


@router.post("/", response_model=DomainRead, status_code=status.HTTP_201_CREATED)
async def create_domain(domain_data: DomainCreate, db: Session = Depends(get_db)) -> DomainRead:
    domain_name = validate_domain_name(domain_data.name)
    if domain_name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid domain.")

    new_domain = domain_controller.create_domain(domain_data, db)
    return DomainRead.from_orm(new_domain)


@router.get("/all", response_model=List[DomainRead], status_code=status.HTTP_200_OK)
async def get_all_domains(db: Session = Depends(get_db)):
    domains = domain_controller.get_all_domains(db)
    return [DomainRead.from_orm(domain) for domain in domains]


@router.get("/scans/{domain_name}", response_model=List[ScanRead], status_code=status.HTTP_200_OK)
async def get_all_scans(domain_name: str, db: Session = Depends(get_db)) -> List[ScanRead]:
    scans = domain_controller.get_all_scans_for_domain(domain_name, db)
    return [ScanRead.from_orm(scan) for scan in scans]


@router.post("/scan", response_model=ScanRead, status_code=status.HTTP_200_OK)
async def scan_domain(domain_name: str = Query(..., alias="domain_name"), db: Session = Depends(get_db)) -> ScanRead:
    domain_name = validate_domain_name(domain_name)
    if domain_name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid domain.")

    scan = domain_controller.scan_domain(domain_name, db)
    if not scan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Domain not found or scan failed")
    return ScanRead.from_orm(scan)
