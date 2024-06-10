import os
import requests
from dotenv import load_dotenv

load_dotenv("/app/.env.docker")

api_url = os.getenv("API_URL")
if api_url is None:
    api_url = "http://api:3004"


def call_api_job(job_name: str):
    try:
        print(f"Calling {job_name}")
        endpoint = f"{api_url}/jobs"
        response = requests.post(endpoint, json={"domain": ""})
        response.raise_for_status()
        print(f"Job {job_name} executed successfully with response: {response.json()}")
    except Exception as e:
        print(f"\n\n\nError: {e}\n\n\n")


call_api_job("Domain Scan")
