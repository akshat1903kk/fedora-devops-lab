
# Networking Reference – Fedora DevOps Lab

A central reference for all IP addresses, port mappings, and networking configurations for the lab environment. This file tracks the "what" and "why" of the lab's connectivity.

---

## 📍 Current Lab Configuration

This is the "at-a-glance" setup for the project.

**IP Address Map**

| Device | IP Address | Purpose |
| :--- | :--- | :--- |
| **Fedora VM** | `192.168.1.13` | The Server. Hosts Nginx, Podman, and the API. |
| **Host Machine**| `192.168.1.125` | The "Client" machine (your main computer). |
| **Router** | `192.168.1.1` | Default gateway (for `ping` tests). |

**Service Access (from Host Machine's Browser)**

* **Nginx (Frontend):** `http://192.168.1.13`
* **FastAPI (Backend):** `http://192.168.1.13:8000` (Direct access for testing)
* **API via Nginx:** `http://192.168.1.13/api/v1/status` (Production path)

---

## 🌐 VirtualBox Networking

This section explains *how* the VM connects to the network.

**Current Mode: `Bridged Adapter`**
* **Adapter:** Intel PRO/1000 MT Desktop
* **Why this mode?** Bridged mode places the VM directly on the host's LAN (192.168.1.x). The VM gets its own IP address from the router, just like a real, physical server.
* **Benefit:** This is the most realistic setup. Any device on the network (your host, your phone, etc.) can access services running on the VM simply by using its IP (`192.168.1.13`), provided the firewall allows it.

**Comparison of VM Network Modes**

| Mode | How it Works | Use Case in this Lab |
| :--- | :--- | :--- |
| **Bridged** | VM gets its own IP from your router (e.g., `192.168.1.13`). | **(Currently Used)** Perfect for "production" testing. Host and other devices can access services just like a real server. |
| **NAT** | VM shares the host's IP. It's on a private, isolated network. | Good for basic setup. Requires "Port Forwarding" in VirtualBox settings to access VM services (e.g., map Host:8080 -> Guest:80). |
| **Host-Only** | Creates a private network *only* between the host and the VM. | Useful for secure services you *don't* want exposed to the LAN (e.g., a database), while the VM has a second (NAT) adapter for internet. |

---

## 🔥 firewalld (Fedora's Firewall)

This controls what traffic is allowed *into* the Fedora VM.

**Current Open Ports (in `public` zone)**
* `ssh` (port 22/tcp): For logging in via terminal.
* `http` (port 80/tcp): For the Nginx web server.
* `https` (port 443/tcp): Reserved for future SSL/TLS.
* `8000/tcp` (custom): For direct access to the FastAPI/Uvicorn service.

---

## 🛠️ Commands & Troubleshooting

A quick-reference for diagnosing network issues.

| Command | What It Does & What to Look For |
| :--- | :--- |
| `ip addr` | **Shows your VM's IP address.** Look for the `enp0s3` interface and its `inet` address (e.g., `192.168.1.13/24`). |
| `ping 192.168.1.1` | **Tests internet/LAN connectivity.** Pinging the router (`192.168.1.1`) or host (`192.168.1.125`) checks if the basic network layer is working. |
| `ss -tuln` | **Checks if your app is running.** This is the best command to see all *listening* ports. Use `ss -tuln \| grep 80` to check for Nginx or `ss -tuln \| grep 8000` for FastAPI. |
| `sudo firewall-cmd --list-all` | **Checks the firewall rules.** This is the *first* place to look if you can't connect. See if your port (e.g., `8000/tcp`) is listed under `ports:`. |
| `sudo firewall-cmd --add-port=8000/tcp --permanent` | **Opens a port.** The `--permanent` flag writes the change so it survives a reboot. |
| `sudo firewall-cmd --reload` | **Applies permanent changes.** You **must** run this after adding or removing a permanent rule for it to take effect. |
```
