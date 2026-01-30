import os
import yaml
import json

# 1. Generar config.yaml (Corregido a minúsculas para el bot)
config_data = {
    "telegram_channel_id": os.getenv("TELEGRAM_CHANNEL_ID", ""),
    "telegram_token": os.getenv("TELEGRAM_TOKEN", "")
}
with open("config.yaml", "w") as f:
    yaml.dump(config_data, f)

# 2. Función para manejar listas
def to_list(env_var):
    val = os.getenv(env_var)
    if not val or val.strip() == "": return []
    try:
        parsed = json.loads(val)
        return parsed if isinstance(parsed, list) else [parsed]
    except:
        return [val]

# 3. Generar args.json (Siguiendo tu modelo exitoso)
args_data = {
    "search_query": os.getenv("SEARCH_QUERY", "laptop"),
    "latitude": os.getenv("LATITUDE", "40.4167"),
    "longitude": os.getenv("LONGITUDE", "-3.7033"),
    "max_distance": os.getenv("MAX_DISTANCE", "0"),
    "condition": os.getenv("CONDITION", "all"),
    "min_price": os.getenv("MIN_PRICE", "0"),
    "max_price": os.getenv("MAX_PRICE", "9999"),
    "title_exclude": to_list("TITLE_EXCLUDE"),
    "description_exclude": to_list("DESCRIPTION_EXCLUDE"),
    "title_must_include": to_list("TITLE_MUST_INCLUDE"),
    "description_must_include": to_list("DESCRIPTION_MUST_INCLUDE"),
    "title_first_word_exclude": to_list("TITLE_FIRST_WORD_EXCLUDE"),
    "title_first_word_include": os.getenv("TITLE_FIRST_WORD_INCLUDE", None)
}

with open("args.json", "w") as f:
    json.dump([args_data], f, indent=4)

print("✅ Configuración generada (Telegram en minúsculas + Args modo manual).")
