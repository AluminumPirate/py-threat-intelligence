from typing import Tuple, Dict, Any

from app.models import ScanStatus

from .base_service import BaseService
import asyncio


async def perform_scans(domain_name: str) -> Tuple[Dict[str, Any], ScanStatus]:
    results: Dict[str, Any] = {}
    statuses: Dict[str, bool] = {}

    async def get_service_info(service_name: str, service: BaseService) -> None:
        try:
            result = await service.get_info(domain_name)
            results[service_name] = result
            statuses[service_name] = "error" not in result  # Assume a successful response has no "error" field
        except Exception as e:
            results[service_name] = {"error": str(e)}
            statuses[service_name] = False

    tasks = [
        get_service_info(service_name, service)
        for service_name, service in BaseService.services.items()
    ]

    await asyncio.gather(*tasks)

    if all(statuses.values()):
        scan_status = ScanStatus.completed.value
    elif any(statuses.values()):
        scan_status = ScanStatus.partially_succeeded.value
    else:
        scan_status = ScanStatus.failed.value

    return results, scan_status
