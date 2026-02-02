import os
import yaml
import json

# --- 1. GENERAR CONFIG.YAML ---
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

# --- 3. PARCHE DE BASE DE DATOS (FORZAR RUTA ABSOLUTA) ---
try:
    db_script_path = "datalayer/database.py"
    with open(db_script_path, "r") as f:
        content = f.read()
    
    # Forzamos al bot a usar siempre /app/database.db
    if "sqlite3.connect('database.db')" in content:
        content = content.replace("sqlite3.connect('database.db')", "sqlite3.connect('/app/database.db')")
        with open(db_script_path, "w") as f:
            f.write(content)
        print("✅ Parche de base de datos aplicado (Ruta absoluta: /app/database.db)")
except Exception as e:
    print(f"❌ Error aplicando parche de DB: {e}")

print("✅ Todo listo.")
