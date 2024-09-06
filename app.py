from flask import Flask, request, jsonify, render_template_string
import requests
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from cachetools import TTLCache

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración de la API de Imgur
IMGUR_CLIENT_ID = os.getenv('IMGUR_CLIENT_ID')

# Verificación de que el Client ID esté configurado
if not IMGUR_CLIENT_ID:
    raise ValueError("Falta el IMGUR_CLIENT_ID en el archivo .env.")

# Caché de imágenes subidas (TTL de 24 horas, max 100 imágenes por IP)
image_cache = TTLCache(maxsize=100, ttl=86400)

# Ruta para subir la imagen a Imgur y devolver un enlace
@app.route('/upload_image', methods=['POST'])
def upload_image():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

    if 'file' not in request.files:
        return jsonify({'error': 'No se ha proporcionado ningún archivo'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'El archivo no tiene nombre'}), 400
    
    filename = secure_filename(file.filename)
    
    # Subir la imagen a Imgur
    headers = {
        'Authorization': f'Client-ID {IMGUR_CLIENT_ID}'
    }
    files = {
        'image': file.read()
    }
    
    response = requests.post('https://api.imgur.com/3/upload', headers=headers, files=files)
    
    if response.status_code == 200:
        imgur_link = response.json()['data']['link']
        
        # Guardar el enlace en la caché de imágenes subidas
        if user_ip not in image_cache:
            image_cache[user_ip] = []
        image_cache[user_ip].append(imgur_link)
        
        return jsonify({'link': imgur_link}), 200
    else:
        return jsonify({'error': 'Error al subir la imagen a Imgur'}), 500

# Ruta para ver las imágenes subidas por el usuario
@app.route('/my_images')
def my_images():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    if user_ip in image_cache:
        return jsonify({'images': image_cache[user_ip]}), 200
    else:
        return jsonify({'message': 'No has subido imágenes recientemente.'}), 200

@app.route('/')
def home():
    html = '''
    <!doctype html>
    <title>Subir Imagen - Gaia OSINT</title>
    <h1>Sube tu Imagen</h1>
    <form method="post" enctype="multipart/form-data" action="/upload_image">
      <input type="file" name="file" required>
      <input type="submit" value="Subir Imagen">
    </form>
    <div class="link" id="link"></div>
    <a href="/my_images">Ver mis imágenes subidas</a>
    '''
    return render_template_string(html)

# Iniciar la aplicación en el puerto asignado por Heroku
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
