#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# EYE OF NAZI v51.0 - ULTRA FINDER
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
\033[97m\033[1m              ULTRA FINDER v51.0\033[0m
\033[2m              Made by Cyber Kurd Team\033[0m
\033[96m=============================================================\033[0m
"""

# 500+ sensitive paths
PATHS = [
    # ENV files
    '.env', '.env.local', '.env.production', '.env.backup', '.env.dev',
    '.env.test', '.env.staging', '.env.old', '.env.save', '.env.bak',
    '.env.example', '.env.sample', '.env.txt', 'env', 'env.txt',
    '.env.production.local', '.env.development', '.env.development.local',
    # Git
    '.git/config', '.git/HEAD', '.git/index', '.git/logs/HEAD',
    '.git/refs/heads/master', '.gitignore', '.gitmodules',
    '.git-credentials', '.gitconfig',
    # SVN / HG
    '.svn/entries', '.svn/wc.db', '.hg/hgrc',
    # SSH
    '.ssh/id_rsa', '.ssh/id_dsa', '.ssh/id_ecdsa', '.ssh/id_ed25519',
    '.ssh/authorized_keys', '.ssh/known_hosts', '.ssh/config',
    'id_rsa', 'id_dsa', 'id_ecdsa', 'id_ed25519',
    'id_rsa.pub', 'id_dsa.pub',
    # AWS
    '.aws/credentials', '.aws/config', 'aws.json',
    '.aws/config.json',
    # GCP / Azure
    'gcloud.json', 'service-account.json', 'gcp-key.json',
    '.azure/credentials', 'azure.json',
    # Config files
    'wp-config.php', 'wp-config.php.bak', 'wp-config.php~',
    'wp-config.php.old', 'wp-config.php.save', 'wp-config.php.orig',
    'wp-config.php.txt', 'wp-config.txt', 'wp-config-sample.php',
    'config.php', 'config.php.bak', 'config.php~',
    'configuration.php', 'configuration.php.bak',
    'config.inc.php', 'config.json', 'config.yml', 'config.yaml',
    'config.xml', 'config.old', 'config.backup', 'config.save',
    'settings.py', 'settings.php', 'settings.json', 'settings.yml',
    'database.yml', 'database.php', 'database.sql',
    'db.php', 'db.php.bak', 'db.sql', 'db_backup.sql',
    '.htaccess', '.htpasswd', 'web.config', 'nginx.conf',
    'config.txt', 'config.cfg', 'config.ini',
    'credentials.json', 'credentials.yml', 'credentials.yaml',
    'secrets.json', 'secrets.yml', 'secrets.yaml',
    'passwords.txt', 'passwords.json',
    'passwd', 'shadow', 'passwords',
    # Docker / K8s
    'Dockerfile', 'docker-compose.yml', 'docker-compose.yaml',
    '.dockerignore', 'docker-compose.override.yml',
    'kubernetes.yml', 'k8s.yml', 'deployment.yml',
    # CI / CD
    '.travis.yml', '.gitlab-ci.yml', '.circleci/config.yml',
    '.github/workflows/deploy.yml', 'Jenkinsfile',
    # Package files
    'package.json', 'package-lock.json', 'yarn.lock',
    'composer.json', 'composer.lock', 'Gemfile', 'Gemfile.lock',
    'requirements.txt', 'Pipfile', 'Pipfile.lock',
    'go.mod', 'go.sum', 'Cargo.toml',
    # Terraform
    'terraform.tfstate', 'terraform.tfvars', 'terraform.tfstate.backup',
    # Backup
    'backup.zip', 'backup.tar.gz', 'backup.tar', 'backup.sql',
    'backup.rar', 'backup.7z', 'backup.bak', 'backup.old',
    'backup-2024.zip', 'backup-2023.zip', 'backup-2022.zip',
    'old.zip', 'old.tar.gz', 'site_backup.zip', 'full_backup.zip',
    'www.zip', 'www.tar.gz', 'site.zip', 'site.tar.gz',
    'web.zip', 'web.tar.gz', 'public_html.zip', 'html.zip',
    'files.zip', 'uploads.zip', 'images.zip', 'assets.zip',
    'db_backup.sql', 'db.sql.gz', 'database.sql.gz',
    'dump.sql', 'db_dump.sql', 'database_dump.sql',
    'wordpress.zip', 'wp-content.zip',
    'backup.7z', 'site.rar', 'web.rar',
    # Admin
    'admin', 'admin/', 'admin.php', 'admin/login', 'admin/login.php',
    'admin/index.php', 'admin/dashboard', 'admin/panel',
    'administrator', 'administrator/', 'administrator.php',
    'wp-admin/', 'wp-login.php', 'wp-admin/install.php',
    'wp-admin/setup-config.php', 'wp-admin/admin-ajax.php',
    'phpmyadmin', 'phpMyAdmin', 'pma', 'myadmin', 'mysql',
    'adminer.php', 'adminer', 'cpanel', 'webmail', 'plesk',
    'directadmin', 'ispconfig', 'manager', 'controlpanel',
    'panel', 'dashboard', 'console', 'backend', 'cms',
    'login', 'login.php', 'signin', 'auth',
    # Logs
    'error.log', 'access.log', 'debug.log', 'error_log',
    'php_error.log', 'php_errorlog', 'errors.log',
    'logs/error.log', 'logs/access.log',
    'var/log/apache2/access.log', 'var/log/apache2/error.log',
    'var/log/nginx/access.log', 'var/log/nginx/error.log',
    'var/log/auth.log', 'var/log/syslog',
    'wp-content/debug.log',
    # Info
    'phpinfo.php', 'info.php', 'test.php', 'debug.php', 'status.php',
    'server-status', 'server-info', 'health', 'healthz',
    'robots.txt', 'sitemap.xml', 'crossdomain.xml',
    'humans.txt', 'security.txt', '.well-known/security.txt',
    'sitemap_index.xml', 'sitemap.xml.gz',
    # WordPress
    'wp-json/', 'wp-json/wp/v2/users', 'wp-json/wp/v2/posts',
    'wp-json/wp/v2/pages', 'wp-json/wp/v2/comments',
    'xmlrpc.php', 'wp-cron.php', 'wp-trackback.php',
    'wp-content/', 'wp-content/uploads/', 'wp-content/plugins/',
    'wp-content/themes/', 'wp-content/backup/',
    'wp-includes/', 'readme.html', 'license.txt',
    'wp-activate.php', 'wp-signup.php',
    # API
    'api/', 'api/v1/', 'api/v2/', 'api/v3/', 'api/v4/',
    'rest/', 'rest/api', 'rest/v1', 'rest/v2',
    'graphql', 'graphiql', 'graphql.php',
    'swagger.json', 'swagger.yaml', 'swagger-ui.html',
    'openapi.json', 'openapi.yaml', 'api-docs/',
    'docs/', 'documentation/', 'redoc',
    # Common dirs
    'uploads/', 'upload/', 'files/', 'downloads/',
    'tmp/', 'temp/', 'cache/', 'logs/',
    'old/', 'bak/', 'backups/', 'backup/',
    'private/', 'hidden/', 'secret/', 'secrets/',
    'install/', 'setup/', 'upgrade/', 'update/',
    'includes/', 'include/', 'inc/', 'lib/', 'libs/',
    'assets/', 'static/', 'public/', 'public_html/',
    'media/', 'images/', 'img/', 'css/', 'js/',
    # Database
    'mysql.sql', 'mysql_backup.sql', 'sql/', 'sql-backup/',
    'database.sqlite', 'db.sqlite', 'database.db',
    'sqlite.db', 'data.db', 'data.sqlite',
    # Misc
    '.DS_Store', 'Thumbs.db', 'desktop.ini',
    'apple-app-site-association', 'assetlinks.json',
    'feed/', 'rss/', 'atom.xml',
    'search/', 'contact/', 'about/', 'faq/', 'terms/', 'privacy/',
    # Sensitive keys
    'key.pem', 'cert.pem', 'private.key', 'public.key',
    'server.key', 'server.crt', 'ca.crt',
    'ssl.key', 'ssl.crt', 'tls.key', 'tls.crt',
    'jwt.key', 'jwt.pem', 'rsa.key', 'rsa.pem',
    '*.pem', '*.key', '*.pfx', '*.p12', '*.jks', '*.keystore',
]

# Password patterns
PASS_PATTERNS = [
    r'password["\']?\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'passwd["\']?\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'pwd["\']?\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'secret["\']?\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'api[_-]?key["\']?\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'token["\']?\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'access[_-]?key["\']?\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'secret[_-]?key["\']?\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'DB_PASSWORD\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'DB_PASS\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'DB_USER\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'DB_NAME\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'DB_HOST\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'MYSQL_PASSWORD\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'MYSQL_ROOT_PASSWORD\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'DATABASE_PASSWORD\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'SMTP_PASSWORD\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'MAIL_PASSWORD\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'ADMIN_PASSWORD\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'JWT_SECRET\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'APP_KEY\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'APP_SECRET\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'SECRET_KEY\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'AWS_SECRET[_-]?ACCESS[_-]?KEY\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'AWS_ACCESS[_-]?KEY[_-]?ID\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'STRIPE[_-]?SECRET\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'STRIPE[_-]?KEY\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'PAYPAL[_-]?SECRET\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'GITHUB[_-]?TOKEN\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'SLACK[_-]?TOKEN\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'SENDGRID[_-]?KEY\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'TWILIO[_-]?TOKEN\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'GOOGLE[_-]?API[_-]?KEY\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'FIREBASE[_-]?KEY\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'DATABASE_URL\s*[:=]\s*["\']([^"\'\s]{3,200})["\']',
    r'REDIS_URL\s*[:=]\s*["\']([^"\'\s]{3,200})["\']',
    r'MONGO_URL\s*[:=]\s*["\']([^"\'\s]{3,200})["\']',
    r'POSTGRES_PASSWORD\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'RABBITMQ_PASSWORD\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'ELASTIC_PASSWORD\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'GRAFANA_PASSWORD\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'JENKINS_PASSWORD\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'GITLAB_PASSWORD\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'POSTGRES_PASSWORD\s*[:=]\s*["\']([^"\'\s]{3,80})["\']',
    r'AKIA[0-9A-Z]{16}',
    r'ghp_[0-9a-zA-Z]{36}',
    r'gho_[0-9a-zA-Z]{36}',
    r'ghu_[0-9a-zA-Z]{36}',
    r'ghs_[0-9a-zA-Z]{36}',
    r'ghr_[0-9a-zA-Z]{36}',
    r'sk_live_[0-9a-zA-Z]{24,}',
    r'sk_test_[0-9a-zA-Z]{24,}',
    r'pk_live_[0-9a-zA-Z]{24,}',
    r'AIza[0-9A-Za-z\-_]{35}',
    r'xox[baprs]-[0-9a-zA-Z\-]+',
    r'ya29\.[0-9A-Za-z\-_]+',
    r'-----BEGIN (?:RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----',
]

KEYWORDS = ['password', 'passwd', 'pwd', 'secret', 'api_key', 'apikey',
            'token', 'access_key', 'db_pass', 'db_password', 'smtp_pass',
            'private_key', 'jwt_secret', 'app_key', 'app_secret',
            'database_url', 'redis_url', 'aws_secret', 'mysql_password']


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


class Finder:
    def __init__(self, url, cl, threads=30):
        self.url = url.rstrip('/')
        self.cl = cl
        self.threads = threads
        self.findings = []
        self.checked = 0
        self.found_files = 0

    def add(self, url, kind, evidence):
        self.findings.append({'url': url, 'type': kind, 'evidence': evidence[:300]})
        icons = {
            'FILE': '\033[92m[FILE]\033[0m',
            'PASSWORD': '\033[41m\033[97m[PASSWORD]\033[0m',
            'KEY': '\033[41m\033[97m[KEY]\033[0m',
            'LISTING': '\033[93m[LISTING]\033[0m',
        }
        icon = icons.get(kind, '[' + kind + ']')
        print("\n  " + icon + " \033[1mCRITICAL\033[0m")
        print("    URL     : " + url[:120])
        print("    Evidence: " + evidence[:200])

    def extract(self, text):
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

    def check(self, base, path):
        url = base.rstrip('/') + '/' + path.lstrip('/')
        r = self.cl.req(url)
        self.checked += 1
        if r['err'] or r['s'] != 200:
            return
        self.found_files += 1
        text = r['t']
        # Check directory listing
        if 'Index of /' in text or 'Directory listing' in text:
            self.add(url, 'LISTING', "Directory listing enabled")
        # Check for passwords
        passwords = self.extract(text)
        if passwords:
            for pwd in passwords[:5]:
                self.add(url, 'PASSWORD', "Password: " + pwd[:80])
        # Check for private keys
        if '-----BEGIN' in text and 'PRIVATE KEY-----' in text:
            self.add(url, 'KEY', "Private key found")
        # Check keywords
        text_low = text.lower()
        for kw in KEYWORDS:
            if kw in text_low:
                self.add(url, 'FILE', "Keyword: " + kw)
                return

    def scan(self):
        print("\n\033[96m" + "=" * 60 + "\033[0m")
        print("\033[1m  [*] TARGET: " + self.url + "\033[0m")
        print("\033[96m" + "=" * 60 + "\033[0m")

        print("\n\033[96m[*]\033[0m Scanning " + str(len(PATHS)) + " paths...")
        print("\033[96m[*]\033[0m Threads: " + str(self.threads))
        print("\033[2m    This may take 5-15 minutes...\033[0m")

        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            futures = []
            for p in PATHS:
                futures.append(ex.submit(self.check, self.url, p))
            done = 0
            for fut in as_completed(futures):
                done += 1
                if done % 50 == 0:
                    print("\033[2m    Progress: " + str(done) + "/" + str(len(PATHS)) + "\033[0m")
                try:
                    fut.result()
                except Exception:
                    pass

        print("\n\033[96m" + "=" * 60 + "\033[0m")
        print("  Files Checked: " + str(self.checked))
        print("  Files Found: \033[1m\033[92m" + str(self.found_files) + "\033[0m")
        print("  Findings: \033[1m\033[91m" + str(len(self.findings)) + "\033[0m")
        print("\033[96m" + "=" * 60 + "\033[0m\n")

        if not self.findings:
            print("  \033[92mNo sensitive files found.\033[0m\n")

    def save_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as fp:
            json.dump({'target': self.url, 'findings': self.findings},
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
    print("\033[92m  Ultra Finder - " + str(len(PATHS)) + " paths to scan.\033[0m")
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
            sc = Finder(url, cl, threads=st['threads'])
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
