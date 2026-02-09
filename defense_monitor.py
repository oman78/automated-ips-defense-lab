import psutil
import time
import os

# Port yang diperbolehkan
WHITELIST = [22, 80, 1716]

def run_monitor():
    print("IPS Monitor Active - Monitoring network processes...")

    try:
        while True:
            connections = psutil.net_connections()
            for conn in connections:
                # Cek port LISTEN yang tidak ada di whitelist
                if conn.status == 'LISTEN' and conn.laddr.port not in WHITELIST:
                    port = conn.laddr.port
                    pid = conn.pid
                    
                    try:
                        proc = psutil.Process(pid)
                        print(f"\n[!] Alert: Unauthorized port {port} detected")
                        print(f"[*] Process: {proc.name()} | Path: {proc.exe()}")
                        
                        # Kill proses mencurigakan
                        print(f"[*] Killing PID {pid}...")
                        proc.kill() 
                        print(f"[+] Success: Port {port} closed.")
                        
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                    except Exception as e:
                        print(f"[-] Error: {e}")
                        
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nStopping monitor...")

if __name__ == "__main__":
    run_monitor()
