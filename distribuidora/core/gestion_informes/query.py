
CONSULTAR_USUARIO = """
SELECT u.id FROM usuario u;
"""

CONSULTA_MOVIMIENTOS_CTA_CORRIENTE = """
	SELECT cc.cuenta_corriente_id AS cta_corriente,p.nombre AS nombre,p.email AS email,((SELECT sum(saldo) FROM movimiento_cta_corriente mccc WHERE
    mccc.usuario = {user}) - (SELECT sum(monto) FROM comprobante_pago cpp INNER JOIN pedido ped WHERE ped.usuario_id = {user})) AS saldo FROM
    movimiento_cta_corriente mcc INNER JOIN cuenta_corriente cc ON mcc.cta_corriente = cc.cuenta_corriente_id INNER JOIN persona p
    ON cc.persona_id = p.persona_id INNER JOIN pedido pe ON pe.usuario_id = mcc.usuario
	WHERE mcc.usuario = {user} AND mcc.ts_created >= ('{fecha_desde}') AND mcc.ts_created <= ('{fecha_hasta}')

	"""
CONSULTAR_PRODUCTOS = """
SELECT pe.producto_envase_id FROM producto_envase pe ;
"""


CONSULTA_MOVIMIENTOS_STOCK = """ SELECT pe.producto_envase_id AS pei ,p.descripcion AS producto , m.descripcion AS marca,
um.descripcion AS umedida, pe.stock_real - (select sum(dp.cantidad) from producto_envase pee
INNER JOIN detalle_pedido dp ON pee.producto_envase_id=dp.producto_envase_id
INNER JOIN pedido p ON p.pedido_id= dp.pedido_id WHERE pee.producto_envase_id = {productoEnvase}
AND p.estado_pedido_id = 1) AS stock, lpp.precio AS precio FROM producto_envase pe INNER JOIN producto p
ON p.producto_id=pe.producto_id
INNER JOIN marca m ON p.marca_id=m.marca_id
INNER JOIN unidad_medida um ON um.unidad_medida_id=pe.unidad_medida_id
INNER JOIN lista_precio_producto lpp ON lpp.producto_envase_id=pe.producto_envase_id
WHERE pe.producto_envase_id = {productoEnvase} AND pe.ts_created>= ('{fecha_desde}') AND pe.ts_created <= ('{fecha_hasta}')
 """


CONSULTA_STOCK_REAL = """
SELECT p.descripcion AS producto, m.descripcion AS marca, um.descripcion AS umedida,sum(dp.cantidad) AS cant,
(lpp.precio * (SELECT sum(dpp.cantidad) FROM detalle_pedido dpp WHERE dpp.producto_envase_id = {productoEnvase})) AS precio
FROM detalle_pedido dp INNER JOIN producto_envase pe ON pe.producto_envase_id = dp.producto_envase_id
INNER JOIN producto p ON p.producto_id = pe.producto_id
INNER JOIN lista_precio_producto lpp ON lpp.producto_envase_id = pe.producto_envase_id
INNER JOIN marca m ON m.marca_id = p.marca_id
INNER JOIN unidad_medida um ON um.unidad_medida_id = pe.unidad_medida_id
WHERE pe.producto_envase_id = {productoEnvase} AND pe.ts_created>= ('{fecha_desde}') AND pe.ts_created <= ('{fecha_hasta}')
GROUP BY pe.producto_envase_id ORDER BY dp.cantidad DESC;
"""
