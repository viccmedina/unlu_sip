LISTAR_PRODUCTOS = """ SELECT p.descripcion as descripcion ,
	m.descripcion as marca, tp.descripcion as tipo_producto
	FROM producto AS p LEFT JOIN tipo_producto AS tp ON
	tp.tipo_producto_id=p.tipo_producto_id
	LEFT JOIN marca AS m ON m.marca_id=p.marca_id"""

PRODUCTO_ENVASE_BY_PRODUCTO_ID = """ SELECT pe.producto_envase_id, p.descripcion AS producto_descripcion,
    m.descripcion AS marca_descripcion, lpp.precio, e.descripcion AS envase_descripcion,
    u.descripcion AS unidad_descripcion, pe.ts_created, tp.descripcion AS tp_descripcion
    FROM producto_envase AS pe
    INNER JOIN producto AS p ON p.producto_id = pe.producto_id
    INNER JOIN marca AS m ON m.marca_id = p.marca_id
    INNER JOIN lista_precio_producto AS lpp ON lpp.producto_envase_id = pe.producto_envase_id
    INNER JOIN envase AS e ON e.envase_id = pe.envase_id
    INNER JOIN unidad_medida AS u ON u.unidad_medida_id = pe.unidad_medida_id
    INNER JOIN tipo_producto AS tp ON p.tipo_producto_id = tp.tipo_producto_id
    WHERE p.producto_id = '{producto_id}'"""

PRODUCTO_BY_DESCRIPCION_MARCA = """ SELECT p.producto_id FROM producto AS p
    INNER JOIN marca AS m ON p.marca_id=m.marca_id
    WHERE p.descripcion='{producto}' AND m.descripcion='{marca}'"""


PRODUCTO_ID_FROM_PRODUCTO_ENVASE = """ SELECT producto_id FROM producto_envase
    WHERE producto_envase_id='{producto_envase_id}'"""


LISTAR_ALL_PRODUCTOS = """
select pe.producto_envase_id as peid, p.descripcion as desc, m.descripcion as descm, um.descripcion as descum,
lpp.precio as precio from producto_envase pe inner join producto p on p.producto_id= pe.producto_id
inner join marca m on m.marca_id = p.marca_id inner join unidad_medida um on
pe.unidad_medida_id = um.unidad_medida_id inner join lista_precio_producto lpp on
pe.producto_envase_id = lpp.producto_envase_id
"""


PRODUCTOS_TO_EXPORT = """
select p.descripcion as producto, m.descripcion as marca, um.descripcion as umedida,
lpp.precio as precio, e.descripcion as envase
from producto_envase pe inner join producto p on p.producto_id= pe.producto_id
inner join marca m on m.marca_id = p.marca_id
inner join unidad_medida um on pe.unidad_medida_id = um.unidad_medida_id
inner join lista_precio_producto lpp on pe.producto_envase_id = lpp.producto_envase_id
inner join envase e on e.envase_id = pe.envase_id
"""

CONSULTAR_ID_PRODUCTO = """
SELECT * FROM producto p WHERE p.descripcion = '{producto}'
"""

CONSULTAR_ID_UMEDIDA = """
SELECT * FROM unidad_medida um WHERE um.descripcion = '{uMedida}'
"""

CONSULTAR_ID_MARCA = """
SELECT * FROM marca m WHERE m.descripcion = '{marca}'
"""

CONSULTAR_ID_TPRODUCTO = """
SELECT tp.tipo_producto_id FROM tipo_producto tp WHERE tp.descripcion = '{tProd}'
"""

CONSULT_ID_MARCA = """
SELECT m.marca_id FROM marca m WHERE m.descripcion = '{marca}'
"""

PRODUCTOS_P_PRODUCTO="""
SELECT p.descripcion as producto, m.descripcion as marca, um.descripcion as umedida, lpp.precio as precio,
tp.descripcion as tipoProd,pe.stock_real as stock FROM producto p INNER JOIN producto_envase pe ON
p.producto_id = pe.producto_id INNER JOIN marca m ON m.marca_id = p.marca_id INNER JOIN unidad_medida um ON
pe.unidad_medida_id = um.unidad_medida_id INNER JOIN tipo_producto tp ON p.tipo_producto_id = tp.tipo_producto_id
INNER JOIN lista_precio_producto lpp ON lpp.producto_envase_id = pe.producto_envase_id
WHERE p.descripcion = '{producto}'
"""

PRODUCTOS_P_MARCA = """
SELECT p.descripcion as producto, m.descripcion as marca, um.descripcion as umedida, lpp.precio as precio,
tp.descripcion as tipoProd,pe.stock_real as stock FROM producto p INNER JOIN producto_envase pe ON
p.producto_id = pe.producto_id INNER JOIN marca m ON m.marca_id = p.marca_id INNER JOIN unidad_medida um ON
pe.unidad_medida_id = um.unidad_medida_id INNER JOIN tipo_producto tp ON p.tipo_producto_id = tp.tipo_producto_id
INNER JOIN lista_precio_producto lpp ON lpp.producto_envase_id = pe.producto_envase_id
WHERE m.descripcion = '{marca}'
"""


PRODUCTOS_P_UMEDIDA = """
SELECT p.descripcion as producto, m.descripcion as marca, um.descripcion as umedida, lpp.precio as precio,
tp.descripcion as tipoProd,pe.stock_real as stock FROM producto p INNER JOIN producto_envase pe ON
p.producto_id = pe.producto_id INNER JOIN marca m ON m.marca_id = p.marca_id INNER JOIN unidad_medida um ON
pe.unidad_medida_id = um.unidad_medida_id INNER JOIN tipo_producto tp ON p.tipo_producto_id = tp.tipo_producto_id
INNER JOIN lista_precio_producto lpp ON lpp.producto_envase_id = pe.producto_envase_id
WHERE um.descripcion = '{uMedida}'
"""

PRODUCTOS_P_PRODUCTO_MARCA = """
SELECT p.descripcion as producto, m.descripcion as marca, um.descripcion as umedida, lpp.precio as precio,
tp.descripcion as tipoProd,pe.stock_real as stock FROM producto p INNER JOIN producto_envase pe ON
p.producto_id = pe.producto_id INNER JOIN marca m ON m.marca_id = p.marca_id INNER JOIN unidad_medida um ON
pe.unidad_medida_id = um.unidad_medida_id INNER JOIN tipo_producto tp ON p.tipo_producto_id = tp.tipo_producto_id
INNER JOIN lista_precio_producto lpp ON lpp.producto_envase_id = pe.producto_envase_id
WHERE p.descripcion = '{producto}' and m.descripcion = '{marca}'
"""

PRODUCTOS_P_PRODUCTO_UMEDIDA = """
SELECT p.descripcion as producto, m.descripcion as marca, um.descripcion as umedida, lpp.precio as precio,
tp.descripcion as tipoProd,pe.stock_real as stock FROM producto p INNER JOIN producto_envase pe ON
p.producto_id = pe.producto_id INNER JOIN marca m ON m.marca_id = p.marca_id INNER JOIN unidad_medida um ON
pe.unidad_medida_id = um.unidad_medida_id INNER JOIN tipo_producto tp ON p.tipo_producto_id = tp.tipo_producto_id
INNER JOIN lista_precio_producto lpp ON lpp.producto_envase_id = pe.producto_envase_id
WHERE p.descripcion = '{producto}' and um.descripcion = '{uMedida}'
"""

PRODUCTOS_P_MARCA_UMEDIDA = """
SELECT p.descripcion as producto, m.descripcion as marca, um.descripcion as umedida, lpp.precio as precio,
tp.descripcion as tipoProd,pe.stock_real as stock FROM producto p INNER JOIN producto_envase pe ON
p.producto_id = pe.producto_id INNER JOIN marca m ON m.marca_id = p.marca_id INNER JOIN unidad_medida um ON
pe.unidad_medida_id = um.unidad_medida_id INNER JOIN tipo_producto tp ON p.tipo_producto_id = tp.tipo_producto_id
INNER JOIN lista_precio_producto lpp ON lpp.producto_envase_id = pe.producto_envase_id
WHERE m.descripcion = '{marca}' and um.descripcion = '{uMedida}'
"""


PRODUCTOS_P_PRODUCTO_MARCA_UMEDIDA  = """
SELECT p.descripcion as producto, m.descripcion as marca, um.descripcion as umedida, lpp.precio as precio,
tp.descripcion as tipoProd,pe.stock_real as stock FROM producto p INNER JOIN producto_envase pe ON
p.producto_id = pe.producto_id INNER JOIN marca m ON m.marca_id = p.marca_id INNER JOIN unidad_medida um ON
pe.unidad_medida_id = um.unidad_medida_id INNER JOIN tipo_producto tp ON p.tipo_producto_id = tp.tipo_producto_id
INNER JOIN lista_precio_producto lpp ON lpp.producto_envase_id = pe.producto_envase_id
WHERE p.descripcion = '{producto}' and m.descripcion = '{marca}' and um.descripcion = '{uMedida}'
"""
UNIDADMEDIDA_IDE = """
SELECT um.unidad_medida_id FROM unidad_medida um WHERE um.descripcion = '{uMedida}'
"""

TIPOPRODUCTOID =  """
SELECT tp.tipo_producto_id FROM tipo_producto tp WHERE tp.descripcion = '{tp}'
"""

ENVASE_IDE = """
SELECT e.envase_id FROM envase e WHERE e.descripcion = '{envase}'
"""

PRODUCTO_IDE ="""
	SELECT p.producto_id FROM producto p INNER JOIN marca m WHERE p.descripcion ='{producto}' and m.descripcion = '{marca}'
"""

INSERT_T_PRODUCTO = """ INSERT INTO producto (descripcion,marca_id,tipo_producto_id)
VALUES ('{producto}',{marca},{tProd}); """


INSERT_T_PRODUCTO_ENVASE = """ INSERT INTO producto_envase (producto_id,envase_id,unidad_medida_id,stock_real)
VALUES ({producto},{envase},{uMedida},0); """

CONSULTAR_ID_UMEDIDA = """
SELECT um.unidad_medida_id FROM unidad_medida um WHERE um.descripcion = '{uMedida}'
"""

CONSULTAR_ID_MARCA = """
SELECT m.marca_id FROM marca m WHERE m.descripcion = '{marca}'
"""

CONSULTA_ID_PRODUCTO_MARCA_UMEDIDA =  """ SELECT (pe.producto_envase_id) FROM producto p INNER JOIN
producto_envase pe on p.producto_id = pe.producto_id
WHERE p.marca_id = {marca} AND pe.unidad_medida_id = {uMedida} AND p.descripcion = '{producto}' """

CONSULTA_STOCK1 = """
SELECT p.descripcion as producto, m.descripcion as marca, um.descripcion as umedida, lpp.precio as precio,
tp.descripcion as tipoProd,pe.stock_real as stock, e.descripcion as envase FROM producto p INNER JOIN producto_envase pe ON
p.producto_id = pe.producto_id INNER JOIN marca m ON m.marca_id = p.marca_id INNER JOIN unidad_medida um ON
pe.unidad_medida_id = um.unidad_medida_id INNER JOIN tipo_producto tp ON p.tipo_producto_id = tp.tipo_producto_id
INNER JOIN lista_precio_producto lpp ON lpp.producto_envase_id = pe.producto_envase_id INNER JOIN envase e ON e.envase_id = pe.envase_id
WHERE pe.producto_envase_id = {producto_envase_id}
"""


ELIMINAR_PRODUCTO_ENVASE = """
DELETE FROM producto_envase WHERE producto_envase_id = {producto}
"""

CONSULTAR_ID_PRODUCTO = """
SELECT p.producto_id FROM producto p INNER JOIN marca m on m.marca_id = p.marca_id
INNER JOIN unidad_medida um ON um.unidad_medida_id = pe.unidad_medida_id
WHERE m.descripcion = '{marca}' AND um.descripcion = '{uMedida}' AND p.descripcion = '{producto}'
"""

ELIMINAR_PRODUCTO = """
DELETE FROM producto WHERE producto_id = {producto}
"""
CONSULTAR_ID_PRODUCTO_MARCA_UMEDIDA =  """ SELECT pe.producto_envase_id, p.producto_id FROM producto p INNER JOIN
producto_envase pe on p.producto_id=pe.producto_id
WHERE p.marca_id = {marca} AND pe.unidad_medida_id = {uMedida} and p.descripcion = '{producto}'"""



UPDATEPRODUCTOENVASE = """
UPDATE producto_envase SET envase_id = {e} , unidad_medida_id = {um} WHERE producto_envase_id = {pe_id}
"""

UPDATEPRODUCTO = """
UPDATE producto SET descripcion= '{pro}', marca_id = {m} , tipo_producto_id = {tp} WHERE producto_id = {p}
"""
