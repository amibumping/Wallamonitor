import os
import yaml
import json
import re

print("--- 🛠️ CONFIGURANDO PERSISTENCIA (VERSIÓN ROBUSTA) ---")

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
        print("🔧 Inyectando lógica en worker.py...")
        
        # Añadimos imports al inicio
        content = "import os\nimport time\n" + content
        
        # Inyectamos métodos de persistencia justo después de la definición de la clase
        persistence_code = """
    def is_visto(self, item_id):
        if not os.path.exists('vistos.txt'): return False
        try:
            with open('vistos.txt', 'r') as f:
                return str(item_id) in f.read()
        except: return False

    def save_visto(self, item_id):
        try:
            with open('vistos.txt', 'a') as f:
                f.write(str(item_id) + '\\n')
        except: pass
"""
        content = re.sub(r"(class Worker.*?:\n)", r"\1" + persistence_code, content, count=1)

        # BUSCADOR FLEXIBLE: Buscamos cualquier línea que contenga 'send_message('
        # y la reemplazamos por el bloque seguro.
        lines = content.splitlines()
        new_lines = []
        for line in lines:
            if "send_message(" in line and "def" not in line:
                indent = line[:line.find("self")]
                # Extraemos el nombre de la variable (ej: article o item)
                var_match = re.search(r"send_message\((.*?)\)", line)
                if var_match:
                    var_name = var_match.group(1)
                    new_lines.append(f"{indent}if not self.is_visto({var_name}.id):")
                    new_lines.append(f"{indent}    try:")
                    new_lines.append(f"{indent}        time.sleep(1.5)")
                    new_lines.append(f"{indent}        {line.strip()}")
                    new_lines.append(f"{indent}        self.save_visto({var_name}.id)")
                    new_lines.append(f"{indent}    except Exception as e:")
                    new_lines.append(f"{indent}        print(f'⚠️ Error en envío: {{e}}')")
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        content = "\n".join(new_lines)
        with open(worker_path, "w") as f:
            f.write(content)
        print("✅ worker.py parcheado con éxito (Buscador Flexible).")
else:
    print("❌ No se encontró managers/worker.py")

print("--- 🏁 FIN DE CONFIGURACIÓN ---")
