from distribuidora import db


class Lista_precio(db.Model):
    """
    Este modelo representará a la lista de precios.
    Contará con los siquientes campos:
    precio_id  --> clave primaria
    descripcion --> descripcion del precio
    valor --> describe el valor numerico del precio
    lista_precio_id --> clave forania refenciando a la tabla lista de precios
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'lista_precio'

    # Atributos
    precio_id = db.Column(db.Integer, primary_key=True)
    fecha_desde = db.Column(db.DateTime, nullable=True)
    fecha_hasta = db.Column(db.DateTime, nullable=True)
    #lista_precio_id = db.Column(db.Integer, db.ForeignKey('lista_precio.lista_precio_id'), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())


    def __init__(self, fecha_desde, fecha_hasta):
        """
        Constructor de la clase precio
        """
        self.fecha_desde = fecha_desde
        self.fecha_hasta = fecha_hasta

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'precio de {}'.format(self.fecha_desde,self.fecha_hasta)

    def entre_fechas(self):
        return 'precio de {}'.format(self.fecha_desde,self.fecha_hasta)        


class Lista_precio_producto(db.Model):
    """
    Este modelo representará a la repacion lista de precio y producto.
    Contará con los siquientes campos:
    precio_id  --> clave primaria
    descripcion --> descripcion del precio
    valor --> describe el valor numerico del precio
    lista_precio_id --> clave forania refenciando a la tabla lista de precios
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'lista_precio_producto'

    # Atributos
    producto_envase_id = db.Column(db.Integer, db.ForeignKey('producto_envase.producto_envase_id'), nullable=False, primary_key=True)
    precio_id = db.Column(db.Integer, db.ForeignKey('lista_precio.precio_id'), nullable=False, primary_key=True)
    precio = db.Column(db.Integer, nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=True)
    fecha_fin = db.Column(db.DateTime, nullable=True)
    #lista_precio_id = db.Column(db.Integer, db.ForeignKey('lista_precio.lista_precio_id'), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())


    def __init__(self, producto_envase_id, precio_id, precio, fecha_inicio, fecha_fin):
        """
        Constructor de la clase precio
        """
        self.producto_envase_id = producto_envase_id
        self.precio_id = precio_id
        self.precio = precio
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return self.precio

    def get_precio(self):
        return self.precio

    def entre_fechas(self):
        return 'precio de {}'.format(self.fecha_desde,self.fecha_hasta)  
