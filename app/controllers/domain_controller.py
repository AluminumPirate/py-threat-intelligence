from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Domain, Scan
from app.schemas import DomainCreate
from app.services.scan_service import perform_scans
import uuid


def get_domain(domain_name: str, db: Session):
    return db.query(Domain).filter(Domain.name == domain_name).first()


def create_domain(domain_data: DomainCreate, db: Session):
    new_domain = Domain(name=domain_data.name)
    db.add(new_domain)
    db.commit()
    db.refresh(new_domain)
    return new_domain


def get_all_domains(db: Session):
    return db.query(Domain).all()


def scan_domain(domain_name: str, db: Session):
    domain = get_domain(domain_name, db)
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")

    # Create initial Scan record with status "scanning"
    scan = Scan(
        id=uuid.uuid4(),
        domain_id=domain.id,
        status="scanning",
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
        scan.status = scan_status
        db.commit()
        db.refresh(scan)
    except Exception as e:
        # Update Scan record with status "failed" in case of an error
        scan.status = "failed"
        scan.data = {"error": str(e)}
        db.commit()
        db.refresh(scan)
        raise HTTPException(status_code=500, detail=str(e))

    return scan
