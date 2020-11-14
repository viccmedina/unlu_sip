LISTAR_PRODUCTOS = """ SELECT p.descripcion as descripcion ,
	m.descripcion as marca, tp.descripcion as tipo_producto
	FROM producto AS p LEFT JOIN tipo_producto AS tp ON
	tp.tipo_producto_id=p.tipo_producto_id
	LEFT JOIN marca AS m ON m.marca_id=p.marca_id"""

PRODUCTO_ENVASE_BY_PRODUCTO_ID = """ SELECT pe.producto_envase_id, p.descripcion,
    m.descripcion, lpp.precio, e.descripcion, u.descripcion, pe.ts_created
    FROM producto_envase AS pe
    INNER JOIN producto AS p ON p.producto_id = pe.producto_id
    INNER JOIN marca AS m ON m.marca_id = p.marca_id
    INNER JOIN lista_precio_producto AS lpp ON lpp.producto_envase_id = pe.producto_envase_id
    INNER JOIN envase AS e ON e.envase_id = pe.envase_id
    INNER JOIN unidad_medida AS u ON u.unidad_medida_id = pe.unidad_medida_id
    WHERE pe.producto_id = ('{producto_id}')"""