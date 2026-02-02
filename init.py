import os
import yaml
import json
import re
import time

print("--- 🛠️ INICIANDO DIAGNÓSTICO Y CONFIGURACIÓN ---")

# 1. Mostrar qué archivos ve el contenedor (Para debug)
print("Archivos en el directorio actual:")
for root, dirs, files in os.walk('.'):
    level = root.replace('.', '').count(os.sep)
    indent = ' ' * 4 * (level)
    print(f"{indent}[{os.path.basename(root)}/]")
    subindent = ' ' * 4 * (level + 1)
    for f in files:
        if f.endswith('.py') or f.endswith('.db'):
            print(f"{subindent}{f}")

# 2. Generar config.yaml
token = os.getenv("TELEGRAM_TOKEN", "").strip().replace('"', '').replace("'", "")
channel = os.getenv("TELEGRAM_CHANNEL_ID", "").strip().replace('"', '').replace("'", "")
config_data = {"telegram_token": str(token), "telegram_channel": str(channel)}
with open("config.yaml", "w") as f:
    yaml.dump(config_data, f, default_flow_style=False)

# 3. Parche de Código: Base de Datos y Flood Control
found_db = False
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            try:
                with open(path, "r") as f:
                    content = f.read()
                
                original_content = content
                
                # A. Parche de Base de Datos (Ruta absoluta)
                # Buscamos sqlite3.connect con cualquier variante de espacios/comillas
                content = re.sub(r"sqlite3\.connect\(.*?\)", "sqlite3.connect('/app/database.db')", content)
                
                # B. Parche de Flood Control (Evitar bloqueo de Telegram)
                # Añadimos un pequeño delay de 1 seg entre mensajes para que no colapse
                if "self.telegram_manager.send_message" in content:
                    content = content.replace(
                        "self.telegram_manager.send_message",
                        "time.sleep(1); self.telegram_manager.send_message"
                    )
                    if "import time" not in content:
                        content = "import time\n" + content

                if content != original_content:
                    with open(path, "w") as f:
                        f.write(content)
                    print(f"✅ Archivo parcheado: {path}")
                    if "sqlite3" in original_content: found_db = True
            except:
                continue

if not found_db:
    print("⚠️ No se pudo parchear la conexión SQLite. Es posible que la ruta sea distinta.")

print("--- 🏁 FIN DEL DIAGNÓSTICO ---")
