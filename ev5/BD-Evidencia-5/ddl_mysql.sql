-- DDL Data Definition Language
-- Órdenes que crean/modifican la BD y sus objetos

CREATE DATABASE IF NOT EXISTS smarthome_ev5
  CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE smarthome_ev5;

CREATE TABLE rol (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
)

CREATE TABLE gestor_usuario (
    id_gestor_usuario INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(100)
)

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
)

CREATE TABLE gestor_domicilio (
    id_gestor_domicilio INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    descripcion VARCHAR(100),
    CONSTRAINT fk_gestor_domicilio_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario) ON DELETE CASCADE
)

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
)

CREATE TABLE gestor_dispositivo (
    id_gestor_dispositivo INT AUTO_INCREMENT PRIMARY KEY,
    id_domicilio INT NOT NULL UNIQUE,
    descripcion VARCHAR(100),
    CONSTRAINT fk_gestor_dispositivo_domicilio FOREIGN KEY (id_domicilio)
        REFERENCES domicilio(id_domicilio) ON DELETE CASCADE
)

CREATE TABLE tipos_dispositivos (
    id_tipo INT AUTO_INCREMENT PRIMARY KEY,
    tipo_dispositivo VARCHAR(100) NOT NULL
)

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
)

CREATE TABLE gestor_automatizacion (
    id_gestor_automatizacion INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(100)
)

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
)

SHOW TABLES;













CREATE TABLE dispositivo (
    id_dispositivo INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    fecha_registro DATE,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE notificaciones (
    id_notificaciones INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    mensaje VARCHAR(200) NOT NULL,
    fecha_hora DATETIME,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE automatizacion (
    id_automatizacion INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_dispositivo INT NOT NULL,
    condicion VARCHAR(50) NOT NULL,
    fecha_hora DATETIME,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_dispositivo) REFERENCES dispositivo(id_dispositivo)
);

SHOW TABLES;