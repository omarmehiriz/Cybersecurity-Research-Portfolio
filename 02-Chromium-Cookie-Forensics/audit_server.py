import socket, json

def start_audit_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 4444))
    s.listen(1)
    
    print("====================================================")
    print("  SECURITY AUDIT SERVER - SESSION INTEGRITY CHECK  ")
    print("====================================================")
    print("[*] Listening for local nodes on port 4444...")

    conn, addr = s.accept()
    print(f"[+] Audit node connected: {addr}")

    while True:
        cmd = input("\nAudit Console >> ").strip().lower()
        if not cmd: continue
        conn.send(cmd.encode())
        
        if cmd == "start_audit":
            print("[*] Receiving encrypted session telemetry...")
            all_entries = []
            f = conn.makefile('r', encoding='utf-8')
            
            while True:
                line = f.readline()
                if not line or "EOF_METADATA" in line: break
                try:
                    all_entries.append(json.loads(line))
                except: continue
            
            with open("audit_session_report.json", "w", encoding="utf-8") as out:
                json.dump(all_entries, out, indent=4)
            print(f"[ SUCCESS ] {len(all_entries)} metadata entries saved to report.")
            
        elif cmd == "exit":
            break

if __name__ == "__main__":
    start_audit_server()