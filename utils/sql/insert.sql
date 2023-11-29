-- -----------------
-- Insert profile --
-- -----------------
INSERT INTO profile (name)
SELECT 'estudiante'
UNION
SELECT 'profesor'
UNION
SELECT 'administrador'
UNION
SELECT 'super_administrador';
-- ----------------
-- Insert career --
-- ----------------
INSERT INTO career (name)
SELECT 'Administración de Empresas'
UNION
SELECT 'Ingeniería de Sistemas'
UNION
SELECT 'Ingeniería Industrial'
UNION
SELECT 'Licenciatura en Pedagogía de la Primera Infancia'
UNION
SELECT 'Negocios Internacionales'
UNION
SELECT 'Psicología'
UNION
SELECT 'Técnica Profesional en Procesos Contables'
UNION
SELECT 'Técnica Profesional en Procesos Logísticos y de Comercio Exterior'
UNION
SELECT 'Técnica Profesional en Procesos Turísticos y Hoteleros'
UNION
SELECT 'Derecho';
-- ----------------------
-- Insert content_type --
-- ----------------------
INSERT INTO content_type (model)
SELECT 'career'
UNION
SELECT 'permission'
UNION
SELECT 'profile'
UNION
SELECT 'user';
-- --------------------
-- Insert permission --
-- --------------------
INSERT INTO permission (
        content_type_id,
        code_name,
        description
    )
SELECT id,
    Concat(model, ':create'),
    'Crear permiso'
FROM content_type
WHERE model = 'permission'
UNION
SELECT id,
    Concat(model, ':read'),
    'Ver permisos'
FROM content_type
WHERE model = 'permission'
UNION
SELECT id,
    Concat(model, ':update'),
    'Editar permiso'
FROM content_type
WHERE model = 'permission'
UNION
SELECT id,
    Concat(model, ':delete'),
    'Eliminar permiso'
FROM content_type
WHERE model = 'permission'
UNION
SELECT id,
    Concat(model, ':create'),
    'Crear usuario'
FROM content_type
WHERE model = 'user'
UNION
SELECT id,
    Concat(model, ':read'),
    'Ver usuarios'
FROM content_type
WHERE model = 'user'
UNION
SELECT id,
    Concat(model, ':update'),
    'Editar usuario'
FROM content_type
WHERE model = 'user'
UNION
SELECT id,
    Concat(model, ':delete'),
    'Eliminar usuario'
FROM content_type
WHERE model = 'user'
UNION
SELECT id,
    Concat(model, ':create'),
    'Crear perfil'
FROM content_type
WHERE model = 'profile'
UNION
SELECT id,
    Concat(model, ':read'),
    'Ver perfiles'
FROM content_type
WHERE model = 'profile'
UNION
SELECT id,
    Concat(model, ':update'),
    'Editar perfil'
FROM content_type
WHERE model = 'profile'
UNION
SELECT id,
    Concat(model, ':delete'),
    'Eliminar perfil'
FROM content_type
WHERE model = 'profile'
UNION
SELECT id,
    Concat(model, ':create'),
    'Crear carrera'
FROM content_type
WHERE model = 'career'
UNION
SELECT id,
    Concat(model, ':read'),
    'Ver carreras'
FROM content_type
WHERE model = 'career'
UNION
SELECT id,
    Concat(model, ':update'),
    'Editar carrera'
FROM content_type
WHERE model = 'career'
UNION
SELECT id,
    Concat(model, ':delete'),
    'Eliminar carrera'
FROM content_type
WHERE model = 'career';
-- -------------------
-- Insert type_room --
-- -------------------
INSERT INTO type_room (name)
SELECT 'Sala de sistema'
UNION
SELECT 'Laboratorio'
UNION
SELECT 'Aula de clase'
UNION
SELECT 'Sede'
UNION
SELECT 'Salón';
-- --------------
-- Insert room --
-- --------------
INSERT INTO room (type_room_id, name, longitude, latitude)
SELECT id,
    'Sala Cisco #1',
    -75.56332592800794,
    6.247649725059612
FROM type_room
WHERE name = 'Sala de sistema'
UNION
SELECT id,
    'Laboratorio de física',
    -75.56332592800794,
    6.247649725059612
FROM type_room
WHERE name = 'Laboratorio'
UNION
SELECT id,
    'Aula #1',
    -75.56332592800794,
    6.247649725059612
FROM type_room
WHERE name = 'Aula de clase'
UNION
SELECT id,
    'Sede Bancolombia',
    -75.56332592800794,
    6.247649725059612
FROM type_room
WHERE name = 'Sede'
UNION
SELECT id,
    'Biblioteca',
    -75.56332592800794,
    6.247649725059612
FROM type_room
WHERE name = 'Salón';
-- -----------------------
-- Insert elements_room --
-- -----------------------
INSERT INTO elements_room (room_id, name)
SELECT id,
    'Registro Biblioteca'
FROM room
WHERE name = 'Biblioteca'
UNION
SELECT id,
    'Router #1'
FROM room
WHERE name = 'Sala Cisco #1'