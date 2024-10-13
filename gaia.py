import os
import requests
import logging
import random
import string
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect
from flask_talisman import Talisman
from datetime import datetime
from dotenv import load_dotenv
from user_agents import parse
from PIL import Image
from PIL.ExifTags import TAGS

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración básica del logger para manejo concurrente de logs
logging.basicConfig(filename='visitor_data.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Cargar las claves API desde .env
API_KEY_IPSTACK = os.getenv('IPSTACK_API_KEY', '0902c6d29b2eb5453520bcaf0dbe4424')
IMGUR_CLIENT_ID = os.getenv('IMGUR_CLIENT_ID', 'f2acd61ca6a4b03')

# Verificar que las claves API estén correctamente cargadas
if not API_KEY_IPSTACK or not IMGUR_CLIENT_ID:
    raise ValueError("Las claves API no están configuradas correctamente. Verifica el archivo .env")

# Crear instancia de la aplicación Flask
app = Flask(__name__)

# Protección de seguridad con Talisman
talisman = Talisman(app)

# Inicializar la base de datos
def init_db():
    conn = sqlite3.connect('visitor_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            country TEXT,
            region TEXT,
            city TEXT,
            code TEXT,
            latitude REAL,
            longitude REAL,
            browser TEXT,
            browser_version TEXT,
            os TEXT,
            os_version TEXT,
            device TEXT,
            user_agent TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Diccionario para almacenar los enlaces de seguimiento
tracking_data = {}

# Extensiones permitidas para la subida de imágenes
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Validar que el archivo tenga una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Generar un ID único para el usuario
def generate_tracking_url(image_link):
    user_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    tracking_url = f"http://127.0.0.1:5000/track/{user_id}"
    tracking_data[user_id] = image_link
    return tracking_url

# Página de inicio con el formulario
@app.route('/')
def index():
    return render_template('index.html')

# Función para extraer metadatos EXIF
def extract_exif(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()
    
    exif = {}
    if exif_data:
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            exif[tag_name] = value
    return exif

# Ruta para subir imagen a Imgur
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return "No se seleccionó ninguna imagen."

    image = request.files['image']

    if image.filename == '' or not allowed_file(image.filename):
        return "Formato de archivo no permitido. Solo se permiten imágenes (png, jpg, jpeg, gif)."
    
    # Guardar temporalmente la imagen para extraer EXIF
    image.save("temp_image.jpg")
    exif_data = extract_exif("temp_image.jpg")
    logging.info(f"Metadatos EXIF de la imagen: {exif_data}")

    headers = {'Authorization': f'Client-ID {IMGUR_CLIENT_ID}'}
    files = {'image': image.read()}

    try:
        response = requests.post('https://api.imgur.com/3/image', headers=headers, files=files)

        if response.status_code == 200:
            data = response.json()
            image_link = data['data']['link']
            tracking_url = generate_tracking_url(image_link)
            return f"Enlace de seguimiento: {tracking_url}"
        else:
            error_msg = response.json().get('data', {}).get('error', 'Error desconocido')
            return f"Error al subir la imagen a Imgur: {error_msg}"

    except requests.exceptions.RequestException as e:
        return f"Error en la solicitud a Imgur: {e}"

# Ruta para capturar la información del visitante
@app.route('/track/<user_id>', methods=['GET'])
def track_user(user_id):
    visitor_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    parsed_ua = parse(user_agent)
    
    logging.info(f"Visitante IP: {visitor_ip}, Navegador: {parsed_ua.browser.family}, "
                 f"Versión del Navegador: {parsed_ua.browser.version_string}, "
                 f"Sistema Operativo: {parsed_ua.os.family}, "
                 f"Versión del Sistema Operativo: {parsed_ua.os.version_string}, "
                 f"Dispositivo: {parsed_ua.device.family}")

    # Obtener la geolocalización de la IP
    location = get_geolocation(visitor_ip)
    
    if location:
        save_visitor_data(visitor_ip, location, user_agent, parsed_ua)
    
    # Redirigir al enlace original de la imagen subida
    image_link = tracking_data.get(user_id, "https://www.example.com")
    return redirect(image_link)

# Función para obtener la geolocalización mediante IP
def get_geolocation(ip):
    try:
        url = f"http://api.ipstack.com/{ip}?access_key={API_KEY_IPSTACK}"
        response = requests.get(url)
            
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Error en la solicitud de geolocalización: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error en la solicitud de geolocalización: {e}")
        return None

# Función para guardar los datos del visitante
def save_visitor_data(ip, location, user_agent, parsed_ua, lat=None, lon=None):
    data = {
        'ip': ip,
        'country': location.get('country_name'),
        'region': location.get('region_name'),
        'city': location.get('city'),
        'code': location.get('country_code'),
        'latitude': lat,
        'longitude': lon,
        'user_agent': user_agent,
        'browser': parsed_ua.browser.family,
        'browser_version': parsed_ua.browser.version_string,
        'os': parsed_ua.os.family,
        'os_version': parsed_ua.os.version_string,
        'device': parsed_ua.device.family,
        'date': str(datetime.now())
    }
    logging.info(f"Datos del visitante guardados: {data}")
    save_to_db(data)  # Guardar en la base de datos

# Guardar datos en la base de datos
def save_to_db(data):
    conn = sqlite3.connect('visitor_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO visitors (ip, country, region, city, code, latitude, longitude, 
                              browser, browser_version, os, os_version, device, user_agent, date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['ip'], data['country'], data['region'], data['city'], data['code'], data['latitude'], 
        data['longitude'], data['browser'], data['browser_version'], data['os'], data['os_version'], 
        data['device'], data['user_agent'], data['date']
    ))
    conn.commit()
    conn.close()

# Función para procesar datos geográficos (integración)
def procesar_geolocalizacion(geo):
    # Lista para almacenar códigos únicos
    code_list = []

    # Iterar sobre los datos de geolocalización
    for i in geo:
        print(f"ip: {i['ip']}")
        print(f"country: {i['country']}")
        print(f"region: {i['region']}")
        print(f"code: {i['code']}")
        print("")

        # Evitar duplicados en los códigos
        if i["code"] not in code_list:
            print(i["code"])
            code_list.append(i["code"])

# Ejemplo de uso para procesar datos de geolocalización
geo_data = [
    {"ip": "192.168.1.1", "country": "Spain", "region": "Madrid", "code": "ES"},
    {"ip": "172.16.0.1", "country": "France", "region": "Paris", "code": "FR"},
    {"ip": "10.0.0.1", "country": "Germany", "region": "Berlin", "code": "DE"}
]
procesar_geolocalizacion(geo_data)

# Ruta para guardar ubicación precisa desde el navegador
@app.route('/save_location', methods=['POST'])
def save_location():
    data = request.json
    lat = data.get('latitud')
    lon = data
