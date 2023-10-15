-- -----------------
-- Insert profile --
-- -----------------
INSERT INTO profile (name)
	SELECT 'estudiante' UNION
	SELECT 'profesor' UNION
	SELECT 'administrador' UNION
	SELECT 'super_administrador';


-- ----------------
-- Insert career --
-- ----------------
INSERT INTO career (name)
	SELECT 'Administración de Empresas' UNION
	SELECT 'Ingeniería de Sistemas' UNION
	SELECT 'Ingeniería Industrial' UNION
	SELECT 'Licenciatura en Pedagogía de la Primera Infancia' UNION
	SELECT 'Negocios Internacionales' UNION
	SELECT 'Psicología' UNION
	SELECT 'Técnica Profesional en Procesos Contables' UNION
	SELECT 'Técnica Profesional en Procesos Logísticos y de Comercio Exterior' UNION
	SELECT 'Técnica Profesional en Procesos Turísticos y Hoteleros' UNION
	SELECT 'Derecho';


-- ----------------------
-- Insert content_type --
-- ----------------------
INSERT INTO content_type (model)
    SELECT 'career' UNION
	SELECT 'permission' UNION
	SELECT 'profile' UNION
	SELECT 'user';


-- --------------------
-- Insert permission --
-- --------------------
INSERT INTO permission (content_type_id, code_name, description)
	SELECT id, CONCAT(model, ':create'), 'Crear permiso' FROM content_type WHERE model = 'permission' UNION
	SELECT id, CONCAT(model, ':read'), 'Leer permiso' FROM content_type WHERE model = 'permission' UNION
	SELECT id, CONCAT(model, ':update'), 'Editar permiso' FROM content_type WHERE model = 'permission' UNION
	SELECT id, CONCAT(model, ':delete'), 'Eliminar permiso' FROM content_type WHERE model = 'permission' UNION
	SELECT id, CONCAT(model, ':create'), 'Crear usuario' FROM content_type WHERE model = 'user' UNION
	SELECT id, CONCAT(model, ':read'), 'Leer usuario' FROM content_type WHERE model = 'user' UNION
	SELECT id, CONCAT(model, ':update'), 'Editar usuario' FROM content_type WHERE model = 'user' UNION
	SELECT id, CONCAT(model, ':delete'), 'Eliminar usuario' FROM content_type WHERE model = 'user' UNION
	SELECT id, CONCAT(model, ':create'), 'Crear perfil' FROM content_type WHERE model = 'profile' UNION
	SELECT id, CONCAT(model, ':read'), 'Leer perfil' FROM content_type WHERE model = 'profile' UNION
	SELECT id, CONCAT(model, ':update'), 'Editar perfil' FROM content_type WHERE model = 'profile' UNION
	SELECT id, CONCAT(model, ':delete'), 'Eliminar perfil' FROM content_type WHERE model = 'profile' UNION
    SELECT id, CONCAT(model, ':create'), 'Crear carrera' FROM content_type WHERE model = 'career' UNION
	SELECT id, CONCAT(model, ':read'), 'Leer carrera' FROM content_type WHERE model = 'career' UNION
	SELECT id, CONCAT(model, ':update'), 'Editar carrera' FROM content_type WHERE model = 'career' UNION
	SELECT id, CONCAT(model, ':delete'), 'Eliminar carrera' FROM content_type WHERE model = 'career';
