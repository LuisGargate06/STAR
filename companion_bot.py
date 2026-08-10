import time
import threading
import pygetwindow as gw
import tkinter as tk

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
        self.root.geometry("260x90+20+800")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        #Transparencia
        COLOR_TRANSPARENTE = "#000001"
        self.root.wm_attributes("-transparentcolor", COLOR_TRANSPARENTE)
        self.root.config(bg=COLOR_TRANSPARENTE)

        #Elementos visuales

        self.burbuja = tk.Frame(root, bg="#1e1e2e", bd=0, highlightbackground="#3b4252", highlightthickness=2)
        self.burbuja.pack(fill="both", expand=True, padx=5, pady=5)

        self.lbl_avatar = tk.Label(self.burbuja, text="🤖", font=("Arial", 16, "bold"), fg="#89b4fa", bg="#1e1e2e")
        self.lbl_avatar.pack(side="left", padx=(10,5), pady=10)

        frame_texto = tk.Frame(self.burbuja, bg="#1e1e2e")
        frame_texto.pack(side="left", fill="both", expand=True, pady=5)

        self.lbl_titulo = tk.Label(frame_texto, text="MiniBot dice:", font=("Arial", 8, "bold"), fg="#74c7ec", bg="#1e1e2e")
        self.lbl_titulo.pack(anchor="w")

        self.lbl_mensaje = tk.Label(frame_texto, text="Iniciando sistemas...", font=("Arial", 9), fg="#cdd6f4", bg="#1e1e2e", wraplength=180, justify="left")
        self.lbl_mensaje.pack(anchor="w", pady=(2,0))

        btn_cerrar =tk.Button(root, text="✖", font=("Arial", 8), fg="#f38ba8", bg="#1e1e2e", bd=0, command=root.quit)
        btn_cerrar.pack(side="right", anchor="n", padx=5, pady=5)

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