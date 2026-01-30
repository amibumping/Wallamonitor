import os
import yaml
import json

# --- 1. GENERAR CONFIGURACIONES ---
config_data = {
    "TELEGRAM_CHANNEL_ID": os.getenv("TELEGRAM_CHANNEL_ID", ""),
    "TELEGRAM_TOKEN": os.getenv("TELEGRAM_TOKEN", "")
}
with open("config.yaml", "w") as f:
    yaml.dump(config_data, f)

def to_list(env_var):
    val = os.getenv(env_var)
    if not val or val.strip() == "": return []
    try:
        parsed = json.loads(val)
        return parsed if isinstance(parsed, list) else [parsed]
    except:
        return [val]

args_data = {
    "search_query": os.getenv("SEARCH_QUERY", "laptop"),
    "min_price": int(os.getenv("MIN_PRICE", "0")),
    "max_price": int(os.getenv("MAX_PRICE", "999999")),
    "latitude": float(os.getenv("LATITUDE")) if os.getenv("LATITUDE") else 40.4167,
    "longitude": float(os.getenv("LONGITUDE")) if os.getenv("LONGITUDE") else -3.7033,
    "max_distance": int(os.getenv("MAX_DISTANCE")) if os.getenv("MAX_DISTANCE") else 2000,
    "condition": os.getenv("CONDITION", None),
    "title_exclude": to_list("TITLE_EXCLUDE"),
    "description_exclude": to_list("DESCRIPTION_EXCLUDE"),
    "title_must_include": to_list("TITLE_MUST_INCLUDE"),
    "description_must_include": to_list("DESCRIPTION_MUST_INCLUDE"),
    "title_first_word_include": os.getenv("TITLE_FIRST_WORD_INCLUDE", None),
    "title_first_word_exclude": os.getenv("TITLE_FIRST_WORD_EXCLUDE", None)
}

with open("args.json", "w") as f:
    json.dump([args_data], f, indent=4)

print("✅ Archivos de configuración generados.")

# --- 2. PARCHE QUIRÚRGICO DE CÓDIGO (Evita el Error 400) ---
try:
    worker_path = "managers/worker.py"
    with open(worker_path, "r") as f:
        content = f.read()

    # Buscamos la línea de la URL que da problemas
    old_url_part = '&language=es_ES&distance_in_km={item.max_distance}&condition={item.condition}'
    
    # La sustituimos por una lógica que no envía 'condition' si es None y asegura distancia
    new_url_part = '&language=es_ES&distance_in_km={item.max_distance if item.max_distance else 2000}"'
    new_url_part += ' + (f"&condition={item.condition}" if item.condition and str(item.condition) != "None" else "") + f"'

    # Aplicamos el cambio si no se ha aplicado ya
    if old_url_part in content:
        content = content.replace(old_url_part, new_url_part)
        with open(worker_path, "w") as f:
            f.write(content)
        print("✅ Parche de URL aplicado con éxito.")
    else:
        print("⚠️ El parche ya estaba aplicado o no se encontró la línea.")
except Exception as e:
    print(f"❌ Error aplicando el parche: {e}")
