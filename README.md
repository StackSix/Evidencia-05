🚀 Propósito de la Evidencia 5

La Evidencia 5 se enfoca en la implementación de clases de un sistema Smart Home utilizando el enfoque de **Desarrollo Guiado por Pruebas (TDD)**, el diseño y la implementación de una **Base de Datos** con scripts DDL y DML, y la documentación del **Diagrama de Clases**.

📂 Estructura del Repositorio

En la raíz de este repositorio, se deben encontrar las siguientes carpetas, cada una con su propósito específico:

1.  **`POO-SmartHome/`**
    *   **Propósito:** Contiene la implementación de clases bajo el enfoque de **Desarrollo Guiado por Pruebas (TDD)**. Es importante destacar que **no se requiere la implementación de un menú (`main.py`) ni la lógica de programación relacionada con la gestión directa de dispositivos** (altas, bajas, modificaciones, etc.).
    *   **Estándares de Codificación:** El código Python debe respetar las **nomenclaturas estándar de la comunidad**. Se recomienda seguir la **Guía PEP 8**, propuesta por Guido van Rossum, que promueve un código limpio y legible. Esto incluye el uso de nombres de variables y funciones descriptivos, en minúsculas y separados por guiones bajos.
    *   **Calidad del Código:** Se valorará especialmente la **modularidad y la legibilidad** del código.

2.  **`Diseño-Evidencia-5/`**
    *   **Contenido:** Esta carpeta debe contener el **Diagrama de Clases** del sistema, acompañado de las **justificaciones pertinentes**.

3.  **`BD-Evidencia-5/`**
    *   **Propósito:** Almacena todos los componentes relacionados con la base de datos.
    *   **Contenido:**
        *   Un archivo con extensión `.SQL` que contenga las **consultas DDL** (Data Definition Language). Estas consultas son esenciales para **definir y crear la base de datos y sus tablas**, estableciendo las estructuras adecuadas para la integración de datos.
        *   Un archivo con extensión `.SQL` que incluya las **consultas DML** (Data Manipulation Language). Estas deben permitir la **inserción de al menos 30 datos iniciales** en la base de datos y realizar una **consulta simple para cada tabla**.
        *   Un archivo `README` específico para esta carpeta, que **explique cómo ejecutar cada script en un sistema de gestión de bases de datos (DBMS) online**. Es fundamental **indicar qué DBMS se ha utilizado** (por ejemplo, `https://onecompiler.com/` o `https://runsql.com/`), dado que existen pequeñas variaciones sintácticas entre motores de bases de datos como SQL Server, PostgreSQL o MySQL.

