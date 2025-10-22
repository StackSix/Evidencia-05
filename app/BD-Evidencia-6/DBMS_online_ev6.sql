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

-- Insertar roles
INSERT INTO rol (nombre) VALUES ('Admin'), ('Usuario');

-- Insertar usuarios iniciales (1..10)
INSERT INTO usuario (dni, nombre, apellido, email, contrasena, rol) VALUES
    (30111222, 'daniel',    'gonzalez', 'danigonzalez@hotmail.com',    '21345558', 2),
    (30222333, 'nicolas',   'romano',   'nico_romano@hotmail.com',     '13345558', 2),
    (30333444, 'Francisco', 'perez',    'franperez@hotmail.com',       '12367876', 2),
    (30444555, 'florencia','Bri',       'florenciabri@hotmail.com',    '12375466', 2),
    (30555666, 'luis',      'Vazques',  'luisvazques@hotmail.com',     '12345558', 2),
    (30666777, 'Marisa',    'Perez',    'mariperez@hotmail.com',       '12344559', 2),
    (30777888, 'Claudia',   'Torres',   'clautorres@hotmail.com',      '12765558', 2),
    (30888999, 'pepe',      'Lopez',    'pepe_lopez@hotmail.com',      '12345678', 2),
    (30999000, 'Pablo',     'juarez',   'pablito22@hotmail.com',       '19072874', 2),
    (31100111, 'Valentina', 'Gomez',    'valentina@gmail.com',         '12873545', 2);

-- Insertar domicilios para usuarios iniciales (1..10)
INSERT INTO domicilio (direccion, ciudad, nombre_domicilio, id_usuario) VALUES
    ('Calle Falsa 123',        'san luis',       'Casa',             1),
    ('Av. Siemprevivas 742',   'Buenos Aires',   'Home',             2),
    ('Calle 13 #300',          'Córdoba',        'mi casa',          3),
    ('Calle 24 #400',          'Rosario',        'guarida',          4),
    ('Calle 76 #500',          'Mendoza',        'baticueva',        5),
    ('velez sarsfield #600',   'Salta',          'depto',            6),
    ('peru 320 #320',          'Buenos Aires',   'Casa alquiler',    7),
    ('la rioja #800',          'Buenos Aires',   'Casa 2',           8),
    ('dean funes #900',        'Córdoba',        'Casa vacaciones',  9),
    ('brasil #1000',           'Buenos Aires',   'Casa Valentina',  10);

-- Insertar tipos de dispositivos
INSERT INTO tipo_dispositivo (tipo_dispositivo) VALUES
    ('Sensor'),
    ('Actuador'),
    ('Cámara');

-- Insertar dispositivos para los domicilios iniciales
-- id_tipo: 1=Sensor, 2=Actuador, 3=Cámara
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

-- Insertar automatizaciones para los domicilios iniciales
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

-- Insertar usuarios adicionales (11..20)
INSERT INTO usuario (dni, nombre, apellido, email, contrasena, rol) VALUES
    (40111222, 'roberto', 'Volm',      'roberto_volm@hotmail.com',   '1234567',    2),
    (40222333, 'marcelo', 'Tribu',     'marcelo_tribu@hotmail.com',  'fran23412345',2),
    (40333444, 'Lucia',   'castelli',  'lucia_castelli@gmail.com',   '1236luc24',  2),
    (40444555, 'Mariano', 'hernandez', 'marianoher@hotmail.com',     '45mariano12',2),
    (40555666, 'Julio',   'agosto',    'julioagosto@hotmail.com',    'juedo1238',  2),
    (40666777, 'Ricardo', 'roca',      'ricardoroca@hotmail.com',    '1des1239',   1),
    (40777888, 'Analia',  'Torres',    'anatorres@hotmail.com',      'ju231240',   2),
    (40888999, 'Paola',   'Lopez',     'paola_lopez@hotmail.com',    'pao1241',    2),
    (40999000, 'Paula',   'oviedo',    'pau2022@gmail.com',          'oviedo2874', 2),
    (41100111, 'Valentin','Valentin',  'valentin_2012@gmail.com',    'valen12875', 2);

-- Insertar domicilios para los usuarios adicionales (11..20)
-- Los id_usuario de estos usuarios serán 11..20 respectivamente
INSERT INTO domicilio (direccion, ciudad, nombre_domicilio, id_usuario) VALUES
    ('Av. San Martin 100',   'Buenos Aires', 'Casa Roberto',   11),
    ('Calle Tribu 200',      'Rosario',       'Casa Marcelo',  12),
    ('Av. Merida 300',       'Córdoba',       'Casa Lucia',    13),
    ('Calle Bri 400',        'Buenos Aires',  'Casa Mariano',  14),
    ('Calle Vazques 500',    'Mendoza',       'Casa Julio',    15),
    ('Calle Perez 600',      'Buenos Aires',  'Casa Ricardo',  16),
    ('Calle Torres 700',     'Rosario',       'Casa Analia',   17),
    ('Calle Lopez 800',      'Salta',         'Casa Paola',    18),
    ('Calle Pau 900',        'Córdoba',       'Casa Paula',    19),
    ('Calle Valentin 1000',  'Buenos Aires',  'Casa Valentin', 20);

-- Insertar dispositivos adicionales para los nuevos domicilios
-- Reutilizamos las mismas etiquetas y tipos pero asignándolas a los domicilios 11..13 para ilustrar
INSERT INTO dispositivo (id_domicilio, id_tipo, estado, etiqueta) VALUES
    (11, 1, 'activo', 'Detector de Gas'),
    (11, 2, 'activo', 'Enchufe Inteligente'),
    (12, 1, 'activo', 'Sensor de Vibración'),
    (12, 3, 'activo', 'Cámara Exterior'),
    (13, 2, 'activo', 'Persiana Automática'),
    (13, 1, 'activo', 'Sensor de Lluvia'),
    (12, 2, 'activo', 'Riego Automático'),
    (11, 2, 'activo', 'Sirena Inteligente'),
    (13, 1, 'activo', 'Medidor de Energía'),
    (12, 3, 'activo', 'Cámara Interior');

-- Insertar automatizaciones adicionales para los nuevos domicilios
INSERT INTO automatizacion (id_domicilio, nombre, accion, estado, hora_encendido, hora_apagado) VALUES
    (11, 'Alarma Gas',           'Apagar gas si se detecta fuga',             TRUE, '18:00:00', NULL),
    (12, 'Luz Entrada',          'Encender luz exterior al anochecer',        TRUE, '19:30:00', NULL),
    (13, 'Riego Jardín',         'Activar riego a las 07:00 horas',           TRUE, '07:00:00', NULL),
    (14, 'Persiana Dormitorio',  'Bajar persianas al atardecer',              TRUE, '20:00:00', NULL),
    (15, 'Sirena Emergencia',    'Activar sirena ante intruso',               TRUE, '23:00:00', NULL),
    (16, 'Ventilador Auto',      'Encender ventilador al superar 30°C',       TRUE, '15:00:00', NULL),
    (17, 'Iluminación Patio',    'Encender luces del patio a las 21:00',      TRUE, '21:00:00', NULL),
    (18, 'Detección Humo',       'Enviar alerta si se detecta humo',          TRUE, '16:00:00', NULL),
    (19, 'Alarma Energía',       'Alertar si consumo supera 500W',            TRUE, '17:30:00', NULL),
    (20, 'Luces Automáticas',    'Apagar luces automáticamente a medianoche', TRUE, '00:00:00', NULL);

-- ====== Consultas de verificación ======

-- Mostrar todas las tablas
SHOW TABLES;

-- Describir estructura de las tablas principales
DESCRIBE usuario;
DESCRIBE domicilio;
DESCRIBE dispositivo;
DESCRIBE automatizacion;

-- Mostrar los primeros cinco usuarios
SELECT nombre, apellido, email
FROM usuario
ORDER BY id_usuario
LIMIT 5;

-- Actualizar la contraseña del usuario con id 1
UPDATE usuario
SET contrasena = 'prueba1234'
WHERE id_usuario = 1;

-- Actualizar el email del usuario con id 1
UPDATE usuario
SET email = 'danigonzalez@gmail.com'
WHERE id_usuario = 1;

-- Mostrar el nombre y tipo de los dispositivos pertenecientes al usuario con id = 1
SELECT d.etiqueta AS nombre, t.tipo_dispositivo AS tipo
FROM dispositivo d
JOIN tipo_dispositivo t ON d.id_tipo = t.id_tipo
JOIN domicilio dom ON d.id_domicilio = dom.id_domicilio
WHERE dom.id_usuario = 1;

-- Mostrar automatizaciones programadas a partir de las 15:00
SELECT nombre, accion, hora_encendido
FROM automatizacion
WHERE hora_encendido >= '15:00:00';

-- ====== Consultas multitablas adaptadas ======

-- 1. Mostrar todos los dispositivos con su dueño y tipo
SELECT u.nombre AS nombre_usuario, u.apellido AS apellido_usuario,
       d.etiqueta AS dispositivo, t.tipo_dispositivo AS tipo
FROM usuario u
JOIN domicilio dom ON u.id_usuario = dom.id_usuario
JOIN dispositivo d ON dom.id_domicilio = d.id_domicilio
JOIN tipo_dispositivo t ON d.id_tipo = t.id_tipo
ORDER BY u.id_usuario;

-- 2. Cantidad de dispositivos por usuario
SELECT u.nombre AS nombre_usuario, u.apellido AS apellido_usuario,
       COUNT(d.id_dispositivo) AS cantidad_dispositivos
FROM usuario u
JOIN domicilio dom ON u.id_usuario = dom.id_usuario
LEFT JOIN dispositivo d ON dom.id_domicilio = d.id_domicilio
GROUP BY u.id_usuario
ORDER BY cantidad_dispositivos DESC;

-- 3. Cantidad de automatizaciones por usuario
SELECT u.nombre AS nombre_usuario, u.apellido AS apellido_usuario,
       COUNT(a.id_automatizacion) AS cantidad_automatizacion
FROM usuario u
JOIN domicilio dom ON u.id_usuario = dom.id_usuario
LEFT JOIN automatizacion a ON dom.id_domicilio = a.id_domicilio
GROUP BY u.id_usuario
ORDER BY cantidad_automatizacion DESC;

-- 4. Usuarios con más de 2 dispositivos
SELECT u.nombre AS nombre_usuario, u.apellido AS apellido_usuario
FROM usuario u
WHERE u.id_usuario IN (
    SELECT dom.id_usuario
    FROM domicilio dom
    JOIN dispositivo d ON dom.id_domicilio = d.id_domicilio
    GROUP BY dom.id_usuario
    HAVING COUNT(d.id_dispositivo) > 2
);

-- 5. Usuarios sin dispositivos
SELECT u.nombre AS nombre_usuario, u.apellido AS apellido_usuario
FROM usuario u
LEFT JOIN domicilio dom ON u.id_usuario = dom.id_usuario
LEFT JOIN dispositivo d ON dom.id_domicilio = d.id_domicilio
GROUP BY u.id_usuario
HAVING COUNT(d.id_dispositivo) = 0;

-- 6. Dispositivo más reciente de cada usuario
SELECT u.nombre AS nombre_usuario, u.apellido AS apellido_usuario,
       d.etiqueta AS dispositivo_reciente, d.id_dispositivo
FROM usuario u
JOIN domicilio dom ON u.id_usuario = dom.id_usuario
JOIN dispositivo d ON dom.id_domicilio = d.id_domicilio
WHERE d.id_dispositivo = (
    SELECT MAX(d2.id_dispositivo)
    FROM domicilio dom2
    JOIN dispositivo d2 ON dom2.id_domicilio = d2.id_domicilio
    WHERE dom2.id_usuario = u.id_usuario
);

-- 7. Listado de automatizaciones con detalles del usuario y domicilio
SELECT a.nombre AS automatizacion, a.accion, a.hora_encendido,
       u.nombre AS nombre_usuario, u.apellido AS apellido_usuario,
       dom.nombre_domicilio
FROM automatizacion a
JOIN domicilio dom ON a.id_domicilio = dom.id_domicilio
JOIN usuario u ON dom.id_usuario = u.id_usuario
ORDER BY a.id_automatizacion;