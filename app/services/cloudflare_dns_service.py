import httpx
from typing import Any, Dict
from .base_service import BaseService

CLOUDFLARE_DNS_API_URL = "https://cloudflare-dns.com/dns-query"


@BaseService.register("cloudflare_dns")
class CloudflareDNSService(BaseService):
    async def get_info(self, domain_name: str) -> Dict[str, Any]:
        headers = {
            "Accept": "application/dns-json"
        }
        params = {
            "name": domain_name,
            "type": "A"  # You can change this to any DNS record type you need
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(CLOUDFLARE_DNS_API_URL, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.status_code, "message": response.text}
