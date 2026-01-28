import tkinter as tk
from tkinter import messagebox, ttk
import random
import threading
import winsound
import os
from PIL import Image, ImageTk, ImageEnhance, ImageDraw

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
        self.root.title("MAL Roulette: Dark Edition v2")
        
        # Geometría 500x500
        w, h = 500, 500 
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.resizable(False, False)

        # Estilos Combobox
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", 
                        fieldbackground="#222222", 
                        background="#333333", 
                        foreground="white",
                        arrowcolor="white",
                        bordercolor="#222222",
                        lightcolor="#222222",
                        darkcolor="#222222")
        
        style.map('TCombobox', 
                  fieldbackground=[('readonly', '#222222')],
                  selectbackground=[('readonly', '#222222')],
                  selectforeground=[('readonly', 'white')],
                  background=[('readonly', '#333333')])

        self.root.option_add('*TCombobox*Listbox.background', '#222222')
        self.root.option_add('*TCombobox*Listbox.foreground', 'white')
        self.root.option_add('*TCombobox*Listbox.selectBackground', '#d32f2f')
        self.root.option_add('*TCombobox*Listbox.selectForeground', 'white')
        self.root.option_add('*TCombobox*Listbox.justify', 'center') 

        try:
            self.client = MALClient()
        except ValueError as e:
            messagebox.showerror("Configuration Error", str(e))
            self.root.destroy()
            return

        # VARIABLES
        self.lista_animes = []
        self.is_spinning = False
        self.current_winner = ""
        self.last_fetched_user = ""
        self.last_fetched_list = ""
        
        self.bg_image = None
        self.panel_img = None 

        self.list_options = {
            "On Hold": "on_hold",
            "Plan to Watch": "plan_to_watch",
            "Currently Watching": "watching",
            "Completed": "completed",
            "Dropped": "dropped",
            "ALL LIST": "all" 
        }

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
        """Dibuja polígonos sólidos"""
        points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1,
                  x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius,
                  x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2,
                  x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    def crear_imagen_transparente(self, w, h, radius, color_hex, alpha):
        img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        r = int(color_hex[1:3], 16)
        g = int(color_hex[3:5], 16)
        b = int(color_hex[5:7], 16)
        draw.rounded_rectangle((0, 0, w, h), radius=radius, fill=(r, g, b, alpha))
        return ImageTk.PhotoImage(img)

    def crear_interfaz(self):
        self.canvas = tk.Canvas(self.root, width=500, height=500, highlightthickness=0, bg="black")
        self.canvas.pack(fill="both", expand=True)

        # Fondo
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Título Principal
        self.crear_texto_con_sombra(250, 35, "MYANIMELIST ROULETTE", 24)

        # Panel Transparente
        self.panel_img = self.crear_imagen_transparente(260, 150, radius=20, color_hex="#000000", alpha=180)
        self.canvas.create_image(250, 145, image=self.panel_img)
        
        # SECCIÓN 1: USUARIO
        self.canvas.create_text(250, 85, text="USERNAME:", fill="#aaaaaa", font=("Arial", 8, "bold"))
        self.entry_user = tk.Entry(self.root, justify="center", bg="#222222", fg="white", 
                                   insertbackground="white", relief="flat", font=("Arial", 11))
        self.entry_user.place(x=150, y=100, width=200, height=25)

        # SECCIÓN 2: LISTA
        self.canvas.create_text(250, 140, text="SELECT LIST:", fill="#aaaaaa", font=("Arial", 8, "bold"))
        
        self.combo_list = ttk.Combobox(self.root, values=list(self.list_options.keys()), 
                                       state="readonly", justify="center", font=("Arial", 10))
        self.combo_list.place(x=150, y=155, width=200)
        
        # BOTÓN RESET
        self.btn_reset_bg = self.round_rectangle(210, 190, 290, 210, radius=10, fill="#444444", outline="#555555")
        self.btn_reset_text = self.canvas.create_text(250, 200, text="RESET", fill="#cccccc", font=("Arial", 7, "bold"))
        self.canvas.tag_bind(self.btn_reset_bg, '<Button-1>', self.reiniciar_datos)
        self.canvas.tag_bind(self.btn_reset_text, '<Button-1>', self.reiniciar_datos)
        
        # --- CORRECCIÓN ESPACIADO (Movemos todo 30px hacia abajo) ---
        # Título del anime (y=250 -> y=280)
        self.txt_res_shadow = self.canvas.create_text(252, 282, text="PRESS START", fill="black", font=("Impact", 26), justify="center")
        self.txt_res_main = self.canvas.create_text(250, 280, text="PRESS START", fill="white", font=("Impact", 26), justify="center")
        
        # Texto de estado (y=310 -> y=340)
        self.text_status_id = self.canvas.create_text(250, 340, text="Waiting...", fill="#cccccc", font=("Arial", 10, "italic"))

        # Botón Copiar (y=330-360 -> y=360-390)
        self.btn_copy_bg = self.round_rectangle(200, 360, 300, 390, radius=10, fill="#444444", outline="#666666", state='hidden')
        self.btn_copy_text = self.canvas.create_text(250, 375, text="COPY TITLE", fill="white", font=("Arial", 8, "bold"), state='hidden')
        self.canvas.tag_bind(self.btn_copy_bg, '<Button-1>', self.copiar_titulo)
        self.canvas.tag_bind(self.btn_copy_text, '<Button-1>', self.copiar_titulo)

        # SPIN BTN (Se mantiene en y=410)
        self.btn_x1, self.btn_y1, self.btn_x2, self.btn_y2 = 150, 410, 350, 460
        self.btn_shadow = self.round_rectangle(self.btn_x1+3, self.btn_y1+3, self.btn_x2+3, self.btn_y2+3, radius=20, fill="#111111")
        self.btn_bg = self.round_rectangle(self.btn_x1, self.btn_y1, self.btn_x2, self.btn_y2, radius=20, fill="#d32f2f", outline="#ff5252")
        self.btn_text = self.canvas.create_text(250, 435, text="SPIN ROULETTE", fill="white", font=("Arial", 12, "bold"))
        self.canvas.tag_bind(self.btn_bg, '<Button-1>', self.on_btn_click)
        self.canvas.tag_bind(self.btn_text, '<Button-1>', self.on_btn_click)

    def crear_texto_con_sombra(self, x, y, texto, size, color="white"):
        shadow = self.canvas.create_text(x+2, y+2, text=texto, fill="black", font=("Impact", size))
        main = self.canvas.create_text(x, y, text=texto, fill=color, font=("Impact", size))
        return shadow, main

    def on_btn_click(self, event):
        if not self.is_spinning:
            self.iniciar_giro()

    def reiniciar_datos(self, event):
        """Borra campos y reinicia variables"""
        if self.is_spinning: return 
        
        self.entry_user.delete(0, tk.END) 
        self.combo_list.set('') 
        
        self.lista_animes = []
        self.last_fetched_user = ""
        self.last_fetched_list = ""
        self.current_winner = ""
        
        winsound.MessageBeep(winsound.MB_OK) 
        self.canvas.itemconfig(self.text_status_id, text="Data cleared.", fill="#81c784") 
        
        self.canvas.itemconfig(self.txt_res_shadow, text="PRESS START")
        self.canvas.itemconfig(self.txt_res_main, text="PRESS START", fill="white")
        
        self.canvas.itemconfig(self.btn_copy_bg, state='hidden')
        self.canvas.itemconfig(self.btn_copy_text, state='hidden')

        self.root.after(1000, lambda: self.canvas.itemconfig(self.text_status_id, text="Waiting...", fill="#cccccc"))

    def copiar_titulo(self, event):
        if self.current_winner:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.current_winner)
            self.canvas.itemconfig(self.btn_copy_text, text="COPIED!", fill="#81c784")
            self.root.after(1500, lambda: self.canvas.itemconfig(self.btn_copy_text, text="COPY TITLE", fill="white"))

    def iniciar_giro(self):
        usuario_actual = self.entry_user.get().strip()
        nombre_lista = self.combo_list.get()

        if not usuario_actual:
            self.mostrar_error_visual("TYPE A USERNAME")
            return

        if not nombre_lista:
            self.mostrar_error_visual("SELECT A LIST")
            return

        if not self.obtener_datos(usuario_actual, nombre_lista): 
            return

        self.is_spinning = True
        self.current_winner = ""
        
        self.canvas.itemconfig(self.btn_copy_bg, state='hidden')
        self.canvas.itemconfig(self.btn_copy_text, state='hidden')
        
        self.canvas.itemconfig(self.text_status_id, text="Spinning...", font=("Arial", 10, "italic"), fill="#cccccc")
        self.canvas.itemconfig(self.btn_bg, fill="#b71c1c") 
        
        threading.Thread(target=self.reproducir_sonido, daemon=True).start()
        self.animar(30)

    def reproducir_sonido(self):
        if os.path.exists(self.sound_path):
            winsound.PlaySound(self.sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)

    def obtener_datos(self, usuario_actual, nombre_lista_seleccionada):
        clave_api_seleccionada = self.list_options[nombre_lista_seleccionada]

        if (usuario_actual != self.last_fetched_user) or (clave_api_seleccionada != self.last_fetched_list):
            self.lista_animes = []

        if not self.lista_animes:
            self.canvas.itemconfig(self.text_status_id, text=f"📡 Downloading '{nombre_lista_seleccionada}'...")
            self.root.update()
            
            animes = self.client.get_animes(usuario_actual, clave_api_seleccionada)
            
            if not animes:
                self.mostrar_error_visual("LIST IS EMPTY\nOR USER NOT FOUND")
                return False
            
            self.lista_animes = animes
            self.last_fetched_user = usuario_actual
            self.last_fetched_list = clave_api_seleccionada
            
        return True

    def mostrar_error_visual(self, mensaje_error):
        winsound.PlaySound(None, winsound.SND_PURGE)
        winsound.MessageBeep(winsound.MB_ICONHAND)
        
        self.canvas.itemconfig(self.txt_res_shadow, text=mensaje_error)
        self.canvas.itemconfig(self.txt_res_main, text=mensaje_error, fill="#ff5252") 
        
        subtexto = "Check details"
        if "TYPE" in mensaje_error:
             subtexto = "Please enter a username"
        elif "SELECT" in mensaje_error:
             subtexto = "Please choose a list from the menu"
        else:
             subtexto = "Check spelling or privacy settings"

        self.canvas.itemconfig(self.text_status_id, text=subtexto, font=("Arial", 10), fill="#ff5252")
        
        self.is_spinning = False
        self.canvas.itemconfig(self.btn_bg, fill="#d32f2f")

    def animar(self, pasos_restantes):
        if pasos_restantes > 0:
            random_anime = random.choice(self.lista_animes)
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
        
        display_text = self.current_winner
        if len(self.current_winner) > 20:
             mid = len(self.current_winner) // 2
             split_idx = self.current_winner.find(' ', mid)
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
