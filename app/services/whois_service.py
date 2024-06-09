import os
import requests
from dotenv import load_dotenv
from typing import Any, Dict
from .base_service import BaseService

load_dotenv()

WHOIS_API_KEY = os.getenv("WHOIS_JSON_API_KEY")
WHOIS_URL = "https://whoisjson.com/api/v1/whois"


@BaseService.register("whois")
class WhoisService(BaseService):
    def get_info(self, domain_name: str) -> Dict[str, Any]:
        headers = {
            "Authorization": f"TOKEN={WHOIS_API_KEY}"
        }
        params = {
            "domain": domain_name
        }
        response = requests.get(WHOIS_URL, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.status_code, "message": response.text}
