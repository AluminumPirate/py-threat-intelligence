import requests
from typing import Any, Dict
from .base_service import BaseService

GOOGLE_DNS_API_URL = "https://dns.google/resolve"


@BaseService.register("google_dns")
class GoogleDNSService(BaseService):
    def get_info(self, domain_name: str) -> Dict[str, Any]:
        params = {
            "name": domain_name,
            "type": "Any"
        }
        response = requests.get(GOOGLE_DNS_API_URL, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.status_code, "message": response.text}
