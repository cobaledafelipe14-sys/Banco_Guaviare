# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
from datetime import datetime

app = FastAPI(
    title="Sistema Bancario Backend (JSON) - San José del Guaviare",
    description="API para gestión bancaria persistiendo datos en un archivo banco.json",
    version="1.0"
)

DB_FILE = "banco.json"

# --- FUNCIONES DE LECTURA Y ESCRITURA EN JSON ---
def cargar_datos():
    if not os.path.exists(DB_FILE):
        estructura_inicial = {"clientes": [], "cuentas": [], "transacciones": []}
        guardar_datos(estructura_inicial)
        return estructura_inicial
    
    with open(DB_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {"clientes": [], "cuentas": [], "transacciones": []}

def guardar_datos(datos):
    with open(DB_FILE, "w", encoding="utf-8") as file:
        json.dump(datos, file, indent=4, ensure_ascii=False)


# --- MODELOS DE DATOS (PYDANTIC) ---
class ClienteCreate(BaseModel):
    cedula: str
    nombre: str
    email: str

class CuentaCreate(BaseModel):
    cliente_id: int
    saldo_inicial: float = 0.0

class Operacion(BaseModel):
    numero_cuenta: str
    monto: float

class Transferencia(BaseModel):
    cuenta_origen: str
    cuenta_destino: str
    monto: float


# ==========================================
# MÓDULO DEV 1: CLIENTES, CUENTAS Y SALDOS
# ==========================================

@app.post("/clientes", tags=["Dev 1 - Clientes"])
def registrar_cliente(cliente: ClienteCreate):
    datos = cargar_datos()
    for c in datos["clientes"]:
        if c["cedula"] == cliente.cedula:
            raise HTTPException(status_code=400, detail="La cédula ya se encuentra registrada.")
    
    nuevo_id = len(datos["clientes"]) + 1
    nuevo_cliente = {
        "id": nuevo_id,
        "cedula": cliente.cedula,
        "nombre": cliente.nombre,
        "email": cliente.email
    }
    
    datos["clientes"].append(nuevo_cliente)
    guardar_datos(datos)
    return {"mensaje": "Cliente registrado exitosamente", "cliente": nuevo_cliente}

@app.post("/cuentas", tags=["Dev 1 - Cuentas"])
def crear_cuenta(cuenta: CuentaCreate):
    datos = cargar_datos()
    cliente_existe = any(c["id"] == cuenta.cliente_id for c in datos["clientes"])
    if not cliente_existe:
        raise HTTPException(status_code=404, detail="El cliente especificado no existe.")
    
    num_cuenta = f"CTA-{len(datos['cuentas']) + 1001}"
    nueva_cuenta = {
        "numero_cuenta": num_cuenta,
        "cliente_id": cuenta.cliente_id,
        "saldo": cuenta.saldo_inicial
    }
    
    datos["cuentas"].append(nueva_cuenta)
    guardar_datos(datos)
    return {"mensaje": "Cuenta creada con éxito", "cuenta": nueva_cuenta}

@app.get("/cuentas/{numero_cuenta}/saldo", tags=["Dev 1 - Cuentas"])
def consultar_saldo(numero_cuenta: str):
    datos = cargar_datos()
    cuenta = next((c for c in datos["cuentas"] if c["numero_cuenta"] == numero_cuenta), None)
    
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada.")
    return {"numero_cuenta": cuenta["numero_cuenta"], "saldo_actual": cuenta["saldo"]}


# ==========================================
# MÓDULO DEV 2: TRANSACCIONES
# ==========================================

@app.post("/transacciones/consignar", tags=["Dev 2 - Transacciones"])
def consignar(op: Operacion):
    if op.monto <= 0:
        raise HTTPException(status_code=400, detail="El monto debe ser mayor a 0.")
    
    datos = cargar_datos()
    cuenta = next((c for c in datos["cuentas"] if c["numero_cuenta"] == op.numero_cuenta), None)
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada.")
    
    cuenta["saldo"] += op.monto
    
    transaccion = {
        "id": len(datos["transacciones"]) + 1,
        "tipo": "CONSIGNACION",
        "cuenta_origen": op.numero_cuenta,
        "cuenta_destino": None,
        "monto": op.monto,
        "fecha": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    }
    datos["transacciones"].append(transaccion)
    guardar_datos(datos)
    
    return {"mensaje": "Consignación exitosa", "nuevo_saldo": cuenta["saldo"]}

@app.post("/transacciones/retirar", tags=["Dev 2 - Transacciones"])
def retirar(op: Operacion):
    if op.monto <= 0:
        raise HTTPException(status_code=400, detail="El monto debe ser mayor a 0.")
    
    datos = cargar_datos()
    cuenta = next((c for c in datos["cuentas"] if c["numero_cuenta"] == op.numero_cuenta), None)
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada.")
    
    if cuenta["saldo"] < op.monto:
        raise HTTPException(status_code=400, detail="Saldo insuficiente para realizar el retiro.")
    
    cuenta["saldo"] -= op.monto
    
    transaccion = {
        "id": len(datos["transacciones"]) + 1,
        "tipo": "RETIRO",
        "cuenta_origen": op.numero_cuenta,
        "cuenta_destino": None,
        "monto": op.monto,
        "fecha": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    }
    datos["transacciones"].append(transaccion)
    guardar_datos(datos)
    
    return {"mensaje": "Retiro exitoso", "nuevo_saldo": cuenta["saldo"]}

@app.post("/transacciones/transferir", tags=["Dev 2 - Transacciones"])
def transferir(trans: Transferencia):
    if trans.monto <= 0:
        raise HTTPException(status_code=400, detail="El monto debe ser mayor a 0.")
    if trans.cuenta_origen == trans.cuenta_destino:
        raise HTTPException(status_code=400, detail="La cuenta de origen y destino deben ser diferentes.")
    
    datos = cargar_datos()
    origen = next((c for c in datos["cuentas"] if c["numero_cuenta"] == trans.cuenta_origen), None)
    destino = next((c for c in datos["cuentas"] if c["numero_cuenta"] == trans.cuenta_destino), None)
    
    if not origen or not destino:
        raise HTTPException(status_code=404, detail="Una o ambas cuentas no existen.")
    
    if origen["saldo"] < trans.monto:
        raise HTTPException(status_code=400, detail="Saldo insuficiente en la cuenta de origen.")
    
    origen["saldo"] -= trans.monto
    destino["saldo"] += trans.monto
    
    transaccion = {
        "id": len(datos["transacciones"]) + 1,
        "tipo": "TRANSFERENCIA",
        "cuenta_origen": trans.cuenta_origen,
        "cuenta_destino": trans.cuenta_destino,
        "monto": trans.monto,
        "fecha": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    }
    datos["transacciones"].append(transaccion)
    guardar_datos(datos)
    
    return {"mensaje": "Transferencia realizada con éxito", "monto": trans.monto}