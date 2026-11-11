# Builds the website's topic pages (/install/, /docker/, /windows/, /migrate/, /cpanel-alternative/)
# from index.html's own style, nav and footer. Run from the website repository's top folder.
import re, json, os, html
SITE = 'https://sentorareloaded2027.github.io'
idx = open('index.html').read()
style = re.search(r'<style>(.*?)</style>', idx, re.S).group(1)
fonts = '\n'.join(re.findall(r'<link rel="(?:preconnect|stylesheet)"[^>]*>', idx))
nav = re.search(r'<nav aria-label="Main">.*?</nav>', idx, re.S).group(0)
nav = nav.replace('href="#top"', 'href="/"').replace('href="#', 'href="/#')
footer = re.search(r'<footer>.*?</footer>', idx, re.S).group(0)
copyjs = re.search(r"(document\.querySelectorAll\('\.cmd button'\).*?\n\}\);)", idx, re.S).group(1)

EXTRA = '''
/* topic pages */
.page-hero { padding-block: 56px 18px; }
.page-hero .wrap { display: grid; gap: 16px; }
.page-hero h1 { font-size: clamp(40px, 7vw, 74px); line-height: .95; }
.crumbs { font-size: 14px; color: var(--muted); }
.crumbs a { color: var(--muted); }
.topic section { padding-block: 34px; }
.topic h2 { font-size: clamp(28px, 4vw, 40px); margin-bottom: 14px; }
.prose { display: grid; gap: 14px; color: var(--muted); }
.prose > * { max-width: 82ch; }
.prose > .tblwrap, .prose > .cmd { max-width: 920px; }
.topic h2 { color: var(--text); }
.prose b, .prose strong { color: var(--text); font-weight: 600; }
.prose code, .tbl code { font: 14px var(--mono); color: var(--foam); }
.prose .cmd code { white-space: pre; }
.tbl { width: 100%; border-collapse: collapse; font-size: 15px; border-top: 1px solid var(--line); }
.tbl th, .tbl td { text-align: left; vertical-align: top; padding: 12px 14px; border-bottom: 1px solid var(--line); }
.tbl thead th { font: 600 12px/1.2 var(--body); letter-spacing: .1em; text-transform: uppercase; color: var(--muted); }
.tbl tbody th { font-weight: 600; color: var(--text); }
.tbl td { color: var(--muted); }
.tblwrap { overflow-x: auto; }
.next { border-top: 1px solid var(--line); }
'''
open('assets/site.css', 'w').write(style.strip() + '\n' + EXTRA.strip() + '\n')

PAGES = [
  ('install', 'Install on Linux', 'Ubuntu, Debian, AlmaLinux, Rocky, RHEL and Fedora: one command'),
  ('docker', 'Docker', 'A ready-made image that installs itself, with backups that outlive it'),
  ('windows', 'Windows', 'Windows 11 and Server 2025 through WSL, with a setup program'),
  ('migrate', 'Move from old Sentora', 'Accounts, sites, mail and databases from Sentora 1.0 or 2.0'),
  ('cpanel-alternative', 'Free cPanel alternative', 'Everything a hosting server needs, with no licence fees'),
]
def cmd(c): return '<div class="cmd"><code>%s</code><button type="button">Copy</button></div>' % c

def page(slug, short, title, desc, eyebrow, h1, lede, body):
    others = ''.join('<a href="/%s/"><b>%s</b><span>%s</span></a>' % (s, n, d) for s, n, d in PAGES if s != slug)
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Sentora 2027", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": short, "item": "%s/%s/" % (SITE, slug)}]}
    out = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="icon" href="/favicon.ico">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}/{slug}/">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#051620">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Sentora 2027">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{SITE}/{slug}/">
<meta property="og:image" content="{SITE}/assets/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{SITE}/assets/og-image.jpg">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
{fonts}
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">
{json.dumps(ld, indent=1)}
</script>
</head>
<body class="topic">
{nav}
<main>
<header class="page-hero">
  <div class="wrap">
    <p class="crumbs"><a href="/">Sentora 2027</a> / {short}</p>
    <p class="eyebrow">{eyebrow}</p>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
  </div>
</header>
{body}
<section class="next">
  <div class="wrap">
    <h2>More about Sentora 2027</h2>
    <div class="deeper">{others}<a href="/"><b>Home</b><span>Screenshots, security, what's inside</span></a></div>
  </div>
</section>
</main>
{footer}
<script>
{copyjs}
</script>
</body>
</html>
'''
    os.makedirs(slug, exist_ok=True)
    open(f'{slug}/index.html', 'w').write(out)
    print('wrote', slug)

def sec(h, inner): return f'<section>\n  <div class="wrap prose">\n    <h2>{h}</h2>\n{inner}\n  </div>\n</section>\n'

INSTALL_CMD = 'curl -fLo sentora2027-install https://github.com/RusTus/sentora-installers-2027/releases/download/current/sentora2027-install &amp;&amp; bash sentora2027-install'

# ---------------------------------------------------------------- install
page('install', 'Install on Linux',
  'Install Sentora 2027 on Ubuntu, Debian, AlmaLinux, Rocky Linux, RHEL or Fedora',
  'One command installs the free Sentora 2027 hosting control panel on Ubuntu 26.04, Debian 13, AlmaLinux 10, Rocky Linux 10, RHEL 10 or Fedora 45, with SELinux or AppArmor kept on.',
  'One command, six Linux systems', 'Install Sentora 2027 on Linux',
  'On a fresh server, as root. The installer finds out which Linux it runs on, downloads that system\'s installer, checks it against its SHA-256 and runs it.',
  sec('The command', f'''    {cmd(INSTALL_CMD)}
    <p>It asks for the time zone, the panel's address (for example <b>panel.example.com</b>), the server's IP address and your contact details, installs everything, and ends with a restart. Every password it makes is shown once and saved in <code>/root/passwords.txt</code>, readable by root only. In the tests before each release, an install takes about 5 to 15 minutes.</p>''')
  + sec('Supported systems', '''    <div class="tblwrap"><table class="tbl">
      <thead><tr><th>System</th><th>PHP</th><th>Database</th><th>Guard</th></tr></thead>
      <tbody>
        <tr><th>Ubuntu 26.04</th><td>8.5 (8.2, 8.3, 8.4 per domain)</td><td>MySQL 8.4</td><td>AppArmor on</td></tr>
        <tr><th>Debian 13</th><td>8.4 (8.2, 8.3, 8.5 per domain)</td><td>MariaDB 11.8</td><td>AppArmor on</td></tr>
        <tr><th>AlmaLinux 10, Rocky Linux 10, RHEL 10</th><td>8.3 (8.2, 8.4, 8.5 per domain)</td><td>MariaDB 10.11</td><td>SELinux enforcing</td></tr>
        <tr><th>Fedora 45</th><td>8.5</td><td>MariaDB 12</td><td>SELinux enforcing</td></tr>
      </tbody></table></div>
    <p>Every system gets the same panel: Apache 2.4, Postfix, Dovecot, SOGo with ActiveSync, Roundcube, SpamAssassin and ClamAV, BIND, ProFTPD with FTPS required, phpMyAdmin and fail2ban. On Debian, the RHEL family and Fedora, the services come from the system's own packages, so its daily security updates keep them current. Red Hat Enterprise Linux must be registered first (Red Hat's free developer subscription works).</p>''')
  + sec('What the server needs', '''    <ul class="ticks">
      <li>A <b>clean install</b> of one of the systems above (amd64), with no other control panel, web or mail server. A minimal install with only SSH is enough.</li>
      <li><b>Root access</b>, and access from the server to github.com.</li>
      <li>A <b>correct clock</b>: the installer checks it and stops if it is more than 2 minutes off.</li>
      <li>A <b>full host name</b> for the panel, ideally with a DNS A record pointing at the server. Once it does, Sencrypt SSL in the panel gets a free Let's Encrypt certificate for it.</li>
      <li>Memory: ClamAV (the virus scanner) needs about 1.5 GB of its own; on a smaller server it is left off and can be switched on later.</li>
    </ul>''')
  + sec('After the restart', f'''    <p>Wait five minutes for the panel's daemon to do its first run, then check the server:</p>
    {cmd('sentora-post-install-check')}
    <p>It looks at about a hundred things, from open ports and file permissions to TLS and stored passwords. Then use the server the way a client would, in 26 real steps (a client, a website, FTP upload, mail sent and delivered, a virus and spam refused, a database, backup and restore), everything removed afterwards:</p>
    {cmd('sentora-smoke-test')}
    <p>Every release is installed from scratch on Ubuntu 26.04, Debian 13, AlmaLinux 10, Rocky Linux 10 and Fedora 45 and must pass both before it is published. The full guide: <a href="https://github.com/RusTus/sentora-core-2027#installing">Installing, in the README</a>.</p>''')
)

# ---------------------------------------------------------------- docker
DOCKER_CMD = '''docker run -d --name sentora --hostname panel.example.com \\
  -e SENTORA_EMAIL=you@example.com -e TZ=America/Chicago \\
  --restart unless-stopped --cgroupns=private --security-opt writable-cgroups=true \\
  --tmpfs /run --tmpfs /run/lock --cap-add NET_ADMIN -v sentora-backup:/backup \\
  -p 80:80 -p 443:443 -p 21:21 -p 61000-61099:61000-61099 -p 25:25 -p 465:465 -p 587:587 \\
  -p 110:110 -p 143:143 -p 993:993 -p 995:995 -p 4190:4190 \\
  ghcr.io/rustus/sentora2027'''
page('docker', 'Docker',
  'Sentora 2027 Docker image: a free hosting control panel in a container',
  'ghcr.io/rustus/sentora2027: the Sentora 2027 hosting control panel as a Docker image. Installs itself on the first start with its own passwords, runs without --privileged, nightly backups to a volume.',
  'ghcr.io/rustus/sentora2027', 'Sentora 2027 in Docker',
  'A complete hosting server (websites, mail, DNS, FTP, databases) in one container, on a Linux host with Docker. GitHub installs, checks and smoke-tests the image before every release is published.',
  sec('Run it', f'''    <p>Put in your panel's address and your email, then run this as root:</p>
    {cmd(DOCKER_CMD)}
    <p>Watch it install (about five minutes in our tests), then read the passwords:</p>
    {cmd('docker logs -f sentora')}
    {cmd('docker exec sentora cat /root/passwords.txt')}
    <p>Then log in at <b>https://</b> your panel's address as <b>zadmin</b>, and check the server with <code>docker exec sentora sentora-post-install-check</code>.</p>''')
  + sec('Its own passwords, every time', '''    <p>Nothing of Sentora is baked into the image: it holds Debian 13, systemd and Sentora's own installer. <b>The first time a container starts, it installs Sentora</b>, so every container gets its own passwords, keys and certificate. Passwords never reach <code>docker logs</code>; the test before each release checks that too.</p>''')
  + sec('No --privileged', '''    <div class="tblwrap"><table class="tbl">
      <thead><tr><th>Option</th><th>Why</th></tr></thead>
      <tbody>
        <tr><th><code>--hostname</code></th><td>The panel's address. Its DNS A record should point at the host.</td></tr>
        <tr><th><code>--cgroupns=private --security-opt writable-cgroups=true</code></th><td>systemd inside manages its services. The container gets its own branch of the host's cgroups and can write only there.</td></tr>
        <tr><th><code>--cap-add NET_ADMIN</code></th><td>fail2ban can ban addresses, in the container's own network only.</td></tr>
        <tr><th><code>-v sentora-backup:/backup</code></th><td>The nightly full backup goes here, and stays on the host when the container is removed.</td></tr>
        <tr><th><code>-p ...</code></th><td>Web, FTP (passive ports 61000&ndash;61099 in a container), mail, IMAP, POP3 and ManageSieve. Add <code>-p 53:53/tcp -p 53:53/udp</code> when this server is the DNS server for its domains.</td></tr>
      </tbody></table></div>''')
  + sec('Backups that outlive the container', '''    <p>With the <b>sentora-backup</b> volume, the first start switches on the nightly full backup into it: every account's files, every database, the mailboxes, and the panel's settings and keys, 14 nights kept. If the container is ever removed, start a new one with the same <code>--hostname</code> and volume; its log says it found a backup, and Admin &gt; Backup Config &gt; Restore brings everything back. Before each release, GitHub does exactly that and checks that a website comes back the same.</p>''')
  + sec('Good to know', '''    <ul class="ticks">
      <li><b>Treat the container as the server:</b> websites, mail and databases live inside it. Restarts and host reboots keep everything; <code>docker rm</code> deletes it (the backup volume stays).</li>
      <li><b>Updates happen inside:</b> <code>docker exec -it sentora sentora-update</code> for the panel; Debian's security updates install themselves.</li>
      <li><b>AppArmor:</b> Docker's own profile confines the container; Sentora's AppArmor rules apply on a plain server only. For hosting other people's websites, a plain Linux server keeps every guard on.</li>
      <li>Tested on GitHub with Docker 29 on a Linux host with cgroup v2. Every option explained: <a href="https://github.com/RusTus/sentora-core-2027#in-docker">In Docker, in the README</a>.</li>
    </ul>''')
)

# ---------------------------------------------------------------- windows
page('windows', 'Windows',
  'Sentora 2027 on Windows 11 and Windows Server 2025 (WSL)',
  'Run the free Sentora 2027 hosting control panel on Windows 11 or Windows Server 2025 through WSL: a setup program, a tray icon, starts with Windows, uninstalls cleanly.',
  'New in 2027', 'Sentora on Windows',
  'A full Sentora server on Windows 11 and Windows Server 2025, through WSL, the Windows Subsystem for Linux: Windows\' own built-in way to run Linux, so nothing else to install.',
  sec('Install it', '''    <p><b>The setup program:</b> download it and double-click it. It registers <b>Sentora 2027</b> in Settings &gt; Apps and the Start menu; a newer setup updates it in place.</p>
    <p><a class="btn primary" href="https://github.com/RusTus/sentora-installers-2027/releases/download/current/Sentora2027Setup.exe">Download Sentora2027Setup.exe</a></p>
    <p>It is not signed, so SmartScreen shows "Windows protected your PC" once: More info &gt; Run anyway. Or, in PowerShell as administrator:</p>
    ''' + cmd('Invoke-WebRequest -OutFile sentora2027-wsl.ps1 https://github.com/RusTus/sentora-installers-2027/releases/download/current/sentora2027-wsl.ps1') + '''
    ''' + cmd('powershell -ExecutionPolicy Bypass -File .\\sentora2027-wsl.ps1'))
  + sec('What it sets up', '''    <ul class="ticks">
      <li>WSL if needed, with its own <b>Debian 13 or Ubuntu 26.04</b> named Sentora, and the same Linux installer inside it</li>
      <li>Sentora's ports in the Windows firewall</li>
      <li>A startup task: <b>Sentora runs whenever Windows runs</b>, also with nobody logged in</li>
      <li>A <b>Sentora Panel</b> shortcut on every desktop, and a <b>tray icon</b>: green while the panel answers, one click opens it</li>
      <li>Sentora Status, Backup and Uninstall in the Start menu. Uninstalling in Settings &gt; Apps removes everything; backups stay.</li>
      <li>The Windows administrator decides whether Windows Defender leaves Sentora's disk image alone</li>
    </ul>''')
  + sec('What it needs', '''    <ul class="ticks">
      <li><b>Windows 11 (22H2 or newer) or Windows Server 2025</b>, with virtualization switched on</li>
      <li>In a virtual machine: switch on <b>nested virtualization</b> first (VMware: Processors &gt; Virtualize Intel VT-x/EPT or AMD-V/RVI)</li>
      <li>We suggest <b>8 GB of memory or more</b></li>
    </ul>
    <p>Tried on a real Windows 11 PC: installed in 14 minutes, the post-install check with 0 FAIL, the smoke test 26 of 26, and the panel answering from another PC after a restart.</p>''')
  + sec('Windows or Linux?', '''    <p>Inside WSL there is no SELinux or AppArmor, and Windows updates restart the PC (and Sentora with it). Windows is great for trying Sentora, a home lab or an office server; for hosting other people's websites, a <a href="/install/">Linux server</a> is the better home. The full guide: <a href="https://github.com/RusTus/sentora-core-2027#on-windows">On Windows, in the README</a>.</p>''')
)

# ---------------------------------------------------------------- migrate
page('migrate', 'Move from old Sentora',
  'Move from Sentora 1.0 or 2.0 to Sentora 2027: accounts, sites, mail and databases',
  'Two commands move a whole old Sentora 1.0.x or 2.0.x server (Debian, Ubuntu or CentOS) into Sentora 2027: accounts, domains, DNS, websites, databases and mailboxes with all their mail.',
  'Coming from Sentora 1.0 or 2.0?', 'Bring everything over',
  'Sentora 2027 goes on a fresh server; your old one stays as it is. Two commands move its accounts across, one at a time or all at once. Reading the old server changes nothing on it.',
  sec('The commands', '''    <p class="where">On the old server, as root</p>
    ''' + cmd('wget https://github.com/RusTus/sentora-installers-2027/releases/download/current/sentora-migrate-export') + '''
    ''' + cmd('bash sentora-migrate-export --to-server &lt;new server&gt;') + '''
    <p>That sends everything straight to the new server over SSH (its root password is asked once). Without <code>--to-server</code> the export is written on the old server, to copy across yourself.</p>
    <p class="where">On the new server</p>
    ''' + cmd('sentora-migrate-import /root/sentora-export-&lt;server&gt;-&lt;date&gt; --all --yes') + '''
    <p>Leave out <code>--yes</code> first: it shows what it would do, and changes nothing.</p>''')
  + sec('What comes along', '''    <ul class="ticks">
      <li><b>Accounts, resellers and packages</b>, matched by name, made on the new server when missing</li>
      <li><b>Domains</b>, sub-domains and parked domains, with their <b>DNS records</b> (those pointing to the old server get the new one's IP)</li>
      <li><b>Websites and databases</b>, with every database user and its password</li>
      <li><b>Mailboxes with all their mail</b>, aliases, forwarders, filters and out-of-office replies, and webmail address books</li>
      <li>FTP accounts, cron jobs and protected folders</li>
      <li><b>Checksums</b> on every file; running it again adds only what is missing</li>
    </ul>''')
  + sec('Old sites keep working', '''    <p>Moved sites run on <b>PHP 7.1</b> at first, as many old Sentora sites need it, and move to PHP 8 when you are ready (one setting per domain). PHP 7.1 gets no security fixes any more, so the panel reminds you to move them on. Old <code>.htaccess</code> lines that today's Apache refuses are listed, and fixed after asking. Tried on a real Sentora 1.0.3 server. The full guide: <a href="https://github.com/RusTus/sentora-core-2027#moving-websites-from-an-old-sentora-server">Moving websites, in the README</a>.</p>''')
)

# ---------------------------------------------------------------- cpanel alternative
page('cpanel-alternative', 'Free cPanel alternative',
  'A free, open-source alternative to cPanel: Sentora 2027',
  'Looking for a free cPanel alternative? Sentora 2027 is an open-source web hosting control panel under the GPL: websites, mail, DNS, FTP, databases, resellers and billing, with no licence fees.',
  'Free and open source', 'A free alternative to cPanel',
  'Sentora 2027 runs a whole web hosting server from the browser, for any number of client accounts and resellers. It is open source under the GNU GPL v3: no licence key and no fee per account or per server.',
  sec('Everything a hosting server needs', '''    <div class="tblwrap"><table class="tbl">
      <tbody>
        <tr><th>Websites</th><td>Apache 2.4 with HTTP/2, PHP through PHP-FPM with several versions side by side (chosen per domain), free Let's Encrypt certificates</td></tr>
        <tr><th>Mail</th><td>Postfix and Dovecot, Roundcube webmail, SOGo with calendars, contacts and ActiveSync, SpamAssassin and ClamAV</td></tr>
        <tr><th>Databases</th><td>MySQL 8.4 or MariaDB, with phpMyAdmin</td></tr>
        <tr><th>DNS and FTP</th><td>BIND, and ProFTPD with FTPS required</td></tr>
        <tr><th>Statistics</th><td>GoAccess and Matomo</td></tr>
        <tr><th>Backups</th><td>Per account, and a nightly full backup of the whole server to another machine, with restore</td></tr>
      </tbody></table></div>''')
  + sec('For hosting businesses', '''    <ul class="ticks">
      <li><b>Resellers</b> sell hosting to their own clients, with their own packages, groups and themes</li>
      <li>The <b>Payment Plans</b> add-on: each seller prices their packages and is paid through PayPal or Stripe; new clients are billed automatically</li>
      <li>Your own brand on the panel, the login page and its emails</li>
      <li>A web service API to automate accounts and billing</li>
    </ul>''')
  + sec('Secure by default', '''    <ul class="ticks">
      <li>Every hosting account runs as <b>its own Linux user</b>, with its own PHP pool and closed folder: one site can't read another</li>
      <li><b>SELinux or AppArmor stay on</b>, on every Linux system</li>
      <li>ModSecurity with the OWASP Core Rule Set through the Web Hardening add-on; fail2ban, two-factor login and modern TLS only</li>
      <li>Every release is installed from scratch on five Linux systems and must pass its checks before it is published</li>
    </ul>''')
  + sec('Where it runs', '''    <p>Ubuntu 26.04, Debian 13, AlmaLinux 10, Rocky Linux 10, Red Hat Enterprise Linux 10 and Fedora 45 (<a href="/install/">install</a>), Windows 11 and Windows Server 2025 through WSL (<a href="/windows/">Windows</a>), and as a <a href="/docker/">Docker image</a>. Coming from an old Sentora server? <a href="/migrate/">Bring everything over</a>. Updates are one click in the panel: it downloads, checks, backs up, updates itself and can roll back.</p>''')
)
