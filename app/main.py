import sys
import os

# Ensure the root directory is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, initialize_database, async_engine
from app.routers import domain, jobs, domains
from app.models import *  # Ensure models are imported so Base can see them

# Import service modules to ensure they are registered
from app.services import virus_total_service, whois_service, google_dns_service, cloudflare_dns_service, \
    hackertarget_dns_service

app = FastAPI(
    title="Threat Intelligence",
    version="0.1.2",
    description="An Async FastAPI Server for Threat Intelligence"
)

# Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routers
app.include_router(domain.router, prefix="/domain", tags=["Domain"])
app.include_router(domains.router, prefix="/domains", tags=["Domains"])
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])

# Initialize the database (create if not exists)
initialize_database()


# Create the tables asynchronously
@app.on_event("startup")
async def on_startup():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=3004, reload=True)
