from app.services.virus_total_service import get_virus_total_info
from app.services.whois_service import get_whois_info

# Mapping of service functions to user-friendly names
SERVICE_NAME_MAPPING = {
    get_virus_total_info: "virustotal",
    get_whois_info: "whois"
}


def perform_scans(domain_name: str):
    services = [get_virus_total_info, get_whois_info]
    results = {}
    statuses = []

    for service in services:
        try:
            result = service(domain_name)
            service_name = SERVICE_NAME_MAPPING.get(service, service.__name__)
            results[service_name] = result
            statuses.append(result.get("error") is None)  # Assume a successful response has no "error" field
        except Exception as e:
            service_name = SERVICE_NAME_MAPPING.get(service, service.__name__)
            results[service_name] = {"error": str(e)}
            statuses.append(False)

    if all(statuses):
        scan_status = "completed"
    elif any(statuses):
        scan_status = "partially succeeded"
    else:
        scan_status = "failed"

    return results, scan_status
