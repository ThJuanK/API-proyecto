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
destinatario = 'juanksr0@gmail.com'
asunto = "correo de prueba desde Python"
cuerpo = '<h1>Hola mundo!</h1>'

contra = "JuanK112406"
puerto_smtp = 587

correo = MIMEMultipart()
correo['From'] = remitente
correo['To'] = destinatario
correo['Subject'] = asunto
correo.attach(MIMEText(cuerpo, 'html'))

# Conexión al servidor SMTP
with smtplib.SMTP("smtp-mail.outlook.com", puerto_smtp) as servidor:
    servidor.starttls()  # Habilitar TLS (opcional)
    servidor.login(remitente, contra)  # Iniciar sesión en el servidor SMTP
    servidor.send_message(correo)  # Enviar correo electrónico
    print('El correo ha sido enviado correctamente.')


@app.get('/')
def index():
    return{'message': 'todo OK'}

@app.get('/id/{_id}')
def enviar_correo(_id: str):
    persona = coleccion.find_one({"_id": ObjectId(_id)})
    return {'name': persona['nombre']}

