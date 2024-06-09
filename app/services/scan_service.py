from typing import Tuple, Dict, Any
from .base_service import BaseService


def perform_scans(domain_name: str) -> Tuple[Dict[str, Any], str]:
    results: Dict[str, Any] = {}
    statuses: Dict[str, bool] = {}

    for service_name, service in BaseService.services.items():
        try:
            result = service.get_info(domain_name)
            results[service_name] = result
            statuses[service_name] = "error" not in result  # Assume a successful response has no "error" field
        except Exception as e:
            results[service_name] = {"error": str(e)}
            statuses[service_name] = False

    if all(statuses.values()):
        scan_status = "completed"
    elif any(statuses.values()):
        scan_status = "partially succeeded"
    else:
        scan_status = "failed"

    return results, scan_status
