# Fedora DevOps Lab
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Introduction
Welcome to the **Fedora DevOps Lab** — a hands-on, self-hosted learning environment designed to simulate modern DevOps workflows using Fedora Server as the foundation. This project serves as a personal DevOps mini-lab where I explore, implement, and document key concepts including system administration, containerization, CI/CD automation, and infrastructure monitoring.

Whether you're a fellow learner or an experienced practitioner, this repository provides a structured roadmap and practical examples for building a production-grade DevOps infrastructure from scratch.

## Vision (7-Week Projection)
The Fedora DevOps Lab is a hands-on environment designed to simulate modern DevOps workflows using Fedora Server as the base system. Over the course of 7 weeks, this project will evolve from a minimal server setup into a fully containerized, automated infrastructure showcasing continuous integration, deployment, and monitoring practices.

## Phase Breakdown
### Week 1–2: Foundation & Web Server
- Base Fedora server setup and documentation
- Secure SSH access and network configuration
- Nginx web server deployment and verification
- Git integration for infrastructure documentation and version control

### Week 3–4: Containerization
- Installation and configuration of Docker and Docker Compose
- Deployment of a sample web application container
- Setup of private container registry or GitHub Container Registry (GHCR)
- Documentation of container workflows

### Week 5–6: CI/CD & Monitoring
- Integration of CI/CD pipeline using GitHub Actions
- Automated build and deployment for the sample app
- Setup of monitoring stack with Prometheus and Grafana
- Logging pipeline via Fluentd or Loki

### Week 7: Infrastructure as Code
- Ansible playbooks for complete server provisioning
- Automated deployment of entire DevOps stack
- Documentation and cleanup

## Current Status
✅ Fedora Server setup complete
🚧 Nginx web server deployment in progress

## Project Structure
```
fedora-devops-lab/
├── configs/           # Configuration files for various services
├── scripts/           # Automation scripts
├── ansible/           # Ansible playbooks (Week 7)
└── README.md          # This file
```
## Technologies & Tools
- **Operating System**: Fedora Server
- **Web Server**: Nginx
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus, Grafana
- **Logging**: Fluentd / Loki
- **IaC**: Ansible
- **Version Control**: Git & GitHub
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
The MIT License is a permissive open-source license that allows you to:
- ✅ Use the code commercially
- ✅ Modify and distribute
- ✅ Use privately
- ✅ Include in proprietary software
With the only requirement being to include the original copyright and license notice.
## Contact
**Akshat**
- GitHub: [@akshat1903kk](https://github.com/akshat1903kk)
- Repository: [fedora-devops-lab](https://github.com/akshat1903kk/fedora-devops-lab)
---
*This is a living project — documentation and features will be continuously updated as the 7-week journey progresses. Star ⭐ this repository to follow along!*
