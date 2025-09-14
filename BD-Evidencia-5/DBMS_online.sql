-- Listo para copiar y pegar en MySQL 8 (OneCompiler)

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS evento_dispositivo;
DROP TABLE IF EXISTS camara;
DROP TABLE IF EXISTS dispositivos;
DROP TABLE IF EXISTS email;
DROP TABLE IF EXISTS usuario;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE usuario (
  id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nombre          VARCHAR(120)      NOT NULL,
  contraseña_hash   VARCHAR(255)      NOT NULL,
  rol             ENUM('user','admin') NOT NULL DEFAULT 'user',
  permisos        BOOLEAN           NULL,
  created_at      TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE email (
  usuario_id        INT UNSIGNED NOT NULL,
  direccion_email   VARCHAR(255) NOT NULL,
  PRIMARY KEY (usuario_id),
  UNIQUE KEY uq_email_direccion (direccion_email),
  CONSTRAINT fk_email_usuario
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
    ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE dispositivos (
  id                  BIGINT UNSIGNED PRIMARY KEY,
  tipo                ENUM('CAMARA','SENSOR','OTRO') NOT NULL,
  estado_dispositivo  ENUM('ON','OFF') NOT NULL,
  usuario_id          INT UNSIGNED NOT NULL,
  CONSTRAINT fk_dispositivo_usuario
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE camara (
  dispositivo_id        BIGINT UNSIGNED PRIMARY KEY,
  nombre                VARCHAR(120) NOT NULL,
  modelo                VARCHAR(60)  NOT NULL,
  grabacion_modo        ENUM('AUTO','MANUAL') NOT NULL,
  estado_automatizacion BOOLEAN NOT NULL DEFAULT FALSE,
  CONSTRAINT fk_camara_dispositivo
    FOREIGN KEY (dispositivo_id) REFERENCES dispositivos(id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE evento_dispositivo (
  id                      BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  camara_id               BIGINT UNSIGNED NOT NULL,
  evento                  ENUM('MOTION','SOUND','MANUAL_ON','MANUAL_OFF') NOT NULL,
  ocurrido_en             TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  notificacion_enviada    BOOLEAN NOT NULL DEFAULT FALSE,
  CONSTRAINT fk_evento_camara
    FOREIGN KEY (camara_id) REFERENCES camara(dispositivo_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

-- ===== DML =====

INSERT INTO usuario (id, nombre, password_hash, rol, permisos)
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
  (10, 'Nicolás Román',    'pbkdf2$120000$aaA$hA', 'user',  FALSE);

INSERT INTO email (usuario_id, direccion_email)
VALUES
  (1, 'daniel@gmail.com'),
  (2, 'ana@yahoo.com'),
  (3, 'luis@hotmail.com'),
  (4, 'carla@icloud.com'),
  (5, 'nahir@live.com'),
  (6, 'sofia@gmail.com'),
  (7, 'root@hotmail.com'),
  (8, 'nightop@yahoo.com.ar'),
  (9, 'dayop@gmail.com'),
  (10,'nicolas.roman@gmail.com');

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

INSERT INTO camara (dispositivo_id, nombre, modelo, grabacion_modo, estado_automatizacion)
VALUES
  (101, 'Patio Trasero',    'X1', 'AUTO',   TRUE),
  (102, 'Entrada Principal','X2', 'MANUAL', FALSE),
  (103, 'Garage',           'X1', 'AUTO',   TRUE),
  (104, 'Cocina',           'X3', 'AUTO',   TRUE),
  (105, 'Living',           'X2', 'MANUAL', FALSE),
  (106, 'Balcón',           'X1', 'AUTO',   TRUE),
  (107, 'Porch',            'X4', 'AUTO',   TRUE),
  (108, 'Oficina',          'X3', 'MANUAL', FALSE),
  (109, 'Depósito',         'X5', 'AUTO',   TRUE),
  (110, 'Terraza',          'X2', 'AUTO',   TRUE);

INSERT INTO evento_dispositivo (id, camara_id, evento, ocurrido_en, notificacion_enviada)
VALUES
  (1001, 101, 'MOTION',     NOW() - INTERVAL 2 DAY,   TRUE),
  (1002, 101, 'MOTION',     NOW() - INTERVAL 1 DAY,   TRUE),
  (1003, 102, 'MANUAL_ON',  NOW() - INTERVAL 12 HOUR, FALSE),
  (1004, 102, 'MANUAL_OFF', NOW() - INTERVAL 11 HOUR, FALSE),
  (1005, 103, 'MOTION',     NOW() - INTERVAL 3 HOUR,  TRUE),
  (1006, 104, 'MOTION',     NOW() - INTERVAL 5 HOUR,  TRUE),
  (1007, 105, 'SOUND',      NOW() - INTERVAL 9 HOUR,  FALSE),
  (1008, 106, 'MOTION',     NOW() - INTERVAL 7 HOUR,  TRUE),
  (1009, 107, 'MOTION',     NOW() - INTERVAL 1 HOUR,  TRUE),
  (1010, 107, 'SOUND',      NOW() - INTERVAL 50 MINUTE, TRUE),
  (1011, 108, 'MANUAL_ON',  NOW() - INTERVAL 2 HOUR,  FALSE),
  (1012, 108, 'MANUAL_OFF', NOW() - INTERVAL 90 MINUTE, FALSE),
  (1013, 109, 'MOTION',     NOW() - INTERVAL 30 MINUTE, TRUE),
  (1014, 110, 'MOTION',     NOW() - INTERVAL 10 MINUTE, TRUE),
  (1015, 110, 'SOUND',      NOW() - INTERVAL 5 MINUTE,  TRUE);

-- ===== Verificación =====

-- Tablas
SHOW TABLES;

DESCRIBE usuario;
DESCRIBE email;
DESCRIBE dispositivos;
DESCRIBE camara;
DESCRIBE evento_dispositivo;

-- Consultas simples
SELECT id, nombre, rol, permisos, created_at
FROM usuario
ORDER BY id;

SELECT usuario_id, direccion_email
FROM email
ORDER BY usuario_id;

SELECT id, tipo, estado_dispositivo, usuario_id
FROM dispositivos
ORDER BY id;

SELECT dispositivo_id, nombre, modelo, grabacion_modo, estado_automatizacion
FROM camara
ORDER BY dispositivo_id;

SELECT id, camara_id, evento, ocurrido_en, notificacion_enviada
FROM evento_dispositivo
ORDER BY ocurrido_en DESC;

-- JOIN
SELECT u.id AS usuario_id, u.nombre, e.direccion_email,
       d.id AS dispositivo_id, c.nombre AS camara, d.estado_dispositivo
FROM usuario u
JOIN email e           ON e.usuario_id = u.id
JOIN dispositivos d    ON d.usuario_id = u.id
JOIN camara c          ON c.dispositivo_id = d.id
ORDER BY u.id, d.id;
