import json
import os

ARCHIVO_JSON = "banco.json"

def cargar_datos():
    if not os.path.exists(ARCHIVO_JSON):
        datos_base = {"clientes": [], "cuentas": [], "transacciones": []}
        guardar_datos(datos_base)
        return datos_base
    
    with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"clientes": [], "cuentas": [], "transacciones": []}

def guardar_datos(datos):
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)