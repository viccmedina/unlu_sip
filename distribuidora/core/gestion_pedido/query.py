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

INSERT_NUEVO_HISTORIAL_PEDIDO_ESTADO = """ INSERT INTO historial_estado_pedido (pedido_estado_id, pedido_id)
    VALUES ('{pedido_estado_id}', '{pedido_id}')"""

SELECT_ULTIMO_PEDIDO_ID_POR_CLIENTE = """ SELECT hpe.pedido_id, pe.descripcion_corta, max(hpe.ts_created)
    FROM historial_estado_pedido AS hpe
    INNER JOIN pedido AS p ON hpe.pedido_id = p.pedido_id
    INNER JOIN pedido_estado AS pe ON pe.pedido_estado_id = hpe.pedido_estado_id
    WHERE p.usuario_id = '{usuario_id}' AND pe.descripcion_corta = 'PCC'"""

CANTIDAD_ESTADOS_DEL_PEDIDO = """ SELECT COUNT(*) AS cantidad FROM historial_estado_pedido
    WHERE pedido_id='{pedido_id}'"""

SELECT_ID_ULTIMO_PEDIDO = """ SELECT pedido_id FROM pedido WHERE usuario_id='{usuario_id}'
    ORDER BY ts_created DESC LIMIT 1 """

SELECT_PEDIDOS_ESTADO_PCO = """ SELECT hep.pedido_id, pe.descripcion FROM historial_estado_pedido AS hep
    INNER JOIN pedido_estado AS pe ON hep.pedido_estado_id = pe.pedido_estado_id
    WHERE pe.descripcion_corta='PCO' AND hep.pedido_id IN
    	(SELECT pedido_id FROM historial_estado_pedido
    		GROUP BY pedido_id HAVING COUNT(pedido_id) = 2 )"""

SELECT_PEDIDOS_ESTADO_PCC = """ SELECT hep.pedido_id, pe.descripcion FROM historial_estado_pedido AS hep
    INNER JOIN pedido_estado AS pe ON hep.pedido_estado_id = pe.pedido_estado_id
    INNER JOIN pedido AS p ON p.pedido_id=hep.pedido_id
    WHERE p.usuario_id='{usuario_id}' AND pe.descripcion_corta='PCC'
        AND hep.pedido_id IN
        	(SELECT pedido_id FROM historial_estado_pedido
        		GROUP BY pedido_id HAVING COUNT(pedido_id) = 1 )"""


INSERT_INTO_DETALLE_PEDIDO = """ INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad)
    VALUES ('{pedido_id}', '{producto_id}', '{cantidad}')"""

UPDATE_CANTIDAD_DETALLE_PEDIDO = """ UPDATE detalle_pedido set cantidad='{cantidad}'
    WHERE detalle_id='{detalle_id}'"""
