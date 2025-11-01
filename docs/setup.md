# Project Log – Fedora DevOps Lab

A chronological log of project milestones, key setup steps, and lessons learned. This project now uses two server environments:

1.  **Fedora VM Lab:** The primary development/testing lab for heavy-duty tools (Podman, Ansible).
2.  **Android Server:** A 24/7, low-power "production" server for hosting the live API.

> This file tracks the "when" and "what" of the project's history. For deep technical details on the "how" and "why," see the main `README.md` (or `teaching_insights.md`).

---

## ✅ Milestone 1: Core Fedora VM & Network Setup
* **Goal:** Establish a secure, accessible Fedora VM for the lab.
* **Actions:**
    * Installed Fedora Server in VirtualBox, configured Bridged Networking.
    * Opened `ssh`, `http`, `https` ports in `firewalld`.
    * Configured GitHub SSH keys (`id_ed25519`) for the VM.
* **Result:** Full SSH access and a base environment for container testing.

---

## ✅ Milestone 2: Backend API (Containerized)
* **Goal:** Containerize the FastAPI backend on the Fedora VM.
* **Actions:**
    * Wrote a `Dockerfile` for the Python API.
    * Built the image with `podman build -t my-backend-api .`.
    * Opened port `8080` in `firewalld`.
    * Ran the container, mapping host port `8080` to container port `8000`:
      `podman run -d --name fedora-api -p 8080:8000 my-backend-api`
* **Result:** A portable, isolated backend service accessible at `http://192.168.1.13:8080`.

---

## ✅ Milestone 3: Frontend Setup (Local Dev)
* **Goal:** Create the React + TypeScript frontend and connect it to the VM.
* **Actions:**
    * Bootstrapped the app with `npm create vite@latest frontend`.
    * Configured `vite.config.ts` to proxy `/api` requests to the Fedora VM's container: `target: 'http://192.168.1.13:8080'`.
* **Result:** Successful local development with the React app fetching live data from the containerized backend.

---

## ✅ Milestone 4: CI/CD Pipeline (GitHub Actions)
* **Date:** 2025-11-01
* **Goal:** Automate code quality and build validation.
* **Actions:**
    * Created a `tests` branch to work on CI.
    * Created `.github/workflows/lint.yml` to run `black --check` (Python) and `npm run lint` (React) on every push.
    * Created `.github/workflows/build.yml` to automatically test-build the backend `Dockerfile` using `podman build`.
* **Result:** A full CI pipeline that provides automatic quality checks on all new code.

---

## ✅ Milestone 5: Android 24/7 Server Setup
* **Date:** 2025-11-01
* **Goal:** Create an "always-on," low-power server using a spare Realme 3i phone.
* **Actions:**
    * Installed **Termux** from F-Droid (the only supported version).
    * Disabled battery optimization for Termux (set to "Unrestricted").
    * Installed `pkg install openssh python nginx git`.
    * Configured and started the `sshd` server on port `8022`.
    * Logged in from PC: `ssh u0_a202@192.168.1.13 -p 8022`.
* **Result:** A stable, 24/7 server that is now the primary host for the API.

---

## 🚧 Milestone 6: Deploy & Secure API on Android
* **Date:** (In Progress)
* **Goal:** Deploy the FastAPI app on the Termux server and secure it with HTTPS.
* **Actions:**
    * [x] Generated GitHub SSH keys *inside* Termux.
    * [x] Cloned the repo to the phone: `git clone git@...`
    * [x] Installed Python dependencies: `pip install -r requirements.txt`.
    * [ ] Generate a **self-signed SSL certificate** using `openssl`.
    * [ ] Configure `nginx.conf` in Termux to proxy `/api` to the Uvicorn service and use the SSL certificate (listen on port `443`).
    * [ ] Run the Uvicorn app.

---

## 🚀 Roadmap (Next Steps)

1.  **Finalize Android Server:**
    * Assign a **Static IP** to the phone via the router's settings.
    * Use `tmux` to run `sshd`, `nginx`, and `uvicorn` persistently.
    * Deploy the `dist/` folder from the frontend build to Nginx.

2.  **Observability (Fedora Lab):**
    * Integrate the **Prometheus & Grafana** stack (in containers).
    * Scrape metrics from the FastAPI container.

3.  **Infrastructure as Code (IaC) (Fedora Lab):**
    * Write an **Ansible Playbook** to automate the *entire* Fedora VM setup (install Podman, configure `firewalld`, clone repo, run `podman-compose`).
