CREATE_TRIGGER_BUmov_stock= """
CREATE TRIGGER BU_mov_stock
BEFORE UPDATE ON producto_envase
BEGIN
    SELECT CASE
    WHEN (NEW.stock_real < 0 )THEN
    RAISE(ABORT, 'Error - El stock no puedo ser menor a 0 ')
    END;
END;

"""

CREATE_TRIGGER_BIPedido = """
CREATE TRIGGER BI_Pedido
BEFORE INSERT ON pedido
BEGIN
SELECT CASE
    WHEN ((select p.pedido_id from pedido p where new.usuario_id = usuario_id and
    estado_pedido_id = 1) IS NOT NULL) THEN
    RAISE(ABORT, 'Error - Cliente con pedido pendiente de confirmacion ')
END;
END;
"""

# Por ids
CREATE_TRIGGER_BU_Pedido = """
CREATE TRIGGER BU_Pedido
BEFORE UPDATE ON pedido
BEGIN
    SELECT CASE
    WHEN (old.estado_pedido_id = 1 and new.estado_pedido_id = 3 or
        old.estado_pedido_id = 1 and new.estado_pedido_id = 4 or
        old.estado_pedido_id = 1 and new.estado_pedido_id = 5 or
        old.estado_pedido_id = 1 and new.estado_pedido_id = 6 or
        old.estado_pedido_id = 1 and new.estado_pedido_id = 8)THEN
        RAISE(ABORT, 'Error - Cambio de estado del pedido incorrecto ')
    END;
    SELECT CASE
    WHEN (old.estado_pedido_id = 2 and new.estado_pedido_id = 1 or
        old.estado_pedido_id = 2 and new.estado_pedido_id = 4 or
        old.estado_pedido_id = 2 and new.estado_pedido_id = 5 or
        old.estado_pedido_id = 2 and new.estado_pedido_id = 6 or
        old.estado_pedido_id = 2 and new.estado_pedido_id = 8)THEN
        RAISE(ABORT, 'Error - Cambio de estado del pedido incorrecto ')
    END;
    SELECT CASE
        WHEN (old.estado_pedido_id = 3 and new.estado_pedido_id = 1 or
        old.estado_pedido_id = 3 and new.estado_pedido_id = 2 or
        old.estado_pedido_id = 3 and new.estado_pedido_id = 5 or
        old.estado_pedido_id = 3 and new.estado_pedido_id = 6 or
        old.estado_pedido_id = 3 and new.estado_pedido_id = 7 or
        old.estado_pedido_id = 3 and new.estado_pedido_id = 8)THEN
        RAISE(ABORT, 'Error - Cambio de estado del pedido incorrecto ')
    END;
    SELECT CASE
        WHEN (old.estado_pedido_id = 4 and new.estado_pedido_id = 1 or
        old.estado_pedido_id = 4 and new.estado_pedido_id = 2 or
        old.estado_pedido_id = 4 and new.estado_pedido_id = 3 or
        old.estado_pedido_id = 4 and new.estado_pedido_id = 7 or
        old.estado_pedido_id = 4 and new.estado_pedido_id = 8)THEN
        RAISE(ABORT, 'Error - Cambio de estado del pedido incorrecto ')
    END;
    SELECT CASE
        WHEN (old.estado_pedido_id = 5 and new.estado_pedido_id = 1 or
        old.estado_pedido_id = 5 and new.estado_pedido_id = 2 or
        old.estado_pedido_id = 5 and new.estado_pedido_id = 3 or
        old.estado_pedido_id = 5 and new.estado_pedido_id = 4 or
        old.estado_pedido_id = 5 and new.estado_pedido_id = 7)THEN
        RAISE(ABORT, 'Error - Cambio de estado del pedido incorrecto ')
    END;
    SELECT CASE
        WHEN (old.estado_pedido_id = 6 and new.estado_pedido_id = 1 or
        old.estado_pedido_id = 6 and new.estado_pedido_id = 2 or
        old.estado_pedido_id = 6 and new.estado_pedido_id = 3 or
        old.estado_pedido_id = 6 and new.estado_pedido_id = 4 or
        old.estado_pedido_id = 6 and new.estado_pedido_id = 7 )THEN
        RAISE(ABORT, 'Error - Cambio de estado del pedido incorrecto ')
    END;

END;
"""

# Por desc corta del pedido estado
CREATE_TRIGGER_BU_Pedido2 ="""
CREATE TRIGGER BU_Pedido
BEFORE UPDATE ON pedido
BEGIN
    SELECT CASE
    WHEN (old.descripcion_corta = 'PCO' and new.descripcion_corta = 'PCC' or
        old.descripcion_corta = 'PCO' and new.descripcion_corta = 'EC' or
        old.descripcion_corta = 'PCO' and new.descripcion_corta = 'E' or
        old.descripcion_corta = 'PCO' and new.descripcion_corta = 'D' or
        old.descripcion_corta = 'PCO' and new.descripcion_corta = 'RPO' or
        old.descripcion_corta = 'PCO' and new.descripcion_corta = 'APC')THEN
        RAISE(ABORT, 'Error - Cambio de estado del pedido incorrecto ')
    END;
    SELECT CASE
        WHEN (old.descripcion_corta = 'EP' and new.estado_pedido_id = 'PCC' or
        old.descripcion_corta = 'EP' and new.descripcion_corta = 'PCO' or
        old.descripcion_corta = 'EP' and new.descripcion_corta = 'E' or
        old.descripcion_corta = 'EP' and new.descripcion_corta = 'D' or
        old.descripcion_corta = 'EP' and new.descripcion_corta = 'RPO' or
        old.descripcion_corta = 'EP' and new.descripcion_corta = 'APC')THEN
        RAISE(ABORT, 'Error - Cambio de estado del pedido incorrecto ')
    END;
    SELECT CASE
        WHEN (old.descripcion_corta = 'EC' and new.descripcion_corta = 'PCC' or
        old.descripcion_corta = 'EC' and new.descripcion_corta = 'PCO' or
        old.descripcion_corta = 'EC' and new.descripcion_corta = 'EP' or
        old.descripcion_corta = 'EC' and new.descripcion_corta = 'D' or
        old.descripcion_corta = 'EC' and new.descripcion_corta = 'RPO' or
        old.descripcion_corta = 'EC' and new.descripcion_corta = 'APC')THEN
        RAISE(ABORT, 'Error - Cambio de estado del pedido incorrecto ')
    END;
    SELECT CASE
        WHEN (old.descripcion_corta = 'E' and new.descripcion_corta = 'PCC' or
        old.descripcion_corta = 'E' and new.descripcion_corta = 'PCO' or
        old.descripcion_corta = 'E' and new.descripcion_corta = 'EP' or
        old.descripcion_corta = 'E' and new.descripcion_corta = 'EC' or
        old.descripcion_corta = 'E' and new.descripcion_corta = 'D' or
        old.descripcion_corta = 'E' and new.descripcion_corta = 'RPO' or
        old.descripcion_corta = 'E' and new.descripcion_corta = 'APC')THEN
        RAISE(ABORT, 'Error - Cambio de estado del pedido incorrecto ')
    END;
    SELECT CASE
        WHEN (old.descripcion_corta = 'D' and new.descripcion_corta = PCC' or
        old.descripcion_corta = 'D' and new.descripcion_corta = 'PCO' or
        old.descripcion_corta = 'D' and new.descripcion_corta = 'EP' or
        old.descripcion_corta = 'D' and new.descripcion_corta = 'EC' or
        old.descripcion_corta = 'D' and new.descripcion_corta = 'RPO' or
        old.descripcion_corta = 'D' and new.descripcion_corta = 'APC')THEN
        RAISE(ABORT, 'Error - Cambio de estado del pedido incorrecto ')
    END;

END;
"""



#CREATE TRIGGER BI_Pedido BEFORE INSERT ON pedidos BEGIN SELECT CASE WHEN ((select p.pedido_id from pedido p where new.usuario_id = old.usuario_id and estado_pedido_id = 1) ISNOTNULL) THEN RAISE(ABORT, 'Error - Cliente con pedido pendiente de confirmacion ')END;END;
