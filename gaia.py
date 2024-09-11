import os
import requests
from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv

# Cargar las claves de las variables de entorno
load_dotenv()

app = Flask(__name__)

# Claves API desde las variables de entorno
API_KEY_IPSTACK = os.getenv('API_KEY_IPSTACK')
IMGUR_CLIENT_ID = os.getenv('IMGUR_CLIENT_ID')

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
    headers = {'Authorization': f'Client-ID {IMGUR_CLIENT_ID}'}
    files = {'image': image.read()}
    response = requests.post('https://api.imgur.com/3/image', headers=headers, files=files)

    if response.status_code == 200:
        data = response.json()
        return f"Enlace de la imagen: {data['data']['link']}"
    else:
        return "Error al subir la imagen a Imgur."

# Ruta para capturar la información del visitante
@app.route('/track/<user_id>', methods=['GET'])
def track_user(user_id):
    visitor_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    print(f"Visitante IP: {visitor_ip}")
    print(f"User-Agent: {user_agent}")

    # Obtener la geolocalización de la IP
    location = get_geolocation(visitor_ip)
    if location:
        save_visitor_data(visitor_ip, location, user_agent)
        return f"Ubicación aproximada: {location}"
    else:
        return "Error al obtener la geolocalización."

# Función para obtener la geolocalización mediante IP
def get_geolocation(ip):
    url = f"http://api.ipstack.com/{ip}?access_key={API_KEY_IPSTACK}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Función para guardar los datos del visitante
def save_visitor_data(ip, location, user_agent):
    data = {
        'ip': ip,
        'location': location,
        'user_agent': user_agent
    }
    with open('visitor_data.log', 'a') as file:
        file.write(str(data) + '\n')
    print(f"Datos del visitante guardados: {data}")

if __name__ == "__main__":
    app.run(debug=True)
