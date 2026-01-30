import os
import yaml
import json

# 1. Generar config.yaml
config_data = {
    "TELEGRAM_CHANNEL_ID": os.getenv("TELEGRAM_CHANNEL_ID", ""),
    "TELEGRAM_TOKEN": os.getenv("TELEGRAM_TOKEN", "")
}
with open("config.yaml", "w") as f:
    yaml.dump(config_data, f)

# 2. Generar args.json
def to_list(env_var):
    val = os.getenv(env_var)
    if not val: return None
    try:
        return json.loads(val)
    except:
        return [val]

args_data = {
    "search_query": os.getenv("SEARCH_QUERY", "laptop"),
    "min_price": int(os.getenv("MIN_PRICE", "0")),
    "max_price": int(os.getenv("MAX_PRICE", "9999")),
    "latitude": float(os.getenv("LATITUDE")) if os.getenv("LATITUDE") else None,
    "longitude": float(os.getenv("LONGITUDE")) if os.getenv("LONGITUDE") else None,
    "max_distance": int(os.getenv("MAX_DISTANCE")) if os.getenv("MAX_DISTANCE") else None,
    "condition": os.getenv("CONDITION"),
    "title_exclude": to_list("TITLE_EXCLUDE"),
    "description_exclude": to_list("DESCRIPTION_EXCLUDE"),
    "title_must_include": to_list("TITLE_MUST_INCLUDE"),
    "description_must_include": to_list("DESCRIPTION_MUST_INCLUDE"),
    "title_first_word_include": os.getenv("TITLE_FIRST_WORD_INCLUDE")
}

# Limpiar valores Nulos
args_data = {k: v for k, v in args_data.items() if v is not None}

# IMPORTANTE: El bot espera una LISTA de búsquedas, no una búsqueda sola
args_list = [args_data]

with open("args.json", "w") as f:
    json.dump(args_list, f, indent=4)

print("Configuraciones generadas correctamente.")
