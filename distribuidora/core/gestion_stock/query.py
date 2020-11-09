# consulta la suma cantidad de producto "Cargados" en detalle_stock
CONSULTA_STOCK = """ SELECT
    (SELECT sum(cantidad) FROM movimiento_stock WHERE tipo_movimiento_stock_id = 1 and producto_id = {producto_id})
    -
    (SELECT sum(cantidad) FROM movimiento_stock WHERE tipo_movimiento_stock_id = 2 and producto_id = {producto_id}) """

CONSULTAR_ID_MARCA = """SELECT m.marca_id FROM marca m WHERE m.descripcion = ('{marca}')"""

CONSULTAR_ID_UMEDIDA = """SELECT um.unidad_medida_id FROM unidad_medida um WHERE um.descripcion = ('{uMedida}')"""

CONSULTAR_ID_PRODUCTO = """ SELECT DISTINCT (p.producto_id) FROM producto p INNER JOIN
producto_envase pe WHERE p.descripcion = '{producto}' and pe.unidad_medida_id = {uMedida} and
p.marca_id = {marca}"""


CONSULTA_ENTRADA_STOCK = """ SELECT sum(cantidad) FROM movimiento_stock WHERE tipo_movimiento_stock_id = 1 and producto_id = {producto_id} """

CONSULTA_SALIDA_STOCK = """ SELECT sum(cantidad) FROM movimiento_stock WHERE tipo_movimiento_stock_id = 2 and producto_id = {producto_id} """
#SELECT ((SELECT sum(cantidad) FROM movimiento_stock WHERE tipo_movimiento_stock_id = 1 and producto_id = 3 ) - (SELECT sum(cantidad) FROM movimiento_stock WHERE tipo_movimiento_stock_id = 2 and producto_id = 3));

#SELECT sum(cantidad) FROM movimiento_stock WHERE tipo_movimiento_stock_id = 1 and producto_id = 3;
