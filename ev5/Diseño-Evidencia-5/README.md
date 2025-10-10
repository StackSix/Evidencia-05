SmartHome – Modelo de Clases

Este proyecto implementa un sistema simplificado de usuarios, dispositivos y cámara inteligente, siguiendo principios de diseño orientado a objetos y un modelo de base de datos relacional.

📌 Diagrama de clases

El sistema se basa en el siguiente modelo UML (diagrama_de_clases.jpeg):

Usuario (entidad base con email, nombre, contraseña y rol).

Admin (especialización de Usuario con permisos de gestión).

Dispositivos (entidad genérica que representa cualquier dispositivo del hogar (De momento una camara)).

Camara (subclase de Dispositivos con funciones de grabación y automatización).

Email (objeto de valor, composición 1:1 con Usuario).

EventoDispositivo (eventos generados por dispositivos, en especial cámaras).

ControlAutomatizacion (interfaz para la automatización horaria).


Principios aplicados
1) Abstracción

-Usuario/Admin encapsulan autenticación y gestión.
-Dispositivos representan un concepto general, y Camara especializa con atributos propios (grabación, automatización).

2) Encapsulamiento

-Atributos privados (prefijo _ en código).
-Métodos públicos controlan el acceso:
-Usuario.mostrar_datos_usuario() → devuelve vista segura.
-Dispositivos.modificar_estado_dispositivo() → controla cambios válidos.

3) Herencia

-Admin → hereda de Usuario.
-Camara → hereda de Dispositivos.

Permite reutilizar atributos comunes y aplicar polimorfismo.

4) Composición

Usuario *-- Email: el email no existe sin usuario.

5) Agregación

-Usuario o-- Dispositivos: un usuario puede tener varios dispositivos.

-Camara o-- EventoDispositivo: una cámara genera múltiples eventos.

6) Polimorfismo e Interfaces

-ControlAutomatizacion define un contrato.
-Camara implementa la interfaz → en el futuro, más dispositivos pueden hacerlo (ej. luces inteligentes).

7) Responsabilidad Única (SRP)

-Email: validación y representación.
-Usuario: identidad/autenticación.
-Admin: gestión de roles y dispositivos.
-Camara: lógica de grabación y automatización.

8) Extensibilidad

Agregar un nuevo dispositivo solo requiere crear una subclase de Dispositivos.

9) Cohesión y Bajo Acoplamiento

Cada clase resuelve un aspecto concreto del dominio.

La interfaz desacopla clientes de implementaciones concretas.