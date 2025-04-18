# 🚀 **Py CDN**

**Py CDN** is a simple python project for saving files over HTTP.

> [!WARNING]
> **Warning:** This script is very basic and lacks authentication, file filtering, or file retention policies. **Do not use in production environments.**

## 📑 **Table of Contents**

1. [Installation](#-installation)
2. [Starting the Server](#-starting-the-server)
3. [Usage](#-usage)

## 📦 **Installation**

Clone the repository to get started and install requirements:

```bash
git clone https://github.com/6C656C65/pycdn.git
cd pycdn/
pip install -r requirements.txt
```

## 🖥️ **Starting the Server**

To launch the server, run the following command:

```bash
python3 server.py --host 0.0.0.0 --port 8080 --upload-dir ./srv/cdn/uploads
```

- `--host`: IP address to bind to (e.g., `0.0.0.0` for all interfaces).
- `--port`: Port number to listen on.
- `--upload-dir`: Directory where uploaded files will be saved.

---

## 🛠️ **Usage**

You can interact with the server using tools like `curl`.

### 🔼 Upload a file
```bash
curl -F "file=@file.txt" http://localhost:8000/upload
```

### 🔽 Download a file
```bash
curl -O http://localhost:8000/download/file.txt
```

---