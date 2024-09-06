import os
import webbrowser
import requests
import logging
import redis
import exifread
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PIL import Image
import torch
import torchvision.transforms as transforms
from torchvision import models
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from fpdf import FPDF
from celery import Celery

# Configuración de la aplicación Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # Tamaño máximo de archivo de 5MB
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'supersecretkey')  # Para autenticación JWT

# Configuración de Celery para tareas asíncronas
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

jwt = JWTManager(app)
cache = redis.StrictRedis(host='localhost', port=6379, db=0)
logging.basicConfig(level=logging.INFO)

# Cargar modelo de clasificación de imágenes (ResNet)
model = models.resnet50(pretrained=True)
model.eval()

# Cargar etiquetas de ImageNet
imagenet_labels = requests.get('https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json').json()

# Funciones Auxiliares
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def transform_image(image_bytes):
    my_transforms = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image = Image.open(image_bytes)
    return my_transforms(image).unsqueeze(0)

def predict(image_bytes):
    tensor = transform_image(image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = y_hat.item()
    return imagenet_labels[predicted_idx]

def cache_or_predict(image_path):
    cache_key = f"prediction_{image_path}"
    cached_prediction = cache.get(cache_key)
    
    if cached_prediction:
        return cached_prediction.decode('utf-8')
    
    with open(image_path, 'rb') as img_file:
        prediction = predict(img_file)
    
    cache.set(cache_key, prediction)
    return prediction

def extract_exif(filepath):
    try:
        with open(filepath, 'rb') as img_file:
            tags = exifread.process_file(img_file)
            return {tag: str(value) for tag, value in tags.items() if tag.startswith("GPS")}
    except Exception as e:
        logging.error(f"Error al extraer EXIF: {e}")
        return {}

def generate_osint_report(ip, geo_data, vpn_status, user_agent):
    report = FPDF()
    report.add_page()
    report.set_font("Arial", size=12)
    
    report.cell(200, 10, txt="Informe OSINT", ln=True, align='C')
    report.cell(200, 10, txt=f"IP: {ip}", ln=True)
    report.cell(200, 10, txt=f"Ciudad: {geo_data.get('city')}", ln=True)
    report.cell(200, 10, txt=f"Región: {geo_data.get('region')}", ln=True)
    report.cell(200, 10, txt=f"País: {geo_data.get('country')}", ln=True)
    report.cell(200, 10, txt=f"Ubicación (lat, lon): {geo_data.get('loc')}", ln=True)
    report.cell(200, 10, txt=f"User-Agent: {user_agent}", ln=True)
    report.cell(200, 10, txt=f"VPN/Proxy: {'Sí' if vpn_status else 'No'}", ln=True)
    
    report_name = f"osint_report_{ip}.pdf"
    report.output(report_name)
    
    return report_name

def detect_vpn_proxy(ip):
    iphub_key = os.getenv('IPHUB_API_KEY')
    vpn_check_url = f"http://v2.api.iphub.info/ip/{ip}"
    headers = {"X-Key": iphub_key}
    
    try:
        vpn_response = requests.get(vpn_check_url, headers=headers)
        vpn_data = vpn_response.json()
        return vpn_data.get('block', 0)
    except Exception as e:
        logging.error(f"Error al detectar VPN/Proxy: {e}")
        return 0

# Tarea asíncrona para predecir imágenes con IA
@celery.task
def async_predict(image_path):
    prediction = cache_or_predict(image_path)
    return prediction

# Endpoints de la aplicación

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/handle_image', methods=['POST'])
@jwt_required()
def handle_image():
    if 'file' not in request.files:
        flash("No se ha subido ningún archivo", "error")
        return redirect(url_for('index'))

    file = request.files['file']
    
    if file.filename == '':
        flash("No se ha seleccionado ningún archivo", "error")
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Procesar la predicción de manera asíncrona
        task = async_predict.delay(filepath)
        flash("La predicción de la IA está en progreso. Esto puede tomar unos momentos.", "info")

        # Extraer metadatos EXIF
        exif_data = extract_exif(filepath)
        if exif_data:
            flash(f"Metadatos EXIF encontrados: {exif_data}", "info")
        
        os.remove(filepath)
        return redirect(url_for('index'))
    
    else:
        flash("Archivo no permitido. Solo se aceptan imágenes en formato png, jpg, jpeg, gif.", "error")
        return redirect(url_for('index'))

@app.route('/track_image/<image_id>')
@jwt_required()
def track_image(image_id):
    ip = request.remote_addr
    ipstack_key = os.getenv('IPSTACK_API_KEY')
    geo_service_url = f"http://api.ipstack.com/{ip}?access_key={ipstack_key}"
    backup_geo_url = f"https://ipinfo.io/{ip}/json"
    
    geo_data = {}
    try:
        geo_response = requests.get(geo_service_url)
        if geo_response.status_code == 200:
            geo_data = geo_response.json()
        else:
            logging.error("Error con IPStack, usando ipinfo.io")
            geo_response = requests.get(backup_geo_url)
            geo_data = geo_response.json()
        
        user_agent = request.headers.get('User-Agent')
        vpn_or_proxy = detect_vpn_proxy(ip)
        
        report_name = generate_osint_report(ip, geo_data, vpn_or_proxy, user_agent)
        
        return render_template('geolocation.html', geo_data=geo_data, vpn_or_proxy=vpn_or_proxy, report_name=report_name)
    
    except Exception as e:
        logging.error(f"Error en la solicitud de geolocalización: {e}")
        return "Error al obtener la geolocalización", 500

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if username == 'admin' and password == 'password':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Credenciales incorrectas"}), 401

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
