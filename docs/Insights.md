# Teachings & Insights — Fedora DevOps Lab

A structured knowledge base for building a self-hosted DevOps environment on Fedora Linux.

> Project goal: Transform a bare-metal Fedora Server into a fully automated, observable, and extensible DevOps environment — from secure system foundations to a live PWA analytics dashboard.  
> Learning philosophy: Build → Document → Automate → Share. Every command, failure, and fix becomes a reusable lesson.

---

## Contents
- 1 — Fedora Linux (why, commands, security)
- 2 — Networking & firewalls
- 3 — Nginx (static hosting + reverse proxy)
- 4 — FastAPI + Uvicorn (API backbone)
- 5 — tmux (workflows)
- 6 — Git & documentation discipline
- 7 — Real-world case studies (failure → learning)
- 8 — Skills gained & roadmap
- Appendices: tips, service unit example, quick checklist

---

## 1. Fedora Linux — The core OS

Why Fedora?
- Bleeding-edge packages (good for modern DevOps tooling).
- RPM ecosystem with dnf and strong Red Hat lineage.
- Regular release cadence (approx. 6 months).
- Secure-by-default: SELinux (enforcing), firewalld.

Key tools & commands

| Tool | Purpose | Common commands |
|------|---------|-----------------|
| dnf | Package manager | `sudo dnf update && sudo dnf install <pkg>` |
| systemctl | Service control | `sudo systemctl start|stop|enable --now <service>` |
| journalctl | Logs | `sudo journalctl -u <service> -f` |
| podman | Rootless container engine | `podman run -d --name nginx nginx` |
| firewall-cmd | firewalld management | `sudo firewall-cmd --add-port=8000/tcp --permanent && sudo firewall-cmd --reload` |

Insight: SELinux prevents many classes of privilege escalation — learn to read denials (audit logs) and set correct file contexts when needed.

---

## 2. Networking & Connectivity

VirtualBox common modes (for lab VMs)
- NAT — isolated, host-to-guest NAT; use port forwarding for exposing services.
- Bridged — VM gets LAN IP via DHCP; useful when you need other LAN devices to access the VM directly.

Firewalld basics
- Open common services (HTTP/HTTPS):
  sudo firewall-cmd --add-service=http --permanent
  sudo firewall-cmd --add-service=https --permanent
  sudo firewall-cmd --reload

- Open a custom port (example: FastAPI on 8000):
  sudo firewall-cmd --add-port=8000/tcp --permanent
  sudo firewall-cmd --reload

Troubleshooting checklist (networking)
1. Confirm service is listening: ss -tuln | grep 8000
2. Confirm service bound to 0.0.0.0 (or IPv4 address) — binding to 127.0.0.1 restricts external access.
3. Confirm firewalld rules: firewall-cmd --list-all
4. Confirm VM networking mode vs host reachability (NAT vs Bridged).
5. Check host/guest routing and any host firewall.

---

## 3. Nginx — Static site + reverse proxy

Role in the lab:
- Serve static assets (/var/www/html)
- Reverse proxy API traffic (HTTP 80 → FastAPI on port 8000)

Minimal example: /etc/nginx/conf.d/lab.conf
```nginx
server {
    listen 80;
    server_name _;

    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Best practices
- Keep Uvicorn behind a reverse proxy — leverage nginx for TLS termination, gzip, and better client handling.
- Use systemd to manage backend processes (avoid dev `--reload` in production).
- Configure appropriate timeouts and buffering for proxied endpoints.

---

## 4. FastAPI + Uvicorn — API backbone

Why FastAPI?
- Fast, async-first, Pydantic validation, built-in OpenAPI docs.

Minimal app example: src/main.py
```python
from fastapi import FastAPI

app = FastAPI(title="DevOps Lab API", version="0.1.0")

@app.get("/")
async def read_root():
    return {"status": "Fedora Lab API Live"}

@app.get("/health")
async def health_check():
    return {"db": "connected", "cache": "healthy"}
```

Run in development (not for production):
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

Systemd service (recommended for production)
See Appendix A for a sample systemd unit to run Uvicorn via a venv or as a user service.

Common issue: 502 Bad Gateway
- Symptom: Nginx returns 502 when proxying to the API.
- Causes:
  - Uvicorn not running
  - Uvicorn bound only to 127.0.0.1 while Nginx proxy expects 127.0.0.1:8000 (or vice versa)
  - A stale process or port conflict
- Fixes:
  - ps aux | grep uvicorn → restart/kill stale processes
  - Ensure uvicorn uses --host 0.0.0.0 or bind to appropriate address
  - Use systemctl to manage the service and check logs: sudo journalctl -u devops-lab-api -f

Lesson: Always validate the backend independently (curl http://localhost:8000) before chasing proxy problems.

---

## 5. tmux — Terminal multiplexing for workflows

Why tmux?
- Pane splitting, persistent sessions, scriptable, and easy to attach/detach.

Essential quick commands
- Start a named session: tmux new -s devops-lab
- Start detached: tmux new -s devops-lab -d
- List sessions: tmux ls
- Attach: tmux attach -t devops-lab
- Split panes: Ctrl+b " (horizontal), Ctrl+b % (vertical)
- Detach: Ctrl+b d

Example workspace panes
- Pane 1: tail -f /var/log/nginx/access.log
- Pane 2: systemctl status devops-lab-api && journalctl -u devops-lab-api -f
- Pane 3: htop or watch ss -tuln
- Pane 4: git status & code edits

Pro tip (~/.tmux.conf)
set -g mouse on
set -g history-limit 10000

---

## 6. Git & documentation discipline

Project layout (example)
```
fedora-devops-lab/
├── README.md
├── docs/
│   ├── progress.md
│   └── teaching_insights.md
├── configs/
│   ├── nginx.conf
│   └── firewall-rules.xml
├── scripts/
│   └── setup-nginx.sh
├── src/
│   └── main.py
└── ansible/
```

Best practices
- Commit early, commit often — use git add -p for focused commits.
- Use clear commit types: feat:, fix:, docs:, chore:, refactor:
- Branch naming: feature/<name>, bugfix/<issue>, chore/<task>
- Keep docs close to code — update docs when configs or behavior change.

---

## 7. Real-world case studies (failure → learning)

502 Bad Gateway
- Symptom: Nginx returns 502 for API routes.
- Diagnosis: Uvicorn not running / bound incorrectly.
- Fix: Start Uvicorn with proper host or fix systemd unit; validate via curl.
- Lesson: Validate backend before debugging proxy.

Firewall Block (service reachable locally, not externally)
- Symptom: curl localhost:8000 works on VM but host cannot access.
- Diagnosis: firewalld blocking inbound port or VM networking mode.
- Fix: firewall-cmd --add-port=8000/tcp --permanent && firewall-cmd --reload OR switch VM to bridged networking.
- Lesson: Check bind address + firewall rules + VM network mode.

tmux session lost after reboot
- Symptom: Reboot removed tmux session and panes.
- Diagnosis: session wasn't started detached or persisted.
- Fix: Start session in background: tmux new -s lab -d and use startup scripts to recreate sessions.
- Lesson: Use systemd or tmuxinator/tmuxp if you need reproducible dev workspaces.

---

## 8. What you’ve mastered & next-level goals

Skills gained
- Linux systems: systemd, dnf, networking basics
- Web services: nginx reverse proxy, static hosting, TLS groundwork
- Python DevOps: FastAPI fundamentals, deploying ASGI apps
- Productivity: tmux workflows, logging, debugging
- Security: firewalld, SELinux awareness
- Version control: commit discipline, feature branches

Roadmap (Weeks 3–7)
- Weeks 3–4: Podman / Containerization — image building and registries
- Week 5: GitHub Actions — CI/CD pipelines and tests
- Week 6: Prometheus & Grafana — metrics, alerts, dashboards
- Week 7: Ansible & PWA — IaC automation and a Chart.js frontend

Final insight
"The best DevOps engineers don’t avoid failures — they document, automate, and teach from them." Treat this repo as a living curriculum: commit lessons and automate repeatable fixes.

---

Appendix A — Example systemd unit for Uvicorn (production)
```ini
# /etc/systemd/system/devops-lab-api.service
[Unit]
Description=DevOps Lab FastAPI (Uvicorn)
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/srv/devops-lab
Environment="PATH=/srv/devops-lab/venv/bin"
ExecStart=/srv/devops-lab/venv/bin/uvicorn src.main:app --host 127.0.0.1 --port 8000 --workers 2
Restart=on-failure
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```
Notes:
- Run Uvicorn bound to 127.0.0.1 when using nginx proxy_pass to that address.
- Use a virtual environment and keep the PATH updated.
- Use a non-root user for service security.

Appendix B — Quick troubleshooting checklist
- Is the process running? `ps aux | grep uvicorn` or `systemctl status ...`
- Is the service listening? `ss -tuln | grep 8000`
- Is the bind address correct (0.0.0.0 vs 127.0.0.1)?
- Are firewall rules allowing the port? `firewall-cmd --list-all`
- Is nginx config correct and testable? `sudo nginx -t && sudo systemctl reload nginx`
- Check logs: `journalctl -u <service> -f` and `/var/log/nginx/error.log`

How to use and update this file
1. Save as docs/teaching_insights.md
2. Commit with:
   git add docs/teaching_insights.md && git commit -m "docs: improve teaching insights and troubleshooting guidance"
3. Link from README: `[📖 Teachings & Insights](docs/teaching_insights.md)`
4. Update weekly — treat this as a living textbook tied to your hands-on work.

Last Updated: 2025-10-29 | Day 2 of #100DaysOfCode  
Repo: akshat1903kk/fedora-devops-lab — Follow the build: @AkshatKush1903
