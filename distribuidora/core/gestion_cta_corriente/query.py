CONSULTAR_NRO_CUENTA_CORRIENTE = """
	SELECT cuenta_corriente_id FROM cuenta_corriente
	WHERE persona_id=('{nro_cliente}')
"""

CONSULTA_MOVIMIENTOS_CTA_CORRIENTE = """

	SELECT * FROM movimiento_cta_corriente
	WHERE ts_created>=DATETIME('{fecha_desde}') and
		ts_created<=('{fecha_hasta}') and cta_corriente=('{nro_cliente}')


	"""

SELECT_TIPO_MOVIMIENTOS = """

	SELECT descripcion FROM tipo_movimiento_cta_corriente
	"""
