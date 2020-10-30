CONSULTA_CTA_CORRIENTE = """
	SELECT * FROM movimiento_cta_corriente 
	WHERE cta_corriente == {id_cuenta_corriente} and 
	ts_created>=DATETIME('{fecha_desde}') and ts_created<=('{fecha_hasta}')"""