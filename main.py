from bson import ObjectId
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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



def cuerpo(nombre: str):
    return  f'<h1>Gracias por renovar tu suscripción, {nombre}!!</h1><h4>Ve a nuestro sitio para revisar nuestras ultimas novedades! <a href = "#">Vamos a la pagina!</a> </h4>'


# permisos de política de seguridad CORS
origins = [
    "http://localhost:4200",
    "https://confirmacion-pa-etitc.netlify.app/"
] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

@app.get('/')
def index():
    return{'message': 'todo OK'}

@app.get('/id/{_id}')
def enviar_correo(_id: str):
    correo = MIMEMultipart()
    correo['From'] = remitente
    correo['Subject'] = asunto
    persona = coleccion.find_one({"_id": ObjectId(_id)})

    destinatario = persona['correo']
    correo['To'] = destinatario

    correo.attach(MIMEText(cuerpo(persona['nombre']), 'html'))
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
        x = coleccion.find_one({'_id': ObjectId(_id)})
        if x is not None:
            return True
        else: 
            return False
    
    except(Exception):
        return False
    
