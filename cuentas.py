import random
from database import cargar_datos, guardar_datos

def generar_numero_cuenta(tipo_cuenta):
    datos = cargar_datos()
    prefijo = "C-A-" if tipo_cuenta == "AHORROS" else "C-C-"
    
    cuentas = datos.get("cuentas", [])
    numeros = []
    
    # Buscar cuentas existentes que tengan el mismo prefijo para calcular el consecutivo
    for c in cuentas:
        num = str(c.get("numero_cuenta", ""))
        if num.startswith(prefijo):
            try:
                consecutivo = int(num.replace(prefijo, ""))
                numeros.append(consecutivo)
            except ValueError:
                pass
    
    siguiente_numero = max(numeros, default=0) + 1
    # Genera el formato C-A-001, C-A-002, etc. (se ajusta automáticamente si pasa de 999)
    return f"{prefijo}{siguiente_numero:03d}"

def obtener_cuentas_cliente(cliente_id, cuentas):
    return [c for c in cuentas if str(c.get("cliente_id")) == str(cliente_id)]

def ver_cuentas():
    datos = cargar_datos()
    cuentas = datos.get("cuentas", [])
    clientes = {c.get("id"): f"{c.get('nombres')} {c.get('apellidos', '')}" for c in datos.get("clientes", [])}
    
    if not cuentas:
        print("\nNo hay cuentas registradas en el sistema.")
        return

    print("\n" + "="*50)
    print("         CONSULTA DE CUENTAS BANCARIAS")
    print("="*50)
    print("1. Ver TODAS las cuentas (organizadas por tipo)")
    print("2. Ver únicamente Cuentas de AHORROS")
    print("3. Ver únicamente Cuentas CORRIENTES")
    
    opc = input("Seleccione una opción (1-3): ").strip()
    
    ahorros = [c for c in cuentas if c.get("tipo_cuenta") == "AHORROS"]
    corrientes = [c for c in cuentas if c.get("tipo_cuenta") == "CORRIENTE"]

    if opc == "1":
        _imprimir_bloque_cuentas("CUENTAS DE AHORROS", ahorros, clientes)
        _imprimir_bloque_cuentas("CUENTAS CORRIENTES", corrientes, clientes)
    elif opc == "2":
        _imprimir_bloque_cuentas("CUENTAS DE AHORROS", ahorros, clientes)
    elif opc == "3":
        _imprimir_bloque_cuentas("CUENTAS CORRIENTES", corrientes, clientes)
    else:
        print("\n❌ Opción no válida.")

def _imprimir_bloque_cuentas(titulo, lista, clientes_dict):
    print("\n" + "-"*50)
    print(f" {titulo} (Total: {len(lista)})")
    print("-" * 50)
    if not lista:
        print(" No existen cuentas en esta categoría.")
        return
    
    for cta in lista:
        titular = clientes_dict.get(cta.get("cliente_id"), "Titular Desconocido")
        print(f"• No. Cuenta: {cta.get('numero_cuenta')} | Titular: {titular}")
        print(f"  Saldo actual: ${cta.get('saldo', 0):,} | Cliente ID: {cta.get('cliente_id')}")
        print("-" * 35)

def eliminar_cuenta():
    datos = cargar_datos()
    num_cuenta = input("\nIngrese el número de cuenta a eliminar: ").strip()
    
    cuenta = next((c for c in datos.get("cuentas", []) if str(c.get("numero_cuenta")) == num_cuenta), None)
    
    if not cuenta:
        print("\n❌ No se encontró ninguna cuenta con ese número.")
        return

    titular = next((c for c in datos.get("clientes", []) if str(c.get("id")) == str(cuenta.get("cliente_id"))), None)
    nombre_titular = f"{titular.get('nombres')} {titular.get('apellidos', '')}" if titular else "Desconocido"

    print("\n" + "⚠️  " * 8 + " ATENCIÓN " + "⚠️  " * 8)
    print("Cuenta bancaria a eliminar:")
    print(f"  • Número: {cuenta.get('numero_cuenta')}")
    print(f"  • Tipo: {cuenta.get('tipo_cuenta')}")
    print(f"  • Titular: {nombre_titular}")
    print(f"  • Saldo actual: ${cuenta.get('saldo', 0):,}")
    
    confirmacion = input("\n¿Está seguro de eliminar esta cuenta? (S/N): ").strip().lower()
    
    if confirmacion == 's':
        datos["cuentas"] = [c for c in datos["cuentas"] if str(c.get("numero_cuenta")) != num_cuenta]
        guardar_datos(datos)
        print("\n✅ La cuenta bancaria ha sido eliminada con éxito.")
    else:
        print("\n❌ Operación cancelada. No se realizaron cambios.")
        from database import cargar_datos, guardar_datos

def agregar_cuenta_a_cliente():
    datos = cargar_datos()
    print("\n" + "="*50)
    print("      CREAR NUEVA CUENTA A CLIENTE EXISTENTE")
    print("="*50)
    
    busqueda = input("Ingrese el ID o Documento del cliente: ").strip()
    if not busqueda:
        print("\n❌ Entrada no válida.")
        return

    # Buscar el cliente por ID o por documento
    cliente = None
    for c in datos.get("clientes", []):
        if str(c.get("id")) == busqueda or str(c.get("documento", "")).strip() == busqueda:
            cliente = c
            break

    if not cliente:
        print(f"\n❌ No se encontró ningún cliente con ID o Documento '{busqueda}'.")
        return

    cliente_id = cliente.get("id")
    nombre_cliente = cliente.get("nombre", "Cliente")

    # Obtener las cuentas que ya posee este cliente
    cuentas_cliente = [c for c in datos.get("cuentas", []) if str(c.get("cliente_id")) == str(cliente_id)]
    tipos_actuales = [c.get("tipo_cuenta") for c in cuentas_cliente]

    print(f"\n👤 Cliente: {nombre_cliente} (ID: {cliente_id})")
    print(f"💳 Cuentas actuales: {', '.join(tipos_actuales) if tipos_actuales else 'Ninguna'}")

    # Verificar cuáles tipos de cuenta le faltan por tener
    opciones_disponibles = {}
    if "AHORROS" not in tipos_actuales:
        opciones_disponibles["1"] = "AHORROS"
    if "CORRIENTE" not in tipos_actuales:
        opciones_disponibles["2"] = "CORRIENTE"

    # Si ya tiene ambas cuentas
    if not opciones_disponibles:
        print(f"\n⚠️ El cliente {nombre_cliente} ya tiene registradas ambas cuentas (AHORROS y CORRIENTE).")
        return

    print("\n¿Qué tipo de cuenta desea aperturar?")
    for clave, tipo in opciones_disponibles.items():
        print(f"  {clave}. Cuenta de {tipo}")

    eleccion = input("Seleccione una opción: ").strip()

    if eleccion not in opciones_disponibles:
        print("\n❌ Selección no válida o el cliente ya tiene ese tipo de cuenta.")
        return

    tipo_cuenta_seleccionado = opciones_disponibles[eleccion]

    # Pedir saldo inicial
    try:
        monto_inicial = float(input("\nIngrese el saldo inicial para esta cuenta ($): ").strip())
        if monto_inicial < 0:
            print("\n❌ El saldo inicial no puede ser negativo.")
            return
    except ValueError:
        print("\n❌ Valor de monto inválido.")
        return

    # Generar el nuevo número de cuenta con formato C-A-XXX o C-C-XXX
    nuevo_numero = generar_numero_cuenta(tipo_cuenta_seleccionado)

    nueva_cuenta = {
        "numero_cuenta": nuevo_numero,
        "cliente_id": cliente_id,
        "tipo_cuenta": tipo_cuenta_seleccionado,
        "saldo": monto_inicial
    }

    datos.setdefault("cuentas", []).append(nueva_cuenta)
    guardar_datos(datos)

    print(f"\n✅ ¡Cuenta creada exitosamente!")
    print(f"   • Titular: {nombre_cliente}")
    print(f"   • Tipo de cuenta: {tipo_cuenta_seleccionado}")
    print(f"   • Número asignado: {nuevo_numero}")
    print(f"   • Saldo inicial: ${monto_inicial:,.2f}")

def sub_menu_cuentas():
    while True:
        print("\n" + "="*50)
        print("          GESTIÓN DE CUENTAS")
        print("="*50)
        print("1. Abrir adicional a cliente existente")
        print("2. Consultar cuentas")
        print("3. Volver al menú principal")
        print("="*50)
        
        opc = input("Seleccione una opción: ").strip()
        
        if opc == "1":
            agregar_cuenta_a_cliente()
        elif opc == "2":
            # Tu función actual de consultar cuentas
            pass
        elif opc == "3":
            break
        else:
            print("\n❌ Opción inválida.")