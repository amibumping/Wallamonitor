FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# --- PARCHE PARA REPARAR EL BOT ---
# 1. Corregimos el constructor de URL para que no envíe "None" o vacío en la condición y distancia
RUN sed -i "s/&condition={item.condition}//g" managers/worker.py && \
    sed -i "s/&distance_in_km={item.max_distance}/&distance_in_km={item.max_distance if item.max_distance else 2000}/g" managers/worker.py && \
    sed -i "/language=es_ES/ s/\"$/\&condition={item.condition}\" if item.condition else \"\"/" managers/worker.py

CMD python init.py && python wallamonitor.py
