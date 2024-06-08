from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.models import Domain
from app.controllers.domain_controller import scan_domain


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scan_domains, 'interval', days=30)  # Configurable interval
    scheduler.start()


def scan_domains():
    db = SessionLocal()
    try:
        domains = db.query(Domain).all()
        for domain in domains:
            scan_domain(domain.name, db)
    finally:
        db.close()
