-- Script DBMS (DDL + DML) para SmartHome en OneCompiler (MySQL 8)
SET FOREIGN_KEY_CHECKS = 0;

-- Eliminar las tablas existentes (en orden inverso de dependencias)
DROP TABLE IF EXISTS automatizacion;
DROP TABLE IF EXISTS dispositivo;
DROP TABLE IF EXISTS tipo_dispositivo;
DROP TABLE IF EXISTS domicilio;
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS rol;

SET FOREIGN_KEY_CHECKS = 1;

-- ====== DDL: Definición del esquema ======

-- Tabla de roles
CREATE TABLE rol (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    rol VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

-- Tabla de usuarios
CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    dni INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    rol INT NOT NULL,
    CONSTRAINT fk_usuario_rol FOREIGN KEY (rol) REFERENCES rol(rol)
) ENGINE=InnoDB;

-- Tabla de domicilios
CREATE TABLE domicilio (
    id_domicilio INT AUTO_INCREMENT PRIMARY KEY,
    direccion VARCHAR(200) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    nombre_domicilio VARCHAR(100) NOT NULL,
    id_usuario INT NOT NULL,
    CONSTRAINT fk_domicilio_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Tabla de tipos de dispositivos
CREATE TABLE tipo_dispositivo (
    id_tipo INT AUTO_INCREMENT PRIMARY KEY,
    tipo_dispositivo VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

-- Tabla de dispositivos
CREATE TABLE dispositivo (
    id_dispositivo INT AUTO_INCREMENT PRIMARY KEY,
    id_domicilio INT NOT NULL,
    id_tipo INT NOT NULL,
    estado VARCHAR(50) NOT NULL,
    etiqueta VARCHAR(100) NOT NULL,
    CONSTRAINT fk_dispositivo_domicilio FOREIGN KEY (id_domicilio)
        REFERENCES domicilio(id_domicilio) ON DELETE CASCADE,
    CONSTRAINT fk_dispositivo_tipo FOREIGN KEY (id_tipo)
        REFERENCES tipo_dispositivo(id_tipo)
) ENGINE=InnoDB;

-- Tabla de automatizaciones
CREATE TABLE automatizacion (
    id_automatizacion INT AUTO_INCREMENT PRIMARY KEY,
    id_domicilio INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    accion VARCHAR(100) NOT NULL,
    estado BOOLEAN NOT NULL,
    hora_encendido TIME,
    hora_apagado TIME,
    CONSTRAINT fk_automatizaciones_domicilio FOREIGN KEY (id_domicilio)
        REFERENCES domicilio(id_domicilio) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ====== DML: Inserción de datos ======

-- Roles
INSERT INTO rol (rol) VALUES ('Admin'), ('Usuario');

-- Usuarios
INSERT INTO usuario (dni, nombre, apellido, email, contrasena, rol) VALUES
    (30111222, 'daniel',    'gonzalez', 'danigonzalez@hotmail.com',    '21345558', 2),
    (30222333, 'nicolas',   'romano',    'nico_romano@hotmail.com',    '13345558', 2),
    (30333444, 'Francisco', 'perez',     'franperez@hotmail.com',       '12367876', 2),
    (30444555, 'florencia', 'Bri',        'florenciabri@hotmail.com',    '12375466', 2),
    (30555666, 'luis',      'Vazques',   'luisvazques@hotmail.com',     '12345558', 2),
    (30666777, 'Marisa',    'Perez',     'mariperez@hotmail.com',       '12344559', 2),
    (30777888, 'Claudia',   'Torres',    'clautorres@hotmail.com',      '12765558', 2),
    (30888999, 'pepe',      'Lopez',     'pepe_lopez@hotmail.com',      '12345678', 2),
    (30999000, 'Pablo',     'juarez',    'pablito22@hotmail.com',       '19072874', 2),
    (31100111, 'Valentina', 'Gomez',     'valentina@gmail.com',         '12873545', 2);

-- Domicilios
INSERT INTO domicilio (direccion, ciudad, nombre_domicilio, id_usuario) VALUES
    ('Calle Falsa 123',        'san luis',       'Casa',            1),
    ('Av. Siemprevivas 742',   'Buenos Aires',   'Home',            2),
    ('Calle 13 #300',          'Córdoba',        'mi casa',         3),
    ('Calle 24 #400',          'Rosario',        'guarida',         4),
    ('Calle 76 #500',          'Mendoza',        'baticueva',       5),
    ('velez sarsfield #600',   'Salta',          'depto',           6),
    ('peru 320 #320',          'Buenos Aires',   'Casa alquiler',   7),
    ('la rioja #800',          'Buenos Aires',   'Casa 2',          8),
    ('dean funes #900',        'Córdoba',        'Casa vacaciones', 9),
    ('brasil #1000',           'Buenos Aires',   'Casa Valentina', 10);

-- Tipos de dispositivos
INSERT INTO tipo_dispositivo (tipo_dispositivo) VALUES
    ('Sensor'),
    ('Actuador'),
    ('Cámara');

-- Dispositivos
INSERT INTO dispositivo (id_domicilio, id_tipo, estado, etiqueta) VALUES
    (1,  1, 'activo', 'Sensor Temperatura'),
    (2,  2, 'activo', 'Lámpara LED'),
    (3,  3, 'activo', 'Cámara IP'),
    (4,  1, 'activo', 'Sensor Humedad'),
    (5,  2, 'activo', 'Termostato'),
    (6,  1, 'activo', 'Sensor Movimiento'),
    (7,  2, 'activo', 'Bombilla Inteligente'),
    (8,  2, 'activo', 'Cerradura Smart'),
    (9,  1, 'activo', 'Sensor Luz'),
    (10, 2, 'activo', 'Alarma');

-- Automatizaciones
INSERT INTO automatizacion (id_domicilio, nombre, accion, estado, hora_encendido, hora_apagado) VALUES
    (1,  'Automatizacion 1',  '38°C',                         TRUE, '08:10:00', NULL),
    (1,  'Automatizacion 2',  'Encender si temperatura 38°C', TRUE, '08:20:00', NULL),
    (2,  'Automatizacion 3',  'Detectar movimiento',          TRUE, '10:10:00', NULL),
    (3,  'Automatizacion 4',  'Encender si humedad <40%',     TRUE, '11:10:00', NULL),
    (4,  'Automatizacion 5',  'Apagar si movimiento',         TRUE, '12:10:00', NULL),
    (5,  'Automatizacion 6',  'Encender a las 20:00',         TRUE, '13:10:00', NULL),
    (6,  'Automatizacion 7',  'Cerrar si puerta abierta',     TRUE, '14:10:00', NULL),
    (7,  'Automatizacion 8',  'Activar si luz <50',           TRUE, '15:10:00', NULL),
    (8,  'Automatizacion 9',  'Activar alarma si movimiento', TRUE, '16:10:00', NULL),
    (9,  'Automatizacion 10', 'Medir temperatura cada 10 min',TRUE, '17:10:00', NULL);

-- ====== Consultas de verificación ======

-- Mostrar todas las tablas
SHOW TABLES;

DESCRIBE usuario;
DESCRIBE domicilio;
DESCRIBE dispositivo;
DESCRIBE automatizacion;

SELECT nombre, apellido, email
FROM usuario
ORDER BY id_usuario
LIMIT 5;

UPDATE usuario
SET contrasena = 'prueba1234'
WHERE id_usuario = 1;

UPDATE usuario
SET email = 'danigonzalez@gmail.com'
WHERE id_usuario = 1;

SELECT d.etiqueta AS nombre, t.tipo_dispositivo AS tipo
FROM dispositivo d
JOIN tipo_dispositivo t ON d.id_tipo = t.id_tipo
JOIN domicilio dom ON d.id_domicilio = dom.id_domicilio
WHERE dom.id_usuario = 1;

SELECT nombre, accion, hora_encendido
FROM automatizacion
WHERE hora_encendido >= '15:00:00';