# Networking Information – Fedora DevOps Lab

## 🌍 VM Configuration Summary
**Adapter Type:** Intel PRO/1000 MT Desktop  
**Mode:** Bridged Adapter  
**IP Range:** 192.168.1.x (Local network)

## 🧩 Key Concepts
- NAT: Isolated access to internet.
- Bridged: VM directly on LAN.
- Host-Only: Only host-VM private network.

## 🧠 Commands Used
```bash
ip addr
ping 192.168.1.13
sudo firewall-cmd --list-all
sudo firewall-cmd --add-port=8000/tcp --permanent
sudo firewall-cmd --reload
```

## 🔎 Current IP Setup
- Fedora internal IP: 192.168.1.13  
- Host IP: 192.168.1.125  
- Browser access:
  - http://192.168.1.13 → Nginx  
  - http://192.168.1.13:8000 → FastAPI app