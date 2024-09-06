import webbrowser
from flask import Flask, request, jsonify, render_template_string
import os

# Configura tu app Flask
app = Flask(__name__)

@app.route('/')
def index():
    html_content = """
    <h1>Bienvenido a Gaia OSINT</h1>
    <p>Por favor, sube una imagen o accede a /track_image/<image_id> para rastrear la geolocalización.</p>
    <button onclick="window.location.href='/upload_image'">Subir Imagen</button>
    """
    return render_template_string(html_content)

@app.route('/upload_image')
def upload_image():
    html_content = """
    <h1>Subir Imagen</h1>
    <form method="post" enctype="multipart/form-data" action="/handle_image">
        <input type="file" name="file" accept="image/*">
        <button type="submit">Subir</button>
    </form>
    """
    return render_template_string(html_content)

@app.route('/handle_image', methods=['POST'])
def handle_image():
    # Aquí iría la lógica para manejar la imagen, subirla a Imgur, etc.
    # Por ejemplo, podrías subir la imagen a Imgur y devolver el enlace.
    return "Imagen subida correctamente."

@app.route('/track_image/<image_id>')
def track_image(image_id):
    # Aquí iría la lógica para rastrear la geolocalización del usuario que visualiza la imagen.
    return f"Rastreando la geolocalización de la imagen con ID: {image_id}"

# Ejecutar la aplicación en el puerto 5001
if __name__ == '__main__':
    # Abrir automáticamente la aplicación de Heroku en el navegador
    heroku_url = "https://gaiaosint-709ed257d657.herokuapp.com/"
    webbrowser.open(heroku_url)
    
    # Ejecutar Flask en el puerto 5001
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
