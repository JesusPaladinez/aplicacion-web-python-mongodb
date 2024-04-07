import yagmail

# Remitente
email = 'jesuspaladinez18@gmail.com'
password = 'njynostitfoeatbk'

# Se envía el correo al destinatario
def enviarEmailDeConfirmacion(usuario):
    yag = yagmail.SMTP(user = email, password = password)
    destinatarios = ['jesuspaladinez18@gmail.com']
    asunto = f'Confirmación de ingreso'
    mensaje = f'Me permito informar que el usuario {usuario['nombre']} ha ingresado al sistema!'
    yag.send(destinatarios, asunto, mensaje)
    
