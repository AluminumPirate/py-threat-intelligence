import os
import requests
from dotenv import load_dotenv

load_dotenv()

VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
VIRUSTOTAL_URL = "https://www.virustotal.com/api/v3/domains/"


def get_virus_total_info(domain_name: str):
    # must implement error key in return json if error occurred

    headers = {
        "x-apikey": VIRUSTOTAL_API_KEY
    }
    response = requests.get(f"{VIRUSTOTAL_URL}{domain_name}", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}
