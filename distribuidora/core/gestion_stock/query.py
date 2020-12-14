CONSULTAR_ID_PRODUCTO = """
SELECT pe.producto_envase_id from producto p INNER JOIN producto_envase pe ON pe.producto_id = p.producto_id
WHERE p.descripcion = '{producto}'
"""


# consulta la suma cantidad de producto "Cargados" en detalle_stock
CONSULTA_STOCK = """ SELECT p.descripcion AS descripcion_p,m.descripcion as descripcion_m,
um.descripcion, pe.stock_real - (select sum(dp.cantidad) from producto_envase pee
INNER JOIN detalle_pedido dp ON pee.producto_envase_id=dp.producto_envase_id
INNER JOIN pedido p ON p.pedido_id= dp.pedido_id WHERE pee.producto_envase_id = {producto_id}
AND p.estado_pedido_id = 1) AS cantidad FROM (((producto_envase pe INNER JOIN producto p
ON p.producto_id=pe.producto_id )
INNER JOIN marca m ON p.marca_id=m.marca_id)
INNER JOIN unidad_medida um ON um.unidad_medida_id=pe.unidad_medida_id)
WHERE p.descripcion = '{producto}' and p.marca_id = {marca} and pe.unidad_medida_id = {uMedida}
 """


CONSULTA_STOCK_POR_PRODUCTO = """ SELECT p.descripcion AS descripcion_p,m.descripcion as descripcion_m,
um.descripcion, pe.stock_real - (select sum(dp.cantidad) from producto_envase pee
INNER JOIN detalle_pedido dp ON pee.producto_envase_id=dp.producto_envase_id
INNER JOIN pedido p ON p.pedido_id= dp.pedido_id WHERE pee.producto_envase_id = {producto_id}
AND p.estado_pedido_id = 1) AS cantidad FROM (((producto_envase pe INNER JOIN producto p
ON p.producto_id=pe.producto_id )
INNER JOIN marca m ON p.marca_id=m.marca_id)
INNER JOIN unidad_medida um ON um.unidad_medida_id=pe.unidad_medida_id)
WHERE pe.producto_envase_id = {producto_id}
 """




CONSULTA_STOCK_POR_MARCA = """
SELECT p.descripcion AS descripcion_p,m.descripcion as descripcion_m,
um.descripcion, pe.stock_real - (select sum(dp.cantidad) from producto_envase pee
INNER JOIN detalle_pedido dp ON pee.producto_envase_id=dp.producto_envase_id
INNER JOIN pedido p ON p.pedido_id= dp.pedido_id WHERE m.marca_id = {marca}
AND p.estado_pedido_id = 1) AS cantidad FROM (((producto_envase pe INNER JOIN producto p
ON p.producto_id=pe.producto_id )
INNER JOIN marca m ON p.marca_id=m.marca_id)
INNER JOIN unidad_medida um ON um.unidad_medida_id=pe.unidad_medida_id)
WHERE m.marca_id = {marca}
"""

CONSULTA_STOCK_POR_UMEDIDA = """
SELECT p.descripcion AS descripcion_p,m.descripcion as descripcion_m,
um.descripcion, pe.stock_real - (select sum(dp.cantidad) from producto_envase pee
INNER JOIN detalle_pedido dp ON pee.producto_envase_id=dp.producto_envase_id
INNER JOIN pedido p ON p.pedido_id= dp.pedido_id WHERE um.unidad_medida_id = {uMedida}
AND p.estado_pedido_id = 1) AS cantidad FROM (((producto_envase pe INNER JOIN producto p
ON p.producto_id=pe.producto_id )
INNER JOIN marca m ON p.marca_id=m.marca_id)
INNER JOIN unidad_medida um ON um.unidad_medida_id=pe.unidad_medida_id)
WHERE um.unidad_medida_id = {uMedida}
"""

CONSULTA_STOCK_POR_PRODUCTO_MARCA = """
SELECT p.descripcion AS descripcion_p,m.descripcion as descripcion_m,
um.descripcion, pe.stock_real - (select sum(dp.cantidad) from producto_envase pee
INNER JOIN detalle_pedido dp ON pee.producto_envase_id=dp.producto_envase_id
INNER JOIN pedido p ON p.pedido_id= dp.pedido_id WHERE pee.producto_envase_id = {producto}
AND p.estado_pedido_id = 1) AS cantidad FROM (((producto_envase pe INNER JOIN producto p
ON p.producto_id=pe.producto_id )
INNER JOIN marca m ON p.marca_id=m.marca_id)
INNER JOIN unidad_medida um ON um.unidad_medida_id=pe.unidad_medida_id)
WHERE pe.producto_envase_id = {producto}
"""


CONSULTA_STOCK_POR_PRODUCTO_UMEDIDA = """
SELECT p.descripcion AS descripcion_p,m.descripcion as descripcion_m,
um.descripcion, pe.stock_real - (select sum(dp.cantidad) from producto_envase pee
INNER JOIN detalle_pedido dp ON pee.producto_envase_id=dp.producto_envase_id
INNER JOIN pedido p ON p.pedido_id= dp.pedido_id WHERE pee.producto_envase_id = {producto}
AND p.estado_pedido_id = 1) AS cantidad FROM (((producto_envase pe INNER JOIN producto p
ON p.producto_id=pe.producto_id )
INNER JOIN marca m ON p.marca_id=m.marca_id)
INNER JOIN unidad_medida um ON um.unidad_medida_id=pe.unidad_medida_id)
WHERE pe.producto_envase_id = {producto}
"""

CONSULTA_STOCK_POR_MARCA_UMEDIDA = """
SELECT p.descripcion AS descripcion_p,m.descripcion as descripcion_m,
um.descripcion, pe.stock_real - (select sum(dp.cantidad) from producto_envase pee
INNER JOIN detalle_pedido dp ON pee.producto_envase_id=dp.producto_envase_id
INNER JOIN pedido p ON p.pedido_id= dp.pedido_id WHERE pee.producto_envase_id = {producto}
AND p.estado_pedido_id = 1) AS cantidad FROM (((producto_envase pe INNER JOIN producto p
ON p.producto_id=pe.producto_id )
INNER JOIN marca m ON p.marca_id=m.marca_id)
INNER JOIN unidad_medida um ON um.unidad_medida_id=pe.unidad_medida_id)
WHERE pe.producto_envase_id = {producto}
"""


CONSULTAR_PRODUCTOS = """
SELECT pe.producto_envase_id from producto p INNER JOIN producto_envase pe ON pe.producto_id = p.producto_id
WHERE p.descripcion = '{producto}'
"""



CONSULTA_STOCK1 = """ SELECT p.descripcion AS descripcion_p,m.descripcion as descripcion_m,
um.descripcion, pe.stock_real AS cantidad FROM (((producto_envase pe INNER JOIN producto p
ON p.producto_id=pe.producto_id )
INNER JOIN marca m ON p.marca_id=m.marca_id)
INNER JOIN unidad_medida um ON um.unidad_medida_id=pe.unidad_medida_id)
WHERE pe.producto_envase_id = {producto_envase_id}
"""

CONSULTAR_ID_MARCA = """SELECT m.marca_id FROM marca m WHERE m.descripcion = ('{marca}')"""

CONSULTAR_ID_UMEDIDA = """SELECT um.unidad_medida_id FROM unidad_medida um WHERE um.descripcion = ('{uMedida}')"""

CONSULTAR_ID_PRODUCTO_COMPLETO = """ SELECT (pe.producto_envase_id) FROM producto p INNER JOIN
producto_envase pe on p.producto_id=pe.producto_id WHERE p.descripcion = ('{producto}') and pe.unidad_medida_id = {uMedida} and
p.marca_id = {marca} """

CONSULTA_ID_POR_PRODUCTO_MARCA = """ SELECT (pe.producto_envase_id) FROM producto p INNER JOIN
producto_envase pe on p.producto_id=pe.producto_id WHERE p.descripcion = ('{producto}') AND
p.marca_id = {marca} """

CONSULTA_ID_POR_PRODUCTO_UMEDIDA = """ SELECT (pe.producto_envase_id) FROM producto p INNER JOIN
producto_envase pe on p.producto_id=pe.producto_id WHERE p.descripcion = ('{producto}') AND
pe.unidad_medida_id = {uMedida} """


CONSULTA_ID_POR_MARCA_UMEDIDA = """ SELECT (pe.producto_envase_id) FROM producto p INNER JOIN
producto_envase pe on p.producto_id=pe.producto_id WHERE p.marca_id = {marca} AND
pe.unidad_medida_id = {uMedida} """

CONSULTA_ID_PRODUCTO_MARCA_UMEDIDA = """ SELECT (pe.producto_envase_id) FROM producto p INNER JOIN
producto_envase pe on p.producto_id=pe.producto_id WHERE p.marca_id = {marca} AND
pe.unidad_medida_id = {uMedida} and P.descripcion = '{producto}'"""

CONSULTAR_ID_PRODUCTOS1 = """
SELECT pe.producto_envase_id FROM producto_envase pe INNER JOIN producto p ON pe.producto_id=p.producto_id
WHERE p.marca_id = {marca} and p.descripcion = '{producto}'
"""

CONSULTAR_ID_PRODUCTOS2 = """
SELECT pe.producto_envase_id FROM producto_envase pe INNER JOIN producto p ON pe.producto_id=p.producto_id
WHERE pe.unidad_medida_id = {uMedida} and p.descripcion = '{producto}'
"""

INSERT_MOVIMIENTO_STOCK = """ INSERT INTO movimiento_stock (tipo_movimiento_stock_id,usuario_id,
producto_envase_id,descripcion,cantidad) VALUES ({tipo_movimiento},{usuario_id},{producto_envase_id},'{descripcion}',{cantidad}); """

UPDATE_STOCK_REAL = """UPDATE producto_envase SET stock_real = stock_real + '{cantidad}'  WHERE
producto_envase_id = {producto_envase_id}"""

BAJA_PRODUCTO = """UPDATE producto_envase SET stock_real='{stock_real}'  WHERE
producto_envase_id='{producto_envase_id}' """

CONSULTAR_MOVIMIENTOS = """
    SELECT p.descripcion as descripcion_p, m.descripcion as descripcion_m, um.descripcion, u.username,
    mov.ts_created as fecha, mov.cantidad FROM
    (((((movimiento_stock mov INNER JOIN producto_envase pe on mov.producto_envase_id=pe.producto_envase_id)
    INNER JOIN producto p on p.producto_id= pe.producto_id)
    INNER JOIN marca m on p.marca_id= m.marca_id)
    INNER JOIN unidad_medida um on um.unidad_medida_id=pe.unidad_medida_id)
    INNER JOIN usuario u on u.id=mov.usuario_id)
    WHERE mov.ts_created >= DATETIME('{f_desde}') and mov.ts_created <= ('{f_hasta}');

"""


UPDATE_NUEVO_PEDIDO_STOCK_REAL = """ UPDATE producto_envase SET stock_real='{stock_real}'
    WHERE producto_envase_id='{producto_envase_id}'"""

SELECT_TIPO_MOVIMIENTO_STOCK = """ SELECT * FROM tipo_movimiento_stock WHERE descripcion='{descripcion}' """

SELECT_MOVIMIENTOS_BY_FECHA = """ SELECT p.descripcion AS d_producto, m.descripcion AS d_marca, 
	tms.descripcion AS d_tipo_movimiento, um.descripcion AS d_unidad_medida, e.descripcion AS d_envase,
	ms.cantidad AS cantidad, ms.ts_created AS fecha
	FROM movimiento_stock AS ms 
	INNER JOIN tipo_movimiento_stock AS tms ON tms.tipo_movimiento_stock_id=ms.tipo_movimiento_stock_id
	INNER JOIN producto_envase AS pe ON pe.producto_envase_id=ms.producto_envase_id
	INNER JOIN envase AS e ON e.envase_id=pe.envase_id
	INNER JOIN unidad_medida AS um ON um.unidad_medida_id=pe.unidad_medida_id
	INNER JOIN producto AS p ON p.producto_id=pe.producto_id
	INNER JOIN marca AS m ON m.marca_id=p.marca_id
	WHERE ms.ts_created BETWEEN '{fecha_desde}' AND '{fecha_hasta}'"""