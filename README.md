# Threat Intelligence System 🛡️
Welcome to the Threat Intelligence System! This project is designed to gather and present data about domain names from various threat intelligence services. It provides a REST API for interacting with the system.

## Short design explanation 💡
The project contains 3 components. The API server, Database and Scheduler.

* Chosen language is Python using Fast API, pydantic and sqlalchemy.


* Chosen database is Postgres (Though initially I thought about using MongoDB since we have json data from our api servers, I think the tradeoff for non-indexed joins using Mongo with large amount of collected data in the future would be too much for I\O operations does not worth it).


* Scheduling System - I chose to use the cron scheduler because it seems like a good choice - we can configure intervals and even if the service crashed ans we turn it back on it would not matter since we choose a time (x day of the month) and not an actual interval.

All are enclosed in a docker container using docker-compose.yml

## Things to point out 👉
* I have learned about docker and docker-compose files.
* I have learned more about sqlalchemy ORM.
* I have leaned how to create a README file 😉

## Features ✨

- **Domain Management**: Add, delete, and list domains.
- **Scans**: Perform scans on domains using multiple OSINT services.
- **Scheduled Jobs**: Automatically perform scans at regular intervals.

## Setup 🚀

### Prerequisites

- Python 3.8+
- PostgreSQL
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/AluminumPirate/py-threat-intelligence.git
    cd py-threat-intelligence
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Environment Variables**:
    Create a `.env` file in the project root with the following content:
    ```env
    WHOIS_API_KEY=your_whois_api_key
    VIRUSTOTAL_API_KEY=your_virustotal_api_key
   
    DATABASE_URL=postgresql+asyncpg://user:password@localhost/db-name
    POSTGRES_USER=username
    POSTGRES_PASSWORD=password
    POSTGRES_DB=db-name
    API_URL=http://api:3004
    ```

### Running the Server 🖥️

To start the FastAPI server, run:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 3004 --reload
```


### Using Docker 🐳
️
1. **Build the Docker Image**:
    ```bash
    docker compose up --build
    ```

2. **Access The Fast API Docs**:
    The Fast API docs page will be available at: http://localhost:3004/docs
    Or in the docker desktop application of course

### Docker screenshot 📸
![System Architecture](screenshot2.png)



### Scheduled Scans (supported only in linux / docker) ⏰
To schedule scans every X time, you can use a cron job - Currently set to once a month. 
Update the following line to your crontab (the crontab file is inside the scheduler directory):
   ```text
   0 0 1 * * /usr/local/bin/python3 /app/scan_job.py >> /var/log/cron.log 2>&1
   ```

You can see more about the cron expression here and choose a different interval: https://crontab.guru/


### API Endpoints 📡
* GET /domains: List all domains
* POST /domains: Add a new domain
* DELETE /domains/{domain_name}: Delete a domain
* POST /domains/scan: Scan a specific domain
* GET /domains/scans/{domain_name}: Get all scans for a domain
* POST /jobs: Run the scan job manually


### Fast API Screenshot 📸

![System Architecture](screenshot.png)
