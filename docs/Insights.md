# Tech Stack & Insights — Fedora DevOps Lab

A personal knowledge base and technical reference for the *Fedora DevOps Lab* project. This document details the "why," "how," and "what" of every tool in the stack.

> **Project Goal:** Build, deploy, and automate a full-stack application using professional DevOps tools. This project uses two distinct environments:
> 1.  **Fedora VM (Dev Lab):** A sandboxed environment for testing heavy-duty tools (Podman, `firewalld`, SELinux, Ansible).
> 2.  **Android + Termux (Prod Server):** A 24/7, low-power, "always-on" server for hosting the live, secured application.

> **Learning Philosophy:** Build → Document → Automate → Share. Every command, failure, and fix becomes a reusable lesson.

---

## 📚 Contents
- 1 — **Core OS 1:** Fedora Linux (The Dev Lab)
- 2 — **Core OS 2:** Android + Termux (The Prod Server)
- 3 — **Networking:** `firewalld` (Fedora) vs. Termux (Android)
- 4 — **Web Server / Proxy:** Nginx (with SSL)
- 5 — **Containerization:** Podman & Dockerfiles (Fedora Lab)
- 6 — **Backend API:** FastAPI + Uvicorn
- 7 — **Frontend App:** React + Vite + TypeScript
- 8 — **CI/CD:** GitHub Actions (The "Agents")
- 9 — **Workflow:** tmux (Terminal Multiplexer)
- 10 — **Methodology:** Git & Documentation Discipline
- 11 — **Case Studies:** Real-World Failure & Learning
- 12 — **Roadmap:** Next Steps
- 13 — **Project Log (Milestones)**
- 14 — **Networking Reference (IP Map)**
- **Appendices:** Tips, Service Units, Checklists

---

## 1. Core OS 1: Fedora Linux (The Dev Lab)

The foundation of the lab. Chosen for its modern packages, Red Hat lineage, and strong security-first defaults (SELinux, firewalld). **This is the "heavy" environment for testing and learning corporate-level tools.**

**Key Tools & Commands**

| Tool | Purpose | Common Commands |
|------|---------|-----------------|
| `dnf` | Package Manager | `sudo dnf update && sudo dnf install <pkg>` |
| `systemctl` | Service/Unit Control (Systemd) | `sudo systemctl start\|stop\|enable --now <service>` |
| `journalctl` | System Log (Journal) Query | `sudo journalctl -u <service> -f --since "10m ago"` |
| `semanage` | SELinux Policy Management | `sudo semanage fcontext -a -t httpd_sys_content_t "/srv/www(/.*)?"` |
| `restorecon` | Apply SELinux Context | `sudo restorecon -Rv /srv/www` |
| `firewall-cmd` | firewalld Management | `sudo firewall-cmd --add-port=8000/tcp --permanent` |

**Insight:** `systemd` is more than an init system; it manages services, timers, and logs. Use `systemctl status <service>` to see the full picture (logs, cgroup, status) before defaulting to `journalctl`.

---

## 2. Core OS 2: Android + Termux (The Prod Server)

The "always-on," low-power production server (Realme 3i). It uses the **Termux** environment on top of Android.

**Why Termux?**
* **Low Power:** Runs 24/7 for a fraction of a PC's energy cost.
* **Built-in UPS:** The phone battery acts as an Uninterruptible Power Supply.
* **Native Tools:** Provides a full Linux-like environment with `pkg` for installing `nginx`, `python`, `git`, etc.

**Critical Setup Steps**
1.  **Install from F-Droid:** The *only* supported version is from the F-Droid app store. The Play Store version is obsolete.
2.  **Disable Battery Optimization:** Go to **App Info > Battery > Set to "Unrestricted"**. This is essential to prevent Android from killing Termux.
3.  **Run `termux-wake-lock`:** In a dedicated session to prevent the phone's CPU from sleeping.
4.  **Install `sshd`:** Run `pkg install openssh` and `sshd` to enable remote login from a PC (default port `8022`).

**Key Tools & Commands**

| Tool | Purpose | Common Commands |
|------|---------|-----------------|
| `pkg` | Package Manager | `pkg install <pkg>` or `pkg update` |
| `sshd` | SSH Server | `sshd` (Starts the server on port 8022) |
| `passwd` | User Password | `passwd` (Sets the password for SSH login) |
| `ip addr show wlan0` | Find IP | Shows the phone's local IP address. |
| `whoami` | Find User | Shows the Termux user (e.g., `u0_a202`). |
| `termux-wake-lock` | Keep Alive | Prevents Android from sleeping the CPU. |

---

## 3. Networking: `firewalld` vs. Termux

This project has two different networking and security models.

* **Fedora VM (`firewalld`):**
    A professional, kernel-level firewall. All ports are **closed by default**. We must explicitly open them.
    ```bash
    # Example: Open port 8080 for our Podman container
    sudo firewall-cmd --add-port=8080/tcp --permanent
    sudo firewall-cmd --reload
    ```

* **Android/Termux (No `firewalld`):**
    Termux is an *app*, not an OS. It cannot control the phone's kernel-level firewall. Security is handled differently:
    1.  **Android OS:** By default, the Android firewall blocks all incoming connections.
    2.  **Termux Apps:** When you run `sshd` or `nginx`, they bind to a port (e.g., `8022`, `443`), opening it *only* for the Termux app.
    3.  **Our Security:** Our security comes from **Nginx** (using SSL) and **SSH** (using a strong password or keys).

---

## 4. Web Server / Proxy: Nginx (with SSL)

Nginx serves two roles: a static server for React and a reverse proxy for the FastAPI API.

### Config 1: Fedora Lab (HTTP Reverse Proxy)

This is a simple config for *testing* in the lab.
```nginx
# /etc/nginx/conf.d/lab.conf
server {
    listen 80;
    server_name _;

    location /api/ {
        # Proxies to the Podman container's mapped port
        proxy_pass [http://127.0.0.1:8080/](http://127.0.0.1:8080/); 
        ...
    }
}
```


Config 2: Termux Prod (Secure HTTPS Proxy)This is the production config. It redirects all insecure HTTP traffic to HTTPS and serves the API over an encrypted connection.A) Create a Self-Signed SSL Certificate:Bash# Install openssl
pkg install openssl

# Go to nginx config directory and make a folder
cd $PREFIX/etc/nginx
mkdir ssl
cd ssl

# Create the key and cert
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
B) Configure nginx.conf:Nginx# $PREFIX/etc/nginx/nginx.conf

# This block redirects all insecure http:// traffic to https://
server {
    listen 80;
    server_name 192.168.1.13; # Your phone's static IP
    return 301 https://$host$request_uri;
}

# This is the main, secure server
server {
    listen 443 ssl;
    server_name 192.168.1.13; # Your phone's static IP

    # --- SSL Certificate Paths ---
    ssl_certificate      $PREFIX/etc/nginx/ssl/cert.pem;
    ssl_certificate_key  $PREFIX/etc/nginx/ssl/key.pem;

    # (React frontend config would go here)
    # location / { ... }

    # --- API Reverse Proxy ---
    location /api/ {
        # Passes to the Uvicorn app running locally
        proxy_pass [http://127.0.0.1:8000](http://127.0.0.1:8000);
        
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

To use: Test with nginx -t and restart with nginx -s reload.

You are right, that image shows a bad formatting error. It looks like a copy-paste or rendering issue where all the line breaks and Markdown syntax were stripped out, turning everything into a single, unreadable block of text.The file I sent was complete, but it seems to have gotten corrupted on your end.Let's fix this. Here is the rest of the file (starting from Section 5), properly formatted in a new code block. You can use this to replace the broken part.Markdown---

## 5. Containerization: Podman (Fedora Lab)

This technology is used **exclusively in the Fedora VM Lab**. It allows us to build and run our applications in isolated, professional-grade environments.

* **Why Podman?** Rootless, daemon-less, and Docker-compatible.
* **Key Concept:** We have a `Dockerfile` for the backend that is automatically built by our GitHub Actions agent (see Section 8).

| Command | Purpose |
|------|---------|
| `podman build -t my-api .` | Build an image from a `Dockerfile`. |
| `podman ps` | List running containers. |
| `podman run -d -p 8080:8000 --name fedora-api my-api` | Run the API, mapping host port 8080 to container 8000. |

---

## 6. Backend API: FastAPI + Uvicorn

The Python-based API backbone. The *same* code runs on both the Fedora container and the Termux server.

* **Why?** Fast, modern, and has automatic data validation.
* **Run Command (Termux):**
    ```bash
    # From inside the backend directory
    uvicorn app.main:app --host 127.0.0.1 --port 8000
    ```
    *We bind to `127.0.0.1` (localhost) because only Nginx needs to talk to it. Nginx handles all public-facing traffic.*

---

## 7. Frontend App: React + Vite + TypeScript

The modern UI for the lab. This is built on a local dev machine and the *output* is deployed.

* **`npm run dev`:** Starts the local dev server. The `vite.config.ts` proxies `/api` requests to the active server (either the VM or the phone).
* **`npm run build`:** Creates the static `dist/` folder. This folder is what will eventually be copied to our server and served by Nginx.

---

## 8. CI/CD: GitHub Actions (The "Agents")

This is our automated "agent" pipeline. It lives in the `.github/workflows/` directory and runs on every `git push` to ensure code quality and build integrity.

### Workflow 1: `lint.yml` (Code Quality)

This agent checks for style errors in both Python and React code.
```yaml
name: Code Quality Linter

on:
  push:
    branches: ["main", "tests"]
  pull_request:
    branches: ["main"]

jobs:
  backend-lint:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./dashboard/backend
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install black
      - run: black --check .

  frontend-lint:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./dashboard/frontend
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run lint
```
Workflow 2: build.yml (Container Build)This agent test-builds the backend Dockerfile to ensure it's not broken.YAMLname: Build Container Image

on:
  push:
    branches: ["main", "tests"]
  pull_request:
    branches: ["main"]

jobs:
  build-backend-image:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./dashboard/backend
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-qemu-action@v3
      - run: |
          sudo apt-get update
          sudo apt-get -y install podman
      - name: Build the image
        run: podman build -t my-test-image .

---

## 9. Workflow: tmux

A terminal multiplexer. Essential for the Termux server to keep processes running in the background.

* **Use Case:**
    * **Session 1:** Run `termux-wake-lock`.
    * **Session 2:** Run the `uvicorn` server.
    * **Session 3:** Run `nginx`.
    * **Session 4:** Open a shell for `git pull` or monitoring.
* **Commands:**
    * `tmux new -s <name>`: Start a new session.
    * `Ctrl+b d`: Detach (and keep processes running).
    * `tmux a -t <name>`: Re-attach to a session.

---

## 10. Methodology: Git & Documentation Discipline

If it's not in Git, it doesn't exist.

**Project Layout (Updated)**
fedora-devops-lab/ ├── .github/ # <-- NEW! GitHub Actions │ └── workflows/ │ ├── lint.yml │ └── build.yml ├── dashboard/ │ ├── backend/ │ │ ├── app/ │ │ │ └── main.py │ │ ├── Dockerfile │ │ └── requirements.txt │ └── frontend/ │ ├── src/ │ ├── package.json │ └── vite.config.ts ├── docs/ # Documentation │ ├── progress.md │ ├── networking.md │ └── teaching_insights.md (This file) └── README.md


---

## 11. Case Studies (Failure → Learning)

* **Case 1: `connect ETIMEDOUT 192.168.1.13:80`**
    * **Symptom:** React app "failed to fetch" from the VM.
    * **Diagnosis:** The `vite.config.ts` proxy was pointing to port `80` (Nginx) but the new Podman container was on port `8080`.
    * **Lesson:** The frontend proxy must *always* point to the correct **host port** that the backend service is *exposed on*.

* **Case 2: GitHub Actions `lint.yml` Fails**
    * **Symptom:** The "Code Quality" agent failed with an error: `2 files would be reformatted`.
    * **Diagnosis:** This was a **success!** The agent correctly found Python files that did not follow the `black` style guide.
    * **Fix:** Run `black .` locally, commit the formatted files, and push again.

* **Case 3: Termux App Fails (Wrong Install)**
    * **Symptom:** "ReTerminal" app failed to install with `ENOENT` error.
    * **Diagnosis:** Installed the wrong app.
    * **Lesson:** The *only* supported version of Termux is from **F-Droid**.

---

## 12. Roadmap: Next Steps

* **1. Finalize Android Server (Immediate):**
    * [ ] Assign a **Static IP** to the phone via the router's settings.
    * [ ] Use `tmux` to run `sshd`, `nginx`, and `uvicorn` persistently.
    * [ ] Deploy the `dist/` folder from the frontend build to Nginx.

* **2. Observability (Fedora Lab):**
    * Integrate the **Prometheus & Grafana** stack (in containers).
    * Scrape metrics from the FastAPI container.

* **3. Infrastructure as Code (IaC) (Fedora Lab):**
    * Write an **Ansible Playbook** to automate the *entire* Fedora VM setup (install Podman, configure `firewalld`, clone repo, run `podman-compose`).

---

## 13. Project Log (Milestones)

A chronological log of project milestones, key setup steps, and lessons learned. This project now uses two server environments:

1.  **Fedora VM Lab:** The primary development/testing lab for heavy-duty tools (Podman, Ansible).
2.  **Android Server:** A 24/7, low-power "production" server for hosting the live API.

---

### ✅ Milestone 1: Core Fedora VM & Network Setup
* **Goal:** Establish a secure, accessible Fedora VM for the lab.
* **Actions:**
    * Installed Fedora Server in VirtualBox, configured Bridged Networking.
    * Opened `ssh`, `http`, `https` ports in `firewalld`.
    * Configured GitHub SSH keys (`id_ed25519`) for the VM.
* **Result:** Full SSH access and a base environment for container testing.

### ✅ Milestone 2: Backend API (Containerized)
* **Goal:** Containerize the FastAPI backend.
* **Actions:**
    * Wrote a `Dockerfile` for the Python API.
    * Built the image with `podman build`.
    * Ran the container, mapping host port `8080` to container port `8000`.
* **Result:** A portable, isolated backend service (`fedora-api`).

### ✅ Milestone 3: Frontend Setup (Local Dev)
* **Goal:** Create the React + TypeScript frontend.
* **Actions:**
    * Bootstrapped the app with `npm create vite@latest`.
    * Configured `vite.config.ts` to proxy `/api` requests to the Fedora VM (`http://192.168.1.13:8080`).
* **Result:** Successful local development with a live connection to the backend.

### ✅ Milestone 4: CI/CD Pipeline (GitHub Actions)
* **Date:** 2025-11-01
* **Goal:** Automate code quality and build validation.
* **Actions:**
    * Created a `tests` branch to work on CI.
    * Created `.github/workflows/lint.yml` to run `black --check` (Python) and `npm run lint` (React) on every push.
    * Created `.github/workflows/build.yml` to automatically test-build the backend `Dockerfile` using `podman build`.
* **Result:** A full CI pipeline that provides automatic quality checks on all new code.

### ✅ Milestone 5: Android 24/7 Server Setup
* **Date:** 2025-11-01
* **Goal:** Create an "always-on," low-power server using a spare Realme 3i phone.
* **Actions:**
    * Installed **Termux** from F-Droid (the only supported version).
    * Disabled battery optimization for Termux (set to "Unrestricted").
    * Installed `pkg install openssh python nginx git`.
    * Configured and started the `sshd` server on port `8022`.
    * Logged in from PC: `ssh u0_a202@192.168.1.13 -p 8022`.
* **Result:** A stable, 24/7 server that is now the primary host for the API.

### 🚧 Milestone 6: Deploy & Secure API on Android
* **Date:** (In Progress)
* **Goal:** Deploy the FastAPI app on the Termux server and secure it with HTTPS.
* **Next Steps:**
    * [x] Generate GitHub SSH keys *inside* Termux.
    * [x] Clone the repo to the phone.
    * [x] Install Python dependencies: `pip install -r requirements.txt`.
    * [ ] Generate a **self-signed SSL certificate** using `openssl`.
    * [ ] Configure `nginx.conf` in Termux to proxy `/api` to the Uvicorn service and use the SSL certificate (listen on port `443`).
    * [ ] Run the Uvicorn app.

---

## 14. Networking Reference (IP Map)

A central reference for all IP addresses, port mappings, and networking configurations.

This project uses two different server environments, which typically share the **same IP address** (`192.168.1.13`) on the network, but only one is run at a time.

---

### 📍 Server 1: Fedora VM (Heavy Dev Lab)

* **IP Address:** `192.168.1.13`
* **Environment:** VirtualBox VM (Bridged Adapter)
* **OS:** Fedora Server
* **Firewall:** `firewalld`
* **SSH Access:**
    * `ssh akshat@192.168.1.13` (Port 22)
* **Service Ports (Host):**
    * `80/tcp`: Nginx (for testing)
    * `8080/tcp`: Podman-mapped port for the containerized API.

### 📍 Server 2: Android Phone (24/7 Prod Server)

* **IP Address:** `192.168.1.13`
* **Environment:** Realme 3i (Real Hardware)
* **OS:** Android + Termux
* **Firewall:** Android OS (default)
* **SSH Access:**
    * `ssh u0_a202@19S.168.1.13 -p 8022` (Port 8022)
* **Service Ports (Host):**
    * `80/tcp`: Nginx (will be redirected to HTTPS)
    * `443/tcp`: Nginx with SSL (for the secure API)
    * `8000/tcp`: Uvicorn/FastAPI (for Nginx to proxy to)

### 🛠️ Key Commands (Termux)

| Command | Purpose |
| :--- | :--- |
| `ip addr show wlan0` | Find the phone's IP address. |
| `whoami` | Find the Termux username (e.g., `u0_a202`). |
| `passwd` | Set the SSH login password. |
| `sshd` | Start the SSHD server (on port 8022). |
| `termux-wake-lock` | **(CRITICAL)** Run in a session to prevent the phone from sleeping. |
| `nginx` | Start the Nginx server. |
| `nginx -s reload` | Reload the Nginx config after changes. |

---

## Appendix A — Fedora `systemd` unit for Uvicorn
*Note: This is for a "bare-metal" install on the Fedora VM. It is replaced by Podman.*
```ini
[Unit]
Description=DevOps Lab FastAPI
After=network.target
[Service]
...
ExecStart=/path/to/venv/bin/uvicorn src.main:app --host 127.0.0.1
...
[Install]
WantedBy=multi-user.target
```
---

## Appendix B — Quick Troubleshooting Checklist

- Which server am I on? (VM or Phone?)

- Client (Browser): Check DevTools (Network tab). Is it a 404, 502, or CORS error?

- Proxy (Nginx): Test the config with nginx -t. Check logs.

- App (Uvicorn): Is the process running? (ps aux | grep uvicorn or podman ps).

- Firewall (Fedora): Is the port open? (sudo firewall-cmd --list-all).

- Firewall (Android): Is the battery optimization disabled and termux-wake-lock running?
