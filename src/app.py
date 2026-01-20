import tkinter as tk
from tkinter import messagebox
import random
import threading
import winsound
import os
from PIL import Image, ImageTk, ImageEnhance

# Intentamos importar el cliente API
try:
    from api_client import MALClient
except ImportError:
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from api_client import MALClient

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

class AnimeRouletteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MAL Roulette: Dark Edition")
        
        # Centrar ventana
        w, h = 500, 500
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.resizable(False, False)

        try:
            self.client = MALClient()
        except ValueError as e:
            messagebox.showerror("Configuration Error", str(e))
            self.root.destroy()
            return

        # VARIABLES DE ESTADO
        self.lista_animes = []
        self.is_spinning = False
        self.current_winner = ""
        self.last_fetched_user = "" # MEJORA: Recordar el último usuario buscado

        self.cargar_assets()
        self.crear_interfaz()

    def cargar_assets(self):
        try:
            path_img = os.path.join(ASSETS_DIR, 'background.png')
            pil_image = Image.open(path_img)
            
            enhancer = ImageEnhance.Brightness(pil_image)
            pil_image = enhancer.enhance(0.6) 
            
            self.bg_image = ImageTk.PhotoImage(pil_image)
            self.sound_path = os.path.join(ASSETS_DIR, 'spin.wav')
            
        except Exception as e:
            messagebox.showerror("Asset Error", f"Could not load assets:\n{e}")
            self.root.destroy()

    def round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    def crear_interfaz(self):
        self.canvas = tk.Canvas(self.root, width=500, height=500, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Fondo
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Título App
        self.crear_texto_con_sombra(250, 50, "MYANIMELIST ROULETTE", 24)

        # Input Box
        self.round_rectangle(120, 90, 380, 160, radius=20, fill="#000000", outline="#333333")
        self.canvas.create_text(250, 110, text="USERNAME:", fill="#aaaaaa", font=("Arial", 8, "bold"))
        
        self.entry_user = tk.Entry(self.root, justify="center", bg="#222222", fg="white", 
                                   insertbackground="white", relief="flat", font=("Arial", 11))
        self.entry_user.place(x=150, y=125, width=200, height=25)
        self.entry_user.insert(0, "Aceme1pt")

        # AREA PRINCIPAL DE RESULTADO
        # MEJORA: justify="center" asegura que si hay 2 lineas, ambas esten centradas
        # MEJORA: Tamaño reducido a 26 (antes 28)
        self.txt_res_shadow = self.canvas.create_text(252, 242, text="PRESS START", fill="black", font=("Impact", 26), justify="center")
        self.txt_res_main = self.canvas.create_text(250, 240, text="PRESS START", fill="white", font=("Impact", 26), justify="center")
        
        # Texto de Estado (Waiting / Winner / Error)
        self.text_status_id = self.canvas.create_text(250, 300, text="Waiting...", fill="#cccccc", font=("Arial", 10, "italic"))

        # Botón Copiar
        self.btn_copy_bg = self.round_rectangle(200, 320, 300, 350, radius=10, fill="#444444", outline="#666666", state='hidden')
        self.btn_copy_text = self.canvas.create_text(250, 335, text="COPY TITLE", fill="white", font=("Arial", 8, "bold"), state='hidden')
        
        self.canvas.tag_bind(self.btn_copy_bg, '<Button-1>', self.copiar_titulo)
        self.canvas.tag_bind(self.btn_copy_text, '<Button-1>', self.copiar_titulo)

        # Botón Spin
        self.btn_x1, self.btn_y1, self.btn_x2, self.btn_y2 = 150, 400, 350, 450
        self.btn_shadow = self.round_rectangle(self.btn_x1+3, self.btn_y1+3, self.btn_x2+3, self.btn_y2+3, radius=20, fill="#111111")
        self.btn_bg = self.round_rectangle(self.btn_x1, self.btn_y1, self.btn_x2, self.btn_y2, radius=20, fill="#d32f2f", outline="#ff5252")
        self.btn_text = self.canvas.create_text(250, 425, text="SPIN ROULETTE", fill="white", font=("Arial", 12, "bold"))

        self.canvas.tag_bind(self.btn_bg, '<Button-1>', self.on_btn_click)
        self.canvas.tag_bind(self.btn_text, '<Button-1>', self.on_btn_click)

    def crear_texto_con_sombra(self, x, y, texto, size, color="white"):
        # Función auxiliar para textos estáticos (como el título)
        shadow = self.canvas.create_text(x+2, y+2, text=texto, fill="black", font=("Impact", size))
        main = self.canvas.create_text(x, y, text=texto, fill=color, font=("Impact", size))
        return shadow, main

    def on_btn_click(self, event):
        if not self.is_spinning:
            self.iniciar_giro()

    def copiar_titulo(self, event):
        if self.current_winner:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.current_winner)
            self.canvas.itemconfig(self.btn_copy_text, text="COPIED!", fill="#81c784")
            self.root.after(1500, lambda: self.canvas.itemconfig(self.btn_copy_text, text="COPY TITLE", fill="white"))

    def iniciar_giro(self):
        # 1. Intentamos obtener datos. Si falla, obtener_datos se encarga del error visual.
        if not self.obtener_datos(): 
            return

        self.is_spinning = True
        self.current_winner = ""
        
        # Ocultar UI innecesaria
        self.canvas.itemconfig(self.btn_copy_bg, state='hidden')
        self.canvas.itemconfig(self.btn_copy_text, state='hidden')
        
        # Resetear estado
        self.canvas.itemconfig(self.text_status_id, text="Spinning...", font=("Arial", 10, "italic"), fill="#cccccc")
        self.canvas.itemconfig(self.btn_bg, fill="#b71c1c") 
        
        threading.Thread(target=self.reproducir_sonido, daemon=True).start()
        self.animar(30)

    def reproducir_sonido(self):
        if os.path.exists(self.sound_path):
            winsound.PlaySound(self.sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)

    def obtener_datos(self):
        usuario_actual = self.entry_user.get().strip() # .strip() quita espacios accidentales
        
        if not usuario_actual:
            messagebox.showwarning("Warning", "Please enter a username")
            return False

        # MEJORA: LÓGICA DE REINICIO AUTOMÁTICO
        # Si el usuario cambió desde la última vez, borramos la lista para forzar descarga
        if usuario_actual != self.last_fetched_user:
            self.lista_animes = []

        # Si no tenemos animes (porque es nuevo o porque limpiamos la lista), descargamos
        if not self.lista_animes:
            self.canvas.itemconfig(self.text_status_id, text=f"📡 Downloading list for {usuario_actual}...")
            self.root.update()
            
            animes = self.client.get_animes(usuario_actual, "on_hold")
            
            # MEJORA: ERROR VISUAL "USER NOT FOUND"
            if not animes:
                # Mostramos error estilo "Winner" pero en rojo y con mensaje de error
                self.mostrar_error_visual("USER NOT FOUND\n(OR EMPTY LIST)")
                return False
            
            # Si tuvo éxito, guardamos los datos
            self.lista_animes = animes
            self.last_fetched_user = usuario_actual # Actualizamos el "último usuario"
            
        return True

    def mostrar_error_visual(self, mensaje_error):
        """Muestra el error en el centro con estilo"""
        winsound.PlaySound(None, winsound.SND_PURGE) # Cortar sonido si hubiera
        winsound.MessageBeep(winsound.MB_ICONHAND) # Sonido de error de Windows
        
        # Texto central en rojo
        self.canvas.itemconfig(self.txt_res_shadow, text=mensaje_error)
        self.canvas.itemconfig(self.txt_res_main, text=mensaje_error, fill="#ff5252") # Rojo claro
        
        # Texto inferior
        self.canvas.itemconfig(self.text_status_id, text="Check spelling or privacy settings", font=("Arial", 10), fill="#ff5252")
        
        self.is_spinning = False
        self.canvas.itemconfig(self.btn_bg, fill="#d32f2f") # Restaurar botón

    def animar(self, pasos_restantes):
        if pasos_restantes > 0:
            random_anime = random.choice(self.lista_animes)
            # Acortar para la animación rápida
            if len(random_anime) > 25: random_anime = random_anime[:22] + "..."
            
            self.canvas.itemconfig(self.txt_res_shadow, text=random_anime)
            self.canvas.itemconfig(self.txt_res_main, text=random_anime, fill="#cccccc")
            
            delay = 50 + (30 - pasos_restantes) * 10
            self.root.after(int(delay), self.animar, pasos_restantes - 1)
        else:
            self.finalizar_giro()

    def finalizar_giro(self):
        winsound.PlaySound(None, winsound.SND_PURGE)

        self.current_winner = random.choice(self.lista_animes)
        
        # Formatear texto largo con saltos de línea inteligentes
        display_text = self.current_winner
        if len(self.current_winner) > 20:
             mid = len(self.current_winner) // 2
             # Buscamos el espacio más cercano al medio
             split_idx = self.current_winner.find(' ', mid)
             # Si no encuentra espacio cerca del medio, buscamos antes
             if split_idx == -1: 
                 split_idx = self.current_winner.rfind(' ', 0, mid)
             
             if split_idx != -1:
                 display_text = self.current_winner[:split_idx] + "\n" + self.current_winner[split_idx+1:]

        self.canvas.itemconfig(self.txt_res_shadow, text=display_text)
        self.canvas.itemconfig(self.txt_res_main, text=display_text, fill="#ffeb3b")
        
        self.canvas.itemconfig(self.text_status_id, text="WE HAVE A WINNER!", 
                               font=("Arial", 12, "bold italic"), fill="#ffffff")
        
        self.animar_victoria(0)

        self.canvas.itemconfig(self.btn_copy_bg, state='normal')
        self.canvas.itemconfig(self.btn_copy_text, state='normal')
        
        self.is_spinning = False
        self.canvas.itemconfig(self.btn_bg, fill="#d32f2f")
        winsound.MessageBeep(winsound.MB_ICONASTERISK)

    def animar_victoria(self, paso):
        colores = ["#ffeb3b", "#ff5252", "#ffffff", "#ffeb3b"]
        if paso < len(colores):
            self.canvas.itemconfig(self.text_status_id, fill=colores[paso])
            self.root.after(100, self.animar_victoria, paso + 1)
        else:
            self.canvas.itemconfig(self.text_status_id, fill="#ffffff")

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimeRouletteApp(root)
    root.mainloop()