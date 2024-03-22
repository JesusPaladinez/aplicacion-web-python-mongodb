import pymongo

# Conexion al servidor de mongoDB
conexion = pymongo.MongoClient("mongodb://localhost:27017")

# Conexión a la db
db = conexion['gestionProductos']

# Conexión a las collecciones
productos = db['productos']
categorias = db['categorias']
usuarios = db['usuarios']