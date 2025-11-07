# Networking Reference

This document outlines the networking configuration for the project, covering both live production and local development environments.

## 1. Production (Live on Render)

The production environment is hosted on Render and is accessible to the public internet.

* **Public URL:** `https://<your-app-name>.onrender.com`
    * *(You need to replace this with your actual Render service URL).*
* **Public Port:** `443` (Standard HTTPS)
    * Render's load balancers automatically handle all public traffic and provide a free SSL certificate.
* **Internal Port:** **Dynamic (via `$PORT`)**
    * We do **not** use a hardcoded port. Our `Dockerfile` is configured to listen on the `$PORT` environment variable provided by Render.

## 2. Local Development (Docker Compose)

The local environment runs on your PC (`localhost`) using Docker Compose.

* **Backend API (Container):** `http://localhost:8000`
    * `docker-compose.yml` maps your PC's port `8000` to the container's internal port `8000`.
* **Frontend Dev Server (Host):** `http://localhost:5173`
    * This is the default port for the Vite React app when you run `npm run dev`.
* **API Proxy:**
    * To avoid CORS errors, the Vite dev server (`:5173`) proxies all requests starting with `/api` to the backend container (`:8000`).
