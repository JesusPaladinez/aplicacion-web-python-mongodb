from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)

app.secret_key = 'password_secret'
app.config["UPLOAD_FOLDER"]="/static/img"

app.config['MONGODB_SETTINGS'] = [{
    'db': 'gestionProductos',
    'host': 'localhost',
    'port': 27017
}]

db = MongoEngine(app)

from controllers.productosController import *
from controllers.usuariosController import *

if __name__=="__main__":
    app.run(debug=True)