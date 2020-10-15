from distribuidora import db
from distribuidora.models.lista_precio import ListaPrecio


class Precio(db.Model):
    """
    Este modelo representará a los precios.
    Contará con los siquientes campos:
    precio_id  --> clave primaria
    descripcion --> descripcion del precio
    valor --> describe el valor numerico del precio
    lista_precio_id --> clave forania refenciando a la tabla lista de precios
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'precio'

    # Atributos
    precio_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False)
    valor = db.Column(db.Float(), nullable=False)
    lista_precio_id = db.Column(db.Integer, db.ForeignKey('lista_precio.lista_precio_id'), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())


    def __init__(self, descripcion, valor, lista_precio_id):
        """
        Constructor de la clase precio
        """
        self.descripcion = descripcion
        self.valor = valor
        self.lista_precio_id = lista_precio_id

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'precio de {}'.format(self.descripcion)