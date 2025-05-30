# 🐍 Modern Python Backend for Ansible Beautify
FROM python:3.11-slim

# Set metadata
LABEL maintainer="Florian Courouge"
LABEL description="Ansible Beautify Backend - Transform one-liner Ansible tasks to beautiful YAML"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=api.py
ENV FLASK_ENV=production

# Create non-root user for security
RUN groupadd -r appuser && \
    useradd -r -g appuser -m -d /home/appuser appuser

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create Ansible directories with proper permissions
RUN mkdir -p /tmp/.ansible /home/appuser/.ansible/tmp && \
    chown -R appuser:appuser /tmp/.ansible /home/appuser/.ansible && \
    chmod -R 755 /tmp/.ansible /home/appuser/.ansible

# Change ownership to non-root user
RUN chown -R appuser:appuser /app
USER appuser

# Set user-specific environment variables
ENV HOME=/home/appuser
ENV ANSIBLE_CONFIG=/app/ansible.cfg
ENV ANSIBLE_HOST_KEY_CHECKING=False
ENV ANSIBLE_GATHERING=explicit
ENV ANSIBLE_LOCAL_TEMP=/tmp/.ansible
ENV ANSIBLE_REMOTE_TEMP=/tmp/.ansible

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/health', timeout=5)" || exit 1

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "api.py"]