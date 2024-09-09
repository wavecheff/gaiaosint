
# GaiaOSINT

GaiaOSINT es una herramienta de recopilación de información y geolocalización basada en OSINT. Permite la clasificación de imágenes mediante IA, extracción de metadatos y rastreo de la geolocalización de usuarios.

## Características

- Subida de imágenes con clasificación mediante IA.
- Extracción de metadatos EXIF de las imágenes subidas.
- Rastreo de la geolocalización de usuarios mediante dirección IP.
- Generación de informes OSINT en formato PDF.
- Soporte para JWT para autenticación.
   
## Requisitos
   
- Python 3.9 o superior.
- Redis instalado y corriendo localmente.
- Tener un entorno virtual configurado.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/wavecheff/gaiaosint.git
   cd gaiaosint
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Carga automática de variables de entorno:
   El sistema creará automáticamente un archivo `.env` con las claves API necesarias (IMGUR y IPStack) cuando se ejecute el proyecto. Si no deseas que se creen automáticamente, puedes modificar las claves directamente en el código fuente o configurar manualmente el archivo `.env`.

4. Corre el proyecto:
   ```bash
   python app.py
   ```

## Configuración en Heroku

Si despliegas la aplicación en Heroku, asegúrate de establecer las siguientes variables de entorno en las **Config Vars**:

- `IMGUR_CLIENT_ID`
- `IPSTACK_API_KEY`

Heroku asigna dinámicamente el puerto, por lo que la aplicación está configurada para usar el puerto correcto automáticamente.

