# BD-Evidencia-5

Este proyecto contiene los scripts **DDL** y **DML** para crear e inicializar la base de datos del sistema **SmartHome**.  
Los scripts fueron diseñados y probados en **MySQL 8** utilizando la plataforma online [OneCompiler](https://onecompiler.com/mysql).
## 🧪 Cómo ejecutar los scripts

## 📂 Archivos entregados

- `BD_Evidencia-5` → Contiene **ddl_mysql.sql** (creación de tablas con relaciones y restricciones) y **dml_mysql** (inserción de datos iniciales + consultas de verificación). Tambien dejamos listo el archivo para correr en OneCompiler - MySQL **DBMS_online.sql**
- `README.md` → Este archivo con instrucciones de uso.


## 🛠️ Cómo ejecutar los scripts

1. Abrir [OneCompiler - MySQL](https://onecompiler.com/mysql).
2. Copiar y pegar el contenido completo de `bd_smarthome.sql` en el editor.
3. Ejecutar con el botón **Run ▶️**.
4. El script:
   - Elimina tablas previas si existen.
   - Crea las tablas:  
     - `usuario`  
     - `email`  
     - `dispositivos`  
     - `camara`  
     - `evento_dispositivo`
   - Inserta datos iniciales (**≥ 30 registros entre todas las tablas**).
   - Ejecuta consultas de verificación (`SELECT`) y un **JOIN** de control para revisar relaciones.

---

## 🔎 Consultas de verificación incluidas

- Listado de usuarios con su rol y fecha de creación.
- Listado de emails asociados.
- Listado de dispositivos por usuario.
- Listado de cámaras con modo de grabación y estado de automatización.
- Listado de eventos por cámara, ordenados por fecha.
- Consulta `JOIN` para ver usuarios con sus dispositivos y cámaras.

---

## ⚠️ Notas importantes

- El script usa funciones de **MySQL 8** como:
  - `ENUM` para tipos restringidos (`rol`, `estado_dispositivo`, `evento`, etc.).
  - `BOOLEAN` (alias de `TINYINT(1)` en MySQL).
  - `AUTO_INCREMENT` en claves primarias.
  - `NOW() - INTERVAL ...` para generar fechas relativas.
- En algunos entornos online:
  - Si no se permiten **FOREIGN_KEY_CHECKS**, comentar las líneas `SET FOREIGN_KEY_CHECKS = ...`.
  - Si se produce error por `DROP TABLE`, asegúrese de ejecutar el script completo en limpio.

---

## ✅ DBMS elegido

- **DBMS:** MySQL 8  
- **Plataforma recomendada:** [OneCompiler MySQL](https://onecompiler.com/mysql)  
- **Motivo:** la sintaxis utilizada (`ENUM`, `AUTO_INCREMENT`, `INTERVAL`) es nativa de MySQL.
