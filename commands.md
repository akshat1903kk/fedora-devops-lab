# Project Command Reference

A personal cheat sheet for all commands used in the Fedora DevOps Lab, from the Fedora VM to the Termux server and local development.

---

## 1. 🐙 Git & GitHub

Commands for version control, used on both local PC and servers.

| Command | Purpose |
| :--- | :--- |
| `git clone git@github.com:...` | Clones a repo using SSH (for servers). |
| `git clone https://github.com/...`| Clones a repo using HTTPS (for local dev). |
| `git fetch` | Fetches all branch info from the remote (GitHub). |
| `git checkout <branch-name>` | Switches to an existing branch. |
| `git checkout -b <new-branch>` | Creates and switches to a new branch. |
| `git add .` | Stages all changed files for a commit. |
| `git commit -m "..."` | Commits staged files with a message. |
| `git push origin <branch-name>` | Pushes committed changes to GitHub. |
| `git remote -v` | Lists your remote repositories. |
| `git remote set-url origin <url>` | Changes the URL of your remote (e.g., from HTTPS to SSH). |

---

## 2. 🐧 Fedora VM (Dev Lab)

Commands used for managing the Fedora VirtualBox server.

### System & Service Management (systemd)
```bash
# Check the status of a service (e.g., nginx)
sudo systemctl status nginx

# Start a service
sudo systemctl start nginx

# Stop a service
sudo systemctl stop nginx

# Restart a service
sudo systemctl restart nginx

# Start a service AND enable it to run on boot
sudo systemctl enable --now nginx

# Check system logs for a specific service (and follow them)
sudo journalctl -u nginx -f
Package Management (dnf)
Bash

# Install a package
sudo dnf install podman

# Update all packages
sudo dnf update
Networking & Firewall (firewalld)
Bash

# List all open ports and services
sudo firewall-cmd --list-all

# Open a new port (e.g., 8080 for a container)
sudo firewall-cmd --add-port=8080/tcp --permanent

# Apply all permanent firewall changes
sudo firewall-cmd --reload
Containerization (Podman)
Bash

# Build a container image from a Dockerfile in the current directory
podman build -t my-backend-api .

# List all running containers
podman ps

# List all local images
podman images

# Run a container
# -d: detach (run in background)
# -p 8080:8000: map host port 8080 to container port 8000
# --name fedora-api: give the container a name
podman run -d -p 8080:8000 --name fedora-api my-backend-api

# Stop a container
podman stop fedora-api

# Remove a container (must be stopped first)
podman rm fedora-api
3. 📱 Android + Termux (Prod Server)
Commands used for managing the 24/7 phone server.

Package Management (pkg)
Bash

# Update all package lists and upgrade installed packages
pkg update && pkg upgrade

# Install new packages
pkg install openssh python nginx git
Server Administration
Bash

# Find your phone's IP address
ip addr show wlan0

# Find your Termux username (e.g., u0_a202)
whoami

# Set the password for your Termux user (for SSH)
passwd

# Start the SSH server (runs on port 8022)
sshd

# Connect to the Termux server from your PC
ssh u0_a202@192.168.1.13 -p 8022

# (CRITICAL) Prevent the phone from sleeping
termux-wake-lock
SSH Key Generation (for GitHub)
Bash

# Generate a new SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Display the public key to copy to GitHub
cat ~/.ssh/id_ed25519.pub
Web Server (Nginx)
Bash

# Start the Nginx server
nginx

# Test your Nginx config file for errors
nginx -t

# Reload the Nginx config after making changes
nginx -s reload

# Go to the Nginx config directory
cd $PREFIX/etc/nginx
SSL Certificate (OpenSSL)
Bash

# Create a new directory for your certs
mkdir $PREFIX/etc/nginx/ssl

# Generate a self-signed key and certificate valid for 1 year
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
Process Management (tmux & Uvicorn)
Bash

# Start the FastAPI backend API
uvicorn app.main:app --host 127.0.0.1 --port 8000

# Start a new named tmux session (e.g., "server")
tmux new -s server

# Detach from a tmux session (leaves it running)
Ctrl+b, then d

# List all running tmux sessions
tmux ls

# Re-attach to a session
tmux a -t server
4. 💻 Local PC (Development)
Commands run on your Windows machine for development.

Frontend (Vite + React)
Bash

# Create a new React + TypeScript project
npm create vite@latest frontend -- --template react-ts

# Install dependencies (use in your dev environment)
npm install

# Install dependencies (use in CI/CD)
npm ci

# Start the local development server (with proxy)
npm run dev

# Build the static files for production
npm run build
Python & Code Quality
Bash

# Activate the Python virtual environment
./venv/Scripts/Activate

# Install packages from a requirements file
pip install -r requirements.txt

# (CRITICAL) Check code formatting with Black
black --check .

# (CRITICAL) Automatically fix code formatting with Black
black .