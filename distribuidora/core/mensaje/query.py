INSERTAR_NUEVO_MENSAJE = """ INSERT INTO mensaje (sender_id, recipient_id, body, read)
    VALUES ('{sender_id}', '{recipient_id}', '{body}', false)
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