
# Tech Stack & Insights — Fedora DevOps Lab

A personal knowledge base and technical reference for the *Fedora DevOps Lab* project. This document details the "why," "how," and "what" of every tool in the stack.

> **Project Goal:** Transform a bare-metal Fedora Server into a fully automated, observable, and extensible DevOps environment — from secure system foundations to a live containerized full-stack application.
>
> **Learning Philosophy:** Build → Document → Automate → Share. Every command, failure, and fix becomes a reusable lesson.

---

## 📚 Contents
- 1 — **Core OS:** Fedora Linux (Systemd, DNF, Security)
- 2 — **Networking:** firewalld & VirtualBox
- 3 — **Web Server / Proxy:** Nginx
- 4 — **Backend API:** FastAPI + Uvicorn
- 5 — **Containerization:** Podman & Dockerfiles
- 6 — **Frontend App:** React + Vite + TypeScript
- 7 — **Workflow:** tmux (Terminal Multiplexer)
- 8 — **Methodology:** Git & Documentation Discipline
- 9 — **Case Studies:** Real-World Failure & Learning
- 10 — **Roadmap:** Next Steps
- **Appendices:** Tips, Service Units, Checklists

---

## 1. Core OS: Fedora Linux

The foundation of the lab. Chosen for its modern packages, Red Hat lineage, and strong security-first defaults (SELinux, firewalld).

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

## 2. Networking & Connectivity

Controls how the lab is (or isn't) exposed to the outside world.

**VirtualBox Common Modes (for lab VMs)**
* **NAT:** Isolated host-to-guest network. Requires port forwarding to expose services. Good for a secure default.
* **Bridged:** VM gets its own IP on the host's LAN. Useful when other devices on your network need to access the VM directly.

**firewalld Basics**
* **Concept:** Manages traffic using "zones" (e.g., `public`, `internal`). Rules are applied to zones.
* Open common services (HTTP/HTTPS):
    ```bash
    sudo firewall-cmd --add-service=http --permanent
    sudo firewall-cmd --add-service=https --permanent
    sudo firewall-cmd --reload
    ```
* Open a custom port (e.g., FastAPI on 8000):
    ```bash
    sudo firewall-cmd --add-port=8000/tcp --permanent
    sudo firewall-cmd --reload
    ```

**Troubleshooting Checklist (Networking)**
1.  **Is it listening?** `ss -tuln | grep 8000`
2.  **Where is it bound?** `127.0.0.1` (localhost only) or `0.0.0.0` (all interfaces)?
3.  **Is the firewall open?** `sudo firewall-cmd --list-all`
4.  **Is it the VM?** Check VM networking mode (NAT vs. Bridged).
5.  **Is it SELinux?** Check `sudo journalctl -t setroubleshoot`.

---

## 3. Web Server / Proxy: Nginx

The high-performance front door for all HTTP traffic.

**Role in this Lab:**
1.  **Static Server:** Serves the optimized React build (HTML, JS, CSS) from `/var/www/html`.
2.  **Reverse Proxy:** Forwards all requests starting with `/api/` to the backend FastAPI application (running on `127.0.0.1:8000`).

**Minimal Example: `/etc/nginx/conf.d/lab.conf`**
```nginx
server {
    listen 80;
    server_name _; # Listen on all hostnames

    # 1. Serve the static React frontend
    root /var/www/html;
    index index.html;

    location / {
        # Handles React Router (client-side routing)
        # Tries to find the file, then a directory, then falls back to index.html
        try_files $uri $uri/ /index.html;
    }

    # 2. Reverse proxy the backend API
    location /api/ {
        proxy_pass [http://127.0.0.1:8000/](http://127.0.0.1:8000/); # Note the trailing slash
        
        # Set headers to pass real client info to FastAPI
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
````

**Insight:** The `try_files $uri $uri/ /index.html;` line is **critical** for React. It ensures that if a user refreshes the page on a client-side route (e.g., `/dashboard`), Nginx doesn't try to find a file named `/dashboard` on the server, but instead serves `index.html`, letting React Router take over.

-----

## 4\. Backend API: FastAPI + Uvicorn

The Python-based API backbone, providing data to the frontend.

**Why this Stack?**

  * **FastAPI:** Extremely fast (async-first), built-in data validation (Pydantic), and automatic OpenAPI/Swagger docs (`/docs`).
  * **Uvicorn:** The high-performance ASGI server needed to run FastAPI.

**Minimal App: `src/main.py`**

```python
from fastapi import FastAPI

app = FastAPI(title="DevOps Lab API", version="0.1.0")

@app.get("/api/v1/status")
async def read_root():
    return {"status": "Fedora Lab API Live"}

@app.get("/api/v1/health")
async def health_check():
    return {"db": "connected", "cache": "healthy"}
```

**Running for Production (via systemd)**

  * **Do NOT use:** `uvicorn src.main:app --reload` (this is for development only).
  * **Do use:** A `systemd` service (see Appendix A) running Uvicorn workers.
  * **Bind:** The service should bind to `127.0.0.1:8000` since Nginx is on the *same machine* and acts as the proxy. There is no need to expose Uvicorn publicly.

**Common Issue: 502 Bad Gateway**

  * **Symptom:** Nginx returns 502 for `/api/` routes, but static files work.
  * **Meaning:** Nginx tried to forward the request to `http://127.0.0.1:8000` but couldn't connect.
  * **Causes:**
    1.  The Uvicorn service is not running (`systemctl status devops-lab-api`).
    2.  The service is running but failed (check `journalctl -u devops-lab-api -f`).
    3.  Uvicorn is bound to the wrong address (e.g., a different port).
  * **Lesson:** Always validate the backend independently (`curl http://127.0.0.1:8000/api/v1/health`) before debugging Nginx.

-----

## 5\. Containerization: Podman

The engine for building, sharing, and running applications in isolated environments.

**Why Podman?**

  * **Rootless:** Can be run by a non-root user, which is a massive security win.
  * **Daemon-less:** No central daemon (unlike Docker), reducing attack surface and complexity.
  * **Docker-Compatible:** The commands are aliased. `podman build` is the same as `docker build`. We can use `podman-compose` to run `docker-compose.yml` files.

**Key Concepts for this Project**

1.  **`Dockerfile`:** A text file with instructions to build a container image. We will have at least two:
      * **Backend Dockerfile:** Starts from a `python:3.11-slim` image, copies `src/` and `requirements.txt`, installs dependencies, and sets the `CMD` to run `uvicorn`.
      * **Frontend Dockerfile:** Uses a **multi-stage build**.
          * *Stage 1 (Build):* Uses a `node:18` image, copies `package.json`, runs `npm install`, copies source code, and runs `npm run build`.
          * *Stage 2 (Serve):* Starts from a clean `nginx:alpine` image and *only* copies the `dist/` folder (static assets) from *Stage 1*. This results in a tiny, secure production image.
2.  **`podman-compose.yml`:** A YAML file that defines and runs multi-container applications. This will replace our manual `systemd` services. It will define:
      * A `backend` service (built from the backend Dockerfile).
      * A `frontend` service (built from the frontend Dockerfile, running Nginx).
      * A network to link them.
      * Port mapping (e.g., map port 80 on the host to port 80 in the `frontend` container).

**Key Commands**

| Command | Purpose |
|------|---------|
| `podman build -t my-api .` | Build an image from a `Dockerfile` in the current dir. |
| `podman images` | List all local images. |
| `podman run -d -p 8080:80 --name web my-frontend-img` | Run an image, detach, map host port 8080 to container 80. |
| `podman ps` | List running containers. |
| `podman logs -f web` | Follow the logs of the "web" container. |
| `podman-compose up -d` | Build and start all services in `docker-compose.yml`. |
| `podman-compose down` | Stop and remove all services. |

-----

## 6\. Frontend App: React + Vite + TypeScript

The modern, interactive user interface for the lab.

**Why this Stack?**

  * **React:** Component-based UI library for building complex, stateful interfaces.
  * **Vite:** A build tool and dev server. Provides blazing-fast Hot Module Replacement (HMR) for development and an optimized build for production.
  * **TypeScript:** A superset of JavaScript that adds static types. Catches countless bugs at compile-time *before* they hit production.

**Key Concepts & Files**

  * **`vite.config.ts`:** The heart of the Vite setup. We use this to configure the **dev server proxy**.
    ```typescript
    // vite.config.ts
    import { defineConfig } from 'vite'
    import react from '@vitejs/plugin-react'

    export default defineConfig({
      plugins: [react()],
      server: {
        proxy: {
          // Proxy all /api requests to our backend
          '/api': {
            target: '[http://127.0.0.1:8000](http://127.0.0.1:8000)', // Our Fedora API
            changeOrigin: true,
            secure: false,
          }
        }
      }
    })
    ```
  * **`npm run dev`:** Starts the Vite dev server. The proxy config above forwards API calls, solving CORS issues during development.
  * **`npm run build`:** Bundles and minifies all TS/React code into a static `dist/` folder (HTML, JS, CSS). **This `dist` folder is what Nginx serves in production.**
  * **React Router:** Handles client-side routing (e.g., `/dashboard`, `/settings`). This is why the Nginx `try_files` rule is so important.

-----

## 7\. Workflow: tmux

A terminal multiplexer. It lets you run and manage multiple terminal sessions and panes within a single window, and they persist even if you disconnect.

**Why tmux?**

  * **Persistence:** Start a build or server, detach (`Ctrl+b d`), log off. Log back in later, attach (`tmux a`), and it's still running.
  * **Panes:** Split your window into multiple panes.
  * **Workspaces:** A perfect "DevOps Dashboard" for this lab.

**Essential Quick Commands**

  * `tmux new -s <name>`: Start a new named session (e.g., `tmux new -s devops-lab`).
  * `tmux ls`: List running sessions.
  * `tmux attach -t <name>`: Attach to a session.
  * `Ctrl+b d`: Detach from the current session.
  * `Ctrl+b %`: Split pane vertically.
  * `Ctrl+b "`: Split pane horizontally.
  * `Ctrl+b <arrow keys>`: Navigate between panes.

**Example Workspace Panes**

  * **Pane 1 (Logs):** `sudo journalctl -u nginx -u devops-lab-api -f`
  * **Pane 2 (Server):** `ps aux | grep uvicorn` or `htop`
  * **Pane 3 (Code):** `vim src/main.py`
  * **Pane 4 (Shell):** `git status` or running `curl` tests.

-----

## 8\. Methodology: Git & Documentation Discipline

If it's not in Git, it doesn't exist. This doc is proof of that philosophy.

**Project Layout**

```
fedora-devops-lab/
├── README.md
├── docs/                     # This file and progress logs
│   ├── progress.md
│   └── teaching_insights.md
├── backend/                  # The FastAPI source
│   ├── src/
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                 # The React+Vite source
│   ├── public/
│   ├── src/
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.ts
├── .github/                  # (Future) GitHub Actions workflows
│   └── workflows/
│       └── ci.yml
├── compose.yml               # (Future) Replaces docker-compose.yml
└── configs/                  # Nginx configs, systemd units
    ├── nginx.conf
    └── devops-lab-api.service
```

**Best Practices**

  * **Commit Types:** Use conventional commits (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`). It makes the log readable.
  * **Branches:** `main` is for stable, deployed code. `develop` is the integration branch. `feat/<name>` for new work.
  * **Docs-Driven:** Update the docs *as* you make the change, or immediately after. Don't leave it for "later."

-----

## 9\. Case Studies (Failure → Learning)

  * **Case 1: 502 Bad Gateway**

      * **Symptom:** Nginx returns 502 for `/api/` routes.
      * **Diagnosis:** Uvicorn service was not running. `systemctl start` failed because of a typo in the `.service` file.
      * **Lesson:** `systemctl status` is good, but `journalctl -u <service>` is where the *real* error messages are.

  * **Case 2: Firewall Block**

      * **Symptom:** `curl localhost:8000` worked on the VM, but browser couldn't connect from host machine.
      * **Diagnosis:** `firewalld` was blocking the port. `ss -tuln` showed it listening, but `firewall-cmd --list-all` did not show port 8000.
      * **Lesson:** There are 3 layers to check: 1. Is the service running? 2. Is the firewall blocking? 3. Is the VM network (NAT) forwarding?

  * **Case 3: React 404 on Refresh**

      * **Symptom:** React app loaded, but refreshing on `/dashboard` gave an Nginx 404.
      * **Diagnosis:** Nginx `location /` block was missing the `try_files ... /index.html` fallback.
      * **Lesson:** Nginx must be configured to support client-side routing by redirecting all "not found" requests to the main `index.html`.

-----

## 10\. Roadmap: Next Steps

With the core stack (OS, Nginx, API, Frontend, Containers) documented, the next steps focus on automation and observability.

  * **CI/CD:** Create a GitHub Actions workflow (`.github/workflows/ci.yml`) that automatically:

    1.  Lints and tests the Python and TypeScript code.
    2.  Builds the container images.
    3.  Pushes images to a registry (GitHub Container Registry).
    4.  (Future) SSHs into the server and runs `podman-compose pull && podman-compose up -d` to deploy.

  * **Observability:** Integrate the **Prometheus & Grafana** stack.

    1.  **Prometheus:** A time-series database to *scrape* metrics (e.g., Nginx requests, FastAPI response times, system CPU/RAM).
    2.  **Grafana:** A dashboard to *visualize* the data collected by Prometheus.

  * **Infrastructure as Code (IaC):**

    1.  **Ansible:** Create a playbook that automates the *entire setup* of a new Fedora server (installing `dnf` packages, configuring `firewalld`, setting up `systemd` services, or deploying `podman-compose`).

-----

## Appendix A — Example systemd unit for Uvicorn (Bare Metal)

*Note: This is for a "bare-metal" install. This will be replaced by `podman-compose`.*

```ini
# /etc/systemd/system/devops-lab-api.service
[Unit]
Description=DevOps Lab FastAPI (Uvicorn)
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/srv/devops-lab/backend
Environment="PATH=/srv/devops-lab/backend/venv/bin"
ExecStart=/srv/devops-lab/backend/venv/bin/uvicorn src.main:app --host 127.0.0.1 --port 8000 --workers 2
Restart=on-failure
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

  * **To use:** `sudo systemctl daemon-reload` -\> `sudo systemctl enable --now devops-lab-api`

## Appendix B — Quick Troubleshooting Checklist

1.  **Client (Browser):** Check DevTools (Network tab). Is it a `404`, `502`, or `CORS` error?
2.  **Nginx (Proxy):** Check `sudo journalctl -u nginx -f` and `/var/log/nginx/error.log`. Is the `proxy_pass` URL correct? Is `nginx -t` happy?
3.  **FastAPI (App):** Check `sudo journalctl -u devops-lab-api -f` (or `podman logs -f <api_container>`). Is the app crashing on startup?
4.  **Firewall (OS):** Check `sudo firewall-cmd --list-all`. Is the port open?
5.  **SELinux (OS):** Check `sudo journalctl -t setroubleshoot`. Is SELinux blocking Nginx from proxying or Podman from mounting volumes?
6.  **Network (VM):** Check `ss -tuln | grep <port>`. Is the service bound to `127.0.0.1` when it should be `0.0.0.0`?

-----

Last Updated: 2025-10-30
Repo: akshat1903kk/fedora-devops-lab
