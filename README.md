# 🎲 MyAnimeList Roulette (Dark Edition v3.0)

A modern and aesthetic desktop application that randomly selects an anime from your MyAnimeList library. Perfect for fighting the indecision of what to watch next.

**New Version 3.0!** Now available as a standalone Windows application (.exe). No Python installation required!

## 📥 Download (Windows)

Don't have Python installed? No problem!
**[Download the latest .exe installer here](https://github.com/Afard-max/mal-roulette/releases/tag/v3.0)**

Just download, unzip, and double-click `app.exe` to start spinning!

---

## ✨ Features v3.0

* **🚀 Portable Executable:** Run it instantly on Windows 10/11 without configuring environments or installing libraries.
* **Advanced API Integration:** Connects to MyAnimeList API v2. Supports automatic pagination for massive libraries (1000+ animes).
* **Multi-List Support:** Choose between:
    * On Hold
    * Plan to Watch
    * Currently Watching
    * Completed
    * Dropped
    * **★ ALL LIST (Remix):** Mix everything for a chaotic roulette!
* **"Glassmorphism" Interface:** Semi-transparent panel overlaying your custom background.
* **Smart UI:**
    * **RESET Button:** Quickly clears username and list for new searches.
    * **COPY TITLE Button:** Automatically appears upon winning to copy the title to your clipboard.
    * Integrated visual error messages (no annoying pop-ups).
    * Sound effects for spinning and winning.

## 🛠️ Running from Source (For Developers)

If you prefer to run the Python script directly or want to contribute:

### Prerequisites
* Python 3.8 or higher.
* A MyAnimeList Account.

### Steps
1.  Clone this repository:
    ```bash
    git clone [https://github.com/Afard-max/mal-roulette.git](https://github.com/Afard-max/mal-roulette.git)
    cd mal-roulette
    ```

2.  Create a virtual environment and install dependencies:
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # Linux/Mac:
    source .venv/bin/activate
    
    pip install -r requirements.txt
    ```

3.  **API Configuration:**
    * Create a `.env` file in the root folder.
    * Add your MAL Client ID:
        ```env
        MAL_CLIENT_ID=your_client_id_here
        ```

4.  Run the app:
    ```bash
    python src/app.py
    ```

## 🎮 Usage

1.  Enter your **MyAnimeList username**.
2.  Select a **List** from the dropdown menu (or choose "ALL LIST").
3.  Press **SPIN ROULETTE**.
4.  Want to try another user? Press **RESET**.

## 👤 Author

Developed as a portfolio project demonstrating API handling, GUI design (Tkinter + Pillow), Threading, Git Flow, and Software Packaging (PyInstaller).