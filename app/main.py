import sys
import os

# Ensure the root directory is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import domain
from app.models import *
from app.utils.scheduler import start_scheduler

# Import service modules to ensure they are registered
from app.services import virus_total_service, whois_service

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

# Create (if not exists) the database tables
Base.metadata.create_all(bind=engine)

# Start the scheduler
start_scheduler()

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=3004, reload=True)
