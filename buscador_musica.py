import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai

def inicializar_cliente():
    """Carga la API key desde .env y devuelve un cliente Gemini.

    Esta función carga las variables de entorno del archivo .env, comprueba
    que exista la clave GEMINI_API_KEY y crea un cliente de la nueva API.
    Si la clave no está presente, muestra un mensaje de error y sale del programa.
    """
    # Cargamos variables desde .env para que os.getenv pueda leer GEMINI_API_KEY
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("[!] ERROR: No se encontró GEMINI_API_KEY en el archivo .env")
        print("Por favor, crea un archivo .env y añade tu clave.")
        sys.exit(1)
        
    # Inicializamos el cliente con el nuevo SDK de Gemini
    return genai.Client(api_key=api_key)

def generar_archivo_artista(cliente, artista, archivo_salida):
    """Genera un archivo de texto con las playlists de YouTube para un artista.

    Usa el cliente Gemini para solicitar información del artista y guarda la
    respuesta formateada en el archivo de salida.
    """
    
    print(f"Buscando la discografía y listas de reproducción de '{artista}'...")
    print("Conectando con la API de Gemini. Esto puede tardar unos segundos...")
    
    prompt = f"""
    Actúa como un experto musical y un generador de datos.
    Tu objetivo es buscar todos los álbumes de estudio del artista "{artista}" y generar la URL de la lista de reproducción (playlist) oficial o más relevante de YouTube para cada álbum.
    
    REGLA ESTRICTA: El formato de tu respuesta debe ser EXACTAMENTE el siguiente, sin texto adicional, sin saludos, sin formato markdown (ni negritas ni bloques de código). Solo el nombre del artista en la primera línea, y debajo una lista de URLs, una por línea.
    
    Ejemplo exacto de lo que debes devolver:
    {artista}
    https://www.youtube.com/playlist?list=ID_INVENTADO_1
    https://www.youtube.com/playlist?list=ID_INVENTADO_2
    
    Por favor, genera ahora el contenido real para: {artista}
    Intenta que las URLs sean lo más precisas posibles a listas de reproducción reales.
    """
    
    try:
        # Nueva forma de generar contenido según la documentación oficial
        respuesta = cliente.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        texto_generado = respuesta.text.strip()
        
        # Guardar en el archivo (añadiendo al final si ya existe)
        with open(archivo_salida, 'a', encoding='utf-8') as f:
            f.write(texto_generado + "\n\n")
            
        print(f"\n✔ ¡Éxito! Se han añadido las playlists de {artista} al archivo '{archivo_salida}'")
        print("Contenido generado:")
        print("-" * 30)
        print(texto_generado)
        print("-" * 30)
        
    except Exception as e:
        print(f"\n[!] Error al conectar con Gemini o generar el contenido: {e}")

def main():
    parser = argparse.ArgumentParser(description="Buscador de discografías con IA para descargar en MP3.")
    parser.add_argument("artista", help="Nombre del artista que quieres buscar (ej. 'Nirvana')")
    parser.add_argument("-o", "--output", default="artistas.txt", help="Archivo de destino (por defecto: artistas.txt)")
    
    # Mostrar ayuda si no hay argumentos
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()
    
    # Obtenemos el cliente configurado y se lo pasamos a la función
    cliente_gemini = inicializar_cliente()
    generar_archivo_artista(cliente_gemini, args.artista, args.output)

if __name__ == "__main__":
    main()