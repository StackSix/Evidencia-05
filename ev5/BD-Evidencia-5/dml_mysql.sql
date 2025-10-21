
USE bowtbpbberdfnkr3zske;

INSERT INTO rol (nombre) VALUES
    ('Admin'),
    ('Usuario');


INSERT INTO usuario (dni, nombre, apellido, email, contrasena, id_rol) VALUES
    (30111222, 'daniel',    'gonzalez', 'danigonzalez@hotmail.com',    '21345558', 2),
    (30222333, 'nicolas',   'romano',    'nico_romano@hotmail.com',    '13345558', 2),
    (30333444, 'Francisco', 'perez',     'franperez@hotmail.com',       '12367876', 2),
    (30444555, 'florencia','Bri',        'florenciabri@hotmail.com',    '12375466', 2),
    (30555666, 'luis',      'Vazques',   'luisvazques@hotmail.com',     '12345558', 2),
    (30666777, 'Marisa',    'Perez',     'mariperez@hotmail.com',       '12344559', 2),
    (30777888, 'Claudia',   'Torres',    'clautorres@hotmail.com',      '12765558', 2),
    (30888999, 'pepe',      'Lopez',     'pepe_lopez@hotmail.com',      '12345678', 2),
    (30999000, 'Pablo',     'juarez',    'pablito22@hotmail.com',       '19072874', 2),
    (31100111, 'Valentina', 'Gomez',     'valentina@gmail.com',         '12873545', 2);


INSERT INTO domicilio (direccion, ciudad, nombre_domicilio, id_usuario) VALUES
    ('Calle Falsa 123',      'san luis',       'Casa',             1),
    ('Av. Siemprevivas 742', 'Buenos Aires',   'Home',             2),
    ('Calle 13 #300',        'Córdoba',        'mi casa',          3),
    ('Calle 24 #400',        'Rosario',        'guarida',          4),
    ('Calle 76 #500',        'Mendoza',        'baticueva',        5),
    ('velez sarsfield #600', 'Salta',          'depto',            6),
    ('peru 320 #320',        'Buenos Aires',   'Casa alquiler',    7),
    ('la rioja #800',        'Buenos Aires',   'Casa 2',           8),
    ('dean funes #900',      'Córdoba',        'Casa vacaciones',  9),
    ('brasil #1000',         'Buenos Aires',   'Casa Valentina',  10);


INSERT INTO tipos_dispositivos (tipo_dispositivo) VALUES
    ('Sensor'),
    ('Actuador'),
    ('Cámara');


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

INSERT INTO automatizaciones (id_domicilio, nombre, accion, estado, hora_encendido, hora_apagado) VALUES
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


SELECT * FROM usuario;
SELECT * FROM domicilio;
SELECT * FROM dispositivo;
SELECT * FROM automatizaciones;


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
JOIN tipos_dispositivos t ON d.id_tipo = t.id_tipo
JOIN domicilio dom ON d.id_domicilio = dom.id_domicilio
WHERE dom.id_usuario = 1;



SELECT nombre, accion, hora_encendido
FROM automatizaciones
WHERE hora_encendido >= '15:00:00';