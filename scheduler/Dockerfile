FROM python:3.9-slim

# Install cron and other necessary packages
RUN apt-get update && apt-get install -y \
    cron \
    build-essential \
    libpq-dev

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Create app directory
WORKDIR /app

# Install dependencies
COPY requirements-scheduler.txt /app/requirements-scheduler.txt
RUN pip install --no-cache-dir -r /app/requirements-scheduler.txt

# Copy crontab file and script
COPY crontab.txt /etc/cron.d/scheduler-cron
COPY scan_job.py /app/scan_job.py

# Copy the Docker-specific .env file from the parent directory
COPY .env.docker /app/.env

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/scheduler-cron

# Apply cron job
RUN crontab /etc/cron.d/scheduler-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
