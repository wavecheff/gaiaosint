import os
import webbrowser
from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import requests

# Configurar la aplicación Flask
app = Flask(__name__)

# Arte ASCII para mostrar solo una vez
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

# Página principal con formulario de subida de imágenes
@app.route('/')
def index():
    html_content = """
    <h1>Bienvenido a Gaia OSINT</h1>
    <p>Por favor, sube una imagen o accede a /track_image/&lt;image_id&gt; para rastrear la geolocalización.</p>
    <form action="/handle_image" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept="image/*">
        <button type="submit">Subir Imagen</button>
    </form>
    """
    return render_template_string(html_content)

# Manejar la subida de la imagen a Imgur
@app.route('/handle_image', methods=['POST'])
def handle_image():
    if 'file' not in request.files:
        return "No se ha subido ningún archivo", 400
    
    file = request.files['file']
    
    if file.filename == '':
        return "No se ha seleccionado ningún archivo", 400
    
    if file:
        # Subir la imagen a Imgur usando la API de Imgur
        imgur_client_id = os.getenv('IMGUR_CLIENT_ID')
        headers = {"Authorization": f"Client-ID {imgur_client_id}"}
        url = "https://api.imgur.com/3/image"
        
        response = requests.post(
            url, 
            headers=headers, 
            files={"image": file.stream}
        )
        
        if response.status_code == 200:
            data = response.json()
            image_link = data['data']['link']
            return f"Imagen subida exitosamente: <a href='{image_link}'>{image_link}</a>"
        else:
            return "Error al subir la imagen", 500

# Rastreo de geolocalización (esto es un placeholder)
@app.route('/track_image/<image_id>')
def track_image(image_id):
    return f"Rastreando la geolocalización de la imagen con ID: {image_id}"

# Abrir automáticamente la app de Heroku en el navegador y evitar la duplicación del arte ASCII
if __name__ == '__main__':
    heroku_url = "https://gaiaosint-709ed257d657.herokuapp.com/"
    webbrowser.open(heroku_url)
    
    # Solo imprimir el arte ASCII una vez al inicio
    if 'DYNO' not in os.environ:  # Verificar si se ejecuta localmente
        print_ascii_art()
    
    # Ejecutar la aplicación Flask en el puerto 5001 o el definido por Heroku
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
