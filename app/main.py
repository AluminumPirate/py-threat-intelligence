from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import domain
from app.utils.scheduler import start_scheduler

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
app.include_router(domain.router, prefix="/domain", tags=["domain"])

# Create (if not exists) the database tables
Base.metadata.create_all(bind=engine)

# Start the scheduler
start_scheduler()

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=3004, reload=True)
