import psutil
import time
import os

# Authorized ports
WHITELIST = [22, 80, 1716]

def run_monitor():
    print("IPS Monitor Active - Monitoring network processes...")
    
    current_pid = os.getpid()

    try:
        while True:
            # Get current network connections
            connections = psutil.net_connections()
            for conn in connections:
                # Check for unauthorized LISTEN ports
                if conn.status == 'LISTEN' and conn.laddr.port not in WHITELIST:
                    port = conn.laddr.port
                    pid = conn.pid
                    
                    # Avoid self-termination
                    if pid == current_pid:
                        continue
                        
                    try:
                        proc = psutil.Process(pid)
                        print(f"\n[!] Alert: Unauthorized port {port} detected")
                        print(f"[*] Process: {proc.name()} | Path: {proc.exe()}")
                        
                        # Kill suspicious process
                        print(f"[*] Killing PID {pid}...")
                        proc.kill() 
                        print(f"[+] Success: Port {port} closed.")
                        
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                    except Exception as e:
                        print(f"[-] Error: {e}")
            
            # Wait 2 seconds before next check
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nStopping monitor...")

if __name__ == "__main__":
    run_monitor()
