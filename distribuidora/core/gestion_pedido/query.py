# Reperamos todos los pedidos según estado
CONSULTA_POR_ESTADO_PEDIDO =
    """
    SELECT * FROM pedido WHERE
    estado_pedido_id='{estado_pedido}'
    """

# Consulta de un pedido de un usuario
CONSULTA_POR_CLIENTE_PEDIDO = """ SELECT * FROM pedido WHERE
    usuario_id='{usuario_id}' """

# Dado un nro de pedido, recuperamos el detalle del mismo
LISTAR_DETALLE_PEDIDO = """ SELECT * FROM detalle_pedido WHERE
    pedido_id='{pedido_id}' """

# Actualizamos el estado del pedido
UPDATE_ESTADO_PEDIDO ) = """ UPDATE pedido SET estado_pedido='{estado_pedido}'
    WHERE id_pedido='{id_pedido}' """

LISTAR_PEDIDO_SEGUN_FECHA = """ SELECT * FROM pedido WHERE ts_created BETWEEN
    '{fecha_desde}' AND '{fecha_hasta}'"""
