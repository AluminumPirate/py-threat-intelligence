import httpx
from typing import Any, Dict
from .base_service import BaseService

HACKERTARGET_DNS_API_URL = "https://api.hackertarget.com/dnslookup/"


@BaseService.register("hackertarget_dns")
class HackertargetDNSService(BaseService):
    async def get_info(self, domain_name: str) -> Dict[str, Any]:
        params = {
            "q": domain_name
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(HACKERTARGET_DNS_API_URL, params=params)

        if response.status_code == 200:
            return {
                "raw": response.text
            }
        else:
            return {"error": response.status_code, "message": response.text}
