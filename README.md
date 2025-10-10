# Evidencia 6 - SmartHome

## Propósito
Desarrollar una aplicación de consola para la gestión de un sistema **Smart Home**, incorporando el patrón de diseño **DAO** para separar la lógica de dominio del acceso a datos y permitiendo la interacción directa con una base de datos.

## Contexto
Este repositorio continúa el trabajo iniciado en evidencias anteriores para la asignatura **Programación I**. Se parte de las clases de dominio implementadas previamente y se amplía con una capa de acceso a datos, scripts SQL y un programa principal que habilita el registro, autenticación y administración de dispositivos.

## Alcance
- Implementación del patrón DAO para usuarios, roles y dispositivos.
- Creación de un menú de consola (`app/main.py`) que soporta:
  - Registro de usuarios estándar.
  - Inicio de sesión con verificación de contraseña.
  - Menú específico para usuarios estándar (consulta de datos personales y dispositivos asignados).
  - Menú de administración para usuarios con rol **admin** (CRUD de dispositivos y cambio de rol de usuarios).
- Conexión a una base de datos SQLite embebida para facilitar la ejecución local, manteniendo la estructura compatible con los scripts MySQL entregados.
- Scripts SQL con las consultas solicitadas en la carpeta `base-de-datos/BD-Evidencia-6`.

## Autores
- Equipo de Programación I - Comisión 2024.

## Estructura del repositorio
```
app/
 ├── conn/               # Conexión y configuración de la base de datos
 ├── dao/                # Implementaciones DAO
 ├── dominio/            # Clases de dominio
 ├── main.py             # Programa de consola
base-de-datos/
 └── BD-Evidencia-6/     # Scripts SQL y documentación de la base de datos
```

## Requisitos previos
- Python 3.10+
- Dependencias definidas en `requirements.txt` (`pip install -r requirements.txt`)

## Ejecución
```bash
python -m app.main
```
Al ejecutar el programa por primera vez se inicializa la base de datos y se crea un usuario administrador por defecto:
- Email: `admin@smarthome.local`
- Contraseña: `admin123`

Desde el menú principal se puede registrar un usuario estándar, iniciar sesión y acceder a las distintas funcionalidades según el rol.

## Scripts de base de datos
En `base-de-datos/BD-Evidencia-6` se incluyen:
- `Consultas-DDL.sql`: definición del modelo relacional.
- `Consultas-DML.sql`: inserción de datos iniciales y consultas (simples, multitabla y subconsultas).
- `README.md`: instrucciones para ejecutar los scripts en un DBMS online compatible.

## Pruebas
Las pruebas unitarias de evidencias anteriores se mantienen sin modificaciones. Tras instalar los requisitos, pueden ejecutarse mediante:
```bash
pytest
```
