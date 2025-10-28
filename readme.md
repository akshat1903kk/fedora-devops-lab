# **Fedora DevOps Lab**
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ⚙️ **TL;DR**
A self-hosted Fedora Server lab for mastering **DevOps fundamentals** — from secure networking and web hosting to containerization, CI/CD pipelines, and infrastructure monitoring — evolving into a **personal PWA dashboard** powered by FastAPI and Chart.js.

---

## 🧠 **Introduction**
Welcome to the **Fedora DevOps Lab** — a hands-on, self-hosted learning environment designed to simulate modern DevOps workflows using **Fedora Server** as the foundation.  
This project is my sandbox to learn, build, and document full-stack DevOps concepts — including system administration, secure web deployment, CI/CD automation, and real-time monitoring — while keeping everything lean, modular, and reproducible.

Whether you're a fellow learner or a seasoned engineer, this repository offers a structured roadmap and real-world examples for building a **production-grade infrastructure from scratch**.

---

## 🚀 **Vision (7-Week Projection)**
The Fedora DevOps Lab will evolve over 7 weeks from a basic Fedora setup into a **fully containerized, automated infrastructure** featuring:

- Continuous Integration & Deployment pipelines  
- Infrastructure-as-Code provisioning  
- Live traffic monitoring and analytics  
- Secure self-hosted web app deployments  
- A custom **PWA dashboard** built with **FastAPI (backend)** and **Chart.js (frontend)** to visualize server metrics, app performance, and network activity  

This project aims to become a **personal control center** for managing deployed apps, tracking usage, and experimenting with secure network configurations — all running privately on local infrastructure.

---

## 📅 **Phase Breakdown**

### **Week 1–2: Foundation & Web Server**
- Base Fedora server setup and documentation  
- Secure SSH access and network configuration  
- Nginx web server deployment and verification  
- Git integration for infrastructure documentation and version control  

### **Week 3–4: Containerization**
- Installation and configuration of **Docker** and **Docker Compose**  
- Deployment of sample web app containers  
- Setup of a private or GitHub Container Registry (GHCR)  
- Documentation of container workflows  

### **Week 5–6: CI/CD & Monitoring**
- Integration of **GitHub Actions** for automated builds  
- Continuous deployment pipeline for containerized apps  
- Setup of monitoring stack with **Prometheus** and **Grafana**  
- Logging pipeline using **Fluentd** or **Loki**  

### **Week 7: Infrastructure as Code + PWA Integration**
- Build and integrate **FastAPI backend**  
- Create **Chart.js** dashboard for traffic analytics  
- Develop Progressive Web App (PWA) for control and monitoring  
- Write **Ansible** playbooks for complete provisioning  
- Finalize documentation and system diagrams  

---

## 📊 **Current Status**
✅ Fedora Server setup complete  
✅ SSH and Nginx configuration verified  
🚧 Preparing for Docker and FastAPI integration  

---

## 🧩 **Project Structure**
fedora-devops-lab/
├── ansible/ # Ansible playbooks for provisioning (Week 7)
├── configs/ # Configurations for services and network setup
├── docs/ # Documentation and progress logs
├── scripts/ # Automation and setup scripts
├── src/ # FastAPI backend and PWA frontend (coming soon)
└── README.md # You’re reading it

yaml
Copy code

---

## 🛠️ **Technologies & Tools**
| Category | Tools |
|-----------|--------|
| **Operating System** | Fedora Server |
| **Web Server** | Nginx |
| **Backend** | FastAPI |
| **Frontend** | Chart.js, HTML, CSS |
| **Containerization** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |
| **Monitoring** | Prometheus, Grafana |
| **Logging** | Fluentd, Loki |
| **IaC** | Ansible |
| **Version Control** | Git & GitHub |

---

## 🧾 **License**
This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.  

The MIT License allows you to:  
- ✅ Use the code commercially  
- ✅ Modify and distribute it  
- ✅ Include it in proprietary software  
- ✅ Use it privately  
Just keep the original copyright and license notice.

---

## 👤 **Author**
**Akshat**  
- GitHub: [@akshat1903kk](https://github.com/akshat1903kk)  
- Repository: [fedora-devops-lab](https://github.com/akshat1903kk/fedora-devops-lab)  

---

*This is a living project — progress is documented weekly. Star ⭐ the repository to follow the journey as Fedora DevOps Lab evolves into a fully self-hosted PWA control center.*
