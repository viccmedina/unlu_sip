# Reperamos todos los pedidos según estado
CONSULTA_POR_ESTADO_PEDIDO = """ SELECT * FROM pedido WHERE
    estado_pedido_id='{estado_pedido}' """

# Consulta de un pedido de un usuario
CONSULTA_POR_CLIENTE_PEDIDO = """ SELECT * FROM pedido WHERE
    usuario_id='{usuario_id}' """

# Dado un nro de pedido, recuperamos el detalle del mismo
LISTAR_DETALLE_PEDIDO = """ SELECT * FROM detalle_pedido WHERE
    pedido_id='{pedido_id}' """

# Actualizamos el estado del pedido
UPDATE_ESTADO_PEDIDO = """ UPDATE pedido SET estado_pedido='{estado_pedido}'
    WHERE id_pedido='{id_pedido}' """

LISTAR_PEDIDO_SEGUN_FECHA = """ SELECT * FROM pedido WHERE ts_created BETWEEN
    '{fecha_desde}' AND '{fecha_hasta}'"""

CONSULTA_POR_ESTADO_PEDIDO_SEGUN_ID = """ SELECT pedido_estado_id FROM pedido_estado
    WHERE descripcion_corta='{descripcion_corta}'"""

INSERT_NUEVO_PEDIDO = """ INSERT INTO pedido (usuario_id)
    VALUES ('{usuario_id}')"""

INSERT_NUEVO_ESTADO_PEDIDO = """ INSERT INTO estado_pedido (usuario_id, pedido_estado_id)
    VALUES ('{pedido_id}', '{pedido_estado_id}')"""
SELECT_ULTIMO_PEDIDO_ID_POR_CLIENTE = """ SELECT pedido_id FROM pedido WHERE """

SELECT_ID_ULTIMO_PEDIDO = """ SELECT pedido_id FROM pedido WHERE usuario_id='{usuario_id}'
    ORDER BY ts_created DESC LIMIT 1 """

INSERT_NUEVO_ESTADO_PEDIDO = """ INSERT INTO estado_pedido (pedido_id, pedido_estado_id)
    VALUES ('{pedido_id}', '{pedido_estado_id}')"""
