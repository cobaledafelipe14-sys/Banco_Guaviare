import json
import os
from datetime import datetime
from enum import Enum
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI(
    title="Sistema Bancario Backend (JSON) - Guaviare",
    version="2.0",
    description="API REST con persistencia modular en JSON",
)

ARCH_JSON = "banco.json"


# --- ENUMERACIONES (Datos Reales) ---
class TipoDocumento(str, Enum):
    CC = "CC"
    CE = "CE"
    PASAPORTE = "PASAPORTE"


class TipoCuenta(str, Enum):
    AHORROS = "AHORROS"
    CORRIENTE = "CORRIENTE"


# --- MODELOS PYDANTIC ---
class ClienteCreate(BaseModel):
    tipo_documento: TipoDocumento
    cedula: str
    nombres: str
    apellidos: str
    email: EmailStr
    telefono: str


class CuentaCreate(BaseModel):
    cliente_id: int
    tipo_cuenta: TipoCuenta
    saldo_inicial: float


class TransaccionSimple(BaseModel):
    numero_cuenta: str
    monto: float


class TransferenciaCreate(BaseModel):
    cuenta_origen: str
    cuenta_destino: str
    monto: float
    concepto: Optional[str] = "Transferencia entre cuentas"


# --- PERSISTENCIA Y MANEJO DE JSON ---
def cargar_datos():
    if not os.path.exists(ARCH_JSON):
        datos_base = {
            "clientes": [],
            "cuentas": [],
            "transacciones": {
                "consignaciones": [],
                "retiros": [],
                "transferencias": [],
            },
        }
        guardar_datos(datos_base)
        return datos_base

    with open(ARCH_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_datos(datos):
    with open(ARCH_JSON, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


# ==========================================
# DEV 1: CLIENTES Y CUENTAS
# ==========================================


@app.post("/clientes", tags=["Dev 1 - Clientes"])
def registrar_cliente(cliente: ClienteCreate):
    datos = cargar_datos()

    # Validar que la cédula no esté duplicada
    for c in datos["clientes"]:
        if c["cedula"] == cliente.cedula:
            raise HTTPException(
                status_code=400, detail="El cliente con esta cédula ya existe."
            )

    nuevo_id = len(datos["clientes"]) + 1
    nuevo_cliente = {
        "id": nuevo_id,
        "tipo_documento": cliente.tipo_documento,
        "cedula": cliente.cedula,
        "nombres": cliente.nombres,
        "apellidos": cliente.apellidos,
        "email": cliente.email,
        "telefono": cliente.telefono,
        "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    datos["clientes"].append(nuevo_cliente)
    guardar_datos(datos)
    return {
        "mensaje": "Cliente registrado exitosamente",
        "cliente": nuevo_cliente,
    }


@app.post("/cuentas", tags=["Dev 1 - Cuentas"])
def crear_cuenta(cuenta: CuentaCreate):
    datos = cargar_datos()

    # Validar que el cliente exista por su ID interno
    cliente_existe = any(c["id"] == cuenta.cliente_id for c in datos["clientes"])
    if not cliente_existe:
        raise HTTPException(
            status_code=404, detail="El cliente especificado no existe."
        )

    num_cuenta = f"CTA-{40000 + len(datos['cuentas']) + 1}"
    nueva_cuenta = {
        "numero_cuenta": num_cuenta,
        "cliente_id": cuenta.cliente_id,
        "tipo_cuenta": cuenta.tipo_cuenta,
        "saldo": cuenta.saldo_inicial,
        "estado": "ACTIVA",
        "fecha_apertura": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    datos["cuentas"].append(nueva_cuenta)
    guardar_datos(datos)
    return {"mensaje": "Cuenta creada exitosamente", "cuenta": nueva_cuenta}


@app.get("/cuentas/{numero_cuenta}/saldo", tags=["Dev 1 - Cuentas"])
def consultar_saldo(numero_cuenta: str):
    datos = cargar_datos()
    for c in datos["cuentas"]:
        if c["numero_cuenta"] == numero_cuenta:
            return {
                "numero_cuenta": c["numero_cuenta"],
                "tipo_cuenta": c["tipo_cuenta"],
                "saldo_actual": c["saldo"],
                "estado": c["estado"],
            }
    raise HTTPException(status_code=404, detail="Cuenta no encontrada.")


# ==========================================
# DEV 2: TRANSACCIONES DIVIDIDAS
# ==========================================


@app.post("/transacciones/consignar", tags=["Dev 2 - Transacciones"])
def consignar(transaccion: TransaccionSimple):
    datos = cargar_datos()
    cuenta = next(
        (c for c in datos["cuentas"] if c["numero_cuenta"] == transaccion.numero_cuenta),
        None,
    )

    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada.")

    cuenta["saldo"] += transaccion.monto

    registro = {
        "id": f"CNS-{len(datos['transacciones']['consignaciones']) + 1:03d}",
        "numero_cuenta": transaccion.numero_cuenta,
        "monto": transaccion.monto,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    datos["transacciones"]["consignaciones"].append(registro)
    guardar_datos(datos)
    return {
        "mensaje": "Consignación exitosa",
        "nuevo_saldo": cuenta["saldo"],
        "comprobante": registro,
    }


@app.post("/transacciones/retirar", tags=["Dev 2 - Transacciones"])
def retirar(transaccion: TransaccionSimple):
    datos = cargar_datos()
    cuenta = next(
        (c for c in datos["cuentas"] if c["numero_cuenta"] == transaccion.numero_cuenta),
        None,
    )

    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada.")

    if cuenta["saldo"] < transaccion.monto:
        raise HTTPException(
            status_code=400, detail="Saldo insuficiente para realizar el retiro."
        )

    cuenta["saldo"] -= transaccion.monto

    registro = {
        "id": f"RET-{len(datos['transacciones']['retiros']) + 1:03d}",
        "numero_cuenta": transaccion.numero_cuenta,
        "monto": transaccion.monto,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    datos["transacciones"]["retiros"].append(registro)
    guardar_datos(datos)
    return {
        "mensaje": "Retiro exitoso",
        "nuevo_saldo": cuenta["saldo"],
        "comprobante": registro,
    }


@app.post("/transacciones/transferir", tags=["Dev 2 - Transacciones"])
def transferir(transferencia: TransferenciaCreate):
    datos = cargar_datos()

    origen = next(
        (c for c in datos["cuentas"] if c["numero_cuenta"] == transferencia.cuenta_origen),
        None,
    )
    destino = next(
        (c for c in datos["cuentas"] if c["numero_cuenta"] == transferencia.cuenta_destino),
        None,
    )

    if not origen or not destino:
        raise HTTPException(
            status_code=404, detail="Una o ambas cuentas no existen."
        )

    if origen["saldo"] < transferencia.monto:
        raise HTTPException(
            status_code=400, detail="Saldo insuficiente en la cuenta origen."
        )

    origen["saldo"] -= transferencia.monto
    destino["saldo"] += transferencia.monto

    registro = {
        "id": f"TRF-{len(datos['transacciones']['transferencias']) + 1:03d}",
        "cuenta_origen": transferencia.cuenta_origen,
        "cuenta_destino": transferencia.cuenta_destino,
        "monto": transferencia.monto,
        "concepto": transferencia.concepto,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    datos["transacciones"]["transferencias"].append(registro)
    guardar_datos(datos)
    return {
        "mensaje": "Transferencia realizada con éxito",
        "comprobante": registro,
    }