from bson import ObjectId
from fastapi import FastAPI
from pymongo import MongoClient

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# API
app = FastAPI()


# Base de Datos
cliente = MongoClient('mongodb+srv://ThJuanK:7HU25D1lFrllnTzx@clusternuevo.ritsyyg.mongodb.net/test')
db = cliente.usuarios
coleccion = db['proyecto-tesis']


# Correo
remitente = 'jcayalaa@itc.edu.co'
asunto = "Confirmación de la renovación"

contra = "JuanK112406"
puerto_smtp = 587

correo = MIMEMultipart()
correo['From'] = remitente
correo['Subject'] = asunto

def cuerpo(nombre: str):
    return  f'<h1>Gracias por renovar tu suscripción, {nombre}!!</h1><h4>Ve a nuestro sitio para revisar nuestras ultimas novedades! <a href = "#">Vamos a la pagina!</a> </h4>'

@app.get('/')
def index():
    return{'message': 'todo OK'}

@app.get('/id/{_id}')
def enviar_correo(_id: str):
    persona = coleccion.find_one({"_id": ObjectId(_id)})

    destinatario = persona['correo']
    correo['To'] = destinatario

    correo.attach(MIMEText(cuerpo(persona['nombre']), 'html'))
    cuerpo(persona['nombre'])
    # Conexión al servidor SMTP
    with smtplib.SMTP("smtp-mail.outlook.com", puerto_smtp) as servidor:
        servidor.starttls()  # Habilitar TLS (opcional)
        servidor.login(remitente, contra)  # Iniciar sesión en el servidor SMTP
        servidor.send_message(correo)  # Enviar correo electrónico
        print("correo enviado!")

    return {'message': "correo enviado exitosamente.",
            'correo': persona['correo']}
    
@app.get('/comprobar/{_id}')
def comprobar_correo(_id: str):
    try:
        x = coleccion.find_one({'_id': _id})
        if not x:
            return True
    
    except(Exception):
        return False
    
    finally: return False
