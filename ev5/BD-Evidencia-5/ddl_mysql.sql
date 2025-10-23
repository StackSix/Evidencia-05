CREATE DATABASE IF NOT EXISTS bowtbpbberdfnkr3zske
  CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE bowtbpbberdfnkr3zske;

CREATE TABLE rol (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    rol VARCHAR(100) NOT NULL
);

CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    dni INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    rol VARCHAR(100) NOT NULL
    
);

CREATE TABLE domicilio (
    id_domicilio INT AUTO_INCREMENT PRIMARY KEY,
    direccion VARCHAR(200) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    nombre_domicilio VARCHAR(100) NOT NULL,
    id_usuario INT NOT NULL,
    CONSTRAINT fk_domicilio_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE tipo_dispositivo (
    id_tipo INT AUTO_INCREMENT PRIMARY KEY,
    tipo_dispositivo VARCHAR(100) NOT NULL
);

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
);

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
);

SHOW TABLES;