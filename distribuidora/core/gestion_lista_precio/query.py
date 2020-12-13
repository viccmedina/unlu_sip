CONSULTAR_MARCA = """
SELECT m.marca_id FROM marca m WHERE m.descripcion = '{marca}'
"""

CONSULTAR_U_MEDIDA = """
SELECT um.unidad_medida_id FROM unidad_medida um WHERE um.descripcion = '{umedida}'
"""

CONSULTAR_PRODUCTO = """
SELECT pe.producto_envase_id AS producto FROM producto_envase pe
INNER JOIN producto p ON p.producto_id = pe.producto_envase_id
INNER JOIN marca m ON m.marca_id = p.marca_id
INNER JOIN unidad_medida um ON um.unidad_medida_id = pe.unidad_medida_id
WHERE p.descripcion = '{producto}' AND m.marca_id = {marca} AND um.unidad_medida_id = {umedida}
"""


CONSULTAR_PRECIO ="""
SELECT p.descripcion AS producto, m.descripcion AS marca, um.descripcion AS umedida, e.descripcion AS envase, lpp.precio AS precio,
lpp.fecha_fin AS vigencia, pe.producto_envase_id AS id, CURRENT_TIMESTAMP AS hoy
FROM producto_envase pe INNER JOIN producto p ON p.producto_id = pe.producto_id
INNER JOIN marca m ON m.marca_id = p.marca_id
INNER JOIN unidad_medida um ON um.unidad_medida_id = pe.unidad_medida_id
INNER JOIN lista_precio_producto lpp ON lpp.producto_envase_id = pe.producto_envase_id
INNER JOIN envase e ON e.envase_id = pe.envase_id
WHERE pe.producto_envase_id = {producto} AND lpp.fecha_inicio <= (CURRENT_TIMESTAMP) AND lpp.fecha_fin >= (CURRENT_TIMESTAMP)
"""

AGREGAR_PRECIO = """
INSERT INTO lista_precio (fecha_desde,fecha_hasta) VALUES (CURRENT_TIMESTAMP,'{fecha}')
"""

CONSULTAR_ID_PRECIO = """
SELECT lp.precio_id FROM lista_precio lp WHERE lp.fecha_hasta = '{fecha}'
"""
AGREGAR_PRECIO_PRODUCTO = """
INSERT INTO lista_precio_producto (producto_envase_id,precio_id,precio,fecha_inicio,fecha_fin)
VALUES ({producto},{id},'{precio}',CURRENT_TIMESTAMP,'{fecha}')
"""


ACTUALIZAR_PRECIO ="""
UPDATE lista_precio_producto SET precio = {precio} WHERE producto_envase_id = {producto}
"""

ACTUALIZAR_FECHA ="""
UPDATE lista_precio SET fecha_hasta = datetime('{fecha}') WHERE precio_id = {id}
"""

ACTUALIZAR_FECHA_PP ="""
UPDATE lista_precio_producto SET fecha_fin = datetime('{fecha}') WHERE precio_id = {id} and producto_envase_id = {producto}
"""

ACTUALIZAR_FECHA_PRECIO = """
UPDATE lista_precio SET fecha_hasta = datetime('{fecha}') WHERE precio_id = {id}
"""

ACTUALIZAR_FECHA_PRECIO_LISTA ="""
UPDATE lista_precio_producto SET fecha_fin = datetime('{fecha}'), precio = {precio} WHERE precio_id = {id} and producto_envase_id = {producto}
"""
