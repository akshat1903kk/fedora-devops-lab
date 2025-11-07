# Tech Stack & Insights — Cloud DevOps Journey

A personal knowledge base and technical reference for the project. This document details the "why," "how," and "what" of every tool in the cloud-native stack.

> **Project Goal:** Build, deploy, and automate a full-stack application using modern, cloud-native DevOps tools.
> 1.  **Production (Render):** A fully automated PaaS environment that deploys from Git.
> 2.  **Local Dev (Docker Compose):** A containerized environment that mirrors production on a local PC.

---

## 📚 Contents
- 1 — **Production:** Render (PaaS) & Infrastructure as Code
- 2 — **Local Dev:** Docker Compose & Containerization
- 3 — **Backend API:** FastAPI + Uvicorn
- 4 — **Frontend App:** React + Vite + TypeScript
- 5 — **CI/CD Pipeline:** GitHub Actions (The "Agents")
- 6 — **Methodology:** Git Workflow
- **Appendices:** Troubleshooting

---

## 1. Production: Render (PaaS)

We use **Render** as our production environment. It is a Platform as a Service (PaaS) that abstracts away the underlying server, OS, and networking.

* **Why Render?** Zero maintenance, automated SSL (HTTPS), and native Git integration for Continuous Deployment (CD).
* **Key Config: `render.yaml`:** This file is our "Infrastructure as Code." It tells Render exactly how to build and run our services.
* **Dynamic Networking:** Render assigns a dynamic port to our app. Our `Dockerfile` must use `CMD ... --port $PORT` to listen on the correct port.

---

## 2. Local Dev: Docker Compose

For local development, we use **Docker Compose** to spin up the entire stack with one command. It perfectly mimics the containerized production environment.

* **Why Docker Compose?** It defines all our services (backend, frontend, database) in a single YAML file, ensuring every developer has the exact same setup.
* **Command:** `docker-compose up --build`

---

## 3. Backend API: FastAPI + Uvicorn

The core logic of our application. It runs identically in both local and production containers.

* **FastAPI:** Chosen for its speed, automatic data validation (Pydantic), and auto-generated OpenAPI documentation (`/docs`).
* **Containerization (`Dockerfile`):** Uses a lightweight `python:3.11-slim` base image.

---

## 4. Frontend App: React + Vite + TypeScript

The user interface, built for speed and type safety.

* **Vite:** A blazing-fast build tool that provides instant hot-reload during development.
* **Proxying:** In local development, `vite.config.ts` is configured to proxy API requests (`/api`) to our local backend container (`http://localhost:8000`) to avoid CORS issues.

---

## 5. CI/CD Pipeline: GitHub Actions

Our automated workforce. Every push to GitHub triggers these "agents" to ensure quality before code reaches production.

* **Linter Agent (`lint.yml`):** Checks code style (Black for Python, ESLint for React).
* **Builder Agent (`build.yml`):** Attempts to build the Docker container. If the `Dockerfile` is broken, this agent fails the pipeline, preventing a broken deployment to Render.

---

## 6. Methodology: Git Workflow

We follow a professional feature-branch workflow to keep `main` stable.

1.  **New Feature:** Create a branch (e.g., `git checkout -b feat/new-api`).
2.  **Develop Locally:** Write code and test with Docker Compose.
3.  **Push & Test:** Push branch to GitHub; wait for CI agents to pass.
4.  **Merge to Main:** Create a Pull Request and merge.
5.  **Auto-Deploy:** Render detects the merge to `main` and automatically deploys the new version.

---

## Appendix A — Quick Troubleshooting

* **Local API fails to start?** Check if Docker is running. Run `docker-compose down` and try again.
* **Render deployment fails?** Check the Render dashboard logs. Did the `PORT` variable fail to bind?
* **CI Pipeline fails?** Click the "Details" on the GitHub Pull Request to see exactly which linting rule was broken.
