from distribuidora import db

class Tipo_movimiento(db.Model):
    """
    Este modelo representará el tipo de movimiento.
    Contará con los siquientes campos:
    tipo_movimiento_id --> clave primaria
    descripcion --> describe el tipo de moviemiento
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'tipo_movimiento'

    # Atributos
    tipo_movimiento_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, descripcion):
        """
        Constructor de la clase tipo de movimiento
        """
        self.descripcion = descripcion

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'tipo de movimiento:  {}'.format(self.descripcion)


##########################################################
class Tipo_pedido(db.Model):
    """
    Este modelo representará el tipo de pedido.
    Contará con los siquientes campos:
    tipo_pedido_id --> clave primaria
    descripcion --> describe el tipo de pedido
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'tipo_pedido'

    # Atributos
    tipo_pedido_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())
    def __init__(self, descripcion):
        """
        Constructor de la clase tipo de pedido
        """
        self.descripcion = descripcion

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'tipo de pedido:  {}'.format(self.descripcion)

#############################################################################

class Tipo_Producto(db.Model):
    """
    Este modelo representará el tipo de Producto
    Contará con los siquientes campos:
    tipo_producto_id --> clave primaria
    descripcion --> describe el tipo de producto
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'tipo_producto'

    # Atributos
    tipo_producto_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    # producto = db.relationship('Producto', backref='tipo_producto', lazy=True)
    def __init__(self, descripcion):
        """
        Constructor de la clase tipo_producto
        """
        self.descripcion = descripcion

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'tipo de producto:  {}'.format(self.descripcion)


########################################################################################
class movimiento_stock(db.Model):
	"""
	Este modelo representará el movimiento del stock.
	Contará con los siquientes campos:
	movimiento_stock_id --> clave primaria
	descripcion --> describe el tipo de dni
	ts_created --> momento en que el registro fue creado
	"""

	# Nombre de la tabla
	__tablename__ = 'movimiento_stock'

	# Atributos
	movimiento_stock_id = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(80), nullable=False)
	ts_created = db.Column(db.DateTime, server_default=db.func.now())

	def __init__(self, descripcion):
		"""
		Constructor de la clase movimiento_stock
		"""
		self.descripcion = descripcion

	def __repr__(self):
		"""
		Nos devolverá una representación del Modelo
		"""
		return 'movimiento de stock:  {}'.format(self.descripcion)


#####################################################################################
class Estado_pedido(db.Model):
	"""
	Este modelo representará los estados de pedidos.
	Contará con los siquientes campos:
	estado_pedido_id --> clave primaria
	descripcion --> describe el estado del pedido
	ts_created --> momento en que el registro fue creado
	"""

	# Nombre de la tabla
	__tablename__ = 'estado_pedido'

	# Atributos
	estado_pedido_id = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(80), nullable=False)
	ts_created = db.Column(db.DateTime, server_default=db.func.now())

	def __init__(self, descripcion):
		"""
		Constructor de la clase Estado_pedido
		"""
		self.descripcion = descripcion

	def __repr__(self):
		"""
		Nos devolverá una representación del Modelo
		"""
		return 'Estado del pedido:  {}'.format(self.descripcion)

#################################################################################
class Estado_producto(db.Model):
	"""
	Este modelo representará los estados de producto.
	Contará con los siquientes campos:
	estado_producto_id --> clave primaria
	descripcion --> describe el estado del producto
	ts_created --> momento en que el registro fue creado
	"""

	# Nombre de la tabla
	__tablename__ = 'estado_producto'

	# Atributos
	estado_producto_id = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(80), nullable=False)
	ts_created = db.Column(db.DateTime, server_default=db.func.now())

	def __init__(self, descripcion):
		"""
		Constructor de la clase Estado_producto
		"""
		self.descripcion = descripcion

	def __repr__(self):
		"""
		Nos devolverá una representación del Modelo
		"""
		return 'Estado del producto:  {}'.format(self.descripcion)