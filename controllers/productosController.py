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
        
        listaProductos = productos.find()
        todos_productos = []
        for producto in listaProductos:
            cat = categorias.find_one({'_id': ObjectId(producto['categoria'])})
            if cat:
                producto['categoria'] = cat['nombre']
                todos_productos.append(producto)
        return render_template("listarProductos.html", productos=todos_productos)
    else:
        mensaje = "Debe iniciar sesión"
        return render_template("login.html",mensaje=mensaje)
        
@app.route ("/agregarProductos")
def vistaAgregarProducto():
    """
    Se busca las categorias disponibles, y se reenderiza el formulario para agregar productos.
    """
    if("correo"in session):
        listaCategorias = categorias.find()
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
            codigo =int(request.form["codigo"]) 
            nombre = request.form["nombre"]
            precio = int(request.form["precio"])
            idCategoria = request.form["categoria"]
            foto =request.files["imagen"]
            producto ={
                "codigo":codigo,
                "nombre":nombre,
                "precio":precio,
                "categoria":ObjectId(idCategoria)
            }
            resultado = productos.insert_one(producto)
            if (resultado.acknowledged):
                idProducto = resultado.inserted_id
                nombreFoto = f"{idProducto}.jpg"
                foto.save(os.path.join(app.config["UPLOAD_FOLDER"],nombreFoto))
                mensaje = "Producto Agregado Correctamente"
                estado = True
                return redirect (url_for("home"))
            else:
                mensaje="Problemas al agregar"

            return render_template ("/formulario.html",estado= estado, mensaje=mensaje)

        except pymongo.errors.PyMongoError as error:
            mensaje = error
            return error
    else:
        mensaje ="Debe ingresar con sus datos"
        return render_template("login.html",mensaje=mensaje)
    
    
    
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
   