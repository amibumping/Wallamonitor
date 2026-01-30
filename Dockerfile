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

# --- PARCHE DE CÓDIGO (Solución al Error 400) ---
# Usamos Python para reescribir la línea de la URL en managers/worker.py
# Ahora solo añadirá la condición si no es nula/vacía y asegura que la distancia no sea 0
RUN python3 -c " \
fname = 'managers/worker.py'; \
content = open(fname).read(); \
old_line = 'f\"&language=es_ES&distance_in_km={item.max_distance}&condition={item.condition}\"'; \
new_line = 'f\"&language=es_ES&distance_in_km={item.max_distance if item.max_distance else 2000}\" + (f\"&condition={item.condition}\" if item.condition and item.condition != \"None\" else \"\")'; \
content = content.replace(old_line, new_line); \
open(fname, 'w').write(content)"

CMD python init.py && python wallamonitor.py
