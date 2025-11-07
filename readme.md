# Cloud DevOps Journey

A personal project documenting the journey of building a full-stack, cloud-native application. This repository demonstrates a modern DevOps workflow using Docker, GitHub Actions, and Render.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📊 Project Status: Live on Render

This project is fully containerized, automated with CI/CD, and deployed live on the public internet.

* **Production:** The backend API is deployed on **Render** as a web service.
* **CI/CD:**
    * **Continuous Integration (CI):** GitHub Actions automatically lints Python/React code and validates the Docker build on every push.
    * **Continuous Deployment (CD):** Render is connected to this repo and automatically deploys any push to the `main` branch to production.
* **Frontend:** A React + Vite app (in progress).

---

## 🚀 Getting Started (Local Development)

You can run the entire backend stack on your local machine with a single command using Docker Compose.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/akshat1903kk/FastAPI-React-Lab.git](https://github.com/akshat1903kk/FastAPI-React-Lab.git)
    cd FastAPI-React-Lab
    ```

2.  **Start the application:**
    This command builds the Docker image and starts the container.
    ```bash
    docker-compose up --build
    ```

3.  **Test the local API:**
    The server will be running on your local machine.
    ```bash
    curl http://localhost:8000/api/v1/status
    ```
    *(Expected output: `{"status":"DevOps Lab API is Live"}`)*

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Production Host** | Render (PaaS) | Live API Deployment |
| **Local Dev Host** | Docker Compose | Local Testing |
| **Backend** | Python, FastAPI | REST API |
| **Containerization** | Docker | Build/Run Environment |
| **CI/CD** | GitHub Actions | Automated Linting & Builds |
| **Frontend** | React + Vite + TS | User Interface |

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
