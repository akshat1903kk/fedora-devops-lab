---
# Fedora DevOps Lab

A personal, self-hosted DevOps learning environment. This repository documents the journey of building a full-stack monitoring dashboard on a local Fedora server, from bare metal to a containerized, CI/CD-driven application.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Project Goal

The objective is to build a complete, self-hosted DevOps lab from scratch. This involves:
* **Infrastructure:** Setting up a Fedora VM as a bare-metal server.
* **Backend:** A containerized FastAPI application to collect and serve data.
* **Frontend:** A web dashboard (planned) to visualize system metrics.
* **DevOps Pipeline:** Full CI/CD, monitoring, and automation (planned).

---

## 📊 Current Status (Updated)

The project is in the initial development phase. The backend service has been successfully containerized.

* ✅ **Infrastructure:** Base Fedora VM is set up and accessible.
* ✅ **Backend:** Created a basic FastAPI application (`backend/app/main.py`).
* ✅ **Containerization:** Wrote a `Dockerfile` for the backend.
* ✅ **Build:** Successfully built the `fedora-backend` Docker image.
* ✅ **Deployment:** The backend container runs and serves "Hello World" & `/health` endpoints.

**Next Steps:**
* Integrate the backend with a PostgreSQL database.
* Set up Alembic for database migrations.
* Begin development of the frontend dashboard.

---

## 🚀 Getting Started

You can now build and run the backend service.

### Prerequisites

* [Docker](https://www.docker.com/get-started) installed and running.
* [Git](https://git-scm.com/)

### Running the Backend

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/akshat1903kk/fedora-devops-lab.git](https://github.com/akshat1903kk/fedora-devops-lab.git)
    cd fedora-devops-lab/dashboard/backend
    ```

2.  **Build the Docker image:**
    From within the `dashboard/backend` directory, run:
    ```bash
    docker build -t fedora-backend .
    ```

3.  **Run the container:**
    ```bash
    docker run -d -p 8000:8000 --name fedora-api fedora-backend
    ```

4.  **Test the API:**
    Open your browser or use `curl` to test the endpoints:
    ```bash
    # Test the root endpoint
    curl http://localhost:8000/
    # Expected output: {"message":"Hello, Fedora DevOps Lab!"}

    # Test the health check
    curl http://localhost:8000/health
    # Expected output: {"status":"ok"}
    ```

---

## 🛠️ Core Technologies

| Category | Technology | Status |
| :--- | :--- | :--- |
| **Infrastructure** | Fedora VM | ✅ Implemented |
| **Backend** | Python, FastAPI | ✅ Implemented |
| **Database** | PostgreSQL | 🚧 Planned |
| **Migrations** | Alembic | 🚧 Planned |
| **Containerization** | Docker | ✅ Implemented |
| **Frontend** | React / Vue (TBD) | 🚧 Planned |
| **CI/CD** | GitHub Actions | 🚧 Planned |
| **Monitoring** | Prometheus, Grafana | 🚧 Planned |

---

## 📁 Project Structure


fedora-devops-lab/
├── dashboard/
│   ├── backend/
│   │   ├── app/
│   │   │   └── main.py       # FastAPI application logic
│   │   ├── venv/             # Local virtual environment (in .gitignore)
│   │   ├── Dockerfile        # Instructions to build the backend image
│   │   └── requirements.txt  # Python dependencies
│   │
│   └── frontend/             # (Placeholder for frontend code)
│
├── docs/                     # Project documentation, diagrams, etc.
└── readme.md                 # You are here

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

