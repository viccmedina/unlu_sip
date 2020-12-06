from distribuidora import db

class Message(db.Model):
	__tablename__ = 'mensaje'

	id = db.Column(db.Integer, primary_key=True)
	sender_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
	recipient_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
	body = db.Column(db.String(140))
	read = db.Column(db.Boolean, default=False)
	ts_created = db.Column(db.DateTime, server_default=db.func.now())


	def __init__(slef, sender_id, recipient_id, body):
		self.sender_id = sender_id
		self.recipient_id = recipient_id
		self.body = body
		self.read = False

	def __repr__(self):
		return '<Message {}>'.format(self.body)


	def is_read(self):
		return self.read
		
	def get_mensaje_dict(self):
		return {
			'emisor_id': self.sender_id,
			'receptor_id': self.recipient_id,
			'body': self.body,
			'ts': self.ts_created
		}
