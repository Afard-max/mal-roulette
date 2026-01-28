# 🎲 MyAnimeList Roulette (Dark Edition v2.0)

Una aplicación de escritorio moderna y estética que selecciona aleatoriamente un anime de tu biblioteca de MyAnimeList. Ideal para combatir la indecisión de qué ver a continuación.

**¡Nueva Versión 2.0!** Diseño Glassmorphism, soporte para todas las listas y modo Remix.

## ✨ Características V2.0

* **Integración API Avanzada:** Conecta con la API v2 de MyAnimeList. Soporta paginación automática para bibliotecas masivas (+1000 animes).
* **Multi-Lista:** Elige entre:
    * On Hold
    * Plan to Watch
    * Currently Watching
    * Completed
    * Dropped
    * **★ ALL LIST (Remix):** ¡Mezcla todo para una ruleta caótica!
* **Interfaz "Glassmorphism":** Panel semitransparente sobre tu imagen de fondo personalizada.
* **Smart UI:**
    * **Botón RESET:** Limpia usuario y lista para nuevas búsquedas rápidas.
    * **Botón COPY TITLE:** Aparece automáticamente al ganar para copiar el título.
    * Mensajes de error visuales integrados (sin ventanas emergentes).
    * Sonidos de ruleta y victoria.

## 🛠️ Instalación

### Prerrequisitos
* Python 3.8 o superior.
* Cuenta de MyAnimeList.

### Pasos
1.  Clona este repositorio:
    ```bash
    git clone [https://github.com/Afard-max/mal-roulette.git](https://github.com/Afard-max/mal-roulette.git)
    cd mal-roulette
    ```

2.  Crea un entorno virtual e instala dependencias:
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # Linux/Mac:
    source .venv/bin/activate
    
    pip install -r requirements.txt
    ```

3.  **Configuración API:**
    * Crea un archivo `.env` en la carpeta raíz.
    * Añade tu Client ID de MAL:
        ```env
        MAL_CLIENT_ID=tu_client_id_aqui
        ```

4.  Ejecuta:
    ```bash
    python src/app.py
    ```

## 🎮 Uso

1.  Escribe un usuario de MyAnimeList.
2.  Selecciona una lista del menú desplegable.
3.  Presiona **SPIN ROULETTE**.
4.  ¿Quieres cambiar de usuario? Presiona **RESET**.

## 👤 Autor

Desarrollado como proyecto de portafolio demostrando manejo de APIs, GUI (Tkinter + Pillow), Threading y Git Flow.