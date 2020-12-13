GET_ESTADO_PEDIDO = """
SELECT ep.pedido_estado_id FROM pedido_estado ep WHERE ep.descripcion_corta = 'E';
"""

LISTAR_PEDIDOS = """
SELECT DISTINCT (julianday(Date('now')) - julianday(Date(p.ts_created)) )AS dias, p.pedido_id AS pedido FROM pedido p
INNER JOIN detalle_pedido dp ON dp.pedido_id = p.pedido_id
WHERE p.usuario_id = {user} AND p.estado_pedido_id   = {ep}
"""

LIST_PEDIDO_DETALLE = """
SELECT * FROM detalle_pedido dp INNER JOIN pedido p ON p.pedido_id = dp.pedido_id
INNER JOIN producto_envase pe ON pe.producto_envase_id = dp.producto_envase_id
WHERE dp.pedido_id = '{p_id}'
"""

LIST_PRODUCTO_DETALLE = """
SELECT p.descripcion AS producto, m.descripcion AS marca, um.descripcion AS umedida FROM
producto p INNER JOIN marca m ON m.marca_id = p.marca_id
INNER JOIN producto_envase pe ON p.producto_id = pe.producto_envase_id
INNER JOIN unidad_medida um ON um.unidad_medida_id = pe.unidad_medida_id
WHERE pe.producto_envase_id = {producto}
"""

SELECT_ESTADO_DEVOLUCION_BY_DESCRIPCION_CORTA = """ SELECT * FROM estado_devolucion WHERE descripcion_corta='{descripcion_corta}'"""

SELECT_ESTADO_DEVOLUCION_BY_DESCRIPCION = """ SELECT * FROM estado_devolucion WHERE descripcion='{descripcion}'"""

INSERT_INTO_DEVOLUCION = """ INSERT INTO devolucion (pedido_id, estado_devolucion_id, descripcion) VALUES 
	('{pedido_id}', '{estado_devolucion_id}', 'esto es una descripcion') """

SELECT_ALL_DEVOLUCIONES = """ SELECT * FROM devolucion AS d INNER JOIN pedido AS p ON 
	d.pedido_id=p.pedido_id WHERE p.usuario_id = '{usuario_id}'"""

SELECT_DEVOLUCION_BY_PEDIDO = """ SELECT * FROM devolucion WHERE pedido_id='{pedido_id}' """

SELECT_DEVOLUCION_BY_DETALLE_PEDIDO = """ SELECT * FROM detalle_devolucion WHERE detalle_pedido_id='{detalle_pedido}' """

SELECT_DEVOLUCION = """ SELECT * FROM devolucion AS d INNER JOIN pedido AS p ON p.pedido_id = d.pedido_id WHERE devolucion_id = '{devolucion_id}' """

INSERT_INTO_DETALLE_DEVOLUCION = """ INSERT INTO detalle_devolucion (devolucion_id, motivo_id, detalle_pedido_id, cantidad) VALUES('{devolucion_id}', '{motivo_id}', '{detalle_pedido_id}', '{cantidad}')"""

SELECT_ALL_MOTIVOS_BY_DESCRIPCION = """ SELECT * FROM motivo_devolucion WHERE descripcion = '{descripcion}' """

SELECT_ALL_ESTADO_DEVOLUCION_BY_DESCRIPCION_CORTA = """ SELECT * FROM estado_devolucion WHERE descripcion_corta = '{descripcion_corta}' """

SELECT_DEVOLUCION_CON_ESTADO = """ SELECT * FROM devolucion AS d INNER JOIN estado_devolucion AS ed ON d.estado_devolucion_id=ed.estado_devolucion_id WHERE d.devolucion_id='{devolucion_id}'"""

SELECT_ESTADO_DEVOLUCION_BY_ID = """ SELECT * FROM estado_devolucion WHERE estado_devolucion_id = '{estado_id}' """

UPDATE_ESTADO_DEVOLUCION = """ UPDATE devolucion SET estado_devolucion_id='{estado}' WHERE devolucion_id = '{devolucion_id}' """

INSERT_INTO_HISTORIAL_DEVOLUCION = """ INSERT INTO historial_devolucion_estado (devolucion_id, estado_devolucion_id) VALUES('{devolucion_id}', '{estado_id}') """

SELECT_DETALLE_DEVOLUCION = """ SELECT * FROM detalle_devolucion WHERE devolucion_id='{devolucion_id}' """

SELECT_DEVOLUCION_VISTA_OPERADOR = """ SELECT * FROM devolucion AS d INNER JOIN estado_devolucion AS ed ON ed.estado_devolucion_id=d.estado_devolucion_id WHERE ed.descripcion_corta <> 'ECC'"""

SELECT_ALL_ESTADO_DEVOLUCION = """ SELECT * FROM estado_devolucion """

DETALLE_DEVOLUCION_FULL = """  SELECT e.descripcion AS d_envase, m.descripcion AS d_marca, um.descripcion as d_unidad_medida, md.descripcion as d_motivo, p.descripcion AS d_producto 
FROM devolucion AS d INNER JOIN detalle_devolucion AS dd ON dd.devolucion_id=d.devolucion_id
INNER JOIN motivo_devolucion AS md ON dd.motivo_id = md.motivo_devolucion_id
INNER JOIN detalle_pedido AS dp ON dp.detalle_id = dd.detalle_pedido_id
INNER JOIN producto_envase AS pe ON pe.producto_envase_id=dp.producto_envase_id
INNER JOIN producto AS p ON p.producto_id=pe.producto_id
INNER JOIN marca AS m ON m.marca_id=p.marca_id
INNER JOIN unidad_medida AS um ON um.unidad_medida_id=pe.unidad_medida_id
INNER JOIN envase AS e ON e.envase_id=pe.envase_id
WHERE d.devolucion_id = 1"""