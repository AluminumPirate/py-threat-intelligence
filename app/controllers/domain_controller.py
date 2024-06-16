import asyncio

from typing import List, Tuple, Optional

from app.controllers.scan_controller import create_scan
from app.database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from fastapi import HTTPException, status
from app.models import Domain, Scan, DomainStatus
from app.schemas import DomainCreate
import uuid

from sqlalchemy.orm import selectinload


async def get_domain(domain_name: str, db: AsyncSession) -> Optional[Domain]:
    result = await db.execute(select(Domain).filter(Domain.name == domain_name))
    return result.scalars().first()


async def create_domain(domain_data: DomainCreate, db: AsyncSession) -> Domain:
    existing_domain = await get_domain(domain_data.name, db)
    if existing_domain:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Domain already exists")

    new_domain = Domain(
        id=uuid.uuid4(),
        name=domain_data.name,
        status=DomainStatus.pending
    )
    db.add(new_domain)
    await db.commit()
    await db.refresh(new_domain)
    return new_domain


async def delete_domain(domain_name: str, db: AsyncSession) -> None:
    domain = await get_domain(domain_name, db)
    if not domain:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Domain not found")

    # Delete all scans associated with the domain
    await db.execute(delete(Scan).where(Scan.domain_id == domain.id))

    # Delete the domain
    await db.execute(delete(Domain).where(Domain.id == domain.id))
    await db.commit()


async def get_domain_with_latest_scan(domain_name: str, db: AsyncSession) -> Tuple[Optional[Domain], Optional[Scan]]:
    domain = await get_domain(domain_name, db)
    last_scan = None

    if domain:
        result = await db.execute(
            select(Scan).filter(Scan.domain_id == domain.id).order_by(Scan.created_at.desc())
        )
        last_scan = result.scalars().first()

    return domain, last_scan


async def get_domain_with_all_scans(domain_name: str, db: AsyncSession) -> Tuple[Optional[Domain], List[Scan]]:
    result = await db.execute(
        select(Domain).options(selectinload(Domain.scans)).filter(Domain.name == domain_name)
    )
    domain = result.scalars().first()
    if not domain:
        return None, []

    scans = domain.scans
    return domain, scans


async def get_all_domains(db: AsyncSession) -> List[Domain]:
    result = await db.execute(select(Domain))
    return result.scalars().all()


async def get_all_domains_with_scans(db: AsyncSession) -> List[Domain]:
    result = await db.execute(
        select(Domain).options(selectinload(Domain.scans))
    )
    domains = result.scalars().all()
    return domains


async def scan_domains_job(db: AsyncSession) -> List[Tuple[Scan, Domain]]:
    result = await db.execute(select(Domain))
    domains_list = result.scalars().all()

    async def scan_domain_task(domain: Domain) -> Tuple[Scan, Domain]:
        async with AsyncSessionLocal() as session:
            try:

                scan = await create_scan(domain.name, session)

                return scan, domain
            except Exception as e:
                # Handle the exception and return a tuple indicating the failure

                return None, domain

    tasks = [scan_domain_task(domain) for domain in domains_list]
    scans_with_domains = await asyncio.gather(*tasks)

    # Filter out the failed tasks
    successful_scans_with_domains = [(scan, domain) for scan, domain in scans_with_domains if scan is not None]

    return successful_scans_with_domains
