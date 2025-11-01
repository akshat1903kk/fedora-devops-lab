
# Fedora DevOps Lab

A personal, self-hosted DevOps learning environment. This repository documents the journey of building a full-stack application, from bare metal to a containerized, CI/CD-driven app deployed on a 24/7 low-power server.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Project Goal

The objective is to build a complete, self-hosted DevOps lab from scratch. This project now uses **two distinct environments**:

1.  **Fedora VM (Dev Lab):** A sandboxed environment for testing heavy-duty, enterprise-grade tools like Podman, `firewalld`, SELinux, and Ansible.
2.  **Android + Termux (Prod Server):** A 24/7, low-power "always-on" server (a spare phone) for hosting the live, secured application.

---

## 📊 Current Status (Updated)

The project is fully operational with a CI/CD pipeline and a live 24/7 server.

* ✅ **Infrastructure:** Deployed on two environments: a Fedora VM (lab) and an Android + Termux phone (prod).
* ✅ **Backend:** FastAPI app running on the Termux server, proxied by Nginx.
* 🚧 **Security:** Nginx reverse proxy is being configured with a self-signed SSL certificate (HTTPS) on the Termux server.
* ✅ **Frontend:** React + TypeScript app is in progress and proxies to the live server for development.
* ✅ **CI/CD Pipeline:** GitHub Actions are **live** and running on every push.
* ✅ **Automation 1 (Linter):** An agent automatically runs `black` and `npm run lint` to check all Python and React code.
* ✅ **Automation 2 (Builder):** An agent automatically runs `podman build` to validate the backend `Dockerfile`.

---

## 🚀 Getting Started (Fedora Lab)

This guide helps you run the backend service in the **Fedora VM (Dev Lab)** environment.

### Prerequisites

* [Podman](https://podman.io/) installed and running.
* [Git](https://git-scm.com/)

### Running the Backend

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/akshat1903kk/fedora-devops-lab.git](https://github.com/akshat1903kk/fedora-devops-lab.git)
    cd fedora-devops-lab/dashboard/backend
    ```

2.  **Build the Podman image:**
    From within the `dashboard/backend` directory, run:
    ```bash
    podman build -t fedora-backend .
    ```

3.  **Run the container:**
    This maps your VM's port `8080` to the container's port `8000`.
    ```bash
    podman run -d -p 8080:8000 --name fedora-api fedora-backend
    ```

4.  **Test the API:**
    Open your browser or use `curl` to test the endpoints:
    ```bash
    # Test the API status
    curl http://localhost:8080/api/v1/status
    # Expected output: {"status":"Fedora Lab API Live"}
    ```

---

## 🛠️ Core Technologies

| Category | Technology | Status |
| :--- | :--- | :--- |
| **Infrastructure** | Fedora VM & Android (Termux) | ✅ Implemented |
| **Backend** | Python, FastAPI | ✅ Implemented |
| **Database** | PostgreSQL | 🚧 Planned |
| **Migrations** | Alembic | 🚧 Planned |
| **Containerization** | Podman | ✅ Implemented |
| **Frontend** | React + Vite + TS | ✅ In Progress |
| **CI/CD** | GitHub Actions | ✅ Implemented |
| **Monitoring** | Prometheus, Grafana | 🚧 Planned |

---

## 📁 Project Structure

fedora-devops-lab/ ├── .github/ # <-- NEW! GitHub Actions │ └── workflows/ │ ├── lint.yml # CI Linter Agent │ └── build.yml # CI Build Agent ├── dashboard/ │ ├── backend/ │ │ ├── app/ │ │ │ └── main.py │ │ ├── Dockerfile │ │ └── requirements.txt │ └── frontend/ │ ├── src/ │ ├── package.json │ └── vite.config.ts ├── docs/ │ ├── progress.md # Project milestone log │ ├── networking.md # IP/Port reference │ └── teaching_insights.md # Main technical documentation └── README.md # You are here


---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details
