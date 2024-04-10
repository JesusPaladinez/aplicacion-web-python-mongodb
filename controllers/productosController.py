from app import app
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import pymongo
import os
from bson.objectid import ObjectId
import base64
from io import BytesIO
from bson.json_util import dumps
from pymongo import MongoClient
from controllers.usuariosController import *
from models.model import Usuarios, Productos, Categorias
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
        listaProductos = Productos.objects()
        print(len(listaProductos))
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
        listaCategorias = Categorias.objects()
        return render_template("formulario.html",categorias=listaCategorias)
    else:
        mensaje ="Debe ingresar con sus datos"
        return render_template("login.html",mensaje=mensaje)

@app.route('/agregarProducto', methods=['GET', 'POST'])
def agregarProducto():
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria = request.form['categoria']
        foto = request.files['foto']

        # Verificar si el código del producto ya existe en la base de datos
        if Productos.objects(codigo=codigo).first():
            flash('Ya existe un producto con ese código', 'error')
            return redirect(url_for('agregarProducto'))

        # Si el código no existe se guarda en la base de datos
        producto = Productos(
            codigo=codigo,
            nombre=nombre,
            precio=precio,
            categoria=categoria,
            foto=foto.filename
        )
        producto.save() #Esta es la instruccion que guarda el producto

        flash('Producto agregado correctamente', 'success') #Flask  es para mostrar los mensajes desde el lado del cliente
        return redirect(url_for('agregarProducto'))

    else:
        productos = Productos.objects().all()
        return render_template('agregarProducto.html', productos=productos)
    
# conultar producto por codigo
@app.route('/consultar/<codigo>', methods=['GET'])    
def cosultar(codigo):
    if "correo" in session:
        producto = Productos.objects(codigo=codigo).first()
        listaCategorias = Categorias.objects()
        return render_template('listarProductos.html', categorias=listaCategorias, producto=producto)
    else:
        mensaje = 'Datos inválidos.'
        return render_template('login.html', mensaje=mensaje)
    
@app.route('/editarProductoJson', methods=['PUT'])
def editarProductoJson():
    if 'correo' in session:
        estado = False
        mensaje = None
        try:
            datos = request.json
            datosProducto = datos.json['producto']
            fotoBase64 = datos.get('foto')["foto"]
            idProducto = ObjectId(datosProducto['id'])
            producto = Productos.objects(id=idProducto).first()
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

@app.route('/eliminarJson/<id>', methods=['DELETE'])
def eliminarJson(id):
    if 'correo' in session:
        estado = False
        mensaje = None
        try:
            producto = Productos.objects(id=id).first()
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
