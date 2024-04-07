from app import app, productos, categorias
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pymongo
import os
from bson.objectid import ObjectId
import base64
from io import BytesIO
from bson.json_util import dumps
from pymongo import MongoClient
from controllers.usuariosController import *
from models.model import Usuario, Producto, Categoria
from PIL import Image

"""
En cada función del CRUD, primero se verifica que el usuario haya iniciado sesion para poder iniciar a 
la aplicación.
"""

@app.route('/home')
def home():
    """
    Se busca todos los productos en la base de datos, se busca el id de la categoria de cada uno 
    de los productos, y finalmente se agrega a una lista para poder mostrarlos en la interfaz reenderizada.
    """
    if("correo"in session):        
        listaProductos = Producto.objects()
        return render_template("listarProductos.html", productos=listaProductos)
    else:
        mensaje = "Debe iniciar sesión"
        return render_template("login.html",mensaje=mensaje)
        
@app.route ("/agregarProductos")
def vistaAgregarProducto():
    """
    Se busca las categorias disponibles, y se reenderiza el formulario para agregar productos.
    """
    if("correo"in session):
        listaCategorias = Categoria.objects()
        return render_template("formulario.html",categorias=listaCategorias)
    else:
        mensaje ="Debe ingresar con sus datos"
        return render_template("login.html",mensaje=mensaje)

@app.route("/agregarProductos", methods=["POST"])
def agregarProducto():
    """
    Se obtienen los valores de cada campo, esos valores se agregan a un diccionario producto, producto se
    agrega a la colleccion, con acknowledged se verifica que el producto este en la colleccion, se le
    da un id al producto, se carga la imagen de UPLOAD_FOLDER, se muestra un mensaje informando si el
    producto se pudo agregar, y finalmente se redirecciona a la ruta principal.  
    """
    mensaje = None
    estado = False
    if("correo"in session):
        try:
            datos = request.json  # lectura de datos que vienen del formulario
            print(datos)
            datosProducto = request.get('producto')
            print(datosProducto)
            fotoBase64 = datos.get('foto')["foto"]
            producto = Producto(**datosProducto) # objeto con el modelo Producto
            print(producto.precio)
            producto.save() # guardar en la base de datos
            
            # validar el resultado de la inserción del producto
            # si se ha guardado bien, se crea el id del producto
            if(producto.id):
                rutaImagen = f"{os.path.join(app.config['UPLOAD_FOLDER' ])}/(producto.id).jpg"
                #Seleccionar del formato base64, la parte que tiene que
                #ver con la imagen, que va después de la coma.
                fotoBase64 = fotoBase64[fotoBase64.index(',')+1:]
                #decodificar la imagen utilizando la libreria base64
                imagenDecodificada = base64.b64decode(fotoBase64)
                #crear la imagen con Image de la libreria Pillow
                imagen = Image.open(BytesIO(imagenDecodificada))
                #convertir la imagen a tipo de formato
                imagenJpg = imagen.convert("RGB")
                #guardar la imagen en el servidor en la ruta creada
                imagenJpg.save(rutaImagen)
                estado=True
                mensaje="Producto Agregado Correctamente"
            else:
                mensaje="Problemas al agregar el producto"
        except Exception as error:
            mensaje = str(error)
        retorno = {'estado': estado, 'mensaje': mensaje}
        return jsonify(retorno)
    else:
        mensaje ="Debe ingresar con sus datos"
        return render_template("login.html",mensaje=mensaje)
    
# conultar producto por codigo
@app.route('/consultar/<codigo>', methods=['GET'])    
def cosultar(codigo):
    if "correo" in session:
        producto = Producto.objects(codigo=codigo).first()
        listaCategorias = Categoria.objects()
        return render_template('listarProductos.html', categorias=listaCategorias, producto=producto)
    else:
        mensaje = 'Datos inválidos.'
        return render_template('login.html', mensaje=mensaje)
    
@app.route("/editarProducto/<producto_id>", methods=["GET"])
def editar_producto(producto_id):
    """
    Se busca el producto con un id en específico, si existe se busca la categoria a la que pertenece, y 
    finalmente se reenderiza la interfaz para editar el producto.    
    """
    if "correo" in session:
        try:
            producto = productos.find_one({"_id": ObjectId(producto_id)})
            if producto:
                listaCategorias = categorias.find()
                return render_template("editarProducto.html", producto=producto, categorias=listaCategorias)
            else:
                return "Producto no encontrado."
        except pymongo.errors.PyMongoError as error:
            return f"Error al cargar el producto: {error}"
    else:
        mensaje = "Debe ingresar con sus datos"
        return render_template("login.html", mensaje=mensaje)
    
@app.route('/editarProductoJson', methods=['PUT'])
def editarProductoJson():
    if 'correo' in session:
        estado = False
        mensaje = None
        try:
            datos = request.json
            datosProducto = datos.get('producto')
            fotoBase64 = datos.get('foto')["foto"]
            idProducto = ObjectId(datosProducto['id'])
            producto = Producto.objects(id=idProducto).first()
            if producto:
                producto.codigo = int(datosProducto['codigo'])
                producto.nombre = datosProducto['nombre']
                producto.precio = int(datosProducto['precio'])
                producto.categoria = ObjectId(datosProducto['categoria'])
                producto.save()
                
                # si viene la imagen se carga en el servidor
                if fotoBase64:
                    rutaImagen = f'{os.path.join(
                        app.config['UPLOAD_FOLDER'])}/{producto.id}.jpg'
                        
                    fotoBase64 = fotoBase64[fotoBase64.index(',') + 1:]                    
                    imagenDecodificada = base64.b64decode(fotoBase64) # decodifica la imagen        
                    imagen = Image.open(BytesIO(imagenDecodificada)) # crea la imagen
                    imagenJpg = imagen.convert('RGB') # convertir la imagen a tipo de formato
                    imagenJpg.save(rutaImagen) # guarda la imagen en el servidor de la ruta creada 
                mensaje = 'Producto actualizado correctamente'
                estado = True
            
            else:
                mensaje = 'No existe producto con ese código'
        except Exception as error:
            mensaje = str(error)        
        retorno = {'estado': estado, 'mensaje':mensaje}
        return jsonify(retorno)
    else:
        mensaje = 'Datos inválidos.'
        return render_template('login.html', mensaje=mensaje, estado=estado)
    
@app.route("/actualizarProducto/<producto_id>", methods=["POST"])
def actualizar_producto(producto_id):
    """
    Se obtienen los valores de cada campo, esos valores se agregan a un nuevo diccionario producto_actualizado,
    en en el metodo update_one de mongo se entrega el id del producto a actualizar, en el metodo set se 
    entrega el producto_actualizado, se valida si la foto también se va a actualizar, y finalmente se 
    redirecciona a la ruta principal.  
    """
    if "correo" in session:
        try:
            codigo = int(request.form["codigo"]) 
            nombre = request.form["nombre"]
            precio = int(request.form["precio"])
            idCategoria = request.form["categoria"]
            foto = request.files["imagen"]
            producto_actualizado = {
                "codigo": codigo,
                "nombre": nombre,
                "precio": precio,
                "categoria": ObjectId(idCategoria)
            }
            productos.update_one({"_id": ObjectId(producto_id)}, {"$set": producto_actualizado})

            if foto and foto.filename != '':
                nombreFoto = f"{producto_id}.jpg"
                foto.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreFoto))


            return redirect(url_for("home"))

        except pymongo.errors.PyMongoError as error:
            return f"Error al actualizar el producto: {error}"
    else:
        mensaje = "Debe ingresar con sus datos"
        return render_template("login.html", mensaje=mensaje)
    

@app.route('/eliminarJson/<id>', methods=['DELETE'])
def eliminarJson(id):
    if 'correo' in session:
        estado = False
        mensaje = None
        try:
            producto = Producto.objects(id=id).first()
            if producto:
                producto.delete()
                mensaje = 'Producto eliminado correctamente.'
                estado = True
            else:
                mensaje = 'No existe producto con ese id.'
        except Exception as error:
            mensaje = str(error)
            
        retorno = {'estado': estado, 'mensaje': mensaje}
        return jsonify(retorno)
    else:
        mensaje = 'Datos inválidos.'
        return render_template('login.html', mensaje=mensaje, estado=estado)
    
@app.route("/eliminarProducto/<producto_id>", methods=["GET"])
def eliminar_producto(producto_id):
    """
    Se elimina el producto con un id en específico, si se elimina se redirecciona a la ruta pricipal,
    de lo contrario se retorna un mensaje de error al eliminar.
    """
    if("correo"in session):
        try:
            resultado = productos.delete_one({"_id": ObjectId(producto_id)})
            if resultado.deleted_count == 1:
                return redirect(url_for("home"))
            else:
                return "Producto no encontrado."
        except pymongo.errors.PyMongoError as error:
            return f"Error al eliminar el producto: {error}"
    else:
        mensaje ="Debe ingresar con sus datos"
        return render_template("login.html",mensaje=mensaje)
   