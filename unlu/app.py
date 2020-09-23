

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hola Corazon de melon!"

@app.route('/willy')
def willy():
    return "Hola willy!!!"   

    
if __name__ == '__main__':
  	app.run(debug=true)