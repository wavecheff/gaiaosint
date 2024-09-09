from flask import Flask, request, send_file, jsonify
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env automáticamente
load_dotenv()

app = Flask(__name__)

# Obtener las API keys desde las variables de entorno
API_KEY_IPSTACK = os.getenv('IPSTACK_API_KEY')
IMGUR_CLIENT_ID = os.getenv('IMGUR_CLIENT_ID')

# Verificar que las API keys se cargaron correctamente
if not API_KEY_IPSTACK or not IMGUR_CLIENT_ID:
    raise EnvironmentError("Faltan claves de API. Asegúrate de que las claves de IPStack y Imgur estén configuradas en el archivo .env")

# Ruta para servir la imagen y capturar la IP del usuario
@app.route('/imagen/<filename>', methods=['GET'])
def serve_image(filename):
    # Capturar la IP del visitante
    visitor_ip = request.remote_addr
    print(f"Visitante IP: {visitor_ip}")

    # Obtener la geolocalización de la IP
    location = get_geolocation(visitor_ip)
    if location:
        print(f"Ubicación aproximada: {location}")

        # Guardar los datos del visitante en un archivo o base de datos
        save_visitor_data(visitor_ip, location)

    # Enviar la imagen solicitada
    return send_file(f'static/images/{filename}', mimetype='image/jpeg')

# Función para obtener la geolocalización
def get_geolocation(ip):
    url = f"http://api.ipstack.com/{ip}?access_key={API_KEY_IPSTACK}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Función para guardar los datos del visitante
def save_visitor_data(ip, location):
    # Puedes guardar los datos en un archivo o base de datos
    data = {
        'ip': ip,
        'location': location,
        'date': str(datetime.now())
    }
    with open('visitor_data.log', 'a') as file:
        file.write(str(data) + '\n')
    print(f"Datos del visitante guardados: {data}")

# Ruta para subir imágenes a Imgur
@app.route('/upload', methods=['POST'])
def upload_image():
    image = request.files['image']
    headers = {'Authorization': f'Client-ID {IMGUR_CLIENT_ID}'}
    files = {'image': image.read()}
    response = requests.post('https://api.imgur.com/3/image', headers=headers, files=files)

    if response.status_code == 200:
        data = response.json()
        return jsonify({'link': data['data']['link']})
    else:
        return jsonify({'error': 'Error al subir la imagen'}), 500

if __name__ == "__main__":
    app.run(port=5001, debug=True)
