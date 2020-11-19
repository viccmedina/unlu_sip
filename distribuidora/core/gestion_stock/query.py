# consulta la suma cantidad de producto "Cargados" en detalle_stock
CONSULTA_STOCK = """ SELECT p.descripcion AS descripcion_p,m.descripcion as descripcion_m,
um.descripcion, pe.stock_real - (select sum(dp.cantidad) from producto_envase pee
INNER JOIN detalle_pedido dp ON pee.producto_envase_id=dp.producto_envase_id
INNER JOIN pedido p ON p.pedido_id= dp.pedido_id WHERE pee.producto_envase_id = {producto_id}
AND p.estado_pedido_id = 1) AS cantidad FROM (((producto_envase pe INNER JOIN producto p
ON p.producto_id=pe.producto_id )
INNER JOIN marca m ON p.marca_id=m.marca_id)
INNER JOIN unidad_medida um ON um.unidad_medida_id=pe.unidad_medida_id)
WHERE pe.producto_envase_id = {producto_id}

 """


CONSULTA_STOCK1 = """ SELECT p.descripcion AS descripcion_p,m.descripcion as descripcion_m,
um.descripcion, pe.stock_real AS cantidad FROM (((producto_envase pe INNER JOIN producto p
ON p.producto_id=pe.producto_id )
INNER JOIN marca m ON p.marca_id=m.marca_id)
INNER JOIN unidad_medida um ON um.unidad_medida_id=pe.unidad_medida_id)
WHERE pe.producto_envase_id = {producto_id}
"""

CONSULTAR_ID_MARCA = """SELECT m.marca_id FROM marca m WHERE m.descripcion = ('{marca}')"""

CONSULTAR_ID_UMEDIDA = """SELECT um.unidad_medida_id FROM unidad_medida um WHERE um.descripcion = ('{uMedida}')"""

CONSULTAR_ID_PRODUCTO = """ SELECT (pe.producto_envase_id) FROM producto p INNER JOIN
producto_envase pe on p.producto_id=pe.producto_id WHERE p.descripcion = ('{producto}') and pe.unidad_medida_id = {uMedida} and
p.marca_id = {marca} """

INSERT_MOVIMIENTO_STOCK = """ INSERT INTO movimiento_stock (tipo_movimiento_stock_id,usuario_id,
producto_envase_id,descripcion,cantidad) VALUES ({tipo_movimiento},{usuario_id},{producto_envase_id},'{descripcion}',{cantidad}); """

UPDATE_STOCK_REAL = """UPDATE producto_envase SET stock_real = stock_real + '{cantidad}'  WHERE
producto_envase_id = {producto_envase_id}"""

BAJA_PRODUCTO = """UPDATE producto_envase SET stock_real = stock_real - '{cantidad}'  WHERE
producto_envase_id = '{producto_envase_id}' AND (stock_real - '{cantidad}' >= 0) """

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







#SELECT p.descripcion AS descripcion_p,m.descripcion as descripcion_m, um.descripcion, pe.stock_real - (select sum(dp.cantidad) from producto_envase pee INNER JOIN detalle_pedido dp ON pee.producto_envase_id=dp.producto_envase_id INNER JOIN pedido p ON p.pedido_id= dp.pedido_id WHERE pee.producto_envase_id = 1 AND p.estado_pedido_id = 1) AS cantidad FROM (((producto_envase pe INNER JOIN producto p ON p.producto_id=pe.producto_id ) INNER JOIN marca m ON p.marca_id=m.marca_id) INNER JOIN unidad_medida um ON um.unidad_medida_id=pe.unidad_medida_id) WHERE pe.producto_envase_id = 1;




""" SELECT p.descripcion AS descripcion_p,m.descripcion as descripcion_m,
um.descripcion, pe.stock_real - (select sum(dp.cantidad) from producto_envase pee
INNER JOIN detalle_pedido dp ON pee.producto_envase_id=dp.producto_envase_id
INNER JOIN pedido p ON p.pedido_id= dp.pedido_id WHERE pee.producto_envase_id = {producto_id}
AND p.estado_pedido_id = 1) AS cantidad FROM (((producto_envase pe INNER JOIN producto p
ON p.producto_id=pe.producto_id )
INNER JOIN marca m ON p.marca_id=m.marca_id)
INNER JOIN unidad_medida um ON um.unidad_medida_id=pe.unidad_medida_id)
WHERE pe.producto_envase_id = {producto_id}  """

"""



select pe.stock_real - (select sum(dp.cantidad) from producto_envase pee inner join
detalle_pedido dp on pee.producto_envase_id=dp.producto_envase_id
inner join pedido p on p.pedido_id= dp.pedido_id where pee.producto_envase_id = 1
and p.estado_pedido_id = 1) as cantidad from producto_envase pe where pe.producto_envase_id = 1;"""

"""
select pe.stock_real - (select sum(dp.cantidad) from producto_envase pee inner join
detalle_pedido dp on pee.producto_envase_id=dp.producto_envase_id
inner join pedido p on p.pedido_id= dp.pedido_id where pee.producto_envase_id = {producto_id}
and p.estado_pedido_id = 1) as cantidad from producto_envase pe where pe.producto_envase_id = {producto_id}
"""
#""" INSERT INTO movimiento_stock (tipo_movimiento_stock_id,usuario_id,producto_id,descripcion,cantidad) VALUES (1,3,1,'cargaHarina',50); """



"""
SELECT p.descripcion as descripcion_p, m.descripcion as descripcion_m, um.descripcion, u.username,
mov.ts_created, mov.cantidad FROM ((((movimiento_stock mov INNER JOIN producto_envase pe
on mov.producto_envase_id=pe.producto_envase_id) INNER JOIN producto p
on p.producto_id= pe.producto_id) INNER JOIN marca m on p.marca_id= m.marca_id)
INNER JOIN unidad_medida um on um.unidad_medida_id=pe.unidad_medida_id
INNER JOIN usuario u on u.id=mov.usuario_id)
WHERE mov.ts_created >= DATETIME('2020-11-10') and mov.ts_created <= ('2020-11-18');


"""








# andaba consulta stock
""" SELECT p.descripcion as descripcion_p,m.descripcion as descripcion_m,
um.descripcion, pe.stock_real as cantidad FROM (((producto_envase pe INNER JOIN producto p on p.producto_id=pe.producto_id )
INNER JOIN marca m on p.marca_id=m.marca_id)
INNER JOIN unidad_medida um on um.unidad_medida_id=pe.unidad_medida_id)
WHERE pe.producto_envase_id = {producto_id}  """
