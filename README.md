#  Automated Process Monitor & System Defense Tool

### 1. Project Overview
This project is a practical demonstration of automating system defense. The goal was to build a script that can automatically detect and neutralize unauthorized network services in real-time. By utilizing existing containerized environments, I simulated a compromised host and developed a Python-based solution to maintain system integrity.

### 2. Lab Environment
To build a realistic testing scenario, I utilized the following resources:
* **Host:** Parrot Security OS (ARM64 Architecture).
* **Target:** I deployed pre-configured vulnerable images (such as DVWA) using **Docker** to simulate open services.
* **Environment:** All Python developments were managed within a dedicated **Virtual Environment (`venv3`)** to ensure dependency isolation.

### 3. The Problem
Manual monitoring of network ports using tools like `nmap` or `netstat` is effective but not scalable. In a real-world scenario, persistent threats (like backdoors or unauthorized remote access tools) need to be handled instantly before they can be exploited.

### 4. The Solution: Custom Defense Script
I developed a **Python Intrusion Prevention Script** designed to automate the "Detection to Mitigation" pipeline. 

**Key Technical Features:**
* **Real-time Auditing:** Continuously monitors the network stack for `LISTEN` states.
* **Whitelisting Logic:** Only allows pre-approved ports (e.g., Port 22 for SSH, Port 80 for Docker).
* **Automated Mitigation:** Automatically traces the PID (Process ID) to its source binary and terminates the process to prevent further access.
* **Self-Preservation Logic:** Implemented PID filtering to prevent the script from terminating its own process during scanning.

### 5. How It Works
The script utilizes the `psutil` library to bridge the gap between network connections and system processes.

```python
# Core logic: Check for LISTEN ports and avoid self-termination
current_pid = os.getpid()
connections = psutil.net_connections()

for conn in connections:
    if conn.status == 'LISTEN' and conn.laddr.port not in WHITELIST:
        if conn.pid == current_pid:
            continue
            
        # Kill suspicious process
        proc = psutil.Process(conn.pid)
        proc.kill()
```

### 6. Summary of Results
The script successfully managed the security of the lab environment by:
  1. Identifying unauthorized listeners (e.g., nc backdoors and unauthorized services outside the whitelist).
  2. Differentiating between legitimate services (e.g., Docker DVWA on Port 80) and malicious intrusions.
  3. Neutralizing threats within seconds and logging the binary paths for forensics.
 


This project was developed for educational purposes in a controlled lab environment to explore system automation and defensive security principles.
