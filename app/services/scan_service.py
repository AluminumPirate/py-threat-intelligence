from .base_service import BaseService


def perform_scans(domain_name: str):
    results = {}
    statuses = []

    for service_name, service in BaseService.services.items():
        try:
            result = service.get_info(domain_name)
            results[service_name] = result
            statuses.append(result.get("error") is None)  # Assume a successful response has no "error" field
        except Exception as e:
            results[service_name] = {"error": str(e)}
            statuses.append(False)

    if all(statuses):
        scan_status = "completed"
    elif any(statuses):
        scan_status = "partially succeeded"
    else:
        scan_status = "failed"

    return results, scan_status
