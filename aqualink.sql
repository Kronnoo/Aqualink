-- Sistema AquaLink
-- Base de datos

DROP DATABASE IF EXISTS aqualink;

CREATE DATABASE aqualink
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE aqualink;

-- Niveles

CREATE TABLE nivel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    orden TINYINT NOT NULL UNIQUE,
    nombre VARCHAR(40) NOT NULL,
    descripcion VARCHAR(120)
);

-- Alumnos

CREATE TABLE alumno (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo CHAR(11) NOT NULL UNIQUE,
    nombre VARCHAR(60) NOT NULL,
    apellidos VARCHAR(80) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    nivel_id INT NOT NULL,
    tutor_nombre VARCHAR(100) NOT NULL,
    tutor_telefono VARCHAR(15) NOT NULL,
    fecha_alta DATE NOT NULL,
    activo TINYINT(1) NOT NULL DEFAULT 1,

    FOREIGN KEY (nivel_id) REFERENCES nivel(id)
);

-- Asistencias

CREATE TABLE asistencia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT NOT NULL,
    fecha DATE NOT NULL,
    registrada_por VARCHAR(150) NOT NULL,

    UNIQUE (alumno_id, fecha),

    FOREIGN KEY (alumno_id)
    REFERENCES alumno(id)
    ON DELETE CASCADE
);

-- Tiempos

CREATE TABLE tiempo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT NOT NULL,
    prueba VARCHAR(30) NOT NULL,
    segundos DECIMAL(6,2) NOT NULL,
    fecha DATE NOT NULL,

    FOREIGN KEY (alumno_id)
    REFERENCES alumno(id)
    ON DELETE CASCADE
);

-- Evaluaciones

CREATE TABLE evaluacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT NOT NULL,
    fecha DATE NOT NULL,

    area ENUM(
        'Tecnica',
        'Seguridad acuatica',
        'Desarrollo humano'
    ) NOT NULL,

    puntaje TINYINT NOT NULL CHECK (puntaje BETWEEN 1 AND 10),
    observacion VARCHAR(255),

    FOREIGN KEY (alumno_id)
    REFERENCES alumno(id)
    ON DELETE CASCADE
);

-- Incidentes

CREATE TABLE incidente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT NOT NULL,
    fecha DATE NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    accion_tomada VARCHAR(255) NOT NULL,

    FOREIGN KEY (alumno_id)
    REFERENCES alumno(id)
    ON DELETE CASCADE
);

-- Niveles

INSERT INTO nivel (orden, nombre, descripcion) VALUES
(1, 'Coral', 'Se familiariza con el agua y flota con apoyo.'),
(2, 'Camarón', 'Flota y patalea sin apoyo.'),
(3, 'Pez', 'Nada 25 m de crol y dorso.'),
(4, 'Delfin', 'Domina cuatro estilos y vueltas complejas.'),
(5, 'Tiburón', 'Entrena para competencias y mejores tiempos.');

-- 5 alumnos

INSERT INTO alumno
(codigo, nombre, apellidos, fecha_nacimiento, nivel_id,
 tutor_nombre, tutor_telefono, fecha_alta)
VALUES

('AQ-A1R8H2K', 'Ana Rosa', 'Hernández',
 '2012-05-14', 3, 'Laura Hernández',
 '7220000001', '2026-09-21'),

('AQ-E2H7L4M', 'Evelyn', 'Hernández',
 '2013-08-22', 3, 'Carlos Hernández',
 '7220000002', '2026-09-21'),

('AQ-J5P9L3N', 'Juan Pablo', 'Lom',
 '2012-11-09', 4, 'Mario Lom',
 '7220000003', '2026-09-21'),

('AQ-E4L8P6Q', 'Emiliano', 'López',
 '2014-03-18', 2, 'José López',
 '7220000004', '2026-09-21'),

('AQ-A7J2M5D', 'Arely Jasmin', 'Mandujano',
 '2013-07-30', 3, 'María Mandujano',
 '7220000005', '2026-09-21');

-- Asistencias

INSERT INTO asistencia
(alumno_id, fecha, registrada_por)
VALUES
(1, '2026-09-21', 'entrenador1'),
(1, '2026-09-23', 'entrenador1'),
(2, '2026-09-21', 'entrenador1'),
(2, '2026-09-23', 'entrenador1'),
(3, '2026-09-21', 'entrenador1'),
(4, '2026-09-21', 'entrenador1'),
(5, '2026-09-21', 'entrenador1');

-- 3 tiempos por alumno

INSERT INTO tiempo
(alumno_id, prueba, segundos, fecha)
VALUES

(1, '25 m libre', 31.20, '2026-08-24'),
(1, '25 m libre', 29.85, '2026-09-07'),
(1, '25 m libre', 28.40, '2026-09-21'),

(2, '25 m libre', 33.10, '2026-08-24'),
(2, '25 m libre', 31.75, '2026-09-07'),
(2, '25 m libre', 30.50, '2026-09-21'),

(3, '25 m libre', 25.80, '2026-08-24'),
(3, '25 m libre', 24.95, '2026-09-07'),
(3, '25 m libre', 23.70, '2026-09-21'),

(4, '25 m libre', 38.40, '2026-08-24'),
(4, '25 m libre', 36.90, '2026-09-07'),
(4, '25 m libre', 35.60, '2026-09-21'),

(5, '25 m libre', 30.90, '2026-08-24'),
(5, '25 m libre', 29.40, '2026-09-07'),
(5, '25 m libre', 28.75, '2026-09-21');

-- Evaluaciones

INSERT INTO evaluacion
(alumno_id, fecha, area, puntaje, observacion)
VALUES
(1, '2026-09-21', 'Tecnica', 8, 'Buena tecnica de nado.'),
(1, '2026-09-21', 'Desarrollo humano', 9, 'Apoya a sus compañeros.'),

(2, '2026-09-21', 'Tecnica', 8, 'Mejoro su respiracion.'),
(3, '2026-09-21', 'Tecnica', 9, 'Buen dominio de los estilos.'),
(4, '2026-09-21', 'Seguridad acuatica', 8, 'Sigue las indicaciones.'),
(5, '2026-09-21', 'Tecnica', 9, 'Buen progreso.');

-- Incidentes

INSERT INTO incidente
(alumno_id, fecha, descripcion, accion_tomada)
VALUES
(2, '2026-09-14',
 'Calambre en la pantorrilla',
 'Estiramiento y descanso 10 min.');

-- CONSULTA 1
-- Alumnos con su nivel

SELECT
    a.nombre,
    a.apellidos,
    n.nombre AS nivel
FROM alumno a
JOIN nivel n
ON a.nivel_id = n.id;

-- CONSULTA 2
-- Total de asistencias

SELECT
    a.nombre,
    COUNT(s.id) AS asistencias
FROM alumno a
LEFT JOIN asistencia s
ON s.alumno_id = a.id
GROUP BY a.id, a.nombre;

-- CONSULTA 3
-- Mejor tiempo de cada alumno

SELECT
    a.nombre,
    MIN(t.segundos) AS mejor_tiempo
FROM alumno a
JOIN tiempo t
ON t.alumno_id = a.id
WHERE t.prueba = '25 m libre'
GROUP BY a.id, a.nombre;

-- Crear el usuario 'aqualink' con su contraseña
CREATE USER IF NOT EXISTS 'aqualink'@'localhost' IDENTIFIED BY 'Aqua2026!';

-- Darle todos los permisos solo sobre la base de datos 'aqualink'
GRANT ALL PRIVILEGES ON aqualink.* TO 'aqualink'@'localhost';

-- Aplicar los cambios de permisos
FLUSH PRIVILEGES;