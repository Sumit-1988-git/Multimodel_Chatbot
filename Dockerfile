FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure Streamlit secrets file exists before build
RUN mkdir -p /app/.streamlit
COPY .streamlit/secrets.toml /app/.streamlit/secrets.toml

# Create non-root user for security
RUN useradd -m -u 1000 chatbot
USER chatbot

# Expose ports for all services
EXPOSE 8501 8000 8001
