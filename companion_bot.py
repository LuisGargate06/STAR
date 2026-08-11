import time
import threading
import pygetwindow as gw
import tkinter as tk
from PIL import Image, ImageTk

#Creamos un diccionario
PALABRAS_CLAVE_VIGILADAS = {
    #Paginas a las cuales el Bot va reaccionar
    "youtube": "Otra vez entrando a youtube? Música o Asmr? :)",
    "github": "¡Eso es!... VAMOS A PROGRAMAR!!!!!",
    "gemini": "Consultar a la IA trae sus pros y contras ¡NO DEPENDENCIA!",
    "chrome": "Bienvenido CRACK :)"
}

class BotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Bot 🤖")
        #Tamaño del MiniBot
        self.root.geometry("330x100+20+800")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        #Transparencia
        COLOR_TRANSPARENTE = "#000005"
        self.root.wm_attributes("-transparentcolor", COLOR_TRANSPARENTE)
        self.root.config(bg=COLOR_TRANSPARENTE)

        #Elementos visuales

        self.burbuja = tk.Frame(root, bg="#1e1e2e", bd=0, highlightbackground="#3b4252", highlightthickness=2)
        self.burbuja.pack(fill="both", expand=True, padx=5, pady=5)

        try:
            # 1. Cargamos la imagen original (asegúrate de tener 'robot.png' en la misma carpeta)
            raw_image = Image.open("spidey.png")
            
            # 2. Redimensionamos la imagen para que quepa en el widget (ej. 50x50 píxeles)
            resized_image = raw_image.resize((55, 55), Image.Resampling.LANCZOS)
            
            # 3. Convertimos la imagen redimensionada a un formato compatible con Tkinter
            self.robot_img = ImageTk.PhotoImage(resized_image)
            
            # 4. Creamos un label para mostrar la imagen
            self.lbl_img = tk.Label(self.burbuja, image=self.robot_img, bg="#1e1e2e", bd=0)
            self.lbl_img.pack(side="left", padx=(15, 5), pady=10)
            
        except FileNotFoundError:
            # Si no encuentra la imagen, pone un emoji de emergencia
            print("⚠️ Advertencia: No se encontró 'robot.png'. Usando emoji de respaldo.")
            self.lbl_fallback = tk.Label(self.burbuja, text="🤖", font=("Arial", 25), fg="#89b4fa", bg="#1e1e2e")
            self.lbl_fallback.pack(side="left", padx=(15, 5), pady=10)

        self.lbl_avatar = tk.Label(self.burbuja, text="🤖", font=("Arial", 16, "bold"), fg="#89b4fa", bg="#1e1e2e")
        self.lbl_avatar.pack(side="left", padx=(10,5), pady=10)

        frame_texto = tk.Frame(self.burbuja, bg="#1e1e2e")
        frame_texto.pack(side="left", fill="both", expand=True, pady=5)

        self.lbl_titulo = tk.Label(frame_texto, text="MiniBot dice:", font=("Arial", 8, "bold"), fg="#74c7ec", bg="#1e1e2e")
        self.lbl_titulo.pack(anchor="w")

        self.lbl_mensaje = tk.Label(frame_texto, text="Iniciando sistemas...", font=("Arial", 10), fg="#cdd6f4", bg="#1e1e2e", wraplength=210, justify="left")
        self.lbl_mensaje.pack(anchor="w", pady=(5,0))

        btn_cerrar =tk.Button(root, text="✖", font=("Arial", 8), fg="#f38ba8", bg="#1e1e2e", bd=0, command=root.quit)
        btn_cerrar.place(x=305, y=5)

    def actualizar_mensaje(self,texto):
        self.lbl_mensaje.config(text=texto)

# Diccionario para recordar qué apps ya estaban abiertas (para no repetir notificaciones)
def iniciar_vigilancia(app_gui):
    estado_palabras = {clave: False for clave in PALABRAS_CLAVE_VIGILADAS.keys()}

    while True:
        try:
            ventanas_activas = [w.title.lower() for w in gw.getAllWindows() if w.title]

            for palabra, mensaje in PALABRAS_CLAVE_VIGILADAS.items():
                encontrado = any(palabra in titulo for titulo in ventanas_activas)

                if encontrado and not estado_palabras[palabra]:
                #se manda el mensaje
                    app_gui.actualizar_mensaje(mensaje)
                    estado_palabras[palabra] = True
                elif not encontrado and estado_palabras[palabra]:
                    estado_palabras[palabra] = False
            time.sleep(3)
        except Exception:
            time.sleep(3)
#Ejecucion
if __name__ == "__main__":
    root = tk.Tk()
    app = BotApp(root)

    hilo_vigilancia = threading.Thread(target=iniciar_vigilancia, args=(app,), daemon=True)
    hilo_vigilancia.start()

    root.mainloop()