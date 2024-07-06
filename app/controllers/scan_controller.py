from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from fastapi import HTTPException, status
from app.models import Domain, Scan, ScanStatus, DomainStatus
from app.services.scan_service import perform_scans
import uuid


async def create_scan(domain_name: str, db: AsyncSession) -> Scan:
    result = await db.execute(select(Domain).filter(Domain.name == domain_name))
    domain = result.scalars().first()
    if not domain:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Domain not found")

    scan = Scan(
        id=uuid.uuid4(),
        domain_id=domain.id,
        status=ScanStatus.scanning,
        data={}
    )
    db.add(scan)
    await db.commit()
    await db.refresh(scan)

    try:
        results, scan_status = await perform_scans(domain_name)
        scan.data = results
        scan.status = ScanStatus[scan_status.replace(' ', '_')]
        await db.commit()
        await db.refresh(scan)

        if scan_status == "completed":
            domain.status = DomainStatus.scanned.value
            await db.commit()
            await db.refresh(domain)
    except Exception as e:
        scan.status = ScanStatus.failed
        scan.data = {"error": str(e)}
        await db.commit()
        await db.refresh(scan)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return scan


async def delete_scan(scan_id: str, db: AsyncSession) -> None:
    result = await db.execute(select(Scan).filter(Scan.id == scan_id))
    scan = result.scalars().first()
    if not scan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan not found")

    await db.execute(delete(Scan).where(Scan.id == scan_id))
    await db.commit()
