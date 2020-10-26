CONSULTA_CTA_CORRIENTE = """
	SELECT * FROM movimiento_cta_corriente 
	WHERE ts_created>=DATETIME('{fecha_desde}') and ts_created<=('{fecha_hasta}')"""