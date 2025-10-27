# Base de datos evidencia 05

Este proyecto contiene los scripts necesarios para crear e inicializar la base de datos smarthome, correspondiente al ABP SmartHome.
Los scripts están diseñados para MySQL 8 y se han probado en la plataforma en línea OneCompile

## Archivos incluidos

- ddl_mysql.sql – Define las tablas del modelo con sus claves primarias, foráneas y restricciones de integridad para MySQL.

- dml_mysql.sql – Inserta datos de ejemplo y ejecuta consultas de modificación y selección para verificar el estado de la base.

- DBMS_online.sql – Script integral listo para ejecutarse en OneCompiler: elimina las tablas existentes, crea el esquema completo, inserta los datos de ejemplo y lanza varias consultas de verificación.

- Diagrama de clases.pdf – En este caso dejamos el correspondiente a la EV5, el de referencia de esta base de datos esta en BD-Evidencia-6)

- README.md – Este archivo con las instrucciones de uso.


También puedes ejecutar los scripts de forma manual: primero ddl_mysql.sql para crear el esquema de tablas y después dml_mysql.sql para poblar los datos y ejecutar las consultas de prueba.
## Cómo ejecutar los scripts

Accede a OneCompiler – MySQL



```bash
Copia y pega el contenido de DBMS_online.sql en el editor (o súbelo, si la plataforma lo permite).

Ejecuta el script con el botón Run ▶️.

El script realizará las siguientes acciones:

Desactivará temporalmente las comprobaciones de claves foráneas (FOREIGN_KEY_CHECKS) y eliminará las tablas existentes, si las hubiera.

Creará las tablas de la base de datos smarthome_ev6 (o smarthome_ev5 según el nombre definido en tu DDL):
```

### Tablas creadas

- rol

- gestor_usuario

- usuario

- gestor_domicilio

- domicilio

- gestor_dispositivo

- tipos_dispositivos

- dispositivo

- gestor_automatizacion

- automatizaciones

Insertará datos de ejemplo para poblar cada tabla (más de 30 registros en total).

Ejecutará consultas de verificación para comprobar la integridad del modelo y el correcto funcionamiento de las relaciones.

    
## Consultas de verificación incluidas

Consultas de verificación incluidas

Al final de DBMS_online.sql se ejecutan varias consultas de prueba, entre ellas:

- SHOW TABLES para listar las tablas creadas.

- DESCRIBE para obtener la estructura de las tablas usuario, domicilio, dispositivo y automatizaciones.

- Recuperación de los primeros cinco usuarios ordenados por id_usuario.

- Actualización de la contraseña y del correo electrónico del usuario con id_usuario = 1.

- Selección del nombre y del tipo de los dispositivos asociados al usuario con id_usuario = 1 mediante una consulta con JOIN.

- Lista de automatizaciones cuyo hora_encendido es mayor o igual a 15:00.

Estas consultas sirven para validar que las relaciones y restricciones definidas en el esquema funcionan correctamente.


## ⚠️ Notas importantes

Todas las tablas utilizan ENGINE=InnoDB para soportar integridad referencial y transacciones.

Las claves primarias son autoincrementales (AUTO_INCREMENT).

El tipo BOOLEAN se define como un alias de TINYINT(1) en MySQL.

Los scripts presuponen un entorno MySQL 8 sin necesidad de crear bases de datos adicionales; OneCompiler utiliza una base por defecto para cada ejecución.

Si la plataforma arroja errores relacionados con SET FOREIGN_KEY_CHECKS, se pueden comentar temporalmente dichas líneas.

## Base de datos y plataforma

Sistema gestor: MySQL 8

Plataforma recomendada: OneCompiler – MySQL: [onecompiler.com](https://onecompiler.com/)

- Justificación: las instrucciones utilizadas (AUTO_INCREMENT, tipos BOOLEAN, columnas de hora y manejadores de claves foráneas) son nativas de MySQL 8 y la plataforma permite ejecutar el script de forma sencilla y reproducible.