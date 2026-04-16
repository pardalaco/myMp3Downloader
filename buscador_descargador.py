import argparse
import os
import sys

import buscador_musica
import myMp3Downloader


def buscar_y_descargar(artista, archivo_salida='artistas.txt', destino='.', append=False, descargar=True):
    """Genera el archivo de artistas/URLs y ejecuta la descarga si se solicita.

    Esta función orquesta el flujo completo: primero obtiene las playlists con
    Gemini y luego, si descargar=True, procesa el archivo generado para
    descargar los MP3 y etiquetarlos.
    """
    if not append and os.path.exists(archivo_salida):
        print(f"El archivo de salida '{archivo_salida}' ya existe. Se eliminará antes de generar nuevo contenido.")
        os.remove(archivo_salida)

    cliente = buscador_musica.inicializar_cliente()
    buscador_musica.generar_archivo_artista(cliente, artista, archivo_salida)

    if descargar:
        datos = myMp3Downloader.analizar_archivo(archivo_salida)
        if datos:
            myMp3Downloader.descargar_y_etiquetar(datos, destino)
        else:
            print("\n[!] No se encontraron datos válidos en el archivo generado. No se realizará la descarga.")


def main():
    parser = argparse.ArgumentParser(
        description='Busca playlists de un artista con IA y descarga sus contenidos en MP3.'
    )
    parser.add_argument('artista', help="Nombre del artista que quieres buscar (ej. 'Nirvana')")
    parser.add_argument('-o', '--output', default='artistas.txt', help='Archivo de destino para las URLs (por defecto: artistas.txt)')
    parser.add_argument('-d', '--destino', default='.', help='Carpeta donde se guardarán las descargas (por defecto: la carpeta actual)')
    parser.add_argument('--append', action='store_true', help='Añadir al archivo de salida en lugar de sobrescribirlo.')
    parser.add_argument('--no-download', action='store_true', help='Solo generar el archivo de URLs y no descargar audio.')

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    buscar_y_descargar(
        artista=args.artista,
        archivo_salida=args.output,
        destino=args.destino,
        append=args.append,
        descargar=not args.no_download,
    )


if __name__ == '__main__':
    main()
