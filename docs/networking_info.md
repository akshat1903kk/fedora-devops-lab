# Networking Reference – Fedora DevOps Lab

A central reference for all IP addresses, port mappings, and networking configurations.

This project now uses two different server environments. They may share the same IP address on your network, but they run at different times and have different SSH ports.

---

## 📍 Server 1: Fedora VM (Heavy Dev Lab)

* **IP Address:** `192.168.1.13`
* **Environment:** VirtualBox VM (Bridged Adapter)
* **OS:** Fedora Server
* **Firewall:** `firewalld`
* **SSH Access:**
    * `ssh akshat@192.168.1.13` (Port 22)
* **Service Ports (Host):**
    * `80/tcp`: Nginx (for testing)
    * `8080/tcp`: Podman-mapped port for the containerized API.

---

## 📍 Server 2: Android Phone (24/7 Prod Server)

* **IP Address:** `192.168.1.13` (or its current DHCP address)
* **Environment:** Realme 3i (Real Hardware)
* **OS:** Android + Termux
* **Firewall:** Android OS (default)
* **SSH Access:**
    * `ssh u0_a202@192.168.1.13 -p 8022` (Port 8022)
* **Service Ports (Host):**
    * `80/tcp`: Nginx (will be redirected to HTTPS)
    * `443/tcp`: Nginx with SSL (for the secure API)
    * `8000/tcp`: Uvicorn/FastAPI (for Nginx to proxy to)

---

## 🛠️ Key Commands & Troubleshooting

### Fedora VM

| Command | What It Does & What to Look For |
| :--- | :--- |
| `ip addr` | **Shows your VM's IP address.** Look for `inet 192.168.1.13...` |
| `ss -tuln` | **Checks listening ports.** Use `ss -tuln \| grep 8080` to check for Podman. |
| `sudo firewall-cmd --list-all` | **Checks firewall rules.** See if your port (e.g., `8080/tcp`) is listed. |
| `sudo firewall-cmd --add-port=8080/tcp --permanent` | **Opens a port.** |
| `sudo firewall-cmd --reload` | **Applies permanent changes.** |
| `podman ps` | **Checks running containers.** Ensure your API container is running. |

### Android (Termux)

| Command | What It Does & What to Look For |
| :--- | :--- |
| `ip addr show wlan0` | **Finds the phone's IP address.** |
| `whoami` | **Finds the Termux username** (e.g., `u0_a202`). |
| `passwd` | **Sets the SSH login password.** |
| `sshd` | **Starts the SSHD server** (on port 8022). |
| `termux-wake-lock` | **(CRITICAL)** Run in a session to prevent the phone from sleeping. |
| `nginx` | **Starts the Nginx server.** |
| `nginx -s reload` | **Reloads the Nginx config** after changes. |
| `nginx -t` | **Tests the Nginx config** for errors. |
