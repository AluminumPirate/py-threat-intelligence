from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Domain, Scan
from app.services.virus_total_service import get_virus_total_info
from app.services.whois_service import get_whois_info
from app.schemas import DomainCreate, ScanCreate


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

    virus_total_info = get_virus_total_info(domain_name)
    whois_info = get_whois_info(domain_name)

    scan = Scan(
        domain_id=domain.id,
        status="completed",
        data={"virus_total": virus_total_info, "whois": whois_info}
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan
