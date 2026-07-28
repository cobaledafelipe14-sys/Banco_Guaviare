from clientes import listar_clientes, buscar_cliente, crear_cliente, eliminar_cliente
from cuentas import ver_cuentas, eliminar_cuenta, agregar_cuenta_a_cliente
from transacciones import sub_menu_transacciones

def sub_menu_cuentas():
    while True:
        print("\n" + "="*50)
        print("          GESTIÓN DE CUENTAS BANCARIAS")
        print("="*50)
        print("1. Ver cuentas bancarias (Ahorros / Corriente)")
        print("2. Abrir cuenta adicional a cliente existente")
        print("3. Volver al menú principal")
        print("="*50)
        
        opc = input("Seleccione una opción (1-3): ").strip()
        
        if opc == "1":
            ver_cuentas()
        elif opc == "2":
            agregar_cuenta_a_cliente()
        elif opc == "3":
            break
        else:
            print("\n❌ Opción no válida.")

def sub_menu_eliminar():
    print("\n" + "="*50)
    print("          MÓDULO DE ELIMINACIÓN DE DATOS")
    print("="*50)
    print("1. Eliminar un cliente (y sus cuentas asociadas)")
    print("2. Eliminar únicamente una cuenta bancaria")
    print("3. Volver al menú principal")
    print("="*50)
    
    opc = input("Seleccione una opción (1-3): ").strip()
    
    if opc == "1":
        eliminar_cliente()
    elif opc == "2":
        eliminar_cuenta()
    elif opc == "3":
        return
    else:
        print("\n❌ Opción no válida.")

def menu():
    while True:
        print("\n" + "="*50)
        print("     SISTEMA BANCARIO - BANCO GUAVIARE (CLI)")
        print("="*50)
        print("1. Listar todos los clientes (con sus cuentas)")
        print("2. Buscar cliente por documento o ID")
        print("3. Registrar nuevo cliente y aperturar cuenta(s)")
        print("4. Gestión de Cuentas (Ver / Abrir adicional)")
        print("5. Realizar transacciones (Consignar, Retirar, Transferir, Historial)")
        print("6. Eliminar cliente o cuenta bancaria")
        print("7. Salir")
        print("="*50)
        
        opcion = input("Seleccione una opción (1-7): ").strip()
        
        if opcion == "1":
            listar_clientes()
        elif opcion == "2":
            buscar_cliente()
        elif opcion == "3":
            crear_cliente()
        elif opcion == "4":
            sub_menu_cuentas()
        elif opcion == "5":
            sub_menu_transacciones()
        elif opcion == "6":
            sub_menu_eliminar()
        elif opcion == "7":
            print("\n¡Gracias por utilizar el sistema del Banco Guaviare! Hasta luego.\n")
            break
        else:
            print("\n❌ Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    menu()