import time
import psutil
import pygetwindow as gw
from plyer import notification

#Creamos un diccionario
PALABRAS_CLAVE_VIGILADAS = {
    #Paginas a las cuales el Bot va reaccionar
    "youtube": "Otra vez entrando a youtube? Música o Asmr? :)",
    "github": "¡Eso es!... VAMOS A PROGRAMAR!!!!!",
    "gemini": "Consultar a la IA trae sus pros y contras ¡NO DEPENDENCIA!",
    "chrome": "Cuidado vayas a otro lado :/"
}

print("🤖 Iniciando sistemas... Vigilando tu PC.")

# Diccionario para recordar qué apps ya estaban abiertas (para no repetir notificaciones)
estado_palabras = {clave: False for clave in PALABRAS_CLAVE_VIGILADAS.keys()}

while True:
    try:
        ventanas_activas = [w.title.lower() for w in gw.getAllWindows() if w.title]

        for palabra, mensaje in PALABRAS_CLAVE_VIGILADAS.items():
            encontrado = any(palabra in titulo for titulo in ventanas_activas)

            if encontrado and not estado_palabras[palabra]:
                notification.notify(
                    title = "Tu Mini Bot 🤖",
                    message = mensaje,
                    timeout=4
                )
                print(f"[Alerta Web/App] Detectado: {palabra.upper()}")
                estado_palabras[palabra] = True
            elif not encontrado and estado_palabras[palabra]:
                estado_palabras[palabra] = False
        time.sleep(3)
    except KeyboardInterrupt:
        print("\n🤖 [Bot Companion]: Apagándose... ¡Nos vemos!")
        break