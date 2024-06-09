FROM python:3.9-slim

# Install PostgreSQL development libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Create app directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the app code
COPY ./app /app

# Copy the Docker-specific .env file (if needed)
COPY .env.docker /app/.env

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3004", "--reload"]