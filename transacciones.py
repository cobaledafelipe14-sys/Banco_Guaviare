from datetime import datetime
from database import cargar_datos, guardar_datos

def normalizar_cuenta(num_str):
    """Elimina guiones, espacios y convierte a mayúsculas para hacer búsquedas flexibles."""
    if not num_str:
        return ""
    return str(num_str).replace("-", "").strip().upper()

def buscar_cuenta_por_numero(num_ingresado, cuentas):
    """Busca una cuenta ignorando mayúsculas, minúsculas y guiones."""
    num_norm = normalizar_cuenta(num_ingresado)
    for c in cuentas:
        if normalizar_cuenta(c.get("numero_cuenta", "")) == num_norm:
            return c
    return None

def consignar():
    datos = cargar_datos()
    print("\n--- CONSIGNACIÓN EN CUENTA ---")
    num_cuenta = input("Ingrese el número de cuenta: ").strip()
    
    cuenta = buscar_cuenta_por_numero(num_cuenta, datos.get("cuentas", []))
    
    if not cuenta:
        print("\n❌ No se encontró la cuenta especificada.")
        return

    try:
        monto = float(input("Ingrese el valor a consignar ($): ").strip())
        if monto <= 0:
            print("\n❌ El monto a consignar debe ser mayor a cero.")
            return
    except ValueError:
        print("\n❌ Valor inválido.")
        return

    cuenta["saldo"] = cuenta.get("saldo", 0) + monto
    num_real = cuenta.get("numero_cuenta")
    
    nueva_tx = {
        "id": max([t.get("id", 0) for t in datos.get("transacciones", [])], default=0) + 1,
        "tipo": "CONSIGNACION",
        "cuenta_origen": num_real,
        "cuenta_destino": None,
        "monto": monto,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    datos.setdefault("transacciones", []).append(nueva_tx)
    guardar_datos(datos)
    
    print(f"\n✅ Consignación realizada con éxito.")
    print(f"   Nuevo saldo en la cuenta {num_real}: ${cuenta['saldo']:,}")

def retirar():
    datos = cargar_datos()
    print("\n--- RETIRO DE CUENTA ---")
    num_cuenta = input("Ingrese el número de cuenta: ").strip()
    
    cuenta = buscar_cuenta_por_numero(num_cuenta, datos.get("cuentas", []))
    
    if not cuenta:
        print("\n❌ No se encontró la cuenta especificada.")
        return

    try:
        monto = float(input("Ingrese el valor a retirar ($): ").strip())
        if monto <= 0:
            print("\n❌ El monto a retirar debe ser mayor a cero.")
            return
    except ValueError:
        print("\n❌ Valor inválido.")
        return

    if cuenta.get("saldo", 0) < monto:
        print(f"\n❌ Saldo insuficiente. Saldo actual disponible: ${cuenta.get('saldo', 0):,}")
        return

    cuenta["saldo"] -= monto
    num_real = cuenta.get("numero_cuenta")
    
    nueva_tx = {
        "id": max([t.get("id", 0) for t in datos.get("transacciones", [])], default=0) + 1,
        "tipo": "RETIRO",
        "cuenta_origen": num_real,
        "cuenta_destino": None,
        "monto": monto,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    datos.setdefault("transacciones", []).append(nueva_tx)
    guardar_datos(datos)
    
    print(f"\n✅ Retiro realizado con éxito.")
    print(f"   Nuevo saldo disponible en la cuenta {num_real}: ${cuenta['saldo']:,}")

def transferir():
    datos = cargar_datos()
    print("\n--- TRANSFERENCIA ENTRE CUENTAS ---")
    origen_num = input("Ingrese número de cuenta de ORIGEN: ").strip()
    
    cuenta_origen = buscar_cuenta_por_numero(origen_num, datos.get("cuentas", []))
    if not cuenta_origen:
        print("\n❌ La cuenta de origen no existe.")
        return

    destino_num = input("Ingrese número de cuenta de DESTINO: ").strip()
    if normalizar_cuenta(origen_num) == normalizar_cuenta(destino_num):
        print("\n❌ La cuenta de origen y destino no pueden ser la misma.")
        return

    cuenta_destino = buscar_cuenta_por_numero(destino_num, datos.get("cuentas", []))
    if not cuenta_destino:
        print("\n❌ La cuenta de destino no existe.")
        return

    try:
        monto = float(input("Ingrese el monto a transferir ($): ").strip())
        if monto <= 0:
            print("\n❌ El monto a transferir debe ser mayor a cero.")
            return
    except ValueError:
        print("\n❌ Valor inválido.")
        return

    if cuenta_origen.get("saldo", 0) < monto:
        print(f"\n❌ Saldo insuficiente en la cuenta de origen. Disponible: ${cuenta_origen.get('saldo', 0):,}")
        return

    cuenta_origen["saldo"] -= monto
    cuenta_destino["saldo"] = cuenta_destino.get("saldo", 0) + monto

    origen_real = cuenta_origen.get("numero_cuenta")
    destino_real = cuenta_destino.get("numero_cuenta")

    nueva_tx = {
        "id": max([t.get("id", 0) for t in datos.get("transacciones", [])], default=0) + 1,
        "tipo": "TRANSFERENCIA",
        "cuenta_origen": origen_real,
        "cuenta_destino": destino_real,
        "monto": monto,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    datos.setdefault("transacciones", []).append(nueva_tx)
    guardar_datos(datos)

    print(f"\n✅ Transferencia de ${monto:,} realizada exitosamente.")
    print(f"   Nuevo saldo origen ({origen_real}): ${cuenta_origen['saldo']:,}")
    print(f"   Nuevo saldo destino ({destino_real}): ${cuenta_destino['saldo']:,}")

def ver_historial_transacciones():
    datos = cargar_datos()
    num_ingresado = input("\nIngrese el número de cuenta para ver su historial: ").strip()
    num_norm = normalizar_cuenta(num_ingresado)
    
    if not num_norm:
        print("\n❌ Entrada no válida.")
        return

    cuenta_obj = buscar_cuenta_por_numero(num_ingresado, datos.get("cuentas", []))
    
    if not cuenta_obj:
        print(f"\n❌ No se encontró ninguna cuenta asociada a '{num_ingresado}'.")
        return

    num_real = cuenta_obj.get("numero_cuenta")

    # Filtrar ÚNICAMENTE las transacciones donde esta cuenta sea ORIGEN o DESTINO
    txs = [t for t in datos.get("transacciones", []) 
           if normalizar_cuenta(t.get("cuenta_origen")) == num_norm 
           or normalizar_cuenta(t.get("cuenta_destino")) == num_norm]

    print("\n" + "="*70)
    print(f"   HISTORIAL DE MOVIMIENTOS EXCLUSIVO DE LA CUENTA: {num_real}")
    print(f"   (Total de movimientos de esta cuenta: {len(txs)})")
    print("="*70)
    
    if not txs:
        print(" No hay movimientos registrados para esta cuenta.")
        return

    for t in txs:
        tipo = t.get("tipo")
        monto = t.get("monto", 0)
        fecha = t.get("fecha", "N/A")
        origen = t.get("cuenta_origen")
        destino = t.get("cuenta_destino")
        
        if tipo == "CONSIGNACION":
            print(f" [🟢 CONSIGNACIÓN]  Cuenta: {num_real} | Fecha: {fecha} | Monto: +${monto:,}")
        elif tipo == "RETIRO":
            print(f" [🔴 RETIRO]        Cuenta: {num_real} | Fecha: {fecha} | Monto: -${monto:,}")
        elif tipo == "TRANSFERENCIA":
            # Si C-C-004 fue el ORIGEN (envió dinero)
            if normalizar_cuenta(origen) == num_norm:
                print(f" [💸 TRANSF. ENVIADA]   De: {num_real} ➡️ Hacia: {destino} | Fecha: {fecha} | Monto: -${monto:,}")
            # Si C-C-004 fue el DESTINO (recibió dinero)
            else:
                print(f" [💰 TRANSF. RECIBIDA] De: {origen} ➡️ Hacia: {num_real} | Fecha: {fecha} | Monto: +${monto:,}")
        print("-" * 70)

def sub_menu_transacciones():
    print("\n" + "="*50)
    print("      MÓDULO DE TRANSACCIONES BANCARIAS")
    print("="*50)
    print("1. Realizar Consignación (Depósito)")
    print("2. Realizar Retiro")
    print("3. Realizar Transferencia")
    print("4. Consultar Historial de Movimientos de una cuenta")
    print("5. Volver al menú principal")
    print("="*50)
    
    opc = input("Seleccione una opción (1-5): ").strip()
    
    if opc == "1":
        consignar()
    elif opc == "2":
        retirar()
    elif opc == "3":
        transferir()
    elif opc == "4":
        ver_historial_transacciones()
    elif opc == "5":
        return
    else:
        print("\n❌ Opción no válida.")