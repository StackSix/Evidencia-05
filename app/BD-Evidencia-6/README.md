# BD – Evidencia 6: SmartHome

Este directorio contiene el script SQL de la Evidencia 6 y las instrucciones para ejecutarlo en un DBMS online (recomendado **MySQL 8**).

## Archivos

- `ev6_smarthome.sql`  
  Script **todo en uno** con:
  - **DDL**: creación de tablas (usuarios, rol, permiso, domicilios, tipo_habitacion, tipos_dispositivos, dispositivos, automatizaciones) y relaciones (incluye tablas puente `rol_permiso` y `usuarios_domicilios`).
  - **DML**: inserción de datos iniciales (≥10 inserts por tabla).
  - **Consultas de verificación** (SELECT simples).
  - **Consultas multitabla (JOINs)** y **subconsultas** justificadas por el negocio (p. ej., automatizaciones por usuario, cámaras por hogar, usuarios con múltiples hogares, habitaciones con cámaras, etc.).

## Motor (DBMS)

- **MySQL 8.x**.  
  Probado en:
  - OneCompiler (modo MySQL)
  - MySQL Workbench (local)
  - Clever Cloud (MySQL 8 gestionado)

> **Nota:** SQL tiene pequeñas variaciones entre motores. Este script está escrito para **MySQL 8**.

---

## Ejecución en DBMS online

### Opción A: OneCompiler (recomendado)
1. Abrir OneCompiler y elegir **MySQL** como lenguaje.
2. Copiar **todo** el contenido de `ev6_smarthome.sql` en el editor.
3. Hacer clic en **Run**.
4. Verificar los resultados en la consola de salida:
   - Debes ver que se crean las tablas sin errores.
   - Las consultas finales deberían devolver:
     - `total_usuarios` = **10**
     - `total_dispositivos` = **10**
     - `total_automatizaciones` = **10**
   - Y filas con las consultas multitabla/subconsultas.

**Si el entorno no permite `CREATE DATABASE` o `USE`**: el script ya viene preparado **sin** `CREATE DATABASE`. No hace falta crear esquema. Si ves errores de permisos, borra cualquier línea `USE ...;` que tengas agregada manualmente.

### Opción B: runsql.com (o similar)
1. Crear un **snippet** de MySQL.
2. Pegar **todo** el contenido de `ev6_smarthome.sql`.
3. Ejecutar y revisar los resultados como en OneCompiler.

---

## Ejecución local (MySQL Workbench)

1. Conectarse a tu servidor local o gestionado (p.ej. Clever Cloud).
2. Crear un **schema vacío** si es necesario (opcional):
   ```sql
   -- SOLO si tienes permisos y quieres aislar el esquema
   CREATE DATABASE smarthome_ev6 CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
   USE smarthome_ev6;