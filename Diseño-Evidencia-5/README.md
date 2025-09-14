SmartHome – Modelo de Clases

Este proyecto implementa un sistema simplificado de usuarios, dispositivos y cámara inteligente, siguiendo principios de diseño orientado a objetos y un modelo de base de datos relacional.

📌 Diagrama de clases

El sistema se basa en el siguiente modelo UML (diagrama_de_clases.jpeg):

Usuario (entidad base con email, nombre, contraseña y rol).

Admin (especialización de Usuario con permisos de gestión).

Dispositivos (entidad genérica que representa cualquier dispositivo del hogar).

Camara (subclase de Dispositivos con funciones de grabación y automatización).

Email (objeto de valor, composición 1:1 con Usuario).

EventoDispositivo (eventos generados por dispositivos, en especial cámaras).

ControlAutomatizacion (interfaz para la automatización horaria).