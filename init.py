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
# Función auxiliar para convertir strings de entorno en listas si es necesario
def to_list(env_var):
    val = os.getenv(env_var)
    if not val: return None
    try:
        return json.loads(val) # Si envías ["Intel", "i5"] lo parsea bien
    except:
        return [val] # Si envías Intel, lo mete en una lista [Intel]

args_data = {
    "search_query": os.getenv("SEARCH_QUERY", "laptop"),
    "min_price": os.getenv("MIN_PRICE", "0"),
    "max_price": os.getenv("MAX_PRICE", "9999"),
    "latitude": os.getenv("LATITUDE"),
    "longitude": os.getenv("LONGITUDE"),
    "max_distance": os.getenv("MAX_DISTANCE"),
    "condition": os.getenv("CONDITION"),
    "title_exclude": to_list("TITLE_EXCLUDE"),
    "description_exclude": to_list("DESCRIPTION_EXCLUDE"),
    "title_must_include": to_list("TITLE_MUST_INCLUDE"),
    "description_must_include": to_list("DESCRIPTION_MUST_INCLUDE"),
    "title_first_word_include": os.getenv("TITLE_FIRST_WORD_INCLUDE")
}

# Limpiar valores Nulos para que Wallapop no de error
args_data = {k: v for k, v in args_data.items() if v is not None}

with open("args.json", "w") as f:
    json.dump(args_data, f, indent=4)

print("Configuraciones generadas correctamente.")
