import requests
import os
import threading
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, redirect, jsonify, send_file
import random
import string

# Cargar las claves automáticamente desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Claves API desde .env
API_KEY_IPSTACK = os.getenv('API_KEY_IPSTACK')
IMGUR_CLIENT_ID = os.getenv('IMGUR_CLIENT_ID')

# Diccionario para almacenar los enlaces de seguimiento asociados a un ID de usuario
tracking_data = {}

# Función para mostrar el arte ASCII
def print_ascii_art():
    art = """
   ██████   █████  ██  █████  
  ██       ██   ██ ██ ██   ██ 
  ██   ███ ███████ ██ ███████  
  ██    ██ ██   ██ ██   ██  
   ██████  ██   ██ ██ ██   ██  

            By GaiaOSINT
      Desarrollado por BO-ot & If

Advertencia: Esta herramienta es para uso educativo y de investigación.
Cualquier uso malintencionado será responsabilidad del usuario.
    """
    print(art)

# Función para generar una URL de seguimiento única
def generate_tracking_url(image_link):
    user_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    tracking_url = f"http://localhost:5001/track/{user_id}"
    tracking_data[user_id] = image_link
    return user_id, tracking_url

# Función para subir la imagen a Imgur
def upload_image():
    file_path = input("\nArrastra la imagen aquí: ").strip()
    
    if not os.path.exists(file_path):
        print("\nNo se pudo encontrar el archivo. Intenta de nuevo.")
        return
    
    print(f"Ruta recibida: {file_path}")

    try:
        with open(file_path, 'rb') as image:
            headers = {'Authorization': f'Client-ID {IMGUR_CLIENT_ID}'}
            files = {'image': image}
            response = requests.post('https://api.imgur.com/3/image', headers=headers, files=files)

            if response.status_code == 200:
                data = response.json()
                print(f"\nEnlace de la imagen: {data['data']['link']}")
                user_id, tracking_url = generate_tracking_url(data['data']['link'])
                print(f"URL de seguimiento: {tracking_url}")
                return tracking_url, data['data']['link']
            else:
                print("\nError al subir la imagen. Intenta de nuevo.")
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
    except FileNotFoundError as e:
        print(f"Archivo no encontrado: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

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
        'user_agent': user_agent,
        'date': str(datetime.now())
    }
    with open('visitor_data.log', 'a') as file:
        file.write(str(data) + '\n')
    print(f"Datos del visitante guardados: {data}")

# Ruta para capturar la información del visitante (similar a Trape)
@app.route('/track/<user_id>', methods=['GET'])
def track_user(user_id):
    visitor_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    print(f"Visitante IP: {visitor_ip}")
    print(f"User-Agent: {user_agent}")

    # Obtener la geolocalización de la IP
    location = get_geolocation(visitor_ip)
    if location:
        print(f"Ubicación aproximada: {location}")
        save_visitor_data(visitor_ip, location, user_agent)

    # Redirigir a la URL de la imagen asociada con el user_id
    image_link = tracking_data.get(user_id, "https://www.example.com")
    return redirect(image_link)

# Ruta para servir la imagen y capturar la IP del usuario
@app.route('/imagen/<filename>', methods=['GET'])
def serve_image(filename):
    visitor_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    print(f"Visitante IP: {visitor_ip}")
    print(f"User-Agent: {user_agent}")

    # Obtener la geolocalización de la IP
    location = get_geolocation(visitor_ip)
    if location:
        print(f"Ubicación aproximada: {location}")
        save_visitor_data(visitor_ip, location, user_agent)

    image_path = f'static/images/{filename}'
    
    # Verificar si el archivo existe
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/jpeg')
    else:
        return jsonify({"error": "Archivo no encontrado"}), 404

# Menú principal para subir imágenes y generar enlaces
def menu():
    while True:
        print("\nMenú Principal:")
        print("1. Subir imagen y obtener enlace")
        print("2. Salir")
        choice = input("\nElige una opción (1 o 2): ")

        if choice == '1':
            upload_image()
        elif choice == '2':
            print("Saliendo del programa. ¡Adiós!")
            break
        else:
            print("Opción no válida, intenta de nuevo.")

# Función para iniciar Flask en un hilo separado
def run_flask():
    app.run(port=5001, debug=True)

if __name__ == "__main__":
    print_ascii_art()
    
    # Iniciar Flask en un hilo separado
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Mostrar el menú en el hilo principal
      menu()
