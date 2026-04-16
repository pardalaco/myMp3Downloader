# myMp3Downloader

Este proyecto agrupa tres scripts principales para buscar playlists de YouTube con IA y descargar música en MP3.

## Archivos principales

### `buscador_musica.py`

- Carga la clave `GEMINI_API_KEY` desde un archivo `.env`.
- Crea un cliente para la API de Gemini.
- Genera un archivo de texto con el nombre del artista y URLs de playlists de YouTube.
- Está pensado para ejecutar la búsqueda de datos por artista.

Funciones clave:

- `inicializar_cliente()`: carga el `.env` y retorna el cliente Gemini.
- `generar_archivo_artista(cliente, artista, archivo_salida)`: construye un prompt y guarda la respuesta en el archivo.

### `myMp3Downloader.py`

- Toma un archivo `.txt` con artistas y URLs.
- Descarga cada playlist usando `yt_dlp`.
- Convierte el audio a MP3.
- Aplica etiquetas ID3 (`artist` y `album`) a cada archivo descargado.

Funciones clave:

- `analizar_archivo(ruta_archivo)`: parsea el archivo al formato `{ artista: [url1, url2] }`.
- `descargar_y_etiquetar(datos, directorio_base)`: descarga y etiqueta los MP3.

### `buscador_descargador.py`

- Orquesta el flujo completo entre los dos scripts anteriores.
- Genera primero el archivo de playlists con Gemini.
- Luego descarga los MP3 y aplica etiquetas si no se usa `--no-download`.

Funciones clave:

- `buscar_y_descargar(artista, archivo_salida, destino, append, descargar)`: ejecuta la búsqueda y descarga.

## Uso

1. Configura tu `.env` con la variable:

```env
GEMINI_API_KEY=tu_clave_aqui
```

2. Ejecuta la búsqueda y descarga en un solo paso:

```bash
python buscador_descargador.py "Nirvana"
```

3. Solo generar el archivo de playlists sin descargar:

```bash
python buscador_descargador.py "Nirvana" --no-download
```

4. Especificar un archivo de salida y carpeta destino:

```bash
python buscador_descargador.py "Nirvana" -o artistas.txt -d ./descargas
```

5. Añadir al archivo de salida existente en lugar de sobrescribirlo:

```bash
python buscador_descargador.py "Nirvana" --append
```

## Requisitos

- Python 3.8+
- `python-dotenv`
- `yt_dlp`
- `mutagen`
- `google-genai` o la librería compatible de Gemini usada en `buscador_musica.py`

Instala dependencias con:

```bash
pip install -r requirements.txt
```

> Asegúrate de que la clave `GEMINI_API_KEY` esté disponible en tu `.env` antes de ejecutar cualquiera de los scripts.
