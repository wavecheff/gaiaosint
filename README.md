### README.md:

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

---

GaiaOSINT es una herramienta diseñada para rastrear la localización de usuarios a través de la geolocalización de su IP y la subida de imágenes a Imgur. Esta aplicación está pensada para propósitos educativos y de investigación, y **no debe ser utilizada con fines malintencionados**.

## Características

- Subida de imágenes a Imgur y generación de enlaces.
- Rastrear la ubicación aproximada de los visitantes que acceden a los enlaces generados.
- Guardar los datos de los visitantes en un archivo de log para seguimiento.
- Interfaz web sencilla para la interacción del usuario.

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
   API_KEY_IPSTACK=tu_api_key_ipstack
   IMGUR_CLIENT_ID=tu_client_id_imgur
   ```

   - Puedes obtener una clave API de **IPStack** [aquí](https://ipstack.com/).
   - Puedes obtener tu **Client ID** de Imgur [aquí](https://api.imgur.com/).

2. Guarda el archivo y asegúrate de que el archivo `.env` esté protegido por `.gitignore`.

## Uso de la Aplicación

1. **Inicia la aplicación:**

   ```bash
   python gaia.py
   ```

2. **Abre tu navegador y accede a la aplicación**:

   Visita `http://127.0.0.1:5000/` para acceder a la interfaz web.

### Funcionalidades:

#### 1. Subir una Imagen a Imgur
   - En la página principal, selecciona una imagen para subir a Imgur.
   - La imagen generará un enlace que podrás compartir.

#### 2. Rastrear Visitantes
   - Cuando un usuario accede al enlace de la imagen, GaiaOSINT captura su dirección IP y obtiene su localización aproximada utilizando la API de IPStack.
   - Los datos del visitante se guardan en un archivo de log (`visitor_data.log`), que incluye la dirección IP, geolocalización y el User-Agent del navegador.

## Requisitos del Sistema

- Python 3.9 o superior
- Flask 2.1.2
- requests 2.27.1
- python-dotenv 0.19.2

## Contribución

Si deseas contribuir a Gaia OSINT, envía tus pull requests. Todas las mejoras son bienvenidas, ya que la herramienta está en constante evolución.

## Agradecimientos

Esta herramienta ha sido creada en un 50% con la ayuda de ChatGPT, un modelo de inteligencia artificial de OpenAI, como experimento en el desarrollo de aplicaciones con arquitecturas "relativamente complejas".

## Advertencia

**GaiaOSINT es una herramienta para uso educativo y de investigación. El uso indebido o malintencionado es responsabilidad única del usuario.**

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.
```
