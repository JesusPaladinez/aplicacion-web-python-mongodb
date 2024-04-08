from mongoengine import Document, ReferenceField, StringField, IntField, EmailField

# creación de modelos
class Usuarios(Document):
    usuario = StringField(max_length=50, required=True, unique=True)
    contraseña = StringField(max_length=50)
    nombres = StringField(max_length=50)
    apellidos = StringField(max_length=50)
    correo = EmailField(required=True, unique=True)
    
class Categorias(Document):
    nombre = StringField(max_length=50, unique=True)
    
class Productos(Document):
    codigo = IntField(unique=True)
    nombre = StringField(max_length=50)
    precio = IntField()
    categoria = ReferenceField(Categorias, required=True)