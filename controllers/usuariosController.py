from app import app, usuarios
from flask import Flask, render_template, request, redirect, session, url_for
import pymongo

# Esta función solo reenderiza la interfaz del login utilizando el metodo GET
@app.route("/", methods=['GET'])
def Login():
    return render_template ("login.html")

"""
En esta función se realiza una consulta para saber si los datos obtenidos en el formulario concuerdan con
los que están en la base de datos, luego se valida para que pueda ingresar a la aplicación, solo si ha
iniciado sesión.
"""
@app.route("/", methods=["POST"])
def login():
    mensaje=None
    estado=None
    try:
        correo  = request.form["correo"]
        contraseña = request.form["contraseña"]
        consulta = {"correo":correo, "contraseña":contraseña}
        user = usuarios.find_one(consulta)
        if (user):
            session["correo"]=correo
            return redirect (url_for("home"))
        else:
            mensaje = "Datos no validos"   
    except pymongo.errors as error:
        mensaje = error
    return render_template("login.html",estado=estado,mensaje=mensaje)

@app.route("/salir")
def salir():
    """
    Función para cerrar sesión al momento de salir de la aplicación.
    """
    session.clear()
    mensaje="Se ha cerrado sesion"
    return render_template("login.html",mensaje=mensaje)    