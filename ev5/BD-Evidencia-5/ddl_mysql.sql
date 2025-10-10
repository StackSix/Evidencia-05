-- DDL Data Definition Language
-- Órdenes que crean/modifican la BD y sus objetos

CREATE DATABASE IF NOT EXISTS smarthome_ev5
  CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE smarthome_ev5;

-- Limpieza en orden inverso de dependencias
DROP TABLE IF EXISTS evento_dispositivo;
DROP TABLE IF EXISTS camara;
DROP TABLE IF EXISTS dispositivos;
DROP TABLE IF EXISTS email;
DROP TABLE IF EXISTS usuario;

-- usuario (Admin se representa por rol y permisos)
CREATE TABLE usuario (
  id               INT AUTO_INCREMENT PRIMARY KEY,
  nombre           VARCHAR(120)       NOT NULL,
  contraseña_hash  VARCHAR(255)       NOT NULL,
  rol              ENUM('user','admin') NOT NULL DEFAULT 'user',
  permisos         BOOLEAN            NOT NULL DEFAULT FALSE,
  created_at       TIMESTAMP          NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- email (composición 1–1 con usuario)
CREATE TABLE email (
  usuario_id       INT             NOT NULL,
  direccion_email  VARCHAR(190)    NOT NULL,
  PRIMARY KEY (usuario_id),
  UNIQUE KEY uq_email_direccion (direccion_email),
  CONSTRAINT fk_email_usuario
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- dispositivos (agregación 1–N con usuario)
CREATE TABLE dispositivos (
  id                  INT            NOT NULL,
  tipo                VARCHAR(255)   NOT NULL,                -- p.ej. 'CAMARA'
  estado_dispositivo  VARCHAR(255)   NOT NULL DEFAULT 'OFF',  -- o ENUM('ON','OFF')
  usuario_id          INT            NOT NULL,
  PRIMARY KEY (id),
  KEY idx_disp_usuario (usuario_id),
  CONSTRAINT fk_disp_usuario
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- camara (subclase 1–1 de dispositivos; PK=FK)
CREATE TABLE camara (
  dispositivo_id         INT             NOT NULL,
  nombre                 VARCHAR(255)    NOT NULL,
  modelo                 VARCHAR(120)    NOT NULL,
  grabacion_modo         ENUM('AUTO','MANUAL') NOT NULL DEFAULT 'AUTO',
  estado_automatizacion  BOOLEAN         NOT NULL DEFAULT FALSE,
  PRIMARY KEY (dispositivo_id),
  CONSTRAINT fk_camara_dispositivo
    FOREIGN KEY (dispositivo_id) REFERENCES dispositivos(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- evento_dispositivo (agregación 1–N con camara)
CREATE TABLE evento_dispositivo (
  id                     INT AUTO_INCREMENT PRIMARY KEY,
  camara_id              INT            NOT NULL,
  evento                 VARCHAR(100)   NOT NULL,
  ocurrido_en            TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  notificacion_enviada   BOOLEAN        NOT NULL DEFAULT FALSE,
  CONSTRAINT fk_evento_camara
    FOREIGN KEY (camara_id) REFERENCES camara(dispositivo_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB;


CREATE INDEX idx_email_direccion         ON email(direccion_email);
CREATE INDEX idx_evento_camara_ocurrido  ON evento_dispositivo(camara_id, ocurrido_en);
