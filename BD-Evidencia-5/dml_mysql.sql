# DML Data Definition Language
# Ordenes que permiten agregar, modificar o eliminar datos a la base de datos.


USE smarthome_ev5;


# USUARIO 
# Nota: contraseña_hash son placeholders; en app real se usa PBKDF2
INSERT INTO usuario (id, nombre, contraseña_hash, rol, permisos)
VALUES
  (1,  'Daniel González',  'pbkdf2$120000$aa1$h1', 'user',  FALSE),
  (2,  'Ana Pérez',        'pbkdf2$120000$aa2$h2', 'user',  FALSE),
  (3,  'Luis Romero',      'pbkdf2$120000$aa3$h3', 'user',  FALSE),
  (4,  'Carla Suárez',     'pbkdf2$120000$aa4$h4', 'user',  FALSE),
  (5,  'Nahir Bustos',     'pbkdf2$120000$aa5$h5', 'user',  FALSE),
  (6,  'Sofía López',      'pbkdf2$120000$aa6$h6', 'user',  FALSE),
  (7,  'Admin Root',       'pbkdf2$120000$aa7$h7', 'admin', TRUE),
  (8,  'Operador Noche',   'pbkdf2$120000$aa8$h8', 'admin', TRUE),
  (9,  'Operador Día',     'pbkdf2$120000$aa9$h9', 'admin', TRUE),
  (10, 'Nicolas Roman',         'pbkdf2$120000$aaA$hA', 'user',  FALSE);

#EMAIL (1:1 con usuario)
INSERT INTO email (usuario_id, direccion_email)
VALUES
  (1, 'daniel@gmaill.com'),
  (2, 'ana@yahoo.com'),
  (3, 'luis@hotmail.com'),
  (4, 'carla@icloud.com'),
  (5, 'nahir@live.com'),
  (6, 'sofia@gmail.com'),
  (7, 'root@hotmail.com'),
  (8, 'nightop@yahoo.com.ar'),
  (9, 'dayop@gmail.com'),
  (10,'Nicolas_Roman@gmail.com');

#DISPOSITIVOS (agregación: usuario 1..N dispositivos)
INSERT INTO dispositivos (id, tipo, estado_dispositivo, usuario_id)
VALUES
  (101, 'CAMARA', 'OFF', 1),
  (102, 'CAMARA', 'ON',  1),
  (103, 'CAMARA', 'OFF', 2),
  (104, 'CAMARA', 'ON',  2),
  (105, 'CAMARA', 'OFF', 3),
  (106, 'CAMARA', 'OFF', 4),
  (107, 'CAMARA', 'ON',  5),
  (108, 'CAMARA', 'OFF', 6),
  (109, 'CAMARA', 'ON',  7),
  (110, 'CAMARA', 'OFF', 7);

  #CAMARA (agregación: usuario 1..N dispositivos)

INSERT INTO camara (dispositivo_id, nombre, modelo, grabacion_modo, estado_automatizacion)
VALUES
  (101, 'Patio Trasero',   'X1',  'AUTO',   TRUE),
  (102, 'Entrada Principal','X2',  'MANUAL', FALSE),
  (103, 'Garage',          'X1',  'AUTO',   TRUE),
  (104, 'Cocina',          'X3',  'AUTO',   TRUE),
  (105, 'Living',          'X2',  'MANUAL', FALSE),
  (106, 'Balcón',          'X1',  'AUTO',   TRUE),
  (107, 'Porch',           'X4',  'AUTO',   TRUE),
  (108, 'Oficina',         'X3',  'MANUAL', FALSE),
  (109, 'Depósito',        'X5',  'AUTO',   TRUE),
  (110, 'Terraza',         'X2',  'AUTO',   TRUE);

#EVENTO_DISPOSITIVO (agregación: camara 1..N eventos)
INSERT INTO evento_dispositivo (id, camara_id, evento, ocurrido_en, notificacion_enviada)
VALUES
  (1001, 101, 'MOTION',           NOW() - INTERVAL 2 DAY,  TRUE),
  (1002, 101, 'MOTION',           NOW() - INTERVAL 1 DAY,  TRUE),
  (1003, 102, 'MANUAL_ON',        NOW() - INTERVAL 12 HOUR, FALSE),
  (1004, 102, 'MANUAL_OFF',       NOW() - INTERVAL 11 HOUR, FALSE),
  (1005, 103, 'MOTION',           NOW() - INTERVAL 3 HOUR, TRUE),
  (1006, 104, 'MOTION',           NOW() - INTERVAL 5 HOUR, TRUE),
  (1007, 105, 'SOUND',            NOW() - INTERVAL 9 HOUR, FALSE),
  (1008, 106, 'MOTION',           NOW() - INTERVAL 7 HOUR, TRUE),
  (1009, 107, 'MOTION',           NOW() - INTERVAL 1 HOUR, TRUE),
  (1010, 107, 'SOUND',            NOW() - INTERVAL 50 MINUTE, TRUE),
  (1011, 108, 'MANUAL_ON',        NOW() - INTERVAL 2 HOUR, FALSE),
  (1012, 108, 'MANUAL_OFF',       NOW() - INTERVAL 90 MINUTE, FALSE),
  (1013, 109, 'MOTION',           NOW() - INTERVAL 30 MINUTE, TRUE),
  (1014, 110, 'MOTION',           NOW() - INTERVAL 10 MINUTE, TRUE),
  (1015, 110, 'SOUND',            NOW() - INTERVAL 5 MINUTE,  TRUE);


  SELECT id, nombre, rol, permisos, created_at
FROM usuario
ORDER BY id;

-- 2) Emails
SELECT usuario_id, direccion_email
FROM email
ORDER BY usuario_id;

-- 3) Dispositivos
SELECT id, tipo, estado_dispositivo, usuario_id
FROM dispositivos
ORDER BY id;

-- 4) Cámaras
SELECT dispositivo_id, nombre, modelo, grabacion_modo, estado_automatizacion
FROM camara
ORDER BY dispositivo_id;

-- 5) Eventos
SELECT id, camara_id, evento, ocurrido_en, notificacion_enviada
FROM evento_dispositivo
ORDER BY ocurrido_en DESC;

#JOIN

SELECT u.id AS usuario_id, u.nombre, e.direccion_email,
       d.id AS dispositivo_id, c.nombre AS camara, d.estado_dispositivo
FROM usuario u
JOIN email e           ON e.usuario_id = u.id
JOIN dispositivos d    ON d.usuario_id = u.id
JOIN camara c          ON c.dispositivo_id = d.id
ORDER BY u.id, d.id;