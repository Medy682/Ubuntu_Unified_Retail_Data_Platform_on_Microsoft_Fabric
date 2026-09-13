FROM python:3.14-slim

# Prevent Python from creating .pyc files
# and ensure logs are written directly to the container output.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Container working directory
WORKDIR /app

# Copy dependency definition first
# This allows Docker to cache the dependency installation layer.
COPY requirements.txt .

# Install project dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the project files into the image
COPY . .