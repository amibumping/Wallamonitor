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

# 2. Función para manejar listas desde entorno
def to_list(env_var):
    val = os.getenv(env_var)
    if not val or val.strip() == "": return []
    try:
        parsed = json.loads(val)
        return parsed if isinstance(parsed, list) else [parsed]
    except:
        return [val]

# 3. Generar args.json con TODAS las llaves que el bot espera
# Si la variable de entorno no existe, se pone un valor por defecto compatible
args_data = {
    "search_query": os.getenv("SEARCH_QUERY", "laptop"),
    "min_price": int(os.getenv("MIN_PRICE", "0")),
    "max_price": int(os.getenv("MAX_PRICE", "999999")),
    "latitude": float(os.getenv("LATITUDE")) if os.getenv("LATITUDE") else None,
    "longitude": float(os.getenv("LONGITUDE")) if os.getenv("LONGITUDE") else None,
    "max_distance": int(os.getenv("MAX_DISTANCE")) if os.getenv("MAX_DISTANCE") else None,
    "condition": os.getenv("CONDITION", None),
    "title_exclude": to_list("TITLE_EXCLUDE"),
    "description_exclude": to_list("DESCRIPTION_EXCLUDE"),
    "title_must_include": to_list("TITLE_MUST_INCLUDE"),
    "description_must_include": to_list("DESCRIPTION_MUST_INCLUDE"),
    "title_first_word_include": os.getenv("TITLE_FIRST_WORD_INCLUDE", None),
    "title_first_word_exclude": os.getenv("TITLE_FIRST_WORD_EXCLUDE", None) # Esta era la que faltaba
}

# El bot espera una lista de objetos
args_list = [args_data]

with open("args.json", "w") as f:
    json.dump(args_list, f, indent=4)

print("Configuraciones generadas correctamente con todos los campos requeridos.")
