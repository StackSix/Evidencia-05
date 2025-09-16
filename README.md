# 📌 Evidencia 5 - Smart Home

## 🚀 Propósito de la Evidencia 5
La Evidencia 5 se enfoca en la implementación de clases de un sistema Smart Home utilizando el enfoque de **Desarrollo Guiado por Pruebas (TDD)**, el diseño y la implementación de una **Base de Datos** con scripts DDL y DML, y la documentación del **Diagrama de Clases**.

---

## 📂 Estructura del Repositorio

En la raíz de este repositorio, se deben encontrar las siguientes carpetas, cada una con su propósito específico:

1. **`POO-SmartHome/`**
   - **Propósito:** Contiene la implementación de clases bajo el enfoque de **Desarrollo Guiado por Pruebas (TDD)**.  
     👉 No se requiere la implementación de un menú (`main.py`) ni la lógica de programación relacionada con la gestión directa de dispositivos (altas, bajas, modificaciones, etc.).
   - **Estándares de Codificación:** El código Python respeta la **Guía PEP 8**, promoviendo un código limpio y legible.
   - **Calidad del Código:** Se valoró la **modularidad y legibilidad** del código.

2. **`Diseño-Evidencia-5/`**
   - **Contenido:** Contiene el **Diagrama de Clases** del sistema, acompañado de las **justificaciones pertinentes**.

3. **`BD-Evidencia-5/`**
   - **Propósito:** Almacena los componentes relacionados con la base de datos.
   - **Contenido:**
     - Un archivo `.sql` con las consultas **DDL** para crear la base de datos y sus tablas.
     - Un archivo `.sql` con las consultas **DML** que incluyen al menos **30 inserts iniciales** y consultas simples por tabla.
     - Un `README.md` con instrucciones para ejecutar los scripts en un **DBMS online** (por ejemplo, [`onecompiler`](https://onecompiler.com/) o [`runsql`](https://runsql.com/)).

---

## ▶️ Cómo ejecutar el programa

El sistema incluye un **menú de autenticación y configuración de dispositivos** (ubicado en `src/smarthome/router.py`).  

### 🔹 Pasos:

1. Abrí una terminal en la raíz del proyecto (**POO-SmartHome**).
2. Activá el entorno virtual:
   ```bash
   source POO-SmartHome/.venv/bin/activate

3. Ejecutá el programa con:
   PYTHONPATH=src python -m smarthome.router


### 🔹 Integrantes:

- Ariel Nicolás Romano 
- Daniel Estebabn Gonzalez Lara (dgel92)
- Luis Nicolas 	Asensio Lubrano 