-- BD-Evidencia-6/
-- Motor objetivo: MySQL 8 (probado en OneCompiler)

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS rol_permiso;
DROP TABLE IF EXISTS usuarios_hogares;
DROP TABLE IF EXISTS automatizaciones;
DROP TABLE IF EXISTS dispositivos;
DROP TABLE IF EXISTS tipos_dispositivos;
DROP TABLE IF EXISTS tipo_habitacion;
DROP TABLE IF EXISTS domicilios;
DROP TABLE IF EXISTS permiso;
DROP TABLE IF EXISTS rol;
DROP TABLE IF EXISTS usuarios;

SET FOREIGN_KEY_CHECKS = 1;

-- DDL: Tablas principales según diagrama

CREATE DATABASE IF NOT EXISTS ev6_smarthome
  CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE ev6_smarthome;

-- Usuarios
CREATE TABLE usuarios (
  dni INT NOT NUL PRIMARY KEY,
  id_rol INT UNSIGNED AUTO_INCREMENT NOT NULL,
  nombre VARCHAR(120) NOT NULL,
  apellido VARCHAR(120) NOT NULL,
  email VARCHAR(120) NOT NULL UNIQUE,
  contrasena_hash VARCHAR(255) NOT NULL,
  creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_usuario_rol FOREIGN KEY (id_rol) REFERENCES rol(id_rol) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Roles
CREATE TABLE rol (
  id_rol INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(60) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- Permisos (M:N con roles)
CREATE TABLE permiso (
  id_permiso INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- Domicilios
CREATE TABLE domicilios (
  id_hogar INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  direccion VARCHAR(255) NOT NULL,
  numeracion VARCHAR(50),
  ciudad VARCHAR(100),
  nombre_domicilio VARCHAR(120)
) ENGINE=InnoDB;

-- Tipo de habitación
CREATE TABLE tipo_habitacion (
  id_habitacion INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  id_hogar INT UNSIGNED NOT NULL,
  nombre_habitacion VARCHAR(120) NOT NULL,
  CONSTRAINT fk_th_hogar FOREIGN KEY (hogar_id) REFERENCES domicilios(id_hogar) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;


-- Dispositivos
CREATE TABLE dispositivos (
  id_dispositivo INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  id_habitacion INT UNSIGNED NULL,
  estado BOOLEAN NOT NULL DEFAULT FALSE,
  accion VARCHAR(120) NOT NULL,
  creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_disp_habitacion FOREIGN KEY (id_habitacion) REFERENCES tipo_habitacion(id_habitacion) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_disp_tipo FOREIGN KEY (id_tipo) REFERENCES tipos_dispositivos(id_tipo) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;


-- rol <-> permiso
CREATE TABLE rol_permiso (
  id_rol INT UNSIGNED NOT NULL,
  id_permiso INT UNSIGNED NOT NULL,
  PRIMARY KEY (id_rol, id_permiso),
  CONSTRAINT fk_rp_rol FOREIGN KEY (id_rol) REFERENCES rol(id_rol) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_rp_perm FOREIGN KEY (id_permiso) REFERENCES permiso(id_permiso) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Junction usuarios <-> domicilios (M:N)
CREATE TABLE usuarios_domicilios (
  usuario_id INT UNSIGNED NOT NULL,
  id_hogar INT UNSIGNED NOT NULL,
  PRIMARY KEY (usuario_id, hogar_id),
  CONSTRAINT fk_uh_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_uh_hogar FOREIGN KEY (hogar_id) REFERENCES domicilios(id_hogar) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;


-- Tipos de dispositivos
CREATE TABLE tipos_dispositivos (
  id_tipo INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nombre_tipo VARCHAR(80) NOT NULL UNIQUE
) ENGINE=InnoDB;


-- Automatizaciones
CREATE TABLE automatizaciones (
  id_automatizacion INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  id_hogar INT UNSIGNED NOT NULL,
  nombre VARCHAR(140) NOT NULL,
  accion VARCHAR(140) NOT NULL,
  CONSTRAINT fk_auto_hogar FOREIGN KEY (hogar_id) REFERENCES domicilios(id_hogar) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;



-- ======================================
-- DML: Inserciones de ejemplo (>=10 por tablas clave)
-- ======================================

-- Roles (al menos 2)
INSERT INTO rol (nombre) VALUES
  ('admin'), ('usuario'), ('operador');

-- Permisos (ejemplos)
INSERT INTO permiso (nombre) VALUES
  ('gestionar_dispositivos'),
  ('ver_dispositivos'),
  ('modificar_roles'),
  ('ver_automatizaciones'),
  ('gestionar_automatizaciones');

-- Asignaciones rol_permiso
INSERT INTO rol_permiso (id_rol, id_permiso) VALUES
  (1,1), -- admin -> gestionar_dispositivos
  (1,2),
  (1,3),
  (1,4),
  (1,5),
  (2,2), -- usuario -> ver_dispositivos
  (2,4),
  (3,2),
  (3,5);

-- Usuarios (10)
INSERT INTO usuarios (dni, id_rol, nombre, apellido, email, contrasena_hash)
VALUES
  ('20123456', 2, 'Daniel', 'Gonzalez', 'daniel@example.com', 'pbkdf2$120000$aa1$h1'),
  ('27123457', 2, 'Ana', 'Perez', 'ana@example.com', 'pbkdf2$120000$aa2$h2'),
  ('30123458', 2, 'Luis', 'Romero', 'luis@example.com', 'pbkdf2$120000$aa3$h3'),
  ('32123459', 2, 'Carla', 'Suarez', 'carla@example.com', 'pbkdf2$120000$aa4$h4'),
  ('33123460', 2, 'Nahir', 'Bustos', 'nahir@example.com', 'pbkdf2$120000$aa5$h5'),
  ('34123461', 2, 'Sofia', 'Lopez', 'sofia@example.com', 'pbkdf2$120000$aa6$h6'),
  ('40123462', 1, 'Root', 'Admin', 'root@example.com', 'pbkdf2$120000$aa7$h7'),
  ('41123463', 3, 'pepe', 'Op', 'nightop@example.com', 'pbkdf2$120000$aa8$h8'),
  ('42123464', 3, 'Day', 'Op', 'dayop@example.com', 'pbkdf2$120000$aa9$h9'),
  ('43123465', 2, 'Nicolas', 'Roman', 'nicolas@example.com', 'pbkdf2$120000$aaA$hA');

-- Domicilios (10)
INSERT INTO domicilios (direccion, numeracion, ciudad, nombre_domicilio) VALUES
  ('Av. Libertad', '123', 'Cordoba', 'Casa Gonzalez'),
  ('Calle Falsa', '742', 'Cordoba', 'Casa Perez'),
  ('Pje. Verde', '10', 'Cordoba', 'Depto Romero'),
  ('Rivadavia', '200', 'Córdoba', 'PH Suárez'),
  ('Santiago', '45', 'Córdoba', 'Casa Bustos'),
  ('San Martin', '88', 'Villa Maria', 'Casa Lopez'),
  ('Ruta 9', '1000', 'Cordoba', 'Sede Admin'),
  ('Av. Oeste', '500', 'Cordoba', 'Casa Night'),
  ('Av. Este', '777', 'Cordoba', 'Casa Day'),
  ('Boulevard', '1', 'Cordoba', 'Depósito');

-- Vincular usuarios a domicilios (usuarios_hogares) (al menos algunos)
INSERT INTO usuarios_hogares (usuario_id, hogar_id) VALUES
  (1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10);

-- Tipo_habitacion (>=10 entradas)
INSERT INTO tipo_habitacion (hogar_id, nombre_habitacion) VALUES
  (1,'Living'),(1,'Cocina'),(2,'Living'),(2,'Garage'),
  (3,'Oficina'),(4,'Balcón'),(5,'Dormitorio'),(6,'Comedor'),
  (7,'Depósito'),(8,'Patio');

-- Tipos de dispositivos (catálogo)
INSERT INTO tipos_dispositivos (nombre_tipo) VALUES
  ('CAMARA'),('SENSOR_MOVIMIENTO'),('SENSOR_SONIDO'),('ALARM'),('SMART_LOCK'),
  ('LAMP'),('THERMOSTAT'),('OUTLET'),('SENSOR_TEMPERATURA'),('SENSOR_HUMEDAD');

-- Dispositivos (>=10)
INSERT INTO dispositivos (id_habitacion, id_tipo, estado, etiqueta) VALUES
  (1,1, FALSE, 'Cam Patio Trasero'),   -- id_dispositivo auto
  (1,6, TRUE,  'Luz Living'),
  (2,1, TRUE,  'Cam Entrada'),
  (3,2, FALSE, 'Sensor Garage'),
  (4,1, TRUE,  'Cam Cocina'),
  (5,3, FALSE, 'Sensor Sonido Living'),
  (6,6, TRUE,  'Luz Balcón'),
  (7,9, FALSE, 'Sensor Depósito'),
  (8,1, TRUE,  'Cam Porch'),
  (9,1, FALSE, 'Cam Depósito');

-- Automatizaciones (>=10)
INSERT INTO automatizaciones (hogar_id, nombre, accion, dias, hora, activa) VALUES
  (1,'Rutina Noche','ENCENDER_CAMARAS','LU,MA,MI,JU,VI','22:00',TRUE),
  (1,'Apagar Luces Madrugada','APAGAR_LUCES','LU,MA,MI,JU,VI','02:00',TRUE),
  (2,'Alerta Movimiento Garage','ALERTA_MOTION','LU,MA,MI,JU,VI,SA,DO',NULL,TRUE),
  (3,'Rutina Oficina','ENCENDER_OFICINA','LU,MA,MI,JU,VI','08:30',TRUE),
  (4,'Aviso Balcon','NOTIF_BALCON','SA,DO','09:00',FALSE),
  (5,'Guardar Seguridad','ARMAR_SISTEMA','LU,MA,MI,JU,VI','23:30',TRUE),
  (6,'Temporizador','REGULAR_TERMOSTATO','LU,MA,MI,JU,VI','06:00',TRUE),
  (7,'Alerta Deposito','ALARMA_DEPOSITO','LU,MA,MI,JU,VI,SA,DO',NULL,TRUE),
  (8,'Rutina Porch','ENCENDER_PORCH','LU,MA,MI,JU,VI','19:00',TRUE),
  (9,'Apagado General','APAGAR_GENERAL','LU,MA,MI,JU,VI,SA,DO','23:55',TRUE);

-- ======================================
-- Consultas simples (verificación)
-- ======================================

-- 1) Ver usuarios
SELECT id, dni, nombre, apellido, email, id_rol FROM usuarios ORDER BY id;

-- 2) Ver roles
SELECT * FROM rol ORDER BY id_rol;

-- 3) Ver permisos
SELECT * FROM permiso ORDER BY id_permiso;

-- 4) Ver domicilios
SELECT * FROM domicilios ORDER BY id_hogar;

-- 5) Ver tipo_habitacion
SELECT * FROM tipo_habitacion ORDER BY id_habitacion;

-- 6) Ver tipos_dispositivos
SELECT * FROM tipos_dispositivos ORDER BY id_tipo;

-- 7) Ver dispositivos
SELECT id_dispositivo, etiqueta, id_habitacion, id_tipo, estado FROM dispositivos ORDER BY id_dispositivo;

-- 8) Ver automatizaciones
SELECT * FROM automatizaciones ORDER BY id_automatizacion;


-- ======================================
-- Consultas multitabla (mínimo 4) con justificación
-- ======================================

-- MQ1: Usuarios + su domicilio(s) y cantidad de dispositivos en ese hogar.
-- Justificación: respuesta de negocio típica: ¿qué hogares administra un usuario y cuántos dispositivos hay en cada hogar?
SELECT u.id AS usuario_id, u.nombre, u.apellido,
       h.id_hogar, h.nombre_domicilio, h.direccion,
       (SELECT COUNT(*) FROM dispositivos d JOIN tipo_habitacion th ON th.id_habitacion = d.id_habitacion WHERE th.hogar_id = h.id_hogar) AS dispositivos_en_hogar
FROM usuarios u
JOIN usuarios_hogares uh ON uh.usuario_id = u.id
JOIN domicilios h ON h.id_hogar = uh.hogar_id
ORDER BY u.id, h.id_hogar;

-- MQ2: Eventos/automatizaciones relacionadas: listar automatizaciones activas por usuario (a través del hogar)
-- Justificación: permite a un usuario/admin ver las automatizaciones configuradas para sus hogares.
SELECT u.id AS usuario_id, u.nombre, a.id_automatizacion, a.nombre AS automatizacion, a.accion, a.hora, a.activa
FROM usuarios u
JOIN usuarios_hogares uh ON uh.usuario_id = u.id
JOIN domicilios h ON h.id_hogar = uh.hogar_id
JOIN automatizaciones a ON a.hogar_id = h.id_hogar
WHERE a.activa = TRUE
ORDER BY u.id, a.id_automatizacion;

-- MQ3: Listar cámaras (tipo CAMARA) con su hogar y el email del propietario (primer usuario vinculado)
-- Justificación: información operativa: qué cámaras pertenecen a qué hogar y a qué usuario contactar.
SELECT d.id_dispositivo, d.etiqueta AS dispositivo, td.nombre_tipo, h.nombre_domicilio, u.email
FROM dispositivos d
JOIN tipos_dispositivos td ON td.id_tipo = d.id_tipo
LEFT JOIN tipo_habitacion th ON th.id_habitacion = d.id_habitacion
LEFT JOIN domicilios h ON h.id_hogar = th.hogar_id
LEFT JOIN usuarios_hogares uh ON uh.hogar_id = h.id_hogar
LEFT JOIN usuarios u ON u.id = uh.usuario_id
WHERE td.nombre_tipo = 'CAMARA'
GROUP BY d.id_dispositivo;

-- MQ4: Admins y cantidad de automatizaciones en sus hogares (métrica de gestión)
-- Justificación: métricas para administradores: cuántas automatizaciones deben supervisar.
SELECT u.id AS admin_id, u.nombre, COUNT(a.id_automatizacion) AS cantidad_automatizaciones
FROM usuarios u
JOIN usuarios_hogares uh ON uh.usuario_id = u.id
JOIN domicilios h ON h.id_hogar = uh.hogar_id
JOIN automatizaciones a ON a.hogar_id = h.id_hogar
WHERE u.id_rol = (SELECT id_rol FROM rol WHERE nombre='admin' LIMIT 1)
GROUP BY u.id, u.nombre
ORDER BY cantidad_automatizaciones DESC;


-- ======================================
-- Subconsultas (mínimo 2) con justificación
-- ======================================

-- S1: Usuarios que tienen más de 1 hogar (subconsulta en HAVING/COUNT)
-- Justificación: detectar usuarios con múltiples domicilios (p. ej. clientes premium, empresas).
SELECT u.id, u.nombre, u.email, COUNT(uh.hogar_id) AS cantidad_hogares
FROM usuarios u
JOIN usuarios_hogares uh ON uh.usuario_id = u.id
GROUP BY u.id, u.nombre, u.email
HAVING COUNT(uh.hogar_id) > 1;

-- S2: Habitaciones que contienen al menos un dispositivo tipo 'CAMARA' (subconsulta EXISTS)
-- Justificación: localizar habitaciones críticas que contienen cámaras.
SELECT th.id_habitacion, th.nombre_habitacion, th.hogar_id
FROM tipo_habitacion th
WHERE EXISTS (
    SELECT 1 FROM dispositivos d
    JOIN tipos_dispositivos td ON td.id_tipo = d.id_tipo
    WHERE d.id_habitacion = th.id_habitacion
      AND td.nombre_tipo = 'CAMARA'
);

-- S3 (opcional): Ultima automatización activada por hogar (subconsulta en SELECT)
-- Justificación: obtener la última automatización (por id) configurada por hogar.
SELECT h.id_hogar, h.nombre_domicilio,
       (SELECT a.nombre FROM automatizaciones a WHERE a.hogar_id = h.id_hogar ORDER BY a.id_automatizacion DESC LIMIT 1) AS ultima_automatizacion
FROM domicilios h;

-- ======================================
-- FIN del script
-- ======================================

