import json
import random
from datetime import datetime, timedelta

def migrar_y_poblar_datos():
    # 1. Cargar datos actuales
    try:
        with open("banco.json", "r", encoding="utf-8") as f:
            datos = json.load(f)
    except FileNotFoundError:
        print("❌ No se encontró el archivo 'banco.json'. Asegúrate de ejecutar el script en la carpeta raíz del proyecto.")
        return

    clientes = datos.get("clientes", [])
    cuentas = datos.get("cuentas", [])

    if not clientes or not cuentas:
        print("⚠️ No hay suficientes clientes o cuentas en 'banco.json'.")
        return

    # Guardar copia de seguridad por seguridad
    with open("banco_backup.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    print("📦 Copia de seguridad creada como 'banco_backup.json'.")

    # 2. Reestructurar números de cuenta al nuevo formato (C-A-XXX / C-C-XXX)
    cont_ahorros = 1
    cont_corriente = 1

    for cta in cuentas:
        tipo = cta.get("tipo_cuenta")
        if tipo == "AHORROS":
            cta["numero_cuenta"] = f"C-A-{cont_ahorros:03d}"
            cont_ahorros += 1
        else:
            cta["numero_cuenta"] = f"C-C-{cont_corriente:03d}"
            cont_corriente += 1

    todas_las_cuentas = [c["numero_cuenta"] for c in cuentas]

    def fecha_aleatoria():
        inicio = datetime(2026, 1, 1)
        fin = datetime(2026, 7, 27)
        delta = fin - inicio
        segundos_aleatorios = random.randint(0, int(delta.total_seconds()))
        return (inicio + timedelta(seconds=segundos_aleatorios)).strftime("%Y-%m-%d %H:%M:%S")

    transacciones = []

    # 3. Generar 10 consignaciones, 10 retiros y 10 transferencias POR CADA CLIENTE
    for cliente in clientes:
        cid = cliente.get("id")
        cuentas_cliente = [c["numero_cuenta"] for c in cuentas if str(c.get("cliente_id")) == str(cid)]
        
        if not cuentas_cliente:
            continue

        # 10 Consignaciones para este cliente
        for _ in range(10):
            cta = random.choice(cuentas_cliente)
            monto = random.randint(5, 50) * 10000  # $50,000 a $500,000
            transacciones.append({
                "id": 0,
                "tipo": "CONSIGNACION",
                "cuenta_origen": cta,
                "cuenta_destino": None,
                "monto": monto,
                "fecha": fecha_aleatoria()
            })

        # 10 Retiros para este cliente
        for _ in range(10):
            cta = random.choice(cuentas_cliente)
            monto = random.randint(2, 20) * 10000  # $20,000 a $200,000
            transacciones.append({
                "id": 0,
                "tipo": "RETIRO",
                "cuenta_origen": cta,
                "cuenta_destino": None,
                "monto": monto,
                "fecha": fecha_aleatoria()
            })

        # 10 Transferencias enviadas desde las cuentas de este cliente hacia otras cuentas del banco
        for _ in range(10):
            origen = random.choice(cuentas_cliente)
            otras_cuentas = [c for c in todas_las_cuentas if c != origen]
            destino = random.choice(otras_cuentas) if otras_cuentas else origen
            monto = random.randint(3, 30) * 10000  # $30,000 a $300,000
            transacciones.append({
                "id": 0,
                "tipo": "TRANSFERENCIA",
                "cuenta_origen": origen,
                "cuenta_destino": destino,
                "monto": monto,
                "fecha": fecha_aleatoria()
            })

    # Ordenar todas las transacciones de forma cronológica
    transacciones.sort(key=lambda x: x["fecha"])
    
    # Asignar IDs numéricos secuenciales
    for index, tx in enumerate(transacciones, start=1):
        tx["id"] = index

    datos["transacciones"] = transacciones

    # 4. Guardar datos en banco.json
    with open("banco.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

    print("\n✅ ¡Población masiva de historial completada!")
    print(f"   • Clientes procesados: {len(clientes)}")
    print(f"   • Movimientos por cliente: 10 consignaciones + 10 retiros + 10 transferencias = 30 por cliente")
    print(f"   • Total de transacciones generadas en banco.json: {len(transacciones)}")

if __name__ == "__main__":
    migrar_y_poblar_datos()