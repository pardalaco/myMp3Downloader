# myMp3Downloader

Script de Python para descargar música de YouTube organizada por artista y playlist, con etiquetado automático de metadatos ID3.

## Requisitos

- Python 3.x
- FFmpeg (para la conversión a MP3)

## Instalación

### Instalación estándar

1. Clona el repositorio:

```bash
git clone https://github.com/anomalyco/myMp3Downloader.git
cd myMp3Downloader
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

### Instalación en entorno virtual (recomendado)

1. Clona el repositorio:

```bash
git clone https://github.com/anomalyco/myMp3Downloader.git
cd myMp3Downloader
```

2. Crea un entorno virtual:

```bash
python -m venv .venv
```

3. Activa el entorno virtual:
   - En macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
   - En Windows:
     ```bash
     .venv\Scripts\activate
     ```

4. Instala las dependencias en el entorno virtual:

```bash
pip install -r requirements.txt
```

## Formato del archivo de entrada

Crea un archivo de texto (.txt) con el siguiente formato:

**Formato estándar (usa el título de la playlist o "Singles"):**
```
Nombre del Artista
https://www.youtube.com/playlist?list=XXXXXXXXXXXXXXX
https://www.youtube.com/watch?v=XXXXXXXXXXX

Otro Artista
https://www.youtube.com/playlist?list=YYYYYYYYYYYYYYY
```

**Nuevo formato (especifica el nombre del álbum):**
```
Nombre del Artista
Nombre del Álbum - https://www.youtube.com/playlist?list=XXXXXXXXXXXXXXX
Nombre del Álbum - https://www.youtube.com/watch?v=XXXXXXXXXXX
```

- Una línea con el nombre del artista
- Las siguientes líneas con URLs de YouTube (playlists o videos individuales)
- Para especificar el álbum: `Nombre Álbum - URL`
- Líneas en blanco se ignoran
- Puedes mezclar ambos formatos y incluir múltiples artistas

## Uso

```bash
python myMp3Downloader.py <archivo.txt> [carpeta_destino]
```

### Ejemplos

Descargar en la carpeta actual:

```bash
python myMp3Downloader.py lista.txt
```

Descargar en una carpeta específica:

```bash
python myMp3Downloader.py lista.txt ./Musica
```

## Estructura de salida

Las descargas se organizan automáticamente:

```
carpeta_destino/
├── Artista 1/
│   ├── Nombre Playlist 1/
│   │   ├── Cancion 1.mp3
│   │   └── Cancion 2.mp3
│   └── Singles/
│       └── Cancion individual.mp3
└── Artista 2/
    └── ...
```

## Notas

- Los archivos se descargan en formato MP3 a 192kbps
- Se aplican automáticamente etiquetas ID3 (artista y álbum)
- Las playlists se agrupan por su título; los videos individuales van a la carpeta "Singles"
- El script ignora errores de descarga y continúa con el siguiente elemento
