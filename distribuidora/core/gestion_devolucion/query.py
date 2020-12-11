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

SELECT_ESTADO_DEVOLUCION_BY_DESCRIPCION = """ SELECT * FROM estado_devolucion WHERE descripcion_corta='{descripcion_corta}'"""


INSERT_INTO_DEVOLUCION = """ INSERT INTO devolucion (pedido_id, estado_devolucion_id, descripcion) VALUES 
	('{pedido_id}', '{estado_devolucion_id}', 'esto es una descripcion') """

SELECT_ALL_DEVOLUCIONES = """ SELECT * FROM devolucion AS d INNER JOIN pedido AS p ON 
	d.pedido_id=p.pedido_id WHERE p.usuario_id = '{usuario_id}'"""