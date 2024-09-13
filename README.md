
```markdown
# GaiaOSINT

  ██████   █████  ██  █████  
 ██       ██   ██ ██ ██   ██ 
 ██   ███ ███████ ██ ███████ 
 ██    ██ ██   ██ ██ ██   ██ 
  ██████  ██   ██ ██ ██   ██ 

           By GaiaOSINT
    Desarrollado por BO-ot & If

Advertencia: Esta herramienta es para uso educativo y de investigación.
Cualquier uso malintencionado será responsabilidad del usuario.
```
---

## Características

- Subida de imágenes a Imgur y generación de enlaces.
- Capturar y guardar información de visitantes incluyendo:
	- Dirección IP
	- Geolocalización
	- Información del navegador y sistema operativo 
	- Dispositivos utilizados
	- Extraer metadatos EXIF de las imagenes subidas
- Guardar los datos de los visitantes en un archivo de log.
- Implementación de Talisman para mejorar la seguridad.
- Sistema de rotación de logs para evitar sobrecarga de archivos.
- Captura de eventos de clic y metadatos del navegador.

## Instalación

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/wavecheff/gaiaosint.git
   ```

2. **Navega al directorio del proyecto:**

   ```bash
   cd gaiaosint
   ```

3. **Instala las dependencias:**

   Asegúrate de tener un entorno virtual configurado. Luego instala todas las dependencias necesarias con:

   ```bash
   pip install -r requirements.txt
   ```

## Configuración de Claves API

1. **Crea un archivo `.env`** en el directorio principal del proyecto con las siguientes claves API:

   ```bash
   API_KEY_IPSTACK=tu_clave_ipstack
   IMGUR_CLIENT_ID=tu_client_id_imgur
   ```

   - Puedes obtener una clave API de **IPStack** [aquí](https://ipstack.com/).
   - Puedes obtener tu **Client ID** de Imgur [aquí](https://api.imgur.com/).

## Uso de la Aplicación

1. **Inicia la aplicación:**
   
   ```bash
   python gaia.py
   ```

2. **Abre tu navegador y accede a la aplicación:**

   Visita `http://127.0.0.1:5000/` para acceder a la interfaz web.
   
### Funcionalidades:

#### 1. Subir una Imagen a Imgur
   - En la página principal, selecciona una imagen para subir a Imgur.
   - La imagen generará un enlace que podrás compartir.

#### 2. Rastrear Visitantes
   - Cuando un usuario accede al enlace de la imagen, GaiaOSINT captura su dirección IP y obtiene su localización aproximada utilizando la API de IPStack.

   - Los datos del visitante se guardan en un archivo de log (`visitor_data.log`), que incluye la dirección IP, geolocalización y el User-Agent del navegador.

#### 3. Rotación de logs
   - Implementación de rotación de logs para evitar el crecimiento excesivo del archivo de registro.

#### 4. Captura de Eventos de Clic y Metadatos
   - Registra los eventos de clics y los metadatos del navegador del visitante.

#### 5. Protección con Talisman
   - El proyecto incluye protección de seguridad adicional usando **Flask-Talisman**.

## Requisitos del Sistema

- Python 3.9 o superior
- Flask 3.0.0
- requests 2.31.0
- python-dotenv 1.0.1

## Contribución

Si deseas contribuir a Gaia OSINT, envía tus pull requests. Todas las mejoras son bienvenidas, ya que la herramienta está en constante evolución.
   
## Agradecimientos

Esta herramienta ha sido creada en un 50% con la ayuda de ChatGPT, un modelo de inteligencia artificial de OpenAI, como experimento en el desarrollo de aplicaciones con arquitecturas "relativamente complejas".

## Advertencia

**GaiaOSINT es una herramienta para uso educativo y de investigación. El uso indebido o malintencionado es responsabilidad única del usuario.**

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.

---

