

### **README:**

```markdown
# Gaia OSINT

## Descripción
Gaia OSINT es una herramienta de código abierto diseñada para realizar análisis OSINT (Open Source Intelligence) mediante la geolocalización de usuarios que visualizan imágenes. La herramienta permite capturar la dirección IP de quien accede a un enlace de imagen y luego obtener su ubicación aproximada usando la API de IPStack. También soporta la subida de imágenes a Imgur y la generación de informes OSINT.

## Características principales
- **Captura de IP**: Captura la dirección IP del usuario que visualiza una imagen.
- **Geolocalización mediante IP**: Obtiene la geolocalización aproximada del usuario utilizando la API de IPStack.
- **Subida de imágenes a Imgur**: Sube imágenes a Imgur y genera un enlace de imagen para compartir.
- **Extracción de metadatos EXIF**: Extrae metadatos de imágenes para análisis adicionales.
- **Generación de informes OSINT**: Crea informes detallados con los datos recopilados.
- **Soporte para JWT**: Autenticación segura para proteger el acceso.

## Instalación
### Requisitos
- Python 3.6 o superior
- Claves de API para IPStack e Imgur

### Instrucciones de instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/gaia-osint.git
   ```

2. Navegar al directorio del proyecto:
   ```bash
   cd gaia-osint
   ```

3. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Crear el archivo `.env` en la raíz del proyecto con tus claves de API:
   ```
   IPSTACK_API_KEY=tu_clave_de_ipstack
   IMGUR_CLIENT_ID=tu_client_id_de_imgur
   ```

5. Ejecutar la aplicación:
   ```bash
   python gaia.py
   ```

### Uso
1. **Subir una imagen a Imgur**:
   - Envía una imagen a la ruta `/upload` para obtener el enlace de la imagen subida a Imgur.

2. **Compartir el enlace de la imagen**:
   - Envía el enlace generado a un usuario objetivo para rastrear su ubicación.

3. **Capturar la IP del usuario**:
   - Al visualizar la imagen desde el enlace, la aplicación capturará la dirección IP del usuario y la geolocalizará.

4. **Generar informes**:
   - Los datos capturados se almacenan en un archivo de log `visitor_data.log` con la IP, ubicación y fecha de acceso.

## Contribución
Si deseas contribuir a Gaia OSINT, envía tus pull requests. Todas las mejoras son bienvenidas, ya que la herramienta está en constante evolución.

## Agradecimientos
Esta herramienta ha sido creada en un 50% con la ayuda de ChatGPT, un modelo de inteligencia artificial de OpenAI como experimento para la ayuda en el desarrollo de aplicaciones con el objetivo de llegar a obtener aplicaciones 100% desarrolladas por inteligenica artificial.

```
