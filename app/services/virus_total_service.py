import os
import httpx
from dotenv import load_dotenv
from typing import Any, Dict
from .base_service import BaseService

load_dotenv()

VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
VIRUSTOTAL_URL = "https://www.virustotal.com/api/v3/domains/"


@BaseService.register("virustotal")
class VirusTotalService(BaseService):
    async def get_info(self, domain_name: str) -> Dict[str, Any]:
        headers = {
            "x-apikey": VIRUSTOTAL_API_KEY
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{VIRUSTOTAL_URL}{domain_name}", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.status_code, "message": response.text}
