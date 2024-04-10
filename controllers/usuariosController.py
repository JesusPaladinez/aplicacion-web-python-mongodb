import urllib.request
from app import app
from flask import Flask, render_template, request, redirect, session, url_for
import pymongo
from utils.emailConfirmacion import enviarEmailDeConfirmacion
import threading
from models.model import Usuarios
import urllib.request
import urllib.parse
import json
import yagmail

# Esta función solo reenderiza la interfaz del login utilizando el metodo GET
@app.route("/", methods=['GET'])
def Login():
    return render_template ("login.html")

"""
En esta función se realiza una consulta para saber si los datos obtenidos en el formulario concuerdan con
los que están en la base de datos, luego se valida para que pueda ingresar a la aplicación, solo si ha
iniciado sesión, una vez que el usuario haya ingresado a la aplicación se envía un email de confirmación.
"""
@app.route("/", methods=["POST"])
def login():
    mensaje=None
    estado=None
    # validar el recaptcha
    recaptcha_response = request.form['g-recaptcha-response']
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': '6LdpH7cpAAAAAJ-r11shEPkWUc0REbgE19SFBft1',
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode()
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    
    if result['success']:
        try:
            correo  = request.form["correo"]
            contraseña = request.form["contraseña"]
            user = Usuarios.objects(correo=correo, contraseña=contraseña).first()
            if (user):
                session["correo"]=correo
                email = yagmail.SMTP("jesuspaladinez18@gmail.com", open(".contraseña").read(), encoding='UTF-8')
                destinatario = 'jesuspaladinez18@gmail.com'
                asunto = "El usuario ha ingresado al sistema."
                mensaje = f'Se informa que el usuario <b>{user.nombres} {user.apellidos}</b> ha ingresado al sistema.'
                enviarCorreo = email.send(destinatario, asunto, mensaje)
                thread = threading.Thread(target=enviarCorreo,
                                        args=(email, [user.correo], asunto, mensaje))
                thread.start()
                return redirect("/home")
            else:
                mensaje = "Datos no validos"   
        except Exception as error:
            mensaje = str(error)
        return render_template("login.html",estado=estado,mensaje=mensaje)
    else:
        mensaje = 'Debe validar el recaptcha'
        return render_template('login.html', mensaje=mensaje)

@app.route("/salir")
def salir():
    """
    Función para cerrar sesión al momento de salir de la aplicación.
    """
    session.clear()
    mensaje="Se ha cerrado sesion"
    return render_template("login.html",mensaje=mensaje)    