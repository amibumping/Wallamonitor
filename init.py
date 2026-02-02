import os
import yaml
import json

print("--- 🚀 INICIANDO CONFIGURACIÓN DE WALLAMONITOR ---")

# 1. Generar config.yaml (Telegram)
# Limpiamos posibles comillas de las variables de entorno
token = os.getenv("TELEGRAM_TOKEN", "").strip().replace('"', '').replace("'", "")
channel = os.getenv("TELEGRAM_CHANNEL_ID", "").strip().replace('"', '').replace("'", "")

config_data = {
    "telegram_token": str(token),
    "telegram_channel": str(channel)
}

with open("config.yaml", "w") as f:
    yaml.dump(config_data, f, default_flow_style=False)

print("✅ Archivo config.yaml generado.")

# 2. Verificar args.json
if os.path.exists("args.json"):
    print("✅ Archivo args.json detectado. Se usarán las búsquedas configuradas en el archivo.")
else:
    # Si no hay archivo, creamos uno básico para que el bot no de error al arrancar
    print("⚠️ No se detectó args.json, creando uno por defecto con SEARCH_QUERY...")
    args_data = [{
        "search_query": os.getenv("SEARCH_QUERY", "laptop"),
        "latitude": os.getenv("LATITUDE", "40.4167"),
        "longitude": os.getenv("LONGITUDE", "-3.7033"),
        "max_distance": os.getenv("MAX_DISTANCE", "0"),
        "condition": os.getenv("CONDITION", "all"),
        "min_price": os.getenv("MIN_PRICE", "0"),
        "max_price": os.getenv("MAX_PRICE", "9999"),
        "title_exclude": [],
        "description_exclude": [],
        "title_must_include": [],
        "description_must_include": [],
        "title_first_word_exclude": []
    }]
    with open("args.json", "w") as f:
        json.dump(args_data, f, indent=4)

print("--- 🏁 CONFIGURACIÓN COMPLETADA. LANZANDO BOT... ---")
