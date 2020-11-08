LISTAR_PRODUCTOS = """ SELECT p.descripcion as descripcion ,
	m.descripcion as marca, tp.descripcion as tipo_producto 
	FROM producto AS p LEFT JOIN tipo_producto AS tp ON
	tp.tipo_producto_id=p.tipo_producto_id 
	LEFT JOIN marca AS m ON m.marca_id=p.marca_id"""