# myMp3Downloader

Script de Python para descargar música de YouTube organizada por artista y playlist, con etiquetado automático de metadatos ID3.

## Requisitos

- Python 3.x
- FFmpeg (para la conversión a MP3)

## Instalación

### Instalación estándar

1. Clona el repositorio:

```bash
git clone https://github.com/pardalaco/myMp3Downloader.git
cd myMp3Downloader
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

### Instalación en entorno virtual (recomendado)

1. Clona el repositorio:

```bash
git clone https://github.com/pardalaco/myMp3Downloader.git
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

Basado en `ejemplo.txt`:

```
Daft Punk
https://www.youtube.com/watch?v=FGBhQbmPwH8&list=PLSdoVPM5WnndLX6Ngmb8wktMF61dJirKl
https://www.youtube.com/watch?v=A2VpR8HahKc&list=PLSdoVPM5WnndSQEXRz704yQkKwx76GvPV

Sexy Zebras
Bravo - https://www.youtube.com/watch?v=ShWKbooOCOA&list=PLz0St4NdoxsaSZK2UOg-BUg7VA2CHZlVv
https://youtu.be/tMUyEXzhOyQ?si=vRAHyKJSKkKb8LZ3
```

- **Artista**: Línea con nombre inicia sección (ej. `Daft Punk`).
- **URL estándar**: `https://...` → usa título de playlist o "Singles".
- **URL con álbum**: `Nombre Álbum - https://...` → usa el nombre del álbum (ej. `Bravo`).
- Líneas en blanco se ignoran; mezcla ambos formatos libremente.

**Ejemplo usando playlists:**

```
Nombre del Artista
https://www.youtube.com/playlist?list=XXXXXXXXXXXXXXX
https://www.youtube.com/watch?v=XXXXXXXXXXX

Otro Artista
https://www.youtube.com/playlist?list=YYYYYYYYYYYYYYY
```

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
