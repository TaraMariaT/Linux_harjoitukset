# Linux & Cloud Assignments — LEMP + Kubernetes + Streamlit + MQTT Chat

This repository contains a full set of Linux and cloud-related assignments made for OAMK (Oulu University of Applied Sciences).  
It combines traditional LEMP stack work with modern cloud technologies:

- **LEMP Stack** (Linux, Nginx, MySQL, Python/Flask)
- **Kubernetes application** with frontend, backend and MySQL
- **Streamlit analytics dashboard**
- **Real-time MQTT chat**
- **Cat image gallery + voting + charts**
- **Secure secret handling**

---

> ⚠ **Important note:**  
> `kube-app/k8s/mysql-secret.yaml` in this repository is intentionally a **dummy example**.  
> The real MySQL secret file (`mysql-secret-real.yaml`) is *excluded* from Git for security.

---

# 1. LEMP Flask Front Page

The root site is a simple Flask web application demonstrating:

- MySQL connection
- Server timestamp
- ASCII art
- Links to:
  - Streamlit analytics dashboard
  - MQTT chat application

The page uses a green-themed custom UI and runs behind Nginx on:
http://<server-ip>/


---

# 2. Streamlit Dashboard

Located in `data-analysis/`, it includes three sections:

### Cat Database
- Reads cat entries from MySQL
- Auto-detects cat images (jpg/png)
- Shows personality, favorite food, age progress bar
- Visualizes age statistics with Streamlit bar charts

### Weather Data
- 50 most recent weather entries (Helsinki)
- Temperature line chart
- Styled weather cards

### ISS Location Tracker
- Shows ISS positions on a map
- Timestamp converted to Europe/Helsinki time

Runs at:
http://<server-ip>/data-analysis/


---

# 🔷 MQTT WebSocket Chat

A lightweight real-time chat system including:

- Browser client using MQTT-over-WebSocket
- Flask API endpoint for message history (`/chat/api/messages`)
- Messages stored in MySQL
- Automatic refresh of recent messages
- Custom UI with green theme

Available at:
http://<server-ip>/chat/


---

# 4. Kubernetes Application

The `kube-app/` folder contains a full Kubernetes deployment:

### ▶ Backend (Flask API)
Endpoints:
- `/api/cats` — return all cats
- `/api/vote/<id>` — vote for a cat
- `/api/users` — list demo users
- `/api/init-db` — initialize tables + cat data

Includes support for cat images and ensures no duplicate users via:

```sql
ALTER TABLE users ADD UNIQUE(email);

---

# 5. CI/CD Application

- Custom UI styling to match other course assignments
- CI/CD pipeline using GitHub Actions
- Reverse proxied under /cicd