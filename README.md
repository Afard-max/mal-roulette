# 🎲 MyAnimeList Roulette (Dark Edition)

Una aplicación de escritorio moderna desarrollada en Python que selecciona aleatoriamente un anime de tu lista "On Hold" (En Espera) de MyAnimeList. Ideal para combatir la indecisión de qué ver a continuación.

![Screenshot](assets/background.png) 
*(Nota: La imagen de arriba es referencial, la app usa tu propia imagen local)*

## ✨ Características

* **Integración API Real:** Conecta directamente con la API v2 de MyAnimeList para obtener datos actualizados.
* **Interfaz Gráfica (GUI) Personalizada:** Desarrollada con Tkinter y Canvas, sin los bordes estándar de Windows.
* **Experiencia UX:** Sonidos de ruleta, animaciones de desaceleración y efectos visuales de victoria.
* **Modo Oscuro:** Diseñada para ser agradable a la vista con alto contraste.
* **Funciones Inteligentes:** * Detecta si el usuario cambia para recargar la lista automáticamente.
    * Botón para copiar el título ganador al portapapeles.
    * Manejo de errores visuales (Usuario no encontrado).

## 🛠️ Instalación

### Prerrequisitos
* Python 3.8 o superior.
* Una cuenta de MyAnimeList.

### Pasos
1.  Clona este repositorio:
    ```bash
    git clone [https://github.com/TU_USUARIO/mal-roulette.git](https://github.com/TU_USUARIO/mal-roulette.git)
    cd mal-roulette
    ```

2.  Crea un entorno virtual e instala las dependencias:
    ```bash
    python -m venv .venv
    # En Windows:
    .venv\Scripts\activate
    # En Linux/Mac:
    source .venv/bin/activate
    
    pip install -r requirements.txt
    ```

3.  **Configuración de la API (Importante):**
    * Crea un archivo llamado `.env` en la carpeta raíz.
    * Obtén tu `Client ID` en [MyAnimeList API Config](https://myanimelist.net/apiconfig).
    * Añade la siguiente línea al archivo `.env`:
        ```env
        MAL_CLIENT_ID=tu_client_id_aqui
        ```

4.  Ejecuta la aplicación:
    ```bash
    python src/app.py
    ```

## 🎮 Uso

1.  Escribe tu nombre de usuario de MyAnimeList (o el de un amigo).
2.  Presiona **SPIN ROULETTE**.
3.  ¡Disfruta tu próximo anime!
4.  Si te gusta el resultado, presiona "COPY TITLE" para buscarlo rápidamente.

## 📂 Estructura del Proyecto

* `src/app.py`: Lógica de la interfaz gráfica y manejo de eventos.
* `src/api_client.py`: Módulo de conexión con la API de MAL.
* `assets/`: Recursos multimedia (imágenes y sonidos).

## 👤 Autor

Desarrollado como proyecto de portafolio para demostrar manejo de APIs, GUIs y Threading en Python.