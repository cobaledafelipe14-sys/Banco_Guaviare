from database import cargar_datos, guardar_datos
from cuentas import obtener_cuentas_cliente, generar_numero_cuenta

def listar_clientes():
    datos = cargar_datos()
    clientes = datos.get("clientes", [])
    cuentas = datos.get("cuentas", [])
    
    print("\n" + "="*60)
    print("                LISTADO GENERAL DE CLIENTES")
    print("="*60)
    
    if not clientes:
        print("No hay clientes registrados en el sistema.")
        return

    for c in clientes:
        cid = c.get("id")
        cuentas_cli = obtener_cuentas_cliente(cid, cuentas)
        
        print(f"\n👤 ID: {cid} | {c.get('nombres')} {c.get('apellidos', '')}")
        print(f"   Documento: {c.get('tipo_documento', 'CC')} - {c.get('cedula')}")
        print(f"   Email: {c.get('email', 'N/A')}")
        print(f"   Total de Cuentas: {len(cuentas_cli)}")
        
        if cuentas_cli:
            print("   --- Cuentas asociadas ---")
            for cta in cuentas_cli:
                print(f"     • [{cta.get('tipo_cuenta')}] No: {cta.get('numero_cuenta')} | Saldo: ${cta.get('saldo', 0):,}")
        else:
            print("   ⚠️  Sin cuentas asociadas registradas.")
        print("-" * 60)

def buscar_cliente():
    datos = cargar_datos()
    criterio = input("\nIngrese el número de documento o ID del cliente a buscar: ").strip()
    
    cliente = next(
        (c for c in datos.get("clientes", []) 
         if str(c.get("cedula")) == criterio or str(c.get("id")) == criterio), 
        None
    )
    
    if cliente:
        cuentas_cli = obtener_cuentas_cliente(cliente.get("id"), datos.get("cuentas", []))
        print("\n" + "="*50)
        print("              DETALLE DEL CLIENTE")
        print("="*50)
        print(f"ID Cliente: {cliente.get('id')}")
        print(f"Nombre: {cliente.get('nombres')} {cliente.get('apellidos', '')}")
        print(f"Documento: {cliente.get('tipo_documento', 'CC')} {cliente.get('cedula')}")
        print(f"Email: {cliente.get('email', 'N/A')}")
        print(f"\nCuentas registradas ({len(cuentas_cli)}):")
        
        if cuentas_cli:
            for cta in cuentas_cli:
                print(f" • Tipo: {cta.get('tipo_cuenta')} | No: {cta.get('numero_cuenta')} | Saldo: ${cta.get('saldo', 0):,}")
        else:
            print(" • El cliente no tiene cuentas activas.")
        print("="*50)
    else:
        print("\n❌ No se encontró ningún cliente con ese documento o ID.")

def crear_cliente():
    datos = cargar_datos()
    print("\n" + "="*50)
    print("          REGISTRO DE NUEVO CLIENTE Y CUENTA")
    print("="*50)
    
    cedula = input("Número de documento: ").strip()
    
    if any(str(c.get("cedula")) == cedula for c in datos.get("clientes", [])):
        print("\n❌ Error: Ya existe un cliente registrado con esa cédula.")
        return

    tipo_doc = input("Tipo de documento (CC/TI/CE/PASAPORTE): ").strip().upper()
    nombres = input("Nombres: ").strip()
    apellidos = input("Apellidos: ").strip()
    email = input("Correo electrónico: ").strip()
    
    nuevo_id = max([c.get("id", 0) for c in datos.get("clientes", [])], default=0) + 1
    
    nuevo_cliente = {
        "id": nuevo_id,
        "cedula": cedula,
        "tipo_documento": tipo_doc,
        "nombres": nombres,
        "apellidos": apellidos,
        "email": email
    }
    
    print("\n--- SELECCIONE TIPO DE CUENTA A APERTURAR ---")
    print("1. Solo Cuenta de Ahorros")
    print("2. Solo Cuenta Corriente")
    print("3. Ambas Cuentas (Ahorros y Corriente)")
    
    opcion_cuenta = input("Seleccione opción (1, 2 o 3): ").strip()
    
    cuentas_a_crear = []
    if opcion_cuenta == "1":
        cuentas_a_crear.append("AHORROS")
    elif opcion_cuenta == "2":
        cuentas_a_crear.append("CORRIENTE")
    elif opcion_cuenta == "3":
        cuentas_a_crear = ["AHORROS", "CORRIENTE"]
    else:
        print("\n⚠️ Opción no válida. Se creará el cliente pero SIN cuentas asociadas.")

    nuevas_cuentas = []
    for tipo in cuentas_a_crear:
        while True:
            try:
                saldo_str = input(f"Ingrese saldo inicial para la cuenta de {tipo} ($): ").strip()
                saldo = float(saldo_str)
                if saldo < 0:
                    print("El saldo inicial no puede ser negativo.")
                    continue
                break
            except ValueError:
                print("Por favor, ingrese un monto numérico válido.")

        num_cta = generar_numero_cuenta(tipo)
        
        cuenta_obj = {
            "id": max([c.get("id", 0) for c in datos.get("cuentas", [])], default=0) + len(nuevas_cuentas) + 1,
            "numero_cuenta": num_cta,
            "cliente_id": nuevo_id,
            "tipo_cuenta": tipo,
            "saldo": saldo
        }
        nuevas_cuentas.append(cuenta_obj)

    datos["clientes"].append(nuevo_cliente)
    datos["cuentas"].extend(nuevas_cuentas)
    guardar_datos(datos)
    
    print(f"\n✅ Cliente '{nombres} {apellidos}' creado exitosamente.")
    if nuevas_cuentas:
        print("  Cuentas aperturadas con éxito:")
        for cta in nuevas_cuentas:
            print(f"  • {cta['tipo_cuenta']} - No: {cta['numero_cuenta']} | Saldo Inicial: ${cta['saldo']:,}")

def eliminar_cliente():
    datos = cargar_datos()
    criterio = input("\nIngrese el número de documento o ID del cliente a eliminar: ").strip()
    
    cliente = next(
        (c for c in datos.get("clientes", []) 
         if str(c.get("cedula")) == criterio or str(c.get("id")) == criterio), 
        None
    )
    
    if not cliente:
        print("\n❌ No se encontró ningún cliente con ese documento o ID.")
        return

    cid = cliente.get("id")
    cuentas_cli = obtener_cuentas_cliente(cid, datos.get("cuentas", []))
    
    print("\n" + "⚠️  " * 8 + " ATENCIÓN " + "⚠️  " * 8)
    print(f"Cliente a eliminar: {cliente.get('nombres')} {cliente.get('apellidos', '')}")
    print(f"Documento: {cliente.get('tipo_documento', 'CC')} {cliente.get('cedula')}")
    print(f"Cuentas asociadas que se eliminarán ({len(cuentas_cli)}):")
    for cta in cuentas_cli:
        print(f"  • {cta.get('tipo_cuenta')} No: {cta.get('numero_cuenta')} (Saldo: ${cta.get('saldo', 0):,})")
    
    confirmacion = input("\n¿Está seguro de eliminar este cliente y TODAS sus cuentas? (S/N): ").strip().lower()
    
    if confirmacion == 's':
        datos["clientes"] = [c for c in datos["clientes"] if str(c.get("id")) != str(cid)]
        datos["cuentas"] = [c for c in datos["cuentas"] if str(c.get("cliente_id")) != str(cid)]
        guardar_datos(datos)
        print("\n✅ Cliente y sus cuentas asociadas han sido eliminados con éxito.")
    else:
        print("\n❌ Operación cancelada. No se realizaron cambios.")