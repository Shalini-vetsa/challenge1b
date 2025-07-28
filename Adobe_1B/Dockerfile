FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ make build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install torch CPU version + other deps
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu torch==2.2.0 \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
