# 🔐 CyberSecureX — Web-Based Personal & Network Security Toolkit

CyberSecureX is a modern, lightweight, and accessible **personal & small-business security toolkit** built with FastAPI. 
It provides intuitive web-based tools for everyday security tasks like website scanning, local network discovery, password analysis, secure file sharing, and network tools.

---

## 📸 Features

| Feature | Description |
|:----------------------------|:----------------------------------------------------------------------------|
| **Website Scanner** | Check for open ports & common vulnerabilities on any public website. |
| **LAN Device Discovery** | Discover active devices on your local network, along with open ports. |
| **Password Strength Checker** | Evaluate your password’s strength & check if it’s been breached online. |
| **Secure File Transfer** | Upload files securely with expiry time, max download limits, and optional password protection.|
| **Network Tools** | Perform subnetting, supernetting, reverse DNS lookup, and other advanced network utilities. |

---

## ⚙️ Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Database:** SQLite (via sqlite3)
- **Network Tools:** `nmap`, `scapy`, `httpx`, `socket`, `ssl`

---

## 🚀 Getting Started

### 📦 Requirements

- Python3.9+
- `pip` (Python package manager)

### 📥 Install Dependencies

```bash
pip install -r requirements.txt
```

### ⚙️ Run the Application

```bash
python run.py
```
or
```bash
uvicorn app.main:app --reload --host127.0.0.1 --port8000
```

Visit: [http://localhost:8000](http://localhost:8000)

---

## 🚀 Quick Start

Requirements:
- Python3.9+
- pip

1. Create and activate a virtual environment (recommended)
 - Windows:
 ```
 python -m venv .venv
 .venv\Scripts\activate
 ```
 - macOS / Linux:
 ```
 python3 -m venv .venv
 source .venv/bin/activate
 ```

2. Install dependencies
 ```
 pip install -r requirements.txt
 ```

3. Run the application (development)
 ```
 python run.py
 ```
 or
 ```
 uvicorn app.main:app --reload --host127.0.0.1 --port8000
 ```

4. Open your browser at: http://localhost:8000

---

## ⚙️ Environment & Configuration

- Database: SQLite (file-based). No additional DB server required for local use.
- Optional environment variables:
 - PORT (default8000)
 - HOST (default127.0.0.1)
 - DEBUG (enable verbose logs for development)

If your project uses additional configuration files or secrets, store them in environment variables or a .env file and avoid committing them.

---

## 🧭 Project Structure

```
CyberSecureX-main/
├── app/
│ ├── __init__.py
│ ├── main.py # FastAPI app startup & routes
│ ├── database.py # SQLite DB init & file link management
│ ├── routers/
│ │ └── network_tools.py # API router for advanced network tools (subnetting, supernetting, reverse DNS, etc.)
│ ├── utils/
│ │ ├── scanner.py # Website vulnerability scanner logic
│ │ ├── lan_scan.py # LAN device discovery logic
│ │ ├── password_checker.py# Password strength & breach check
│ │ ├── file_share.py # Secure file sharing logic
│ │ └── subnet_tools.py # Subnetting & supernetting utilities
│ ├── static/ # CSS, JS, images, icons
│ ├── templates/ # Jinja2 HTML templates
│ │ ├── base.html
│ │ ├── index.html
│ │ ├── scanner.html
│ │ ├── lan.html
│ │ ├── password.html
│ │ ├── secure_share.html
│ │ └── download_form.html
│ └── uploads/ # Uploaded files storage
│ └── database/file_links.db # SQLite DB file
├── requirements.txt # Python dependencies
├── run.py # Entry point to run uvicorn
└── README.md # Project documentation
```

---

## 🔒 Security & Legal Notice

- Use this tool only on assets you own or have explicit permission to test.
- Unauthorized scanning or probing of networks and systems is illegal and unethical.
- This project is intended for educational and defensive use only.

---

## 🧩 Development Notes

- Tests: add unit/integration tests under a tests/ directory as needed.
- Linting / Formatting: consider using tools like black, flake8, and isort.
- For production deployments, use a proper ASGI server configuration, reverse proxy (e.g., Nginx), and TLS.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.
- Fork the repo
- Create a feature branch (git checkout -b feature-name)
- Commit your changes and open a pull request

Please follow the repository coding style and include tests for new features where possible.

---

## 📦 Docker (Planned)

A Dockerfile and docker-compose configuration may be added in a future update to simplify deployments.

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## ✉️ Contact & Support

For questions or feedback, open an issue in the repository.
