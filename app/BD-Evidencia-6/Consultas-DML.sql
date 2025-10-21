
INSERT INTO usuario (dni, nombre, apellido, email, contrasena, id_rol) VALUES
    (40111222, 'roberto', 'Volm',      'roberto_volm@hotmail.com',   '1234567',   2),
    (40222333, 'marcelo',   'Tribu',     'marcelo_tribu@hotmail.com','fran23412345',2),
    (40333444, 'Lucia',    'castelli',    'lucia_castelli@gmail.com',  '1236luc24', 2),
    (40444555, 'Mariano',  'hernandez',       'marianoher@hotmail.com',  '45mariano12',2),
    (40555666, 'Julio',    'agosto',   'julioagosto@hotmail.com','juedo1238', 2),
    (40666777, 'Ricardo',  'roca',     'ricardoroca@hotmail.com','1des1239',  1),
    (40777888, 'Analia',   'Torres',    'anatorres@hotmail.com',   'ju231240',  2),
    (40888999, 'Paola',    'Lopez',     'paola_lopez@hotmail.com', 'pao1241',   2),
    (40999000, 'Paula',    'oviedo',       'pau2022@gmail.com',       'oviedo2874',2),
    (41100111, 'Valentin', 'Valentin',  'valentin_2012@gmail.com', 'valen12875',2);

INSERT INTO domicilio (direccion, ciudad, nombre_domicilio, id_usuario) VALUES
    ('Av. San Martin 100',   'Buenos Aires', 'Casa Gabriela', 11),
    ('Calle Tribu 200',      'Rosario',       'Casa Franco',   12),
    ('Av. Merida 300',       'Córdoba',       'Casa Lucia',    13),
    ('Calle Bri 400',        'Buenos Aires',  'Casa Mariano',  14),
    ('Calle Vazques 500',    'Mendoza',       'Casa Julio',    15),
    ('Calle Perez 600',      'Buenos Aires',  'Casa Ricardo',  16),
    ('Calle Torres 700',     'Rosario',       'Casa Analia',   17),
    ('Calle Lopez 800',      'Salta',         'Casa Paola',    18),
    ('Calle Pau 900',        'Córdoba',       'Casa Paula',    19),
    ('Calle Valentin 1000',  'Buenos Aires',  'Casa Valentin', 20);

INSERT INTO dispositivo (id_domicilio, id_tipo, estado, etiqueta) VALUES
    (1, 1, 'activo', 'Detector de Gas'),
    (1, 2, 'activo', 'Enchufe Inteligente'),
    (2, 1, 'activo', 'Sensor de Vibración'),
    (2, 3, 'activo', 'Cámara Exterior'),
    (3, 2, 'activo', 'Persiana Automática'),
    (3, 1, 'activo', 'Sensor de Lluvia'),
    (2, 2, 'activo', 'Riego Automático'),
    (1, 2, 'activo', 'Sirena Inteligente'),
    (3, 1, 'activo', 'Medidor de Energía'),
    (2, 3, 'activo', 'Cámara Interior');

INSERT INTO automatizaciones (id_domicilio, nombre, accion, estado, hora_encendido, hora_apagado) VALUES
    (11, 'Alarma Gas',           'Apagar gas si se detecta fuga',            TRUE, '18:00:00', NULL),
    (12, 'Luz Entrada',          'Encender luz exterior al anochecer',       TRUE, '19:30:00', NULL),
    (13, 'Riego Jardín',         'Activar riego a las 07:00 horas',          TRUE, '07:00:00', NULL),
    (14, 'Persiana Dormitorio',  'Bajar persianas al atardecer',             TRUE, '20:00:00', NULL),
    (15, 'Sirena Emergencia',    'Activar sirena ante intruso',              TRUE, '23:00:00', NULL),
    (16, 'Ventilador Auto',      'Encender ventilador al superar 30°C',      TRUE, '15:00:00', NULL),
    (17, 'Iluminación Patio',    'Encender luces del patio a las 21:00',     TRUE, '21:00:00', NULL),
    (18, 'Detección Humo',       'Enviar alerta si se detecta humo',         TRUE, '16:00:00', NULL),
    (19, 'Alarma Energía',       'Alertar si consumo supera 500W',           TRUE, '17:30:00', NULL),
    (20, 'Luces Automáticas',    'Apagar luces automáticamente a medianoche',TRUE, '00:00:00', NULL);


-- Consultas multitablas adaptadas

-- 1. Mostrar todos los dispositivos con su dueño y tipo
SELECT u.nombre AS nombre_usuario, u.apellido AS apellido_usuario,
       d.etiqueta AS dispositivo, t.tipo_dispositivo AS tipo
FROM usuario u
JOIN domicilio dom ON u.id_usuario = dom.id_usuario
JOIN dispositivo d ON dom.id_domicilio = d.id_domicilio
JOIN tipos_dispositivos t ON d.id_tipo = t.id_tipo
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
       COUNT(a.id_automatizacion) AS cantidad_automatizaciones
FROM usuario u
JOIN domicilio dom ON u.id_usuario = dom.id_usuario
LEFT JOIN automatizaciones a ON dom.id_domicilio = a.id_domicilio
GROUP BY u.id_usuario
ORDER BY cantidad_automatizaciones DESC;

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
FROM automatizaciones a
JOIN domicilio dom ON a.id_domicilio = dom.id_domicilio
JOIN usuario u ON dom.id_usuario = u.id_usuario
ORDER BY a.id_automatizacion;