from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import DomainRead, DomainCreate, DomainReadWithAllScans, ScanRead
from app.controllers import domain_controller, scan_controller

router = APIRouter()


# Create domain
@router.post("/", response_model=DomainRead, summary="Create a new domain")
async def create_domain(domain_data: DomainCreate, db: AsyncSession = Depends(get_db)):
    new_domain = await domain_controller.create_domain(domain_data, db)
    return DomainRead.from_orm(new_domain)


# Delete domain by name
@router.delete("/{domain_name}", status_code=204, summary="Delete a domain by name")
async def delete_domain(domain_name: str, db: AsyncSession = Depends(get_db)):
    await domain_controller.delete_domain(domain_name, db)
    return None


# Get domain with the latest scan
@router.get("/{domain_name}", response_model=DomainRead,
            summary="Get a domain with the latest scan or create it if it doesn't exist")
async def get_domain(domain_name: str, db: AsyncSession = Depends(get_db)):
    domain, last_scan = await domain_controller.get_domain_with_latest_scan(domain_name, db)
    if not domain:
        domain = await domain_controller.create_domain(DomainCreate(name=domain_name), db)
        domain_data = DomainRead.from_orm(domain).dict()
        domain_data["last_scan"] = None
    else:
        domain_data = DomainRead.from_orm(domain).dict()
        domain_data["last_scan"] = ScanRead.from_orm(last_scan).dict() if last_scan else None
    return DomainRead(**domain_data)


# Get domain without scan
@router.get("/{domain_name}/no-scan", response_model=DomainRead, summary="Get a domain without its scans")
async def get_domain_no_scan(domain_name: str, db: AsyncSession = Depends(get_db)):
    domain = await domain_controller.get_domain(domain_name, db)
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    return DomainRead.from_orm(domain)


# Get domain with all scans
@router.get("/{domain_name}/all-scans", response_model=DomainReadWithAllScans,
            summary="Get a domain with all its scans")
async def get_domain_with_scans(domain_name: str, db: AsyncSession = Depends(get_db)):
    domain, scans = await domain_controller.get_domain_with_all_scans(domain_name, db)
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    domain_data = DomainRead.from_orm(domain)
    scans_data = [ScanRead.from_orm(scan) for scan in scans]
    return DomainReadWithAllScans(**domain_data.dict(), scans=scans_data)


# Create scan
@router.post("/{domain_name}/scan", response_model=ScanRead, summary="Create a scan for a domain")
async def create_scan(domain_name: str, db: AsyncSession = Depends(get_db)):
    scan = await scan_controller.create_scan(domain_name, db)
    return ScanRead.from_orm(scan)


# Delete scan by ID
@router.delete("/scan/{scan_id}", status_code=204, summary="Delete a scan by ID")
async def delete_scan(scan_id: str, db: AsyncSession = Depends(get_db)):
    await scan_controller.delete_scan(scan_id, db)
    return None
