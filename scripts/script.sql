DROP DATABASE IF EXISTS db_universidad;
CREATE DATABASE db_universidad;
USE db_universidad;

CREATE TABLE rol(
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL
);

CREATE TABLE curso(
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(250) NOT NULL,
  horas_semanales DECIMAL(5,2) NOT NULL,
  creditos DECIMAL(5,2) NOT NULL,
  modalidad char(1) NOT NULL
);

CREATE TABLE usuario(
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(20) NOT NULL,
  pass VARCHAR(20) NOT NULL,
  nombre VARCHAR(40) NOT NULL,
  paterno VARCHAR(60) NOT NULL,
  materno VARCHAR(60) NOT NULL,
  sexo char(1) NOT NULL,
  correo VARCHAR(120) NOT NULL,  
  rol_id INT,
  activo BOOLEAN DEFAULT TRUE,
  FOREIGN KEY (rol_id) REFERENCES rol(id)
);

CREATE TABLE usuario_curso(
	id INT AUTO_INCREMENT PRIMARY KEY,
	usuario_id INT NOT NULL,
    curso_id INT NOT NULL,
	activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id),
	FOREIGN KEY (curso_id) REFERENCES curso(id)
);


CREATE TABLE criterio_evaluacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    curso_id INT NOT NULL,
    nombre_criterio VARCHAR(100) NOT NULL,
    orden INT NOT NULL,
    porcentaje DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (curso_id) REFERENCES curso(id)
);

CREATE TABLE nota (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_curso_id INT NOT NULL,
    criterio_id INT NOT NULL,
    nota DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (usuario_curso_id) REFERENCES usuario_curso(id),
    FOREIGN KEY (criterio_id) REFERENCES criterio_evaluacion(id)
);


INSERT INTO rol (nombre) VALUES ('ALUMNO');
INSERT INTO rol (nombre) VALUES ('PROFESOR');

INSERT INTO usuario (username, pass, nombre, paterno, materno,sexo,correo, rol_id) 
VALUES 
  ('RPRADA', 'Marco1415', 'RICARDO ENRIQUE', 'PRADA', 'GUERRA','M','rprada@hotmail.com', 2),
  ('JMORALES', 'Marco1415', 'JUAN JOSÉ MORALES', 'MORALES', 'VELASQUEZ','M','jmorales@hotmail.com', 1),
  ('NLOPEZO', 'Marco1415', 'NIKOL', 'LOPEZ', 'OCHOA','F','nlopezo@hotmail.com', 1);
  
INSERT INTO curso (nombre,horas_semanales,creditos,modalidad) VALUES ('Taller de programación (1I50N)',4,3,'P');
INSERT INTO curso (nombre,horas_semanales,creditos,modalidad) VALUES ('Herramientas informáticas para la toma de decisiones (1I04N)',2,2,'V');
INSERT INTO curso (nombre,horas_semanales,creditos,modalidad) VALUES ('Administración y organización de empresas (1I27N)',3,3,'V');
INSERT INTO curso (nombre,horas_semanales,creditos,modalidad) VALUES ('Investigación académica (1N02C)',4,4,'V');
INSERT INTO curso (nombre,horas_semanales,creditos,modalidad) VALUES ('Estadística descriptiva y probabilidades (1S21V)',3,3,'V');
INSERT INTO curso (nombre,horas_semanales,creditos,modalidad) VALUES ('Inglés III (1N08I)',3,3,'V');

INSERT INTO usuario_curso (usuario_id,curso_id)
VALUES (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(3,1),(3,2),(3,3);


-- Inserts para criterios de evaluación del curso 'Herramientas informáticas para la toma de decisiones (1I04N)'
INSERT INTO criterio_evaluacion (curso_id, nombre_criterio, orden, porcentaje) 
VALUES 
(2, 'Práctica calificada 1 (PC1)', 1, 20.00),
(2, 'Práctica calificada 2 (PC2)',2, 20.00),
(2, 'Participación en clase (PA)', 3, 30.00),
(2, 'Examen final individual (EXFI)', 4, 30.00);

-- Inserts para criterios de evaluación del curso 'Administración y organización de empresas (1I27N)'
INSERT INTO criterio_evaluacion (curso_id, nombre_criterio, orden, porcentaje) 
VALUES 
(3, 'Avance de proyecto final 1 (APF1)', 1, 20.00),
(3, 'Avance de proyecto final 2 (APF2)', 2, 20.00),
(3, 'Avance de proyecto final 3 (APF3)', 3, 20.00),
(3, 'Participación en clase (PA)', 4, 10.00),
(3, 'Proyecto final (PROY)', 5, 30.00);

-- Inserts para criterios de evaluación del curso 'Taller de programación (1I50N)'
INSERT INTO criterio_evaluacion (curso_id, nombre_criterio, orden, porcentaje) 
VALUES 
(1, 'Práctica calificada 1 (PC1)', 1, 20.00),
(1, 'Práctica calificada 2 (PC2)', 2, 20.00),
(1, 'Práctica calificada 3 (PC3)', 3, 20.00), 
(1, 'Participación en clase (PA)', 4, 10.00), 
(1, 'Proyecto final (PROY)', 5, 30.00);

-- Inserts para criterios de evaluación del curso 'Inglés III (1N08I)'
INSERT INTO criterio_evaluacion (curso_id, nombre_criterio, orden, porcentaje) 
VALUES 
(6, 'Participación en clase (PA)', 4, 35.00),
(6, 'Proyecto final (PROY)', 5, 20.00),
(6, 'Tarea académica 1 (TA1)', 1, 15.00),
(6, 'Tarea académica 2 (TA2)', 2, 15.00),
(6, 'Tarea académica 3 (TA3)',3, 15.00);

-- Inserts para criterios de evaluación del curso 'Estadística descriptiva y probabilidades (1S21V)'
INSERT INTO criterio_evaluacion (curso_id, nombre_criterio, orden, porcentaje) 
VALUES 
(5, 'Práctica calificada 1 (PC1)', 1, 10.00),
(5, 'Práctica calificada 2 (PC2)', 2, 10.00),
(5, 'Avance de proyecto final (APF)', 3, 15.00),
(5, 'Práctica calificada 3 (PC3)', 4, 15.00),
(5, 'Práctica calificada 4 (PC4)', 5, 15.00),
(5, 'Participación en clase (PA)', 6, 15.00),
(5, 'Proyecto final (PROY)', 7, 20.00);

-- Inserts para criterios de evaluación del curso 'Investigación académica (1N02C)'
INSERT INTO criterio_evaluacion (curso_id, nombre_criterio, orden, porcentaje) 
VALUES 
(4, 'Avance de informe 1 (AIF1)', 1, 20.00),
(4, 'Avance de informe 2 (AIF2)', 2, 20.00),
(4, 'Avance de informe 3 (AIF3)', 3, 20.00),
(4, 'Informe final (IF)', 4, 40.00);


SELECT * FROM usuario u WHERE u.username='RPRADA';


