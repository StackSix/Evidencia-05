# DDL Data Definition Language
# Ordenes que crean, modifican la base de datos y sus objetos


# 1
CREATE DATABASE IF NOT EXISTS smarthome_ev5
  CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE smarthome_ev5;

# usuario
CREATE TABLE usuario (
  id               INT AUTO_INCREMENT PRIMARY KEY,
  nombre           VARCHAR(120)       NOT NULL,
  contraseña_hash  VARCHAR(255)       NOT NULL,
  rol              BOOLEAN            NOT NULL DEFAULT false,
  permisos         BOOLEAN            NOT NULL DEFAULT FALSE,
  created_at       TIMESTAMP          NOT NULL DEFAULT CURRENT_TIMESTAMP
)

# email
CREATE TABLE email (
  usuario_id       INT             NOT NULL,
  direccion_email  VARCHAR(190)    NOT NULL,
  PRIMARY KEY (usuario_id),
  UNIQUE KEY uq_email_direccion (direccion_email),
  CONSTRAINT fk_email_usuario
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)

# dispositivos
CREATE TABLE dispositivos (
  id                INT            PRIMARY KEY,
  tipo              VARCHAR(255)   NOT NULL,
  estado_dispositivo VARCHAR(255)  NOT NULL DEFAULT 'OFF',
  usuario_id         INT              NOT NULL,
  PRIMARY KEY (id),
  KEY idx_disp_usuario (usuario_id),
  CONSTRAINT fk_disp_usuario
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
)

# camara (subcable de dispositivos)
CREATE TABLE camara (
  dispositivo_id        INT             NOT NULL,
  nombre               VARCHAR(255)   NOT NULL,
  modelo               VARCHAR(120)   NOT NULL,
  grabacion_modo        ENUM('AUTO','MANUAL') NOT NULL DEFAULT 'AUTO',
  estado_automatizacion BOOLEAN NOT NULL DEFAULT FALSE
  automation_enabled   BOOLEAN        NOT NULL DEFAULT FALSE,
    PRIMARY KEY (dispositivo_id),
    CONSTRAINT fk_camara_dispositivo
    FOREIGN KEY (dispositivo_id) REFERENCES dispositivos(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)


# EventoDispositivo
CREATE TABLE evento_dispositivo (
  camara_id              INT AUTO_INCREMENT PRIMARY KEY,
  evento                 VARCHAR(100)  NOT NULL,  
  ocurrido_en            TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  notificacion_enviada   BOOLEAN       NOT NULL DEFAULT FALSE,
  CONSTRAINT fk_evento_camara
    FOREIGN KEY (camara_id) REFERENCES camara(dispositivo_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)

CREATE INDEX idx_email_direccion         ON email(direccion_email);
CREATE INDEX idx_evento_camara_ocurrido  ON evento_dispositivo(camara_id, ocurrido_en);