#  Automated Process Monitor & System Defense Tool

### 1. Project Overview
This project is a practical demonstration of automating system defense. The goal was to build a script that can automatically detect and neutralize unauthorized network services in real-time. By utilizing existing containerized environments, I simulated a compromised host and developed a Python-based solution to maintain system integrity.

### 2. Lab Environment
To build a realistic testing scenario, I utilized the following resources:
* **Host:** Parrot Security OS (ARM64 Architecture).
* **Authorized Service:** I deployed pre-configured vulnerable images (such as DVWA) using **Docker** to simulate open services.
* **Intrusion Simulation:** I used Netcat (nc) to simulate unauthorized backdoor attempts and listener creation.
* **Environment:** All Python developments were managed within a dedicated **Virtual Environment (`venv3`)** to ensure dependency isolation.

### 3. The Problem
Manual monitoring of network ports using tools like `nmap` or `netstat` is effective but not scalable. In a real-world scenario, persistent threats (like backdoors or unauthorized remote access tools) need to be handled instantly before they can be exploited.

### 4. The Solution: Custom Defense Script
I developed a **Python Intrusion Prevention Script** designed to automate the "Detection to Mitigation" pipeline. 

**Key Technical Features:**
* **Real-time Auditing:** Continuously monitors the network stack for `LISTEN` states.
* **Whitelisting Logic:** Only allows pre-approved ports (e.g., Port 80 for Docker, Port 22 for SSH, and other system-critical ports).
* **Automated Mitigation:** Automatically traces the PID (Process ID) to its source binary and terminates the process to prevent further access.
* **Self-Preservation Logic:** Implemented PID filtering to prevent the script from terminating its own process during scanning.

### 5. How It Works
The script utilizes the `psutil` library to bridge the gap between network connections and system processes.

```python
# Part of the core monitoring loop:
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
```
### 6. Simulation & Demo
> **Note on Scenario:** In this simulation, DVWA (Damn Vulnerable Web Application) is deployed as a legitimate but vulnerable service on Port 80. The script is configured to whitelist Port 80, acknowledging it as an authorized service. The primary objective is to detect and neutralize any unauthorized backdoors (such as a Netcat listener on Port 4444) that might appear if the host is exploited.
[![Automated IPS Demo](https://img.youtube.com/vi/ediroLwLc-w/0.jpg)](https://www.youtube.com/watch?v=ediroLwLc-w)

*Click the image above to watch the full demonstration on YouTube (Available in 2K/4K).*

The demonstration follows a three-terminal workflow:
* **Terminal 1 (Defense):** Running the Python script within the venv3 environment.
* **Terminal 2 (Authorized Service):** Deploying the DVWA container. The script identifies the port but ignores it due to the whitelist.
* **Terminal 3 (Intrusion):** Opening an unauthorized Netcat listener (nc -l -p 4444). The script instantly detects the violation, logs the event, and terminates the process.


### 7. Summary of Results
The script successfully managed the security of the lab environment by:
  1. Identifying unauthorized listeners (e.g., nc backdoors and unauthorized services outside the whitelist).
  2. Differentiating between legitimate services (e.g., Docker DVWA on Port 80) and malicious intrusions.
  3. Neutralizing threats within seconds while providing real-time reporting of binary paths for forensic identification.
 


This project was developed for educational purposes in a controlled lab environment to explore system automation and defensive security principles.
