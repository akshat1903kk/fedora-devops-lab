# Project Log – Fedora DevOps Lab

A chronological log of project milestones, key setup steps, and lessons learned.

> This file tracks the "when" and "what" of the project's history. For deep technical details on the "how" and "why," see `docs/teaching_insights.md`.

---

## ✅ Milestone 1: Core Server & Network Setup
* **Date:** 2025-10-28 (Approx)
* **Goal:** Establish a secure, accessible Fedora VM for the lab.
* **Actions:**
    * Installed base packages: `vim`, `git`, `curl`, `openssh-server`.
    * Enabled and started `sshd.service` to allow remote login.
    * Configured VirtualBox network mode to **Bridged Adapter**.
    * Opened `ssh` (22/tcp) in `firewalld` to allow access from the host.
* **Result:** Full SSH access to the VM (`ssh akshat@192.168.1.13`).
* **Reference:** See `docs/networking.md` for the full IP and firewall configuration.

---

## ✅ Milestone 2: Nginx Web Server
* **Date:** 2025-10-28
* **Goal:** Install and run the Nginx web server to act as the public-facing entry point.
* **Actions:**
    * Installed Nginx: `sudo dnf install nginx`.
    * Enabled and started `nginx.service`.
    * Opened `http` (80/tcp) and `https` (443/tcp) in `firewalld`.
* **Result:** Nginx default test page is visible at `http://192.168.1.13`.

---

## ✅ Milestone 3: Backend API & Reverse Proxy
* **Date:** 2025-10-29
* **Goal:** Deploy the "bare-metal" FastAPI application and proxy it behind Nginx.
* **Actions:**
    * Set up a Python virtual environment (`venv`) for the project.
    * Installed `fastapi` and `uvicorn`.
    * Opened custom port `8000/tcp` in `firewalld` for direct API testing.
    * Created `devops-lab-api.service` (a systemd unit) to run Uvicorn as a background service.
    * Created the Nginx config `dashboard.conf` (in `/etc/nginx/conf.d/`) to `proxy_pass` all requests for `/api/` to the local Uvicorn service (`http://127.0.0.1:8000`).
* **Result:** The API is live. Nginx serves as the single entry point, routing traffic to the correct backend service.

---

## ✅ Milestone 4: Key Troubleshooting & Lessons
* **Date:** 2025-10-29
* **Problem:** **502 Bad Gateway** from Nginx when accessing API routes.
* **Diagnosis:** Nginx was working, but it couldn't connect to the Uvicorn service.
* **Fix:** The `devops-lab-api.service` was not running. Used `systemctl status devops-lab-api` to check and `journalctl -u devops-lab-api -f` to find the error (a typo in the `ExecStart` path).
* **Lesson:** **A 502 error almost always means the *backend* is down.** Always check the status and logs of the upstream service (Uvicorn) before debugging the proxy (Nginx).

* **Problem:** API worked on the VM (`curl localhost:8000`) but not from the host browser.
* **Fix:** The firewall port wasn't open.
* **Lesson:** Remember to check all three layers of networking:
    1.  Is the service running? (`ss -tuln | grep 8000`)
    2.  Is the firewall open? (`sudo firewall-cmd --list-all`)
    3.  Is the VM network configured correctly? (`docs/networking.md`)

---

## ✅ Milestone 5: Documentation & Git
* **Date:** 2025-10-30
* **Goal:** Organize the project for maintainability and knowledge capture.
* **Actions:**
    * Initialized the Git repository and pushed to `akshat1903kk/fedora-devops-lab`.
    * Created the `/docs` directory.
    * Wrote `teaching_insights.md` as the central tech reference.
    * Wrote `networking.md` for IP/port tracking.
    * Wrote this `progress.md` file to log milestones.

---

## 🚧 Milestone 6: Frontend Application
* **Date:** (In Progress)
* **Goal:** Create the React + TypeScript frontend application.
* **Next Steps:**
    * [ ] Bootstrap the app: `npm create vite@latest frontend -- --template react-ts`.
    * [ ] Configure `vite.config.ts` to proxy `/api` calls to `http://192.168.1.13:8000` to solve CORS during development.
    * [ ] Build static assets: `npm run build`.
    * [ ] Update the `lab.conf` Nginx config to serve the static `dist/` folder and add the `try_files ... /index.html` rule for React Router.

---

## 📋 Milestone 7: Containerization with Podman
* **Date:** (Pending)
* **Goal:** Containerize the entire stack (Frontend + Backend) using Podman.
* **Next Steps:**
    * [ ] Write `backend/Dockerfile`.
    * [ ] Write `frontend/Dockerfile` using a multi-stage build.
    * [ ] Create a `compose.yml` to define and link both services.
    * [ ] Run the full stack with `podman-compose up -d`.
    * [ ] This will replace the "bare-metal" systemd services.

---

## 🚀 Next Steps (Roadmap)

See the "Roadmap" section in `docs/teaching_insights.md` for the full plan.

1.  **CI/CD:** Implement GitHub Actions.
2.  **Observability:** Integrate Prometheus & Grafana.
3.  **IaC:** Automate server setup with Ansible.
