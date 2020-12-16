CONSULTAR_NRO_CUENTA_CORRIENTE = """
	SELECT cuenta_corriente_id FROM cuenta_corriente
	WHERE persona_id=('{nro_cliente}')
"""

CONSULTA_MOVIMIENTOS_CTA_CORRIENTE_BY_OPERADOR = """
	SELECT * FROM movimiento_cta_corriente
	WHERE ts_created BETWEEN '{fecha_desde}' and '{fecha_hasta}' and cta_corriente=('{nro_cliente}')
	"""

CONSULT_ALL_USERS= """
SELECT u.id FROM usuario u inner join usuario_rol ur on ur.id = u.id inner join rol r on r.rol_id = ur.rol_id
WHERE r.nombre != 'Gerencia' AND r.nombre != 'Operador'
"""

CONSULTAR_MONTO_CC ="""
SELECT sum(saldo) as saldoCC FROM movimiento_cta_corriente mccc WHERE mccc.usuario = {user}
"""

CONSULTAR_MONTO_CP = """
SELECT sum(monto) as saldoCP FROM comprobante_pago cpp INNER JOIN pedido ped on cpp.pedido = ped.pedido_id
inner join usuario u on ped.usuario_id = u.id WHERE u.id = {user}
"""

CONSULTA_MOVIMIENTOS_CTA_CORRIENTE = """
	SELECT cc.cuenta_corriente_id AS cliente,p.nombre AS nombre,p.email AS email, p.telefono_ppal AS telefono,cp.monto as monto ,mcc.saldo as saldo
	FROM movimiento_cta_corriente mcc
	INNER JOIN cuenta_corriente cc ON mcc.cta_corriente = cc.cuenta_corriente_id
	INNER JOIN persona p ON cc.persona_id = p.persona_id
	INNER JOIN pedido pe ON pe.usuario_id = mcc.usuario
	INNER JOIN usuario u ON u.id = mcc.usuario
	INNER JOIN usuario_rol ur ON ur.id = u.id
	INNER JOIN rol r ON r.rol_id = ur.rol_id
	INNER JOIN comprobante_pago cp ON cp.pedido = pe.pedido_id
	WHERE mcc.usuario = {user} AND r.nombre != 'Gerencia' AND r.nombre != 'Operador'

	"""

#(SELECT sum(saldo) FROM movimiento_cta_corriente mccc WHERE mccc.usuario = 4) - (SELECT sum(monto) FROM comprobante_pago cpp INNER JOIN pedido ped on cpp.pedido = ped.pedido_id inner join usuario u on ped.usuario_id = u.id WHERE u.id = 4;


SELECT_TIPO_MOVIMIENTOS = """
	SELECT descripcion FROM tipo_movimiento_cta_corriente
	"""

SELECT_ID_TIPO_MOVIMIENTO = """
	SELECT id FROM tipo_movimiento_cta_corriente
	WHERE descripcion=('{tipo_movimiento}')
"""

INSERT_MOV_CTA_CORRIENTE = """ INSERT INTO movimiento_cta_corriente
(cta_corriente, tipo_movimiento_cta_corriente, usuario, saldo, descripcion)
VALUES ('{n_cta}', '{t_mov}', '{user}', '{monto}', '{descripcion}') """

# primero sumo todas las deudas(id= 2) y desp le resto los pagos y reembolsos (id= 1 y3 )

CONSULTAR_SALDO = """SELECT DISTINCT mcc.cta_corriente AS cta_corriente, p.email AS email, p.nombre as nombre,
	((SELECT sum(mov.saldo) FROM movimiento_cta_corriente mov WHERE cta_corriente = {nro_cta}
	and tipo_movimiento_cta_corriente = 2)
	-
	(SELECT sum(mov.saldo * -1) FROM movimiento_cta_corriente mov  WHERE cta_corriente = {nro_cta}
	and tipo_movimiento_cta_corriente = 1 or tipo_movimiento_cta_corriente = 3 )) AS saldo
	FROM movimiento_cta_corriente mcc INNER JOIN cuenta_corriente cc ON mcc.cta_corriente = cc.cuenta_corriente_id
	INNER JOIN persona p ON cc.persona_id = p.persona_id WHERE mcc.cta_corriente = {nro_cta}

"""

SELECT_COMPROBANTES_PAGO_ADEUDA = """ SELECT ecp.descripcion_corta, cp.comprobante_id, p.usuario_id, cp.monto
    FROM comprobante_pago AS cp
    INNER JOIN pedido AS p ON cp.pedido=p.pedido_id
    INNER JOIN estado_comprobante_pago AS ecp ON
    ecp.estado_comprobante_pago_id=cp.estado_comprobante_pago_id
    WHERE ecp.descripcion='{estado}' AND p.usuario_id='{usuario_id}' AND
    cp.monto='{monto}' LIMIT 1"""


UPDATE_ESTADO_COMPROBANTE = """ UPDATE comprobante_pago
    SET estado_comprobante_pago_id='{estado}'
    WHERE comprobante_id='{comprobante_id}'
"""

"""
SELECT DISTINCT mcc.cta_corriente AS cta_corriente, p.email AS user,
((SELECT sum(mov1.saldo) FROM movimiento_cta_corriente mov1 WHERE mov1.cta_corriente = 1 and
mov1.tipo_movimiento_cta_corriente = 2)
-
(SELECT sum(mov.saldo * -1) FROM movimiento_cta_corriente mov
WHERE mov.cta_corriente = 1 and mov.tipo_movimiento_cta_corriente = 1 or mov.tipo_movimiento_cta_corriente = 3 )) AS saldo
FROM movimiento_cta_corriente mcc INNER JOIN cuenta_corriente cc ON mcc.cta_corriente = cc.cuenta_corriente_id
INNER JOIN persona p ON cc.persona_id = p.persona_id WHERE mcc.cta_corriente = 1 ;


1|cliente@prueba.com.ar|-1501.0
"""
