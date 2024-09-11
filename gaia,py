import os
import requests
import logging
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración básica del logger para manejo concurrente de logs
logging.basicConfig(filename='visitor_data.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Cargar las claves API desde .env
API_KEY_IPSTACK = os.getenv('API_KEY_IPSTACK')
IMGUR_CLIENT_ID = os.getenv('IMGUR_CLIENT_ID')

# Verificar que las claves API estén correctamente cargadas
if not API_KEY_IPSTACK or not IMGUR_CLIENT_ID:
    raise ValueError("Las claves API no están configuradas correctamente. Verifica el archivo .env")

# Crear instancia de la aplicación Flask
app = Flask(__name__)

# Extensiones permitidas para la subida de imágenes
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Validar que el archivo tenga una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Página de inicio con el formulario
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para subir imagen a Imgur
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return "No se seleccionó ninguna imagen."

    image = request.files['image']

    if image.filename == '' or not allowed_file(image.filename):
        return "Formato de archivo no permitido. Solo se permiten imágenes (png, jpg, jpeg, gif)."

    headers = {'Authorization': f'Client-ID {IMGUR_CLIENT_ID}'}
    files = {'image': image.read()}

    try:
        response = requests.post('https://api.imgur.com/3/image', headers=headers, files=files)

        if response.status_code == 200:
            data = response.json()
            return f"Enlace de la imagen: {data['data']['link']}"
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
    logging.info(f"Visitante IP: {visitor_ip}, User-Agent: {user_agent}")

    # Obtener la geolocalización de la IP
    location = get_geolocation(visitor_ip)
    if location:
        save_visitor_data(visitor_ip, location, user_agent)
        return jsonify({'ip': visitor_ip, 'location': location, 'user_agent': user_agent})
    else:
        return jsonify({'error': 'Error al obtener la geolocalización'}), 500

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
def save_visitor_data(ip, location, user_agent):
    data = {
        'ip': ip,
        'location': location,
        'user_agent': user_agent,
        'date': str(datetime.now())
    }
    logging.info(f"Datos del visitante guardados: {data}")

# Ruta para recibir los metadatos del navegador
@app.route('/save_metadata', methods=['POST'])
def save_metadata():
    data = request.json
    logging.info(f"Metadatos del navegador: {data}")
    return jsonify({"status": "Metadatos guardados"}), 200

# Ruta para recibir los eventos de clic
@app.route('/track_click', methods=['POST'])
def track_click():
    data = request.json
    logging.info(f"Click registrado: {data}")
    return jsonify({"status": "Click guardado"}), 200

# Ruta para recibir la ubicación exacta
@app.route('/save_location', methods=['POST'])
def save_location():
    data = request.json
    logging.info(f"Ubicación del usuario: {data}")
    return jsonify({"status": "Ubicación guardada"}), 200

if __name__ == "__main__":
    app.run(debug=True)
