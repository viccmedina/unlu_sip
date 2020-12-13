
CONSULTAR_USUARIO = """
SELECT u.id FROM usuario u;
"""

CONSULTA_MOVIMIENTOS_CTA_CORRIENTE = """
	SELECT cc.cuenta_corriente_id AS cta_corriente,p.nombre AS nombre,p.email AS email,((SELECT sum(saldo) FROM movimiento_cta_corriente mccc WHERE
    mccc.usuario = {user}) - (SELECT sum(monto) FROM comprobante_pago cpp INNER JOIN pedido ped WHERE ped.usuario_id = {user})) AS saldo FROM
    movimiento_cta_corriente mcc INNER JOIN cuenta_corriente cc ON mcc.cta_corriente = cc.cuenta_corriente_id INNER JOIN persona p
    ON cc.persona_id = p.persona_id INNER JOIN pedido pe ON pe.usuario_id = mcc.usuario
	WHERE mcc.usuario = {user}

	"""


"""
	SELECT cc.cuenta_corriente_id AS cta_corriente,p.nombre AS nombre,p.email AS email,((SELECT sum(saldo) FROM movimiento_cta_corriente mccc WHERE
    mccc.usuario = {user}) - (SELECT sum(monto) FROM comprobante_pago cpp INNER JOIN pedido ped WHERE ped.usuario_id = {user})) AS saldo FROM
    movimiento_cta_corriente mcc INNER JOIN cuenta_corriente cc ON mcc.cta_corriente = cc.cuenta_corriente_id INNER JOIN persona p
    ON cc.persona_id = p.persona_id INNER JOIN pedido pe ON pe.usuario_id = mcc.usuario
	WHERE mcc.usuario = {user} AND mcc.ts_created >= ('{fecha_desde}') AND mcc.ts_created <= ('{fecha_hasta}')

	"""

CONSULTAR_PRODUCTOS = """
SELECT pe.producto_envase_id FROM producto_envase pe ;
"""


CONSULTA_MOVIMIENTOS_STOCK = """ SELECT pe.producto_envase_id AS peid ,p.descripcion AS producto , m.descripcion as marca,
um.descripcion AS umedida, pe.stock_real - (select sum(dp.cantidad) from producto_envase pee
INNER JOIN detalle_pedido dp ON pee.producto_envase_id=dp.producto_envase_id
INNER JOIN pedido p ON p.pedido_id= dp.pedido_id WHERE pee.producto_envase_id = {productoEnvase}
AND p.estado_pedido_id = 1) AS stock, lpp.precio AS precio FROM producto_envase pe INNER JOIN producto p
ON p.producto_id=pe.producto_id
INNER JOIN marca m ON p.marca_id=m.marca_id
INNER JOIN unidad_medida um ON um.unidad_medida_id=pe.unidad_medida_id
INNER JOIN lista_precio_producto lpp ON pe.producto_envase_id = lpp.producto_envase_id
WHERE pe.producto_envase_id = {productoEnvase}
 """

CONSULTA_STOCK_REAL = """
 SELECT pe.producto_envase_id AS peid ,p.descripcion AS producto , m.descripcion as marca,
um.descripcion AS umedida, pe.stock_real AS stock, lpp.precio AS precio FROM producto_envase pe INNER JOIN producto p
ON p.producto_id=pe.producto_id
INNER JOIN marca m ON p.marca_id=m.marca_id
INNER JOIN unidad_medida um ON um.unidad_medida_id=pe.unidad_medida_id
INNER JOIN lista_precio_producto lpp ON pe.producto_envase_id = lpp.producto_envase_id
WHERE pe.producto_envase_id = {productoEnvase}
"""


CONSULTA_LISTA_PRECIOS = """

"""


"""

 select p.descripcion as producto,m.descripcion as marca,um.descripcion as umedida,e.descripcion as envase, select sum(dp.cantidad) from detalle_pedido dp where dp.producto_envase_id = pe.producto_envase_id and dp.ts_created >= fecha_desde and dp.ts_created <= fecha_hasta as cantidad, select sum(lpp.precio * (select sum(dpp.cantidad) from detalle_pedido dpp where dpp.producto_envase_id = pe.producto_envase_id and dpp.ts_created >= fecha_desde and dpp.ts_created <= fecha hasta )) as total  from producto p inner join producto_envase_id on p.producto_id = pe.producto_id inner join envase e on e.envase_id = pe.emvase_id inner join marca m on m.marca_id = p.marca_id inner join unidad_medida um on um.unidad_medida_id = pe.unidad_medida_id inner join lista_precio_producto on lpp.producto_envase_id = pe.producto_envase_id;
 """

CONSULTAR_PRODUCTOS_ALL = """

 SELECT distinct p.descripcion as producto,m.descripcion as marca,um.descripcion as umedida, e.descripcion as envase ,
 (SELECT sum(dp.cantidad) FROM detalle_pedido dp WHERE dp.producto_envase_id = {productoEnvase}) as cantidad ,
 ((SELECT lip.precio FROM lista_precio_producto lip WHERE {productoEnvase} = lip.producto_envase_id) *
 (SELECT sum(ddpp.cantidad) FROM detalle_pedido ddpp WHERE ddpp.producto_envase_id = {productoEnvase})) as precio
 FROM producto p INNER JOIN producto_envase pe on p.producto_id = pe.producto_id
 INNER JOIN marca m on m.marca_id = p.marca_id
 INNER JOIN unidad_medida um on um.unidad_medida_id = pe.unidad_medida_id
 INNER JOIN envase e on e.envase_id = pe.envase_id
 INNER JOIN lista_precio_producto lpp on lpp.producto_envase_id = pe.producto_envase_id
 INNER JOIN detalle_pedido dped
 WHERE pe.producto_envase_id = {productoEnvase} AND dped.ts_created >= '{desde}' AND dped.ts_created <= '{hasta}'
 """
