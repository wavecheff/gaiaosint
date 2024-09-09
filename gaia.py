import os
import webbrowser
import requests
import logging
import redis
import exifread
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PIL import Image
import torch
import torchvision.transforms as transforms
from torchvision import models
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from fpdf import FPDF
from dotenv import load_dotenv

# Crear el archivo .env automáticamente si no existe
env_file_path = '.env'
if not os.path.exists(env_file_path):
    with open(env_file_path, 'w') as f:
        f.write('IMGUR_CLIENT_ID=f2acd61ca6a4b03\n')
        f.write('IPSTACK_API_KEY=0902c6d29b2eb5453520bcaf0dbe4424\n')
        f.write('IPHUB_API_KEY=your_iphub_api_key\n')

# Cargar variables de entorno
load_dotenv()

# Configuración de la aplicación Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # Tamaño máximo de archivo de 5MB
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'supersecretkey')  # Para autenticación JWT

jwt = JWTManager(app)
cache = redis.StrictRedis(host='localhost', port=6379, db=0)
logging.basicConfig(level=logging.INFO)

# Cargar modelo de clasificación de imágenes (ResNet)
model = models.resnet50(weights='IMAGENET1K_V1')  # Usamos la versión más actualizada de las weights
model.eval()

# Cargar etiquetas de ImageNet
imagenet_labels = requests.get('https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json').json()

# Funciones Auxiliares
# (Mantenemos las funciones auxiliares existentes aquí como antes)

# Endpoints de la aplicación
# (Mantenemos los endpoints aquí como antes)

if __name__ == '__main__':
    # Abre automáticamente el navegador en local
    local_url = "http://127.0.0.1:5001"
    heroku_url = "https://gaiaosint-709ed257d657.herokuapp.com/"
    
    if 'DYNO' not in os.environ:
        # Localmente, abre la URL local
        webbrowser.open(local_url)
    else:
        # En Heroku, abre la URL de la app
        webbrowser.open(heroku_url)
    
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
