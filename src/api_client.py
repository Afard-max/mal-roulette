import os
import requests
from dotenv import load_dotenv
from typing import List

# 1. Cargar variables de entorno al inicio (lee el archivo .env)
load_dotenv()

class MALClient:
    """
    Clase encargada de interactuar exclusivamente con la API de MyAnimeList.
    """

    def __init__(self):
        # Recuperamos la credencial del entorno. Si no existe, lanzamos error.
        self.client_id = os.getenv("MAL_CLIENT_ID")
        self.base_url = "https://api.myanimelist.net/v2"

        if not self.client_id:
            raise ValueError("❌ Error Crítico: No se encontró MAL_CLIENT_ID en el archivo .env")

    def get_animes(self, username: str, status: str = "on_hold") -> List[str]:
        """
        Obtiene la lista de animes de un usuario con un estado específico.
        
        Args:
            username (str): Nombre de usuario en MAL.
            status (str): Estado a filtrar ('on_hold', 'plan_to_watch', 'completed', etc).
            
        Returns:
            List[str]: Lista con los títulos de los animes. Devuelve lista vacía si hay error.
        """
        endpoint = f"{self.base_url}/users/{username}/animelist"
        
        # Headers: Aquí es donde nos "identificamos" ante MAL
        headers = {
            "X-MAL-CLIENT-ID": self.client_id
        }

        # Parameters: Configuración de la consulta
        params = {
            "status": status,
            "limit": 1000,  # Pedimos un número alto para evitar paginación compleja
            "fields": "num_episodes" # Podríamos pedir más datos aquí si quisiéramos
        }

        try:
            print(f"📡 Consultando API para el usuario: {username}...")
            response = requests.get(endpoint, headers=headers, params=params, timeout=10)
            
            # Si el código de respuesta es 4xx o 5xx, esto lanzará una excepción
            response.raise_for_status()
            
            data = response.json()
            
            # Extracción limpia de datos usando List Comprehension
            # Navegamos: data -> data -> node -> title
            if 'data' in data:
                titulos = [item['node']['title'] for item in data['data']]
                return titulos
            else:
                return []

        except requests.exceptions.HTTPError as e:
            print(f"⚠️ Error de HTTP: {e}")
            return []
        except Exception as e:
            print(f"⚠️ Error inesperado: {e}")
            return []

# --- BLOQUE DE PRUEBA (Solo se ejecuta si corres este archivo directamente) ---
if __name__ == "__main__":
    # Prueba rápida para verificar que tu API Key funciona
    # Cambia 'TU_USUARIO' por tu usuario real de MAL para probar ahora mismo
    USER_TEST = "Aceme1pt" 
    
    try:
        client = MALClient()
        animes = client.get_animes(USER_TEST, "on_hold")
        print(f"✅ Éxito! Se encontraron {len(animes)} animes en 'On Hold'.")
        if animes:
            print(f"Ejemplo: {animes[0]}")
    except Exception as e:
        print(e)
