import os
import requests
from dotenv import load_dotenv

load_dotenv()

WHOIS_API_KEY = os.getenv("WHOIS_JSON_API_KEY")
WHOIS_URL = "https://whoisjson.com/api/v1/whois"


def get_whois_info(domain_name: str):
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
