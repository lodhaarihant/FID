# Use a base image with Python 3.10
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies required to build SQLite and Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    libsqlite3-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8501 for Streamlit
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "login.py", "--server.port=8501", "--server.enableCORS=false", "--server.headless=true"]