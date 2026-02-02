import os
import yaml
import json
import re

print("--- 🛠️ CONFIGURANDO PERSISTENCIA AVANZADA ---")

# 1. Generar config.yaml
token = os.getenv("TELEGRAM_TOKEN", "").strip().replace('"', '').replace("'", "")
channel = os.getenv("TELEGRAM_CHANNEL_ID", "").strip().replace('"', '').replace("'", "")
config_data = {"telegram_token": str(token), "telegram_channel": str(channel)}
with open("config.yaml", "w") as f:
    yaml.dump(config_data, f, default_flow_style=False)

# 2. Parchear Worker.py
worker_path = "managers/worker.py"
if os.path.exists(worker_path):
    with open(worker_path, "r") as f:
        content = f.read()
    
    if "def is_visto" not in content:
        print("🔧 Inyectando lógica de persistencia en worker.py...")
        
        # Añadimos imports necesarios
        content = "import os\nimport time\n" + content
        
        # Inyectamos métodos de ayuda en la clase Worker
        persistence_methods = """
    def is_visto(self, item_id):
        if not os.path.exists('vistos.txt'): return False
        with open('vistos.txt', 'r') as f:
            return str(item_id) in f.read()

    def save_visto(self, item_id):
        try:
            with open('vistos.txt', 'a') as f:
                f.write(str(item_id) + '\\n')
        except: pass
"""
        content = re.sub(r"(class Worker:.*?\n)", r"\1" + persistence_methods, content, count=1, flags=re.S)
        
        # Parcheamos el envío de mensajes con seguridad (Try/Except)
        # Buscamos la llamada a send_message y la envolvemos
        pattern = r"(\s+)(self\.telegram_manager\.send_message\((.*?)\))"
        replacement = r"""
\1if not self.is_visto(\3.id):
\1    try:
\1        time.sleep(1.5)
\1        \2
\1        self.save_visto(\3.id)
\1    except Exception as e:
\1        print(f"⚠️ Error enviando \3.id: {e}")
"""
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            with open(worker_path, "w") as f:
                f.write(new_content)
            print("✅ worker.py parcheado con éxito.")
        else:
            print("❌ No se encontró la línea de envío de mensajes.")
else:
    print("❌ No se encontró managers/worker.py")

print("--- 🏁 CONFIGURACIÓN FINALIZADA ---")
