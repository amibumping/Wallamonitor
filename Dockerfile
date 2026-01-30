FROM python:3.10-slim

# Instalamos dependencias necesarias para compilar paquetes si fuera necesario en ARM
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "wallamonitor.py"]
