import os
import requests
from dotenv import load_dotenv
from .base_service import BaseService

load_dotenv()

VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
VIRUSTOTAL_URL = "https://www.virustotal.com/api/v3/domains/"


@BaseService.register("virustotal")
class VirusTotalService(BaseService):
    def get_info(self, domain_name: str):
        headers = {
            "x-apikey": VIRUSTOTAL_API_KEY
        }
        response = requests.get(f"{VIRUSTOTAL_URL}{domain_name}", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.status_code, "message": response.text}
