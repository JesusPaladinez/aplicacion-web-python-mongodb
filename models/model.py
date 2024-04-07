from mongoengine import Document, ReferenceField, StringField, IntField, EmailField

# creación de modelos
class Usuario(Document):
    usuario = StringField(max_length=50, required=True, unique=True)
    contraseña = StringField(max_length=50)
    nombres = StringField(max_length=50)
    apellidos = StringField(max_length=50)
    correo = EmailField(required=True, unique=True)
    
class Categoria(Document):
    nombre = StringField(max_length=50, unique=True)
    
class Producto(Document):
    codigo = IntField(unique=True)
    nombre = StringField(max_length=50)
    precio = IntField()
    categoria = ReferenceField(Categoria)
    
# creación de documentos
categoria = Categoria(nombre='Medicamentos')    
categoria.save()

user = Usuario(usuario='userSena', contraseña='13579', nombres='User', apellidos='SENA', correo='userSena@sena.edu.co')
user.save()

# creación de documento en formato json
datos = {
    'usuario': 'jkjkjk',
    'contraseña': '121212',
    'nombres': 'jjj',
    'apellidos': 'kkk',
    'correo': 'jjjkkk@gmail.com'
}

user = Usuario(**datos)
user.save()

