import os
import yaml
import json
import re

# --- 1. GENERAR CONFIGURACIONES ---
token = os.getenv("TELEGRAM_TOKEN", "").strip().replace('"', '').replace("'", "")
channel = os.getenv("TELEGRAM_CHANNEL_ID", "").strip().replace('"', '').replace("'", "")
config_data = {"telegram_token": str(token), "telegram_channel": str(channel)}
with open("config.yaml", "w") as f:
    yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)

# --- 2. GENERAR ARGS.JSON ---
if not os.path.exists("args.json") or os.path.getsize("args.json") < 10:
    def to_list(env_var):
        val = os.getenv(env_var)
        if not val or val.strip() == "": return []
        try:
            parsed = json.loads(val)
            return parsed if isinstance(parsed, list) else [parsed]
        except: return [val]
    args_data = [{
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
    }]
    with open("args.json", "w") as f:
        json.dump(args_data, f, indent=4)

# --- 3. PARCHE INTELIGENTE DE RUTA DE BASE DE DATOS ---
# Buscamos en todas las carpetas el archivo que configure sqlite3
found_db_file = False
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            full_path = os.path.join(root, file)
            try:
                with open(full_path, "r") as f:
                    content = f.read()
                
                # Buscamos la línea que conecta a la base de datos
                if "sqlite3.connect(" in content:
                    # Forzamos una ruta única y absoluta en el contenedor
                    new_content = re.sub(r"sqlite3\.connect\(.*?\)", "sqlite3.connect('/app/wallapop_data.db')", content)
                    if new_content != content:
                        with open(full_path, "w") as f:
                            f.write(new_content)
                        print(f"✅ Parche aplicado en: {full_path} -> Ruta: /app/wallapop_data.db")
                        found_db_file = True
            except:
                continue

if not found_db_file:
    print("⚠️ No se encontró el archivo de conexión SQLite para parchear.")

print("✅ Todo listo.")
