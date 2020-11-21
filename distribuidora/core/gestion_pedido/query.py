# Reperamos todos los pedidos según estado
CONSULTA_POR_ESTADO_PEDIDO = """ SELECT * FROM pedido WHERE
    estado_pedido_id='{estado_pedido}' """

# Consulta de un pedido de un usuario
CONSULTA_POR_CLIENTE_PEDIDO = """ SELECT * FROM pedido WHERE
    usuario_id='{usuario_id}' """

# Dado un nro de pedido, recuperamos el detalle del mismo
LISTAR_DETALLE_PEDIDO = """ SELECT * FROM detalle_pedido WHERE
    pedido_id='{pedido_id}' """

# Vamos a devolver el detalle pero con mas informaciónote
DETALLE_INFORMACION_FULL = """ SELECT dp.detalle_id, dp.producto_envase_id,
    dp.pedido_id, pe.stock_real, dp.cantidad, lpp.precio FROM detalle_pedido AS dp
    INNER JOIN producto_envase AS pe ON dp.producto_envase_id=pe.producto_envase_id
    INNER JOIN lista_precio_producto AS lpp ON dp.producto_envase_id=lpp.producto_envase_id
    WHERE dp.pedido_id = '{pedido_id}' """
# Actualizamos el estado del pedido
UPDATE_ESTADO_PEDIDO = """ UPDATE pedido SET estado_pedido='{estado_pedido}'
    WHERE id_pedido='{id_pedido}' """

LISTAR_PEDIDO_SEGUN_FECHA = """ SELECT * FROM pedido WHERE ts_created BETWEEN
    '{fecha_desde}' AND '{fecha_hasta}'"""

CONSULTA_POR_ESTADO_PEDIDO_SEGUN_ID = """ SELECT pedido_estado_id FROM pedido_estado
    WHERE descripcion_corta='{descripcion_corta}'"""

INSERT_NUEVO_PEDIDO = """ INSERT INTO pedido (usuario_id, estado_pedido_id)
    VALUES ('{usuario_id}', '{estado_pedido_id}')"""

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

SELECT_PEDIDOS_ESTADO_PCO = """ SELECT  hep.historial_estado_pedido_id, hep.pedido_id, pe.descripcion, pe.orden FROM historial_estado_pedido AS hep
    INNER JOIN pedido_estado AS pe ON hep.pedido_estado_id = pe.pedido_estado_id
    WHERE pe.orden>1
    GROUP by hep.pedido_id
    HAVING MAX(hep.ts_created)"""

SELECT_PEDIDOS_ESTADO_PCC = """ SELECT hep.pedido_id, pe.descripcion FROM historial_estado_pedido AS hep
    INNER JOIN pedido_estado AS pe ON hep.pedido_estado_id = pe.pedido_estado_id
    INNER JOIN pedido AS p ON p.pedido_id=hep.pedido_id
    WHERE p.usuario_id='{usuario_id}' AND pe.descripcion_corta='PCC'
        AND hep.pedido_id IN
        	(SELECT pedido_id FROM historial_estado_pedido
        		GROUP BY pedido_id HAVING COUNT(pedido_id) = 1 )"""


INSERT_INTO_DETALLE_PEDIDO = """ INSERT INTO detalle_pedido (pedido_id, producto_envase_id, cantidad)
    VALUES ('{pedido_id}', '{producto_envase_id}', '{cantidad}')"""

UPDATE_CANTIDAD_DETALLE_PEDIDO = """ UPDATE detalle_pedido set cantidad='{cantidad}'
    WHERE detalle_id='{detalle_id}'"""

DELETE_PRODUCTO_FROM_DETALLE_PEDIDO = """ DELETE FROM detalle_pedido
    WHERE producto_envase_id='{producto_envase_id}' AND detalle_id='{detalle_id}' """

SELECT_PEDIDOS_ESTADOS_FOR_OPERADOR = """ SELECT descripcion
    FROM pedido_estado WHERE descripcion_corta NOT IN ('PCC', 'PCO')"""

SELECT_ESTADO_PEDIDO_DESCRIPCION = """ SELECT * FROM pedido_estado
    WHERE descripcion = '{descripcion}' """

UPDATE_PEDIDO_ESTADO = """ UPDATE pedido SET estado_pedido_id='{estado_pedido_id}'
    WHERE pedido_id='{pedido_id}'"""

DELETE_PEDIDO_BY_CLIENTE = """ DELETE FROM pedido WHERE pedido_id='{pedido_id}' """

SELECT_PEDIDO = """ SELECT p.pedido_id, pe.descripcion_corta, pe.descripcion, p.estado_pedido_id
    FROM pedido as p INNER JOIN pedido_estado AS pe ON p.estado_pedido_id=pe.pedido_estado_id
    WHERE p.pedido_id = '{pedido_id}' """

CALCULO_COSTO_PEDIDO =  """ SELECT SUM(dp.cantidad*lpp.precio) AS total
    FROM detalle_pedido AS dp
    INNER JOIN lista_precio_producto AS lpp
    ON dp.producto_envase_id=lpp.producto_envase_id
    WHERE dp.pedido_id='{pedido_id}'  """

SELECT_PEDIDO_BY_PEDIDO_ID = """ SELECT * FROM pedido WHERE pedido_id='{pedido_id}' """

JOIN_PEDIDO_DETALLE = """ SELECT dp.producto_envase_id, dp.cantidad FROM pedido AS p
    INNER JOIN detalle_pedido AS dp ON dp.pedido_id=p.pedido_id
    WHERE dp.pedido_id='{pedido_id}'"""


"""
    CREATE TRIGGER BI_Pedido
    BEFORE INSERT ON pedidos
    BEGIN
    SELECT CASE
        WHEN ((select p.pedido_id from pedido p where new.usuario_id = old.usuario_id and
        estado_pedido_id = 1 ) ISNOTNULL) THEN
        RAISE(ABORT, 'Error - Cliente con pedido pendiente de confirmacion ')
    END;
    END;



    CREATE TRIGGER BU_Pedido
    BEFORE UPDATE ON pedidos
    BEGIN
    SELECT CASE      pco(pend. conf. operador)
        WHEN (old.estado_pedido_id = 2 and new.estado_pedido_id = 1 or
        old.estado_pedido_id = 2 and new.estado_pedido_id = 4 or
        old.estado_pedido_id = 2 and new.estado_pedido_id = 5 or
        old.estado_pedido_id = 2 and new.estado_pedido_id = 6 or
        old.estado_pedido_id = 2 and new.estado_pedido_id = 8)THEN
        RAISE(ABORT, 'Error - Cambio de estado del pedido incorrecto ')
    END;
    SELECT CASE       ep(en preparacion)
        WHEN (old.estado_pedido_id = 3 and new.estado_pedido_id = 1 or
        old.estado_pedido_id = 3 and new.estado_pedido_id = 2 or
        old.estado_pedido_id = 3 and new.estado_pedido_id = 5 or
        old.estado_pedido_id = 3 and new.estado_pedido_id = 6 or
        old.estado_pedido_id = 3 and new.estado_pedido_id = 7 or
        old.estado_pedido_id = 3 and new.estado_pedido_id = 8)THEN
        RAISE(ABORT, 'Error - Cambio de estado del pedido incorrecto ')
    END;
    SELECT CASE      ec(en camino)
        WHEN (old.estado_pedido_id = 4 and new.estado_pedido_id = 1 or
        old.estado_pedido_id = 4 and new.estado_pedido_id = 2 or
        old.estado_pedido_id = 4 and new.estado_pedido_id = 3 or
        old.estado_pedido_id = 4 and new.estado_pedido_id = 7 or
        old.estado_pedido_id = 4 and new.estado_pedido_id = 8)THEN
        RAISE(ABORT, 'Error - Cambio de estado del pedido incorrecto ')
    END;
    SELECT CASE     e(entregado)
        WHEN (old.estado_pedido_id = 5 and new.estado_pedido_id = 1 or
        old.estado_pedido_id = 5 and new.estado_pedido_id = 2 or
        old.estado_pedido_id = 5 and new.estado_pedido_id = 3 or
        old.estado_pedido_id = 5 and new.estado_pedido_id = 4 or
        old.estado_pedido_id = 5 and new.estado_pedido_id = 7)THEN
        RAISE(ABORT, 'Error - Cambio de estado del pedido incorrecto ')
    END;
    SELECT CASE     d(demorado)
        WHEN (old.estado_pedido_id = 6 and new.estado_pedido_id = 1 or
        old.estado_pedido_id = 6 and new.estado_pedido_id = 2 or
        old.estado_pedido_id = 6 and new.estado_pedido_id = 3 or
        old.estado_pedido_id = 6 and new.estado_pedido_id = 4 or
        old.estado_pedido_id = 6 and new.estado_pedido_id = 7 )THEN
        RAISE(ABORT, 'Error - Cambio de estado del pedido incorrecto ')
    END;

    END;
"""
