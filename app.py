from distribuidora import app

@app.route('/')
def index():
	return 'Index Page'

if __name__ == '__main__':
	app.run(debug=True)