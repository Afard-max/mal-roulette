import os
import sys # <--- AGREGAR
import requests
from dotenv import load_dotenv
from typing import List

# --- MISMA FUNCIÓN MAGICA ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Cargar variables de entorno buscando explícitamente en la ruta correcta
load_dotenv(resource_path(".env"))

class MALClient:
    def __init__(self):
        self.client_id = os.getenv("MAL_CLIENT_ID")
        self.base_url = "https://api.myanimelist.net/v2"

        if not self.client_id:
            raise ValueError("❌ Error Crítico: No se encontró MAL_CLIENT_ID en el archivo .env")

    def get_animes(self, username: str, status: str = "on_hold") -> List[str]:
        """
        Obtiene la lista COMPLETA de animes usando paginación.
        """
        # URL inicial
        url = f"{self.base_url}/users/{username}/animelist"
        
        headers = {
            "X-MAL-CLIENT-ID": self.client_id
        }

        # Parámetros iniciales
        params = {
            "limit": 1000, # Pedimos el máximo por página
            "fields": "num_episodes"
        }

        if status != "all":
            params["status"] = status

        animes_totales = []

        try:
            print(f"📡 Iniciando descarga para: {username} ({status})...")
            
            while True:
                # Hacemos la petición
                response = requests.get(url, headers=headers, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                if 'data' not in data:
                    break

                # Agregamos los resultados de esta página a nuestra lista maestra
                nuevos_animes = [item['node']['title'] for item in data['data']]
                animes_totales.extend(nuevos_animes)
                print(f"   ...lote descargado: {len(nuevos_animes)} animes (Total parcial: {len(animes_totales)})")

                # LÓGICA DE PAGINACIÓN
                # La API nos dice si hay una página siguiente en data['paging']['next']
                if "paging" in data and "next" in data["paging"]:
                    url = data["paging"]["next"]
                    # La URL 'next' ya trae sus propios parámetros, así que limpiamos los nuestros
                    # para no duplicarlos o causar conflicto.
                    params = {} 
                else:
                    # No hay más páginas, terminamos
                    break

            return animes_totales

        except requests.exceptions.HTTPError as e:
            print(f"⚠️ Error de HTTP: {e}")
            return []
        except Exception as e:
            print(f"⚠️ Error inesperado: {e}")
            return []

if __name__ == "__main__":
    USER_TEST = "Aceme1pt"
    try:
        client = MALClient()
        print("--- PRUEBA DE PAGINACIÓN (REMIX) ---")
        animes = client.get_animes(USER_TEST, "all") 
        print(f"✅ ÉXITO TOTAL! Se encontraron {len(animes)} animes.")
    except Exception as e:
        print(e)
