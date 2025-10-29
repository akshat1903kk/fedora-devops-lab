# Teachings & Insights – Fedora DevOps Lab  
**A Structured Knowledge Base for Self-Hosted DevOps Mastery on Fedora Linux**  

> **Project Goal**: Transform a bare-metal Fedora Server into a fully automated, observable, and extensible DevOps environment — from secure system foundations to a live PWA analytics dashboard.  
> **Learning Philosophy**: *Build → Document → Automate → Share*. Every command, failure, and fix becomes a reusable lesson.

---

## 1. Fedora Linux – The Core Operating System  
**Why Fedora?**  
- Bleeding-edge packages (ideal for modern DevOps tooling).  
- RPM-based ecosystem (dnf) with strong Red Hat lineage.  
- Predictable 6-month release cycle + long-term rawhide testing.  
- Default security: SELinux enabled, firewalld, Wayland (server minimal install bypasses GUI).  

### Key Commands & Concepts  
| Tool | Purpose | Core Commands |
|------|--------|---------------|
| **dnf** | Package manager (successor to yum) | `dnf update`, `dnf install nginx`, `dnf autoremove` |
| **systemctl** | Service lifecycle control | `systemctl start nginx`, `status`, `enable --now` |
| **systemd** | Init system & process supervisor | `journalctl -u nginx`, `systemd-analyze` |
| **podman** | Rootless container engine (Docker alternative) | `podman run -d nginx` *(planned)* |

> **Insight**: Fedora prioritizes *security by default* — SELinux in enforcing mode prevents privilege escalation even if a service is compromised.

---

## 2. Networking & Connectivity  
### VirtualBox Networking Modes 

| Mode | Use Case | IP Behavior |
|------|---------|------------|
| **NAT** | Isolated testing | 10.0.2.15 (guest) → port-forward 80→8000 |
| **Bridged** | Real LAN integration | DHCP-assigned LAN IP (e.g., 192.168.1.105) |

### Firewall Management with `firewalld`  
```bash
# Open HTTP/HTTPS
sudo firewall-cmd --add-service=http --permanent
sudo firewall-cmd --add-service=https --permanent
sudo firewall-cmd --reload

# Custom port (FastAPI on 8000)
sudo firewall-cmd --add-port=8000/tcp --permanent
Case Study – Firewall Block:
Symptom: curl localhost:8000 works → external access fails.
Root Cause: firewalld blocking inbound 8000.
Fix: --add-port + reload.
Lesson: Always verify both service binding (0.0.0.0) and firewall rules.
3. Nginx – Web Server & Reverse Proxy
Role in the Lab
Serves static assets (/var/www/html).
Reverse proxies API traffic: 80 → localhost:8000 (FastAPI).
Minimal Config (/etc/nginx/conf.d/lab.conf)
server {
    listen 80;
    server_name _;

    location / {
        root /var/www/html;
        try_files $uri $uri/ =404;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
    }
}
Insight: Use proxy_pass for microservices; avoid exposing Uvicorn directly (not hardened for production).
4. FastAPI + Uvicorn – The API Backbone
Stack Breakdown
Component
Role
Why It Matters
FastAPI
Async Python web framework
Auto-generated OpenAPI docs, Pydantic validation, 3x faster than Flask
Uvicorn
ASGI server
Runs FastAPI with hot-reload in dev (--reload)
Minimal App (src/main.py)
from fastapi import FastAPI

app = FastAPI(title="DevOps Lab API", version="0.1.0")

@app.get("/")
def read_root():
    return {"status": "Fedora Lab API Live", "uptime": "2d 3h"}

@app.get("/health")
def health_check():
    return {"db": "connected", "cache": "healthy"}
Run Command
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
Case Study – 502 Bad Gateway
Symptom: Nginx → 502 when proxying to FastAPI.
Root Cause: Uvicorn not running or bound to 127.0.0.1 only.
Fix:
ps aux | grep uvicorn → kill stale process.
Restart with --host 0.0.0.0.
Verify: curl http://localhost:8000 from VM.
Lesson: Never assume a process is running — always validate with systemctl or ps.
5. tmux – Terminal Multiplexing for DevOps Workflows
Why tmux > screen?
Pane splitting, session persistence, scriptable, detachable.
Essential Workflow
# Start named session
tmux new -s devops-lab

# Split panes
Ctrl+b "  → horizontal  
Ctrl+b %  → vertical  

# Detach: Ctrl+b d  
# Reattach: tmux attach -t devops-lab
Use Cases in This Lab
Pane
Running
1
tail -f /var/log/nginx/access.log
2
uvicorn src.main:app --reload
3
htop or watch ss -tuln
4
git status && git log --oneline
Pro Tip: Add to ~/.tmux.conf:
set -g mouse on
set -g status-style bg=blue
6. Git & Documentation Discipline
Repository Structure (Current & Planned)
fedora-devops-lab/
├── README.md              ← Project overview + roadmap
├── docs/
│   └── progress.md        ← Weekly logs (you are here)
├── configs/
│   ├── nginx.conf
│   └── firewall-rules.xml
├── scripts/
│   └── setup-nginx.sh
├── src/
│   └── main.py            ← FastAPI app
└── ansible/               ← IaC playbooks (Week 7)
Git Best Practices Applied
Commit Early, Commit Often: git add -p for granular changes.
Meaningful Messages:
feat: add FastAPI health endpoint
fix: resolve uvicorn binding to 0.0.0.0
docs: update firewall case study
Branching: feature/pwa-dashboard, bugfix/502-proxy
Insight: Treat infrastructure as code — every config change is a commit.
7. Real-World Case Studies (Failure → Learning)
Issue
Symptom
Diagnosis
Fix
Lesson
502 Bad Gateway
Nginx → API fails
Uvicorn not running / wrong host
uvicorn --host 0.0.0.0
Validate backend independently
IP Unreachable
Host can't access VM web
NAT mode + no port forward
Switch to Bridged
Match network mode to use case
Firewall Block
Local OK, remote KO
firewall-cmd --list-all
--add-port=8000/tcp
Always check inbound rules
tmux Session Lost
Reboot → panes gone
No persistence config
tmux new -s lab -d
Use -d for background sessions
8. What You’ve Mastered (So Far)
Domain
Skills Gained
Linux Systems
Process control, package mgmt, systemd, networking
Web Services
Nginx config, reverse proxy, SSL prep (Let’s Encrypt later)
Python DevOps
FastAPI routing, Uvicorn deployment, async APIs
Productivity
tmux workflows, terminal resilience
Security
firewalld zones, SSH hardening, SELinux context
Version Control
Git discipline, branching, documentation as code
Next-Level Goals (Weeks 3–7)
Week
Focus
Key Learning Outcome
3–4
Docker + Podman
Container isolation, image building, registries
5
GitHub Actions
CI/CD pipelines, automated testing
6
Prometheus + Grafana
Metrics scraping, alerting, dashboards
7
Ansible + PWA
IaC automation, FastAPI → Chart.js frontend
Final Insight
"The best DevOps engineers don’t avoid failures — they document, automate, and teach from them."
This lab is not just infrastructure — it’s a living curriculum. Every 502, every firewall rule, every tmux pane is a lesson encoded for future you (and the community).
Keep committing. Keep sharing. Keep learning.
Last Updated: October 29, 2025 | Day 2 of #100DaysOfCode
GitHub: akshat1903kk/fedora-devops-lab
Follow the build: @AkshatKush1903
---

**How to Use This File**:
1. Save as `docs/teachings-insights.md` in your repo.
2. Commit with: `git add docs/teachings-insights.md && git commit -m "docs: expand teachings with tools, case studies, and structure"`
3. Link from README: `[📖 Teachings & Insights](docs/teachings-insights.md)`
4. Update weekly — it becomes your **personal DevOps textbook**.

Let this be the foundation of your knowledge engine.  
Ready for Week 3? Let’s containerize. 🚀