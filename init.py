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

# Generamos args.json asegurando tipos correctos
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

# --- 2. PARCHE QUIRÚRGICO MEJORADO ---
try:
    worker_path = "managers/worker.py"
    with open(worker_path, "r") as f:
        content = f.read()

    # Parche para la CONDICIÓN: Si es None o vacío, no se envía el parámetro
    # Buscamos la parte final de la f-string y la hacemos condicional
    bad_cond = '&condition={item.condition}"'
    good_cond = '{"&condition=" + str(item.condition) if item.condition and str(item.condition) != "None" else ""}"'
    
    # Parche para la DISTANCIA: Si es 0 o None, ponemos 2000 (España)
    bad_dist = 'distance_in_km={item.max_distance}'
    good_dist = 'distance_in_km={item.max_distance if item.max_distance else 2000}'

    if bad_cond in content or bad_dist in content:
        content = content.replace(bad_cond, good_cond)
        content = content.replace(bad_dist, good_dist)
        with open(worker_path, "w") as f:
            f.write(content)
        print("✅ Código del bot parcheado correctamente (URL optimizada).")
    else:
        # Si fallan los anteriores, hacemos un reemplazo directo de la línea de la URL
        print("⚠️ Buscando patrón alternativo...")
        new_content = content.replace('&condition={item.condition}', '{"&condition=" + str(item.condition) if item.condition and str(item.condition) != "None" else ""}')
        if new_content != content:
            with open(worker_path, "w") as f:
                f.write(new_content)
            print("✅ Parche aplicado mediante patrón alternativo.")
        else:
            print("❌ No se pudo encontrar la línea de la URL para parchear.")

except Exception as e:
    print(f"❌ Error crítico en el parcheo: {e}")
