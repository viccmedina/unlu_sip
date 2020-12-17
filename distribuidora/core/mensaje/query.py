INSERTAR_NUEVO_MENSAJE = """ INSERT INTO mensaje (sender_id, recipient_id, body, read)
    VALUES ('{sender_id}', {recipient_id}, '{body}', 0)
"""

SELECT_OPERADORES="""
SELECT p.nombre as name
from persona p INNER JOIN usuario u ON u.persona_id = p.persona_id INNER JOIN usuario_rol ur ON ur.id = u.id INNER JOIN rol r ON r.rol_id = ur.rol_id
WHERE r.descripcion = "Operador";

"""

SELECT_ID_OPERADOR = """
SELECT u.id as id
FROM usuario u INNER JOIN usuario_rol ur ON ur.id = u.id INNER JOIN rol r ON r.rol_id = ur.rol_id where r.nombre = '{oper}';

"""

SELECT_TODOS_MIS_MENSAJES_ENVIADOS = """ SELECT * FROM mensaje
	WHERE sender_id='{usuario_id}' """

SELECT_TODOS_MIS_MENSAJES_RECIBIDOS = """ SELECT * FROM mensaje
	WHERE recipient_id='{usuario_id}' """


SELECT_MENSAJES_SIN_LEER = """ SELECT * FROM mensaje
	WHERE recipient_id='{usuario_id}' AND read=0 """

CANTIDAD_MSJS_SIN_LEER =  """SELECT COUNT(*) AS sin_leer
	FROM mensaje
	WHERE recipient_id='{usuario_id}' AND read=0 """

LEER_MENSAJE = """ UPDATE mensaje set read=true WHERE id='{mensaje_id}' """
