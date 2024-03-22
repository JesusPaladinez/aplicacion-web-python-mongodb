from flask import Flask

app = Flask(__name__)

app.config["UPLOAD_FOLDER"]="./static/img"

from controllers.productosController import *
from controllers.usuariosController import *

if __name__=="__main__":
    app.run(debug=True, port=3000)