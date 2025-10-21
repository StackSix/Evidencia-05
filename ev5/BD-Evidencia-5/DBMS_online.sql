-- Listo para copiar y pegar en MySQL 8 (OneCompiler)

SET FOREIGN_KEY_CHECKS = 0;

-- Eliminar tablas existentes en orden inverso para respetar las claves foráneas
DROP TABLE IF EXISTS automatizaciones;
DROP TABLE IF EXISTS gestor_automatizacion;
DROP TABLE IF EXISTS dispositivo;
DROP TABLE IF EXISTS tipos_dispositivos;
DROP TABLE IF EXISTS gestor_dispositivo;
DROP TABLE IF EXISTS domicilio;
DROP TABLE IF EXISTS gestor_domicilio;
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS gestor_usuario;
DROP TABLE IF EXISTS rol;

SET FOREIGN_KEY_CHECKS = 1;

-- ==== DDL: definición del esquema ====

-- Tabla rol: define los roles del usuario
CREATE TABLE rol (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

-- Tabla gestor_usuario: administra una colección de usuarios
CREATE TABLE gestor_usuario (
    id_gestor_usuario INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(100)
) ENGINE=InnoDB;

-- Tabla usuario: contiene los datos de los usuarios del sistema
CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    dni INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    id_rol INT NOT NULL,
    id_gestor_usuario INT NOT NULL,
    CONSTRAINT fk_usuario_rol FOREIGN KEY (id_rol) REFERENCES rol(id_rol),
    CONSTRAINT fk_usuario_gestor_usuario FOREIGN KEY (id_gestor_usuario)
        REFERENCES gestor_usuario(id_gestor_usuario)
) ENGINE=InnoDB;

-- Tabla gestor_domicilio: administrador de domicilios por usuario
CREATE TABLE gestor_domicilio (
    id_gestor_domicilio INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    descripcion VARCHAR(100),
    CONSTRAINT fk_gestor_domicilio_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Tabla domicilio: describe las viviendas asociadas a los usuarios
CREATE TABLE domicilio (
    id_domicilio INT AUTO_INCREMENT PRIMARY KEY,
    direccion VARCHAR(200) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    nombre_domicilio VARCHAR(100) NOT NULL,
    id_usuario INT NOT NULL,
    id_gestor_domicilio INT NOT NULL UNIQUE,
    CONSTRAINT fk_domicilio_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    CONSTRAINT fk_domicilio_gestor FOREIGN KEY (id_gestor_domicilio)
        REFERENCES gestor_domicilio(id_gestor_domicilio) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Tabla gestor_dispositivo: administrador de dispositivos de cada domicilio
CREATE TABLE gestor_dispositivo (
    id_gestor_dispositivo INT AUTO_INCREMENT PRIMARY KEY,
    id_domicilio INT NOT NULL UNIQUE,
    descripcion VARCHAR(100),
    CONSTRAINT fk_gestor_dispositivo_domicilio FOREIGN KEY (id_domicilio)
        REFERENCES domicilio(id_domicilio) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Tabla tipos_dispositivos: catálogo de tipos de dispositivos
CREATE TABLE tipos_dispositivos (
    id_tipo INT AUTO_INCREMENT PRIMARY KEY,
    tipo_dispositivo VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

-- Tabla dispositivo: listado de dispositivos instalados en los domicilios
CREATE TABLE dispositivo (
    id_dispositivo INT AUTO_INCREMENT PRIMARY KEY,
    id_domicilio INT NOT NULL,
    id_tipo INT NOT NULL,
    estado VARCHAR(50) NOT NULL,
    etiqueta VARCHAR(100) NOT NULL,
    id_gestor_dispositivo INT NOT NULL,
    CONSTRAINT fk_dispositivo_domicilio FOREIGN KEY (id_domicilio)
        REFERENCES domicilio(id_domicilio) ON DELETE CASCADE,
    CONSTRAINT fk_dispositivo_tipo FOREIGN KEY (id_tipo)
        REFERENCES tipos_dispositivos(id_tipo),
    CONSTRAINT fk_dispositivo_gestor FOREIGN KEY (id_gestor_dispositivo)
        REFERENCES gestor_dispositivo(id_gestor_dispositivo) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Tabla gestor_automatizacion: administrador de automatizaciones
CREATE TABLE gestor_automatizacion (
    id_gestor_automatizacion INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(100)
) ENGINE=InnoDB;

-- Tabla automatizaciones: define las automatizaciones programadas
CREATE TABLE automatizaciones (
    id_automatizacion INT AUTO_INCREMENT PRIMARY KEY,
    id_domicilio INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    accion VARCHAR(100) NOT NULL,
    estado BOOLEAN NOT NULL,
    hora_encendido TIME,
    hora_apagado TIME,
    id_gestor_automatizacion INT NOT NULL,
    CONSTRAINT fk_automatizaciones_domicilio FOREIGN KEY (id_domicilio)
        REFERENCES domicilio(id_domicilio) ON DELETE CASCADE,
    CONSTRAINT fk_automatizaciones_gestor FOREIGN KEY (id_gestor_automatizacion)
        REFERENCES gestor_automatizacion(id_gestor_automatizacion) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ==== DML: inserción de datos de ejemplo ====

-- Roles
INSERT INTO rol (nombre) VALUES
    ('Admin'),
    ('Usuario');

-- Gestores de usuarios
INSERT INTO gestor_usuario (descripcion) VALUES
    ('Gestor principal'),
    ('Gestor secundario'),
    ('Gestor terciario');

-- Usuarios
INSERT INTO usuario (dni, nombre, apellido, email, contrasena, id_rol, id_gestor_usuario) VALUES
    (30111222, 'daniel',    'gonzalez', 'danigonzalez@hotmail.com',    '21345558', 2, 1),
    (30222333, 'nicolas',   'romano',    'nico_romano@hotmail.com',    '13345558', 2, 1),
    (30333444, 'Francisco', 'perez',    'franperez@hotmail.com',       '12367876', 2, 1),
    (30444555, 'florencia','Bri',       'florenciabri@hotmail.com',     '12375466', 2, 1),
    (30555666, 'luis',      'Vazques',  'luisvazques@hotmail.com',     '12345558', 2, 2),
    (30666777, 'Marisa',    'Perez',    'mariperez@hotmail.com',       '12344559', 2, 2),
    (30777888, 'Claudia',   'Torres',   'clautorres@hotmail.com',      '12765558', 2, 2),
    (30888999, 'pepe',      'Lopez',    'pepe_lopez@hotmail.com',      '12345678', 2, 3),
    (30999000, 'Pablo',     'juarez',   'pablito22@hotmail.com',       '19072874', 2, 3),
    (31100111, 'Valentina', 'Gomez',    'valentina@gmail.com',         '12873545', 2, 3);

-- Gestores de domicilio
INSERT INTO gestor_domicilio (id_usuario, descripcion) VALUES
    (1,  'Gestor domicilio 1'),
    (2,  'Gestor domicilio 2'),
    (3,  'Gestor domicilio 3'),
    (4,  'Gestor domicilio 4'),
    (5,  'Gestor domicilio 5'),
    (6,  'Gestor domicilio 6'),
    (7,  'Gestor domicilio 7'),
    (8,  'Gestor domicilio 8'),
    (9,  'Gestor domicilio 9'),
    (10, 'Gestor domicilio 10');

-- Domicilios
INSERT INTO domicilio (direccion, ciudad, nombre_domicilio, id_usuario, id_gestor_domicilio) VALUES
    ('Calle Falsa 123',        'san luis',        'Casa',            1,  1),
    ('Av. Siemprevivas 742',   'Buenos Aires',    'Home',            2,  2),
    ('Calle 13 #300',          'Córdoba',         'mi casa',         3,  3),
    ('Calle 24 #400',          'Rosario',         'guarida',         4,  4),
    ('Calle 76 #500',          'Mendoza',         'baticueva',       5,  5),
    ('velez sarsfield #600',   'Salta',           'depto',           6,  6),
    ('peru 320 #320',          'Buenos Aires',    'Casa alquiler',   7,  7),
    ('la rioja #800',          'Buenos Aires',    'Casa 2',          8,  8),
    ('dean funes #900',        'Córdoba',         'Casa vacaciones', 9,  9),
    ('brasil #1000',           'Buenos Aires',    'Casa Valentina', 10, 10);

-- Gestores de dispositivos
INSERT INTO gestor_dispositivo (id_domicilio, descripcion) VALUES
    (1,  'Gestor dispositivos 1'),
    (2,  'Gestor dispositivos 2'),
    (3,  'Gestor dispositivos 3'),
    (4,  'Gestor dispositivos 4'),
    (5,  'Gestor dispositivos 5'),
    (6,  'Gestor dispositivos 6'),
    (7,  'Gestor dispositivos 7'),
    (8,  'Gestor dispositivos 8'),
    (9,  'Gestor dispositivos 9'),
    (10, 'Gestor dispositivos 10');

-- Tipos de dispositivos
INSERT INTO tipos_dispositivos (tipo_dispositivo) VALUES
    ('Sensor'),
    ('Actuador'),
    ('Cámara');

-- Dispositivos
INSERT INTO dispositivo (id_domicilio, id_tipo, estado, etiqueta, id_gestor_dispositivo) VALUES
    (1,  1, 'activo', 'Sensor Temperatura',   1),
    (2,  2, 'activo', 'Lámpara LED',          2),
    (3,  3, 'activo', 'Cámara IP',            3),
    (4,  1, 'activo', 'Sensor Humedad',       4),
    (5,  2, 'activo', 'Termostato',           5),
    (6,  1, 'activo', 'Sensor Movimiento',    6),
    (7,  2, 'activo', 'Bombilla Inteligente', 7),
    (8,  2, 'activo', 'Cerradura Smart',      8),
    (9,  1, 'activo', 'Sensor Luz',           9),
    (10, 2, 'activo', 'Alarma',               10);

-- Gestores de automatización
INSERT INTO gestor_automatizacion (descripcion) VALUES
    ('Gestor automatización 1'),
    ('Gestor automatización 2'),
    ('Gestor automatización 3');

-- Automatizaciones
INSERT INTO automatizaciones (id_domicilio, nombre, accion, estado, hora_encendido, hora_apagado, id_gestor_automatizacion) VALUES
    (1,  'Automatizacion 1',  '38°C',                         TRUE, '08:10:00', NULL, 1),
    (1,  'Automatizacion 2',  'Encender si temperatura 38°C', TRUE, '08:20:00', NULL, 1),
    (2,  'Automatizacion 3',  'Detectar movimiento',          TRUE, '10:10:00', NULL, 1),
    (3,  'Automatizacion 4',  'Encender si humedad <40%',     TRUE, '11:10:00', NULL, 2),
    (4,  'Automatizacion 5',  'Apagar si movimiento',         TRUE, '12:10:00', NULL, 2),
    (5,  'Automatizacion 6',  'Encender a las 20:00',         TRUE, '13:10:00', NULL, 2),
    (6,  'Automatizacion 7',  'Cerrar si puerta abierta',     TRUE, '14:10:00', NULL, 3),
    (7,  'Automatizacion 8',  'Activar si luz <50',           TRUE, '15:10:00', NULL, 3),
    (8,  'Automatizacion 9',  'Activar alarma si movimiento', TRUE, '16:10:00', NULL, 3),
    (9,  'Automatizacion 10', 'Medir temperatura cada 10 min',TRUE, '17:10:00', NULL, 1);

-- ==== Consultas de verificación ====

-- Mostrar todas las tablas
SHOW TABLES;

-- Mostrar la descripción de las tablas principales
DESCRIBE usuario;
DESCRIBE domicilio;
DESCRIBE dispositivo;
DESCRIBE automatizaciones;

-- Consultar los primeros cinco usuarios
SELECT nombre, apellido, email
FROM usuario
ORDER BY id_usuario
LIMIT 5;

-- Actualizar la contraseña del usuario con id 1
UPDATE usuario
SET contrasena = 'prueba1234'
WHERE id_usuario = 1;

-- Actualizar el correo electrónico del usuario con id 1
UPDATE usuario
SET email = 'danigonzalez@gmail.com'
WHERE id_usuario = 1;

-- Mostrar el nombre y tipo de los dispositivos pertenecientes al usuario con id = 1
SELECT d.etiqueta AS nombre, t.tipo_dispositivo AS tipo
FROM dispositivo d
JOIN tipos_dispositivos t ON d.id_tipo = t.id_tipo
JOIN domicilio dom ON d.id_domicilio = dom.id_domicilio
WHERE dom.id_usuario = 1;

-- Mostrar automatizaciones programadas a partir de las 15:00
SELECT nombre, accion, hora_encendido
FROM automatizaciones
WHERE hora_encendido >= '15:00:00';