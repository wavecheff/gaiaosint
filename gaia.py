from flask import Flask, request, jsonify, redirect, render_template_string, url_for
import requests
import os
from dotenv import load_dotenv
from cachetools import TTLCache
import ipaddress
import base64

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

# Subir imagen a Imgur usando la API
def upload_image_to_imgur(image_data):
    url = "https://api.imgur.com/3/image"
    payload = {'image': image_data}
    headers = {'Authorization': f'Client-ID {IMGUR_CLIENT_ID}'}
    
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        return response.json()['data']['link']
    return None

# Ruta para subir imagen
@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Obtener imagen del formulario
        image = request.files['image']
        image_data = base64.b64encode(image.read()).decode('utf-8')
        
        # Subir la imagen a Imgur
        imgur_link = upload_image_to_imgur(image_data)
        
        if imgur_link:
            return f"<h3>Imagen subida exitosamente: <a href='{imgur_link}'>{imgur_link}</a></h3>"
        else:
            return "<h3>Error al subir la imagen.</h3>"
    
    # Mostrar el formulario para subir imágenes
    html_content = """
    <h1>Subir una imagen</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="image" accept="image/*" required>
        <button type="submit">Subir Imagen</button>
    </form>
    """
    return render_template_string(html_content)

# Ruta principal para mostrar una página de inicio con botones
@app.route('/')
def index():
    html_content = """
    <h1>Bienvenido a Gaia OSINT</h1>
    <p>Por favor, sube una imagen para rastrear la geolocalización.</p>
    <button onclick="window.location.href='/upload_image'">Subir Imagen</button>
    """
    return render_template_string(html_content)

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
    print("1. Asegúrate de hacer un uso responsable. Gaia OSINT se exime de su mal uso.")
    print("2. Sube una imagen accediendo a la URL base de la aplicación.")
    print("3. Para rastrear la geolocalización de un usuario que acceda a una imagen, usa /track_image/<image_id>.")
    print("\n¡Disfruta usando Gaia OSINT!\n")

if __name__ == '__main__':
    # Imprimir el arte ASCII y la bienvenida
    print_ascii_art()

    # Iniciar la aplicación en el puerto asignado por Heroku
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

