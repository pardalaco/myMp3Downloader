import os
import sys
import argparse
import re
import yt_dlp
from mutagen.easyid3 import EasyID3
import mutagen

def analizar_archivo(ruta_archivo):
    """Lee el archivo txt y crea un diccionario { 'Artista': [(url, album), ...] }.

    Formatos soportados:
    - Artista
      https://... (usa el título de la playlist o 'Singles')
    
    - Artista
      Nombre Album - https://... (usa 'Nombre Album' como carpeta)
    """
    datos = {}
    artista_actual = None
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                
                # Detectar formato: "Nombre Album - URL"
                match = re.match(r'^(.+?)\s+-\s+(https?://.+)$', linea)
                if match:
                    if artista_actual:
                        album = match.group(1).strip()
                        url = match.group(2).strip()
                        datos[artista_actual].append((url, album))
                elif linea.startswith('http://') or linea.startswith('https://'):
                    if artista_actual:
                        datos[artista_actual].append((linea, None))
                else:
                    # Nueva sección de artista
                    artista_actual = linea
                    if artista_actual not in datos:
                        datos[artista_actual] = []
        return datos
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

def descargar_y_etiquetar(datos, directorio_base):
    """Descarga cada playlist y etiqueta los MP3 resultantes.

    Para cada artista y cada URL encontrada en el diccionario, descarga el audio
    de YouTube con yt_dlp, lo convierte a MP3 y guarda los archivos en una
    carpeta organizada por artista y playlist. Luego aplica etiquetas ID3 básicas.
    """
    
    # Asegurarse de que el directorio base existe
    if not os.path.exists(directorio_base):
        os.makedirs(directorio_base)
        print(f"Creada carpeta de destino: {directorio_base}")

    for artista, items in datos.items():
        print(f"\n{'='*60}")
        print(f" PROCESANDO ARTISTA: {artista}")
        print(f"{'='*60}")
        
        for url, album in items:
            # Si se especifica álbum, usarlo; sino usar playlist_title o Singles
            if album:
                outtmpl = f'{directorio_base}/{artista}/{album}/%(title)s.%(ext)s'
            else:
                outtmpl = f'{directorio_base}/{artista}/%(playlist_title|Singles)s/%(title)s.%(ext)s'
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': outtmpl,
                'quiet': False,
                'ignoreerrors': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        # Aplicar Metadatos navegando por la estructura creada
        ruta_artista = os.path.join(directorio_base, artista)
        if not os.path.exists(ruta_artista):
            continue
            
        for nombre_playlist in os.listdir(ruta_artista):
            ruta_playlist = os.path.join(ruta_artista, nombre_playlist)
            if not os.path.isdir(ruta_playlist):
                continue
                
            print(f"\nEtiquetando álbum: {nombre_playlist}...")
            for archivo in os.listdir(ruta_playlist):
                if archivo.endswith('.mp3') and not archivo.startswith('.'):
                    ruta_archivo = os.path.join(ruta_playlist, archivo)
                    try:
                        try:
                            audio = EasyID3(ruta_archivo)
                        except mutagen.id3.ID3NoHeaderError:
                            audio = mutagen.File(ruta_archivo, easy=True)
                            audio.add_tags()
                            
                        audio['artist'] = artista
                        audio['album'] = nombre_playlist
                        audio.save()
                    except Exception as e:
                        print(f"  [Error] No se pudo etiquetar {archivo}: {e}")

def main():
    # Configuración de argumentos
    parser = argparse.ArgumentParser(description="Descargador de música organizado por artista y playlist.")
    parser.add_argument("archivo", help="Nombre o ruta del archivo .txt con la lista de artistas y URLs")
    parser.add_argument("destino", nargs="?", default=".", help="Carpeta donde se guardarán las descargas (opcional, por defecto es la actual)")

    # Si no hay argumentos, mostrar ayuda y salir
    if len(sys.argv) < 2:
        parser.print_help()
        print("\n[!] ERROR: Debes proporcionar al menos el archivo .txt")
        sys.exit(1)

    args = parser.parse_args()

    # Validar existencia del archivo txt
    if not os.path.isfile(args.archivo):
        print(f"\n[!] ERROR: El archivo '{args.archivo}' no existe o no es un archivo válido.")
        sys.exit(1)

    # Iniciar proceso
    print(f"Iniciando proceso...")
    print(f"Archivo de entrada: {args.archivo}")
    print(f"Carpeta de salida: {os.path.abspath(args.destino)}")

    datos = analizar_archivo(args.archivo)
    
    if datos:
        descargar_y_etiquetar(datos, args.destino)
        print("\n✔ ¡Todo el trabajo ha terminado!")
    else:
        print("\n[!] No se encontraron datos válidos para descargar en el archivo.")

if __name__ == "__main__":
    main()