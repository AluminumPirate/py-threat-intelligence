from typing import List, Tuple, Optional, Type

from sqlalchemy import desc
from sqlalchemy.orm import Session
from pydantic_core import ValidationError as PydanticValidationError
from fastapi import HTTPException
from fastapi import status
from app.models import Domain, Scan, DomainStatus, ScanStatus
from app.services.scan_service import perform_scans
from app.schemas import DomainCreate
import uuid


def get_domain(domain_name: str, db: Session) -> Optional[Domain]:
    try:
        return db.query(Domain).filter(Domain.name == domain_name).first()
    except PydanticValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid domain name format")


def get_all_scans_for_domain(domain_name: str, db: Session) -> List[Scan]:
    domain = db.query(Domain).filter(Domain.name == domain_name).first()
    if not domain:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Domain not found")

    scans = db.query(Scan).filter(Scan.domain_id == domain.id).order_by(desc(Scan.created_at)).all()
    return scans


def get_domain_with_latest_scan(domain_name: str, db: Session, exclude_failed: bool = True) -> Tuple[Optional[Domain], Optional[Scan]]:
    try:
        domain: Optional[Domain] = db.query(Domain).filter(Domain.name == domain_name).first()
        last_scan: Optional[Scan] = None

        if domain:
            query = db.query(Scan).filter(Scan.domain_id == domain.id)
            if exclude_failed:
                query = query.filter(Scan.status != ScanStatus.failed)
            last_scan = query.order_by(desc(Scan.created_at)).first()

        return domain, last_scan

    except PydanticValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid domain name format")


def create_domain(domain_data: DomainCreate, db: Session) -> Domain:
    if db.query(Domain).filter(Domain.name == domain_data.name).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Domain already exists")

    new_domain: Domain = Domain(name=domain_data.name, status=DomainStatus.pending)
    db.add(new_domain)
    db.commit()
    db.refresh(new_domain)
    return new_domain


def get_all_domains(db: Session) -> list[Type[Domain]]:
    return db.query(Domain).all()


def scan_domain(domain_name: str, db: Session) -> Scan:
    domain = get_domain(domain_name, db)
    if not domain:
        # Add domain to analysis list if not found
        create_domain(DomainCreate(name=domain_name), db)
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="Domain added for analysis. Check back later.")

    # Create initial Scan record with status "scanning"
    scan = Scan(
        id=uuid.uuid4(),
        domain_id=domain.id,
        status=ScanStatus.scanning,
        data={}
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)

    try:
        # Perform the scans using the generic scan service
        results, scan_status = perform_scans(domain_name)

        # Update Scan record with results and change status accordingly
        scan.data = results
        scan.status = ScanStatus[scan_status.replace(' ', '_')]  # Convert status to enum compatible
        db.commit()
        db.refresh(scan)

        # Update domain status to scanned if the scan is successful
        if scan_status == "completed":
            domain.status = DomainStatus.scanned
        else:
            pass
            # domain.status = DomainStatus.pending

        db.commit()
        db.refresh(domain)
    except Exception as e:
        # Update Scan record with status "failed" in case of an error
        scan.status = ScanStatus.failed
        scan.data = {"error": str(e)}
        db.commit()
        db.refresh(scan)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return scan


def scan_domains_job(db: Session) -> list[tuple[Scan, Type[Domain]]]:
    domains_list = get_all_domains(db)

    scans_with_domains = []

    for domain in domains_list:
        scan = scan_domain(domain.name, db)
        scans_with_domains.append((scan, domain))

    return scans_with_domains
