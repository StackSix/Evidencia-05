# Base de datos evidencia 06

Este proyecto contiene el script necesario para crear, inicializar y verificar la base de datos **smarthome_ev6**, correspondiente a la **Evidencia 6** del sistema **SmartHome**. El script está diseñado para **MySQL 8** y se ha probado en la plataforma en línea **OneCompiler**.

---

## 📂 Archivos incluidos

- **DBMS_online_ev6.sql** – Script listo para ejecutar en onecompiler, crea y carga la base de datos para la evidencia 6 del sistema SmartHome, además de consultas multitabla de verificación.

- **Consultas-DML.sql** – Conjunto de consultas adicionales sobre los datos ya cargados para pruebas y verificaciones específicas solicitadas en la evidencia 06.

- **Diagrama de clases.pdf** – Referencia visual del modelo de clases utilizado para rediseñar la base de datos, tambien se usa como referencia para el diagrama de clases de la evidencia-05. Representa las relaciones y cardinalidades que dieron origen al modelo relacional.

- **README-ev6.md** – Este archivo con las instrucciones de uso y ejecución del proyecto.

---

## 🚀 Cómo ejecutar el script

### Accede a OneCompiler – MySQL

1. Abre tu navegador y entra a [OneCompiler](https://onecompiler.com/mysql).  
2. Selecciona el lenguaje **MySQL (versión 8)**.  
3. Borra cualquier código que aparezca por defecto en el editor.  
4. Copia y pega el contenido del archivo **DBMS_online_ev6.sql** en el editor.  
5. Ejecuta el script con el botón **Run ▶️**.

> 💡 No es necesario crear una base de datos específica: OneCompiler utiliza una base temporal propia para cada ejecución.

Al finalizar, en la consola de resultados se mostrarán las consultas de verificación y los datos cargados.  
Podés además ejecutar consultas adicionales sobre las tablas creadas.

---

## 🧱 ¿Qué hace el script?

El script se encuentra organizado en varias secciones:

1. **Desactivación de comprobaciones y limpieza**  
   - Desactiva temporalmente las `FOREIGN_KEY_CHECKS`.  
   - Elimina las tablas existentes para evitar conflictos de claves foráneas o duplicaciones.  

2. **Creación de tablas (DDL)**  
   - Define las tablas con sus **claves primarias, campos, restricciones y relaciones (FOREIGN KEY)**.  
   - Todas las tablas utilizan el motor **InnoDB**, que mantiene la **integridad referencial** y soporta **transacciones**.  

3. **Carga de datos (DML)**  
   - Inserta datos iniciales en el siguiente orden lógico para respetar dependencias:  
     1. `rol`  
     2. `usuario`  
     3. `domicilio`  
     4. `tipos_dispositivos`  
     5. `dispositivo`  
     6. `automatizaciones`  

4. **Consultas de verificación y multitabla**  
   - Ejecuta consultas que permiten comprobar la correcta estructura y relaciones entre las tablas:  
     - `SHOW TABLES` para listar todas las tablas creadas.  
     - `DESCRIBE` sobre las tablas principales (`usuario`, `dispositivo`, `automatizaciones`, `domicilio`).  
     - Consultas `SELECT` para listar los primeros registros de cada tabla.  
     - `UPDATE` para modificar valores de prueba (como email o contraseña de un usuario).  
     - Consultas con `JOIN` que relacionan usuarios, domicilios y dispositivos, por ejemplo:  
       - Mostrar todos los dispositivos con su usuario asociado.  
       - Contar el número de dispositivos y automatizaciones por usuario.  
       - Obtener el dispositivo más reciente de cada usuario.  
       - Listar las automatizaciones con detalle del domicilio y usuario correspondiente.

---

### 📋 Tablas creadas

| Tabla | Descripción |
|--------|-------------|
| **rol** | Contiene los los roles (administrador y usuario) del sistema. |
| **usuario** | Registra los datos principales de cada usuario del sistema. |
| **domicilio** | Guarda información de las direcciones y hogares asociados a los usuarios. |
| **tipos_dispositivos** | Define las categorías o tipos de dispositivos inteligentes. |
| **dispositivo** | Almacena los dispositivos registrados, vinculados a usuarios y tipos. |
| **automatizaciones** | Registra las rutinas o configuraciones automáticas creadas por los usuarios. |

---

## 🧠 Consultas de verificación incluidas

Al final del archivo **DBMS_online_ev6.sql**, se incluyen consultas de verificación automática, entre ellas:

- `SHOW TABLES;`  
- `DESCRIBE` de tablas principales.  
- `SELECT * FROM usuario LIMIT 5;`  
- `UPDATE usuario SET email = ... WHERE id_usuario = 1;`  
- Consultas `JOIN` entre `usuario`, `dispositivo` y `automatizaciones`.  
- Listado de automatizaciones cuya `hora_encendido ≥ 15:00`.  

Estas consultas permiten confirmar que las claves foráneas y las relaciones entre entidades funcionan correctamente.

---

## ⚙️ Notas y buenas prácticas

- Todas las tablas usan el motor **InnoDB**.  
- Las claves primarias son **AUTO_INCREMENT**.  
- El tipo **BOOLEAN** se implementa como `TINYINT(1)` en MySQL.  
- Si aparecen errores con `SET FOREIGN_KEY_CHECKS`, se pueden comentar temporalmente esas líneas.  
- Si reutilizás el script fuera de OneCompiler (por ejemplo, en MySQL Workbench), agregá una sentencia inicial:  

  ```sql
  CREATE DATABASE smarthome_ev6;
  USE smarthome_ev6 (en nuestro caso a una clevercloud gratuito nos genera una bd por defecto con el nombre DATABASE bowtbpbberdfnkr3zske);
