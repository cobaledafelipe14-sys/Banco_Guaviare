# 🏦 Sistema Bancario CLI - Banco Guaviare

> **Proyecto Colaborativo de Desarrollo de Software**  
> *Consola interactiva en Python para la gestión integral de clientes, cuentas, transacciones financieras y migración de datos con persistencia JSON.*

---

##  Tabla de Contenidos

1. [Descripción del Proyecto](#-descripción-del-proyecto)
2. [Arquitectura y Estructura del Código](#-arquitectura-y-estructura-del-código)
3. [Funcionalidades Principales del Sistema](#-funcionalidades-principales-del-sistema)
4. [Requisitos Técnicos e Instalación](#-requisitos-técnicos-e-instalación)
5. [Guía de Ejecución y Pruebas](#-guía-de-ejecución-y-pruebas)
6. [Estrategia de Ramificación (Git Flow)](#-estrategia-de-ramificación-git-flow)
7. [Distribución de Trabajo y Módulos por Aprendiz](#-distribución-de-trabajo-y-módulos-por-aprendiz)
8. [Historial Detallado de Commits por Integrante](#-historial-detallado-de-commits-por-integrante)
9. [Persistencia de Datos y Búsqueda Inteligente](#-persistencia-de-datos-y-búsqueda-inteligente)
10. [Autores y Créditos](#-autores-y-créditos)

---

##  Descripción del Proyecto

El **Sistema Bancario Banco Guaviare** es una aplicación desarrollada en lenguaje **Python** que opera bajo la interfaz de línea de comandos (CLI). Su propósito principal es simular la operatividad central de una entidad bancaria, integrando módulos de administración de usuarios, lógica contable para cuentas de ahorros y corrientes, procesamiento seguro de transacciones y un motor de normalización de búsquedas.

El sistema garantiza persistencia de datos local mediante el estándar **JSON** y ha sido construido bajo los estándares del desarrollo modular, facilitando el mantenimiento, la escalabilidad y la colaboración mediante control de versiones con **Git y GitHub**.



## Arquitectura y Estructura del Código

El proyecto fue diseñado aplicando el principio de **separación de responsabilidades**, dividiendo la lógica de negocio en módulos independientes:

```text
banco-guaviare/
│
├──  main.py                 # Punto de entrada principal y menú interactivo CLI
├──  database.py             # Capa de persistencia: lectura y escritura en banco.json
├──  clientes.py             # Módulo de administración de clientes (CRUD)
├──  cuentas.py              # Módulo de lógica de cuentas (Prefijos C-A / C-C)
├──  transacciones.py        # Módulo financiero (consignaciones, retiros, transferencias)
├──  actualizar_datos.py     # Script de migración, estandarización y población masiva
├──  banco.json              # Base de datos persistente del sistema
├──  .gitignore              # Archivo para exclusión de archivos temporales y backups
└──  README.md               # Documentación general e instrucciones del repositorio

 Funcionalidades Principales del Sistema
 
  Módulo de ClientesRegistro de Clientes: Alta de nuevos usuarios solicitando documento de identidad, nombres completos, teléfono y correo electrónico.
  Consulta General: Listado en consola de todos los clientes registrados en la base de datos.
  Búsqueda Flexible: Búsqueda por documento o ID sin importar la presencia de espacios o caracteres especiales.
  Eliminación Segura: Submenú asistido para la baja de clientes y sus cuentas asociadas. 
  Módulo de Cuentas 
  Estructura Estandarizada de Cuentas:Cuentas de Ahorros: Prefijo secuencial C-A-XXX (ej. C-A-001).Cuentas Corrientes: Prefijo secuencial C-C-XXX (ej. C-C-002).Multi-cuenta por Cliente: Posibilidad de aperturar cuentas adicionales a un cliente existente sin duplicar tipos de cuenta no permitidos.
  Generación Automática: Consecutivo dinámico que analiza la base de datos previa para evitar colisiones numéricas.  
  Módulo Financiero y TransaccionesConsignaciones (Depósitos): Incremento de saldo con registro explícito de fecha y detalle.Retiros: Débito de fondos con validación automática de fondos suficientes.
  Transferencias Interbancarias: Débito en cuenta origen y crédito en cuenta destino en una sola operación atómica.Historial Trazable: Registro exhaustivo de más de 10 consignaciones, retiros y transferencias por cuenta con timestamp de auditoría.
   Requisitos Técnicos e Instalación Prerrequisitos Python 3.8+ instalado globalmente o en entorno virtual.
   Git Clone para la clonación y gestión de versiones.Instalación: Clonar el repositorio: Bashgit clone [https://github.com/cobaledafelipe14-sys/TU_REPOSITORIO.git](https://github.com/cobaledafelipe14-sys/TU_REPOSITORIO.git)
 cd TU_REPOSITORIO
Verificar estructura de archivos:Asegúrate de contar con los módulos .py y el archivo banco.json en el directorio raíz.
Guía de Ejecución y Pruebas1. Inicialización o Migración de Datos (Opcional)Si deseas estructurar legacy data o repoblar el archivo banco.json con historial de pruebas completo (más de 10 transacciones por cliente), ejecuta:Bashpython actualizar_datos.py
Ejecutar la Aplicación PrincipalPara iniciar la interfaz interactiva en consola:Bashpython main.py
Estrategia de Ramificación (Git Flow)Para mantener la integridad del código y facilitar el desarrollo simultáneo entre los dos aprendices, se adoptó la estrategia Feature Branch Workflow:Plaintext       [feature/registro-clientes] ──────┐
       [feature/creacion-cuentas-saldo] ──┼──> [develop] ──> [main]
       [feature/consignaciones-retiros] ──┤
       [feature/transferencias] ────────┘
 Distribución de Trabajo y Módulos por AprendizEl proyecto se distribuyó de manera equitativa entre los dos desarrolladores integrando conceptos de arquitectura de software y desarrollo colaborativo:
  Aprendiz 1: Felipe Cobaleda (cobaledafelipe14-sys)Rol: Arquitecto de Base de Datos y Módulo de Cuentas / Transferencias.
  Módulos bajo su responsabilidad:database.py: Estructuración del motor JSON y lectura/escritura de archivos.cuentas.py: Diseño del generador secuencial de prefijos C-A-XXX y C-C-XXX.transacciones.py: Lógica de transferencias de fondos entre cuentas y balance de saldos.Integration & Submenus: Integración del menú de cuentas adicionales (sub_menu_cuentas).
  Ramas administradas: main, feature/creacion-cuentas-saldo, feature/transferencias. 
  Aprendiz 2: Yarlon RochaRol: Desarrollador Módulo de Clientes, Normalización y Scripting de Migración.
  Módulos bajo su responsabilidad:clientes.py: Lógica de registro, búsqueda e interfaz del submenú de eliminación (sub_menu_eliminar).actualizar_datos.py: Desarrollo del script de migración masiva para simulación de historiales contables.Motor de Normalización: Algoritmo de compatibilidad case-insensitive y dash-agnostic para búsquedas (c-a001 ➔ C-A-001).transacciones.py: Lógica básica de retiros, consignaciones y control de sobregiros.
  Ramas administradas: develop, feature/registro-clientes, feature/consignaciones-retiros.

Historial Detallado de Commits por IntegranteFecha / FichaIntegranteRamaMensaje del Commit / Aporte RealizadoFase 1Felipe Cobaledamaindocs: commit inicial y estructura del proyectoFase 1Felipe Cobaledafeature/creacion-cuentas-saldofeat: arquitectura base de banco.json y modulo database.pyFase 2Yarlon Rochafeature/registro-clientesfeat: creacion de clientes.py y registro de usuarios con IDFase 2Yarlon Rochafeature/registro-clientesfeat: implementacion de sub_menu_eliminar para clientesFase 3Felipe Cobaledafeature/creacion-cuentas-saldofeat: generacion secuencial C-A-XXX y C-C-XXX en cuentas.pyFase 3Yarlon Rochafeature/consignaciones-retirosfeat: modulo transacciones.py con consignaciones y validacion de retiroFase 4Felipe Cobaledafeature/transferenciasfeat: logica de transferencias entre cuentas y balance dobleFase 4Yarlon Rochadevelopfix: normalizacion de busquedas tolerancia a mayusculas y guionesFase 5Yarlon Rochadevelopfeat: script actualizar_datos.py para carga masiva de transaccionesFase 5Felipe Cobaledamainfeat: integracion final de submenus y ejecucion fluida en main.pyCierreFelipe Cobaleda & Yarlon Rochamaindocs: documentacion final del proyecto y manual README.md

Persistencia de Datos y Búsqueda Inteligente Estructura del Archivo JSON (banco.json)El archivo almacena la información estructurada bajo el siguiente esquema relacional en JSON:JSON{
  "clientes": [
    {
      "id": "1001",
      "nombre": "Carlos Mendoza",
      "cuentas": [
        {
          "numero": "C-A-001",
          "tipo": "Ahorros",
          "saldo": 1500000.0,
          "historial": [
            {
              "tipo": "consignacion",
              "monto": 500000.0,
              "fecha": "2026-07-28 10:30:00"
            }
          ]
        }
      ]
    }
  ]
}
Normalización de BúsquedasEl sistema incorpora un motor de búsqueda tolerante a variaciones de entrada de usuario. Permite procesar las entradas sin fallos de lectura:PlaintextEntrada Usuario: "c-a001"   ──┐
Entrada Usuario: "C-A-001"  ──┼──> [ Algoritmo Normalizador ] ──> "C-A-001" (Match Exitoso)
Entrada Usuario: "ca001"    ──┘
 Autores y CréditosEste proyecto fue desarrollado por los aprendices del programa de formación en Análisis y Desarrollo de Software:Felipe Cobaleda - Desarrollador / Lógica de Cuentas, Persistencia y Transferencias - GitHub: @cobaledafelipe14-sysYarlon Rocha - Desarrollador / Gestión de Clientes, Normalización y Migración de DatosBanco Guaviare - Proyecto Académico CLI Python
