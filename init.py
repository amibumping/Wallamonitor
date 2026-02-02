import os
import yaml
import json

print("--- 🛠️ CONFIGURANDO PERSISTENCIA Y TELEGRAM ---")

# 1. Generar config.yaml
token = os.getenv("TELEGRAM_TOKEN", "").strip().replace('"', '').replace("'", "")
channel = os.getenv("TELEGRAM_CHANNEL_ID", "").strip().replace('"', '').replace("'", "")
config_data = {"telegram_token": str(token), "telegram_channel": str(channel)}
with open("config.yaml", "w") as f:
    yaml.dump(config_data, f, default_flow_style=False)

# 2. Generar args.json si no existe
if not os.path.exists("args.json") or os.path.getsize("args.json") < 10:
    # (Mantenemos la lógica de generación que ya teníamos)
    args_data = [{"search_query": os.getenv("SEARCH_QUERY", "laptop"), "latitude": os.getenv("LATITUDE", "40.4167"), "longitude": os.getenv("LONGITUDE", "-3.7033"), "max_distance": os.getenv("MAX_DISTANCE", "0"), "condition": os.getenv("CONDITION", "all"), "min_price": os.getenv("MIN_PRICE", "0"), "max_price": os.getenv("MAX_PRICE", "9999")}]
    with open("args.json", "w") as f:
        json.dump(args_data, f, indent=4)

# 3. INYECTAR PERSISTENCIA EN EL BOT (Parche de Worker.py)
# Esto hará que el bot lea/escriba en 'vistos.txt'
worker_path = "managers/worker.py"
if os.path.exists(worker_path):
    with open(worker_path, "r") as f:
        content = f.read()
    
    # Solo parcheamos si no está ya parcheado
    if "vistos.txt" not in content:
        # Añadimos la lógica de guardado
        insertion = """
    def is_visto(self, item_id):
        if not os.path.exists('vistos.txt'): return False
        with open('vistos.txt', 'r') as f:
            return item_id in f.read()

    def save_visto(self, item_id):
        with open('vistos.txt', 'a') as f:
            f.write(item_id + '\\n')
"""
        # Insertamos el código y modificamos la lógica de envío
        content = "import os\nimport time\n" + content
        content = content.replace("class Worker:", "class Worker:" + insertion)
        
        # Modificamos el bucle que envía los anuncios para que compruebe si ya se envió
        # Buscamos donde el bot decide enviar el mensaje (suele ser un if o for)
        content = content.replace(
            "self.telegram_manager.send_message(article)",
            "if not self.is_visto(article.id):\n                time.sleep(1)\n                self.telegram_manager.send_message(article)\n                self.save_visto(article.id)"
        )
        
        with open(worker_path, "w") as f:
            f.write(content)
        print("✅ Persistencia inyectada con éxito en worker.py")
else:
    print("❌ No se encontró managers/worker.py")

print("--- 🏁 CONFIGURACIÓN FINALIZADA ---")
