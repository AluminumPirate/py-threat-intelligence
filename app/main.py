import sys
import os

# Ensure the root directory is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import domain, jobs
from app.models import *

# Import service modules to ensure they are registered
# from app.services import virus_total_service, whois_service, shodan_service
from app.services import virus_total_service, whois_service, google_dns_service, cloudflare_dns_service, \
    hackertarget_dns_service

app = FastAPI()

# Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routers
app.include_router(domain.router, prefix="/domains", tags=["domains"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])

# Create (if not exists) the database tables
Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=3004, reload=True)
