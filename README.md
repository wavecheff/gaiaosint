# GaiaOSINT

```
   ██████   █████  ██  █████  
  ██       ██   ██ ██ ██   ██ 
  ██   ███ ███████ ██ ███████  
  ██    ██ ██   ██ ██ ██   ██  
   ██████  ██   ██ ██ ██   ██  

            By GaiaOSINT
      Desarrollado por BO-ot & If
```

**GaiaOSINT** es una herramienta educativa para el análisis de inteligencia de fuentes abiertas (OSINT).
 Facilita la subida de imágenes a **Imgur**, el rastreo de visitantes mediante **IPStack**, y el registro de datos del navegador y eventos.

## Características

- **Subida de imágenes a Imgur** y obtención de enlaces.
- **Geolocalización**: Captura la IP y geolocalización aproximada de los visitantes.
- **Protección con Talisman**: Mejora de seguridad HTTP.
- **Registro de clics y eventos**.
- **Rotación de Logs**: Registros con rotación automática para evitar saturación.

## Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/wavecheff/gaiaosint.git
   cd gaiaosint
   ```

2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuración de Claves API

Crea un archivo **`.env`** con las claves API:
```bash
API_KEY_IPSTACK=tu_clave_ipstack
IMGUR_CLIENT_ID=tu_client_id_imgur
```

## Uso

1. **Inicia la aplicación**:
   ```bash
   python gaia.py
   ```

2. **Accede a la interfaz** en: `http://127.0.0.1:5000/`

### Funcionalidades:

#### Subida de Imagen a Imgur
- Sube imágenes y genera enlaces directamente desde la página principal.

#### Rastrear Visitantes
- Captura datos de la IP del visitante y geolocalización aproximada. 

## Requisitos del Sistema

- Python 3.9+
- Flask 3.0.0
- requests 2.31.0
- python-dotenv 1.0.1

## Contribución

Si deseas contribuir, envía un pull request. Todas las mejoras son bienvenidas.

## Agradecimientos

Esta herramienta ha sido creada con la ayuda de **ChatGPT** como experimento en el desarrollo de aplicaciones OSINT.

## Advertencia

Esta herramienta es para uso educativo y de investigación. El uso malintencionado es responsabilidad del usuario.

---

