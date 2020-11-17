# consulta la suma cantidad de producto "Cargados" en detalle_stock
CONSULTA_STOCK = """ SELECT p.descripcion as descripcion_p,m.descripcion as descripcion_m,um.descripcion, pe.stock_real
FROM (((producto_envase pe INNER JOIN producto p on p.producto_id=pe.producto_id )
INNER JOIN marca m on p.marca_id=m.marca_id)
INNER JOIN unidad_medida um on um.unidad_medida_id=pe.unidad_medida_id)
WHERE pe.producto_envase_id = {producto_id}  """

CONSULTAR_ID_MARCA = """SELECT m.marca_id FROM marca m WHERE m.descripcion = ('{marca}')"""

CONSULTAR_ID_UMEDIDA = """SELECT um.unidad_medida_id FROM unidad_medida um WHERE um.descripcion = ('{uMedida}')"""

CONSULTAR_ID_PRODUCTO = """ SELECT (pe.producto_envase_id) FROM producto p INNER JOIN
producto_envase pe on p.producto_id=pe.producto_id WHERE p.descripcion = ('{producto}') and pe.unidad_medida_id = {uMedida} and
p.marca_id = {marca} """

INSERT_MOVIMIENTO_STOCK = """ INSERT INTO movimiento_stock (tipo_movimiento_stock_id,usuario_id,
producto_envase_id,descripcion,cantidad) VALUES ({tipo_movimiento},{usuario_id},{producto_envase_id},'{descripcion}',{cantidad}); """

UPDATE_STOCK_REAL = """UPDATE producto_envase SET stock_real = stock_real + {cantidad}  WHERE
producto_envase_id = {producto_envase_id}"""

BAJA_PRODUCTO = """UPDATE producto_envase SET stock_real = stock_real - {cantidad}  WHERE
producto_envase_id = {producto_envase_id}"""

CONSULTAR_MOVIMIENTOS = """
    SELECT p.descripcion as descripcion_p, m.descripcion as descripcion_m, um.descripcion, u.username,
    mov.ts_created, mov.cantidad FROM
    (((((movimiento_stock mov INNER JOIN producto_envase pe on mov.producto_envase_id=pe.producto_envase_id)
    INNER JOIN producto p on p.producto_id= pe.producto_id)
    INNER JOIN marca m on p.marca_id= m.marca_id)
    INNER JOIN unidad_medida um on um.unidad_medida_id=pe.unidad_medida_id)
    INNER JOIN usuario u on u.id=mov.usuario_id)
	WHERE mov.ts_created >= DATETIME('{f_desde}') and mov.ts_created <= ('{f_hasta}')
"""
#""" INSERT INTO movimiento_stock (tipo_movimiento_stock_id,usuario_id,producto_id,descripcion,cantidad) VALUES (1,3,1,'cargaHarina',50); """




#SELECT p.descripcion as descripcion_p, m.descripcion as descripcion_m, um.descripcion, u.username, mov.ts_created, mov.cantidad FROM ((((movimiento_stock mov INNER JOIN producto_envase pe on mov.producto_envase_id=producto_envase_id) INNER JOIN producto p on p.producto_id= pe.producto_id) INNER JOIN marca m on p.marca_id= m.marca_id) INNER JOIN unidad_medida um on um.unidad_medida_id=pe.unidad_medida_id INNER JOIN usuario u on u.id=mov.usuario_id) WHERE mov.ts_created>=DATETIME('2020/11/10') and mov.ts_created<=('2020/11/17');
