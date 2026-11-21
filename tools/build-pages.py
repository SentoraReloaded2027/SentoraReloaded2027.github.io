# Builds the website's topic pages (/install/, /docker/, /windows/, /migrate/, /cpanel-alternative/, /docker-hosting/,
# /kibana-dashboards/, /nodes/)
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
.gallery { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; max-width: 1180px !important; }
.gallery figure { margin: 0; display: grid; gap: 8px; }
.gallery img { width: 100%; height: auto; border: 1px solid var(--line); border-radius: 10px; display: block; }
.gallery figcaption { font-size: 14px; color: var(--muted); }
.gallery figcaption b { color: var(--text); }
@media (max-width: 760px) { .gallery { grid-template-columns: 1fr; } }
'''
open('assets/site.css', 'w').write(style.strip() + '\n' + EXTRA.strip() + '\n')

PAGES = [
  ('install', 'Install on Linux', 'Ubuntu, Debian, AlmaLinux, Rocky, RHEL and Fedora: one command'),
  ('docker', 'Docker', 'A ready-made image that installs itself, with backups that outlive it'),
  ('windows', 'Windows', 'Windows 11 and Server 2025 through WSL, with a setup program'),
  ('migrate', 'Move from old Sentora', 'Accounts, sites, mail and databases from Sentora 1.0 or 2.0'),
  ('cpanel-alternative', 'Free cPanel alternative', 'Everything a hosting server needs, with no licence fees'),
  ('docker-hosting', 'Docker app hosting', 'Docker Hub apps for your customers, on servers of their own'),
  ('kibana-dashboards', 'Ready-made Kibana dashboards', '34 dashboards and walls for a TV, made for you'),
  ('nodes', 'Sentora nodes', 'Backup, Docker and Elk nodes, each set up with one command'),
]
def cmd(c): return '<div class="cmd"><code>%s</code><button type="button">Copy</button></div>' % c

def page(slug, short, title, desc, eyebrow, h1, lede, body, faq=None):
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
</script>{faqld(faq)}
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

def faqld(faq):
    if not faq:
        return ''
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', html.unescape(a))}} for q, a in faq]}
    return '\n<script type="application/ld+json">\n' + json.dumps(ld, indent=1) + '\n</script>'

def faqhtml(faq):
    return ''.join('<details><summary>%s</summary><div class="a"><p>%s</p></div></details>\n' % (html.escape(q), a) for q, a in faq)

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

# ---------------------------------------------------------------- docker app hosting (the Docker Hosting add-on)
DH_FAQ = [
  ('Can I host Docker Hub images for my customers?',
   "Yes. Docker Hosting runs apps from container images (Docker Hub, GitHub's ghcr.io, Quay and other registries) for your customers, each under their own domain with HTTPS. Uptime Kuma, Gitea, Vaultwarden and Nextcloud come ready to start; you add any other image you trust under Your own apps."),
  ('Does the node need Docker installed?',
   "No. The node installer sets up rootless Podman, which runs the same images from Docker Hub without a root daemon. Each customer's apps run under that customer's own Linux user on the node."),
  ("Do the containers run on the panel's server?",
   'Never. They run on separate servers, called nodes: Ubuntu 26.04, Debian 13, AlmaLinux, Rocky Linux or RHEL 10, or Fedora 45. The node calls the panel for its work, so nothing on the node has to be opened for the panel.'),
  ('Can resellers sell Docker app hosting?',
   'Yes. The administrator gives resellers a share (number of apps, CPU, memory, disk, and which apps), resellers give their clients part of theirs, or put them on Docker plans of their own. A client can never go past the share it was given.'),
  ("Is it safe to run my customers' apps?",
   "Each app runs under its customer's own Linux user on a separate node, never as root and never on the panel's server, with limits on CPU, memory, processes and disk, behind HTTPS, and kept out of your private network. SELinux and AppArmor stay on, and every change is tested on five Linux systems, attacks included. Each app sits behind a web firewall (Coraza with the OWASP rules), its image is checked for known security holes (Trivy), repeat attackers are blocked at the node's firewall (CrowdSec), and on Debian and Ubuntu nodes it runs on a sandbox kernel of its own (gVisor)."),
  ('Is Docker Hosting free?',
   'Yes. It is a free add-on, open source under the GNU GPL v3 like the rest of Sentora 2027, installed with one click from Repo Browser in the panel.'),
]
DH_SECURITY = '<section id="security">\n  <div class="wrap prose">\n    <p class="eyebrow">Secure by design</p>\n    <h2>Each customer kept apart, every guard on</h2>\n    <p>Your customers run code you did not write. So every app is fenced in on several sides, nothing is switched off to make it work, and the node itself is reviewed from an attacker\'s point of view: what a review finds is fixed and tested on every system before it ships.</p>\n    <dl class="ledger">\n      <div><dt>Own user</dt><dd><strong>Rootless Podman</strong>: each customer\'s apps run under <strong>their own Linux user</strong> on the node, never as root, with no way to gain privileges (no-new-privileges).</dd></div>\n      <div><dt>Sandbox kernel</dt><dd><strong>gVisor</strong>: each app runs on a small kernel of its own, so an attack on the kernel stays inside the app\'s sandbox instead of reaching the node. On by default on Debian and Ubuntu nodes; an administrator can switch it off for a trusted app, or mark a node of their own as trusted. On AlmaLinux, Rocky, RHEL and Fedora nodes the apps stay confined by SELinux until gVisor works together with it.</dd></div>\n      <div><dt>Web firewall</dt><dd><strong>Coraza</strong> with the OWASP Core Rule Set (the same rules as ModSecurity on the panel) stands in front of every app: SQL and script injection, path tricks, shell commands and known attack tools are refused before they reach it. On by default; Watch or Off per app.</dd></div>\n      <div><dt>Image check</dt><dd><strong>Trivy</strong> checks each app\'s image for known security holes when it starts or updates, and again every night. The app\'s page shows what it found; an administrator can set an app to block images with critical holes that have a fix.</dd></div>\n      <div><dt>Repeat attackers</dt><dd><strong>CrowdSec</strong> watches the apps, SSH and the system: an address that keeps probing or attacking is blocked at the node\'s firewall for a while. Local by default; an administrator can share with the CrowdSec community. The panel shows what is blocked, with an Unblock button and a safe list.</dd></div>\n      <div><dt>Limits</dt><dd><strong>CPU, memory, processes and disk</strong> per app, held by the kernel. An app over its disk limit stops until it is given more room.</dd></div>\n      <div><dt>HTTPS only</dt><dd>Apps listen on the node\'s 127.0.0.1 only, behind <strong>Caddy</strong>, which serves each one at its own address over HTTPS. A new app can sit behind a setup password until it is ready.</dd></div>\n      <div><dt>Network fence</dt><dd>Apps reach the internet, but <strong>not your private network</strong> (other servers, routers, the panel by its local address) unless the administrator opens it for that customer. The cloud\'s metadata address stays closed for every app.</dd></div>\n      <div><dt>SELinux &amp; AppArmor</dt><dd><strong>Stay on</strong> on every system: tested on AlmaLinux with SELinux enforcing, never with a profile disabled.</dd></div>\n      <div><dt>Signed messages</dt><dd>The panel never connects to a node: the node calls the panel. Every message is <strong>signed and sealed</strong> with the panel\'s and the node\'s own keys, and can not be replayed.</dd></div>\n      <div><dt>Updates</dt><dd>The node installs its own <strong>security updates</strong> every night, and the apps can update themselves, with the old version back if the new one does not start.</dd></div>\n      <div><dt>Tested</dt><dd>Every change runs on <strong>five Linux systems</strong> with real nodes before it is published, including attacks: an app must not reach the node\'s own services.</dd></div>\n    </dl>\n  </div>\n</section>\n'
page('docker-hosting', 'Docker app hosting',
  'Docker hosting control panel: host Docker Hub apps for your customers | Sentora 2027',
  'Docker Hosting for Sentora 2027: a free, open-source control panel add-on that runs Docker Hub images (Uptime Kuma, Gitea, Vaultwarden, Nextcloud or any app you add) for your customers and resellers, with rootless Podman on separate servers, HTTPS and limits per customer.',
  'Free add-on: Docker Hosting', 'Host Docker Hub apps for your customers',
  'Sell or give your customers their own apps, straight from Docker Hub: picked in the panel, started on a server of their own (a node), under their own domain with HTTPS. The containers never run on the panel\'s server.',
  sec('How it works', """    <ul class="ticks">
      <li>Install the <b>Docker Hosting</b> add-on from Admin &gt; Repo Browser in your Sentora 2027 panel.</li>
      <li>Add a <b>Docker node</b>: a fresh Linux server for the apps. One command on it installs rootless Podman, the Caddy web server and Sentora's node agent; it shows a key you paste into the panel. The panel shows its own code first, so the node knows it is talking to your panel.</li>
      <li>Give your resellers and clients a <b>share</b>: how many apps, how much CPU, memory and disk, and which apps.</li>
      <li>A customer picks an app, types a name under one of their own domains (for example <b>status.example.com</b>) and presses Start. The panel adds the DNS record if asked, the node downloads the image and starts it.</li>
    </ul>""" + '\n    ' + cmd('curl -fsSL https://raw.githubusercontent.com/RusTus/sentora-installers-2027/master2027/docker-node/sentora2027-docker-node -o sentora2027-docker-node &amp;&amp; sudo bash sentora2027-docker-node') + """
    <p>Run that on the new Docker node as root. Nodes can be Ubuntu 26.04, Debian 13, AlmaLinux 10, Rocky Linux 10, Red Hat Enterprise Linux 10 or Fedora 45.</p>""")
  + sec('Docker Hub apps, ready to start', """    <div class="tblwrap"><table class="tbl">
      <thead><tr><th>App</th><th>What it is</th></tr></thead>
      <tbody>
        <tr><th>Uptime Kuma</th><td>Watches websites and services and tells you when one is down</td></tr>
        <tr><th>Gitea</th><td>Git hosting with issues, pull requests and a wiki</td></tr>
        <tr><th>Vaultwarden</th><td>A password manager that works with the Bitwarden apps</td></tr>
        <tr><th>Nextcloud</th><td>Files, calendars and contacts in your own cloud</td></tr>
        <tr><th>Your own apps</th><td>Any image you trust, from Docker Hub, GitHub's ghcr.io, Quay or another registry: its port, data folders and settings filled in once, then offered like the others</td></tr>
      </tbody></table></div>
    <p>Every app starts behind a setup password, so only its owner can do its first setup (like making its administrator account). Then one switch opens it to the public.</p>""")
  + DH_SECURITY
  + sec('Updates, backups and warnings', """    <ul class="ticks">
      <li><b>App updates</b> with one click, or by themselves at night: the new version is started and checked, and the old one comes back if it does not start.</li>
      <li><b>App backups</b> every night, with Back up now and Put this backup back, carried off the server by Sentora's off-server backup; an app can also <b>move to another node</b> with its data. (Offered when the off-server backup goes to a Sentora backup node.)</li>
      <li>The node's own <b>security updates</b>, restarts and the node software's updates from the panel, or by themselves at night.</li>
      <li><b>Needs a look:</b> a node short of disk, waiting for updates or a restart, or gone quiet is shown at the top of the page, with the button that fixes it, and emailed to the administrators.</li>
    </ul>""")
  + sec('For hosting businesses', """    <p>Docker app hosting fits the way Sentora already sells hosting. The administrator gives <b>resellers</b> a share; resellers give their <b>clients</b> part of theirs, or make <b>Docker plans</b> of their own (for example Small and Large) and put clients on them. Changing a plan changes every client on it, never below what a client already uses. With the Payment Plans add-on, the same sellers bill their clients through PayPal or Stripe.</p>""")
  + sec('Tested', """    <p>Before a change is published, its tests start real nodes on Ubuntu 26.04, Debian 13, AlmaLinux 10, Rocky Linux 10 and Fedora 45 on GitHub, pull Uptime Kuma from Docker Hub, run it, read its limits from the kernel, check the setup password and that an app can not reach the node's own services, then restart and delete it. It has also run on a real AlmaLinux 10 node with SELinux enforcing. The add-on's own guide: <a href="https://github.com/RusTus/sentora-installers-2027/tree/master2027/sentora-repo#readme">the add-on repository's README</a>.</p>""")
  + sec('Questions', '    <div class="faq">' + faqhtml(DH_FAQ) + '</div>'),
  faq=DH_FAQ)

# ---------------------------------------------------------------- ready-made Kibana dashboards (the Elk node)
def shot(name, cap, alt):
    return f"""      <figure><a href="/assets/shots/elk-{name}-light.webp"><picture><source srcset="/assets/shots/elk-{name}-dark.webp" media="(prefers-color-scheme: dark)"><img loading="lazy" decoding="async" src="/assets/shots/elk-{name}-light.webp" width="1600" height="1400" alt="{alt}"></picture></a><figcaption>{cap}</figcaption></figure>
"""
ELK_CMD = 'curl -fsSL https://raw.githubusercontent.com/RusTus/sentora-installers-2027/master2027/elk-node/sentora2027-elk-node -o sentora2027-elk-node &amp;&amp; sudo bash sentora2027-elk-node'
ELK_FAQ = [
  ('Do I have to build the Kibana dashboards myself?',
   'No. The Elk node installs 34 Kibana dashboards, made for Sentora\'s logs and for the other sources it reads (a FortiGate, Veeam, Microsoft 365, Active Directory, VMware vSphere, an online store). They work as soon as the logs arrive. You can still make your own, or copy one under another name and change it.'),
  ('What happens to my own changes when the node is updated?',
   'An update brings every Sentora dashboard back to its newest version. A copy saved under another name is yours and is never touched.'),
  ('What does the Elk node need?',
   'A server of its own (never the panel\'s) with Ubuntu 26.04, at least 4 GB of memory (8 GB or more is better) and room for the logs, kept 30 days unless you choose otherwise. It installs Elasticsearch, Logstash and Kibana 9 from Elastic\'s own packages.'),
  ('Is it free?',
   'Sentora 2027, the Log Forwarder add-on and the Elk node installer are free and open source under the GNU GPL v3. The Elastic stack is installed from Elastic\'s own packages and uses its free features.'),
  ('Can it show my firewall, backups and Active Directory, not only websites?',
   'Yes. Each is switched on with one command on the node: a FortiGate (sites people visit, VPN users, threats), Veeam Backup &amp; Replication (jobs, machines, repositories), Microsoft 365 and Entra (sign-ins, Teams, mail, Microsoft\'s service health), Active Directory (logons, lockouts, admin group changes, through Winlogbeat on each domain controller) and VMware vCenter (hosts, VMs, datastores).'),
]
page('kibana-dashboards', 'Ready-made Kibana dashboards',
  'Ready-made Kibana dashboards for your servers, firewall, backups, Microsoft 365, Active Directory and vSphere | Sentora 2027',
  'The Sentora 2027 Elk node installs Elasticsearch, Logstash and Kibana 9 with 34 ready-made Kibana dashboards: websites, mail, security, uptime, a FortiGate, Veeam backups, Microsoft 365, Active Directory, VMware vSphere and an online store, with walls made for a TV and alerts in the panel.',
  'Log Forwarder and the Elk node', 'Kibana, with the dashboards already made',
  'Most ELK installs leave you with an empty Kibana and weeks of building dashboards. The Sentora 2027 Elk node comes with 34 of them, made for your panel\'s logs and for the systems around it, plus walls to put on a TV: one look tells you what is green, what is yellow and what needs you now.',
  sec('What you see, the day it is installed', """    <div class="gallery">
""" + shot('serverwall', '<b>Server wall.</b> Dials for CPU, memory and disks, moving figures, every website up or down, every certificate\'s days left.', 'The Server wall: CPU, memory and disk dials, websites and certificates as green, yellow and red tiles')
    + shot('backupwall', '<b>Backup wall.</b> Every Veeam job, machine and repository as a tile: green, yellow or red.', 'The Backup wall: Veeam backup jobs, machines and repositories as coloured tiles')
    + shot('netwall', '<b>Network wall.</b> Tunnels to other sites up or down, who is on the VPN, what the internet is used for right now.', 'The Network wall from a FortiGate: site-to-site tunnels, VPN users, apps in use')
    + shot('adwall', '<b>AD wall.</b> Each domain controller, lockouts, failed logons by account and why.', 'The Active Directory wall: domain controllers, lockouts and failed logons')
    + shot('vswall', '<b>vSphere wall.</b> Hosts, datastores and VMs from vCenter, every minute.', 'The vSphere wall: host dials, datastores and virtual machines as tiles')
    + shot('flows', '<b>Flows.</b> Where attacks come from, where they hit and what they tried; visitors; internet use; failed logons.', 'Flow charts: attacks, visits, internet use and failed logons from source to result')
    + """    </div>
    <p>Taken from a test node with sample data. Light or dark follows Kibana's own setting.</p>""")
  + sec('Every dashboard, already made', """    <div class="tblwrap"><table class="tbl">
      <thead><tr><th>Group</th><th>Dashboards</th></tr></thead>
      <tbody>
        <tr><th>Walls for a TV</th><td><b>Server</b>, <b>Backup</b>, <b>Network</b>, <b>Security</b>, <b>Microsoft 365</b>, <b>Sales</b>, <b>AD</b> and <b>vSphere</b> walls: big tiles in green, yellow and red that refresh by themselves, each fitting a 4K screen without scrolling</td></tr>
        <tr><th>At a glance</th><td><b>Today</b> (everything in one page), <b>Week in review</b> (this week against the last, with arrows), <b>Flows</b> (Sankey charts from source to result)</td></tr>
        <tr><th>The panel</th><td>Overview, <b>World map</b> of visitors and attacks, Websites, <b>Website speed</b> (slow pages), Mail, <b>Mail delivery</b> (bounces, where mail goes), Security, <b>Web firewall</b> (ModSecurity), Panel and server, <b>Server health</b>, <b>Uptime</b> and certificates</td></tr>
        <tr><th>Attackers</th><td>One address seen by the panel, the FortiGate, Microsoft 365 and Active Directory, joined up: block the worst first</td></tr>
        <tr><th>FortiGate</th><td>Where people go, VPN and FortiClient users (and site-to-site tunnels), threats, <b>Internet use at the office</b> (busiest hours, streaming and social)</td></tr>
        <tr><th>Veeam</th><td>Backup jobs and why they failed, <b>Backup coverage</b>: every machine's newest backup and every repository's free space</td></tr>
        <tr><th>Microsoft 365</th><td>Sign-ins on a map, failed and risky ones, MFA, Teams and mail per day, each Microsoft service's health</td></tr>
        <tr><th>Active Directory</th><td>Logons and failures with the reason, lockouts and from which computer, admin group changes, accounts created or reset, Group Policy changes, logons outside working hours</td></tr>
        <tr><th>VMware vSphere</th><td>Hosts, VMs and datastores: CPU, memory, space, alarms, snapshots and VMs that are off</td></tr>
        <tr><th>Online store</th><td>A Magento store's orders, sales, best sellers and searches that found nothing; the <b>Store funnel</b> from search to order, and the bots in it</td></tr>
      </tbody></table></div>""")
  + sec('Alerts in the panel, not only on a screen', """    <p>The node checks every 5 minutes and the panel shows what needs a look as a notice, and mails the administrators: a website down, a certificate running out, a full disk, mail piling up, a burst of failed logins, an address attacking in several places, a failed Veeam job or a machine without a recent backup, a repository or datastore filling up, a Microsoft 365 sign-in from a new country, an account locked out, someone added to Domain Admins, a cleared security log, a vSphere host in red. Each alert links to its dashboard.</p>""")
  + sec('More than the panel\'s logs', """    <div class="tblwrap"><table class="tbl">
      <thead><tr><th>Source</th><th>How it arrives</th></tr></thead>
      <tbody>
        <tr><th>The Sentora panel</th><td>Its websites, mail, logins, FTP, DNS, the web firewall and fail2ban, over TLS from the panel's Log Forwarder; its health every minute</td></tr>
        <tr><th>FortiGate</th><td>Syslog over TLS with a certificate the node makes for it, from that address only</td></tr>
        <tr><th>Veeam Backup &amp; Replication</th><td>Its events over TLS, and its REST API read hourly with a read-only user (its certificate pinned)</td></tr>
        <tr><th>Microsoft 365 and Entra</th><td>Read from Microsoft Graph with an app that can only read</td></tr>
        <tr><th>Active Directory</th><td>Winlogbeat on each domain controller, TLS both ways, its own certificate, from its own address only; one setup script per DC</td></tr>
        <tr><th>VMware vCenter</th><td>Metricbeat on the node with a read-only vCenter user, vCenter's certificate pinned</td></tr>
        <tr><th>Online store</th><td>A Magento store's orders and searches from the panel (no customer names, mail or street addresses)</td></tr>
      </tbody></table></div>
    <p>Each one is off until you switch it on with one command on the node, which then shows the steps for the other side.</p>""")
  + sec('Set it up', """    <ul class="ticks">
      <li>On the panel: install <b>Log Forwarder</b> from Admin &gt; Repo Browser and open Advanced &gt; Log Forwarder, Elk node.</li>
      <li>On a new Ubuntu 26.04 server (at least 4 GB of memory), run the installer as root. It asks for the panel's address and shows the panel's code to compare with the page.</li>
      <li>It ends with the node's key and the Kibana login: paste the key in the panel's <b>Add the Elk node</b>. The logs start coming, and the dashboards fill.</li>
    </ul>
    """ + cmd(ELK_CMD) + """
    <p>Kibana answers on the node's own address over HTTPS with its own login, which can read the logs but never delete them. <code>sentora-elk-node update</code> keeps the node and its dashboards up to date.</p>""")
  + sec('Secure by default', """    <ul class="ticks">
      <li>Elasticsearch's security is on; every user can do only its own job (Logstash writes, Kibana's login reads, the alerts read).</li>
      <li>The node has its own small certificate authority. The panel and the node check each other's certificates; nothing secret is typed.</li>
      <li>The firewall lets each source in from its own address only: the panel, the FortiGate, Veeam, each domain controller.</li>
      <li>Readers of other systems use read-only accounts, and their certificates are pinned once you confirm them.</li>
    </ul>""")
  + sec('Tested', """    <p>Every change installs a whole Elk node on GitHub and sends it the panel's logs and every source from stand-ins: FortiGate and Veeam lines, Microsoft Graph, Veeam's API, a Magento store, a domain controller through Winlogbeat's protocol and VMware's own vCenter simulator. It checks that each arrives and is understood, that every dashboard is there, that alerts fire, and that a stranger's certificate or address gets nothing in. Every dashboard is also looked at, light and dark.</p>""")
  + sec('Questions', '    <div class="faq">' + faqhtml(ELK_FAQ) + '</div>'),
  faq=ELK_FAQ)

# ---------------------------------------------------------------- nodes
NODE_FAQ = [
  ('What is a Sentora node?',
   'A server of its own that extends your panel: a backup node keeps the nightly copies, a Docker node runs your customers\' apps, an Elk node keeps the logs and shows them in Kibana. Each is set up with one command and paired with the panel by codes, never by typing a password across.'),
  ('Do nodes need the panel\'s server to be opened up?',
   'No more than it is. A Docker node calls the panel over HTTPS; the panel calls a backup node over SSH with its own key; the panel sends its logs to an Elk node over TLS. Each side checks the other\'s key or certificate first.'),
]
page('nodes', 'Sentora nodes',
  'Sentora nodes: backup, Docker and Elk servers, each set up with one command | Sentora 2027',
  'Grow a Sentora 2027 panel past one server: a backup node for nightly off-server copies with one-click restore, Docker nodes for your customers\' apps, and an Elk node with 34 ready-made Kibana dashboards. Each is installed with one command and paired by codes.',
  'Grow past one server', 'Sentora nodes',
  'A node is a server of its own that takes on one job for your panel. Every kind is installed the same way: one command on the new server, a code to compare, a key to paste. Nothing secret is typed across, and each side checks the other by itself.',
  sec('Three kinds of node', """    <div class="tblwrap"><table class="tbl">
      <thead><tr><th>Node</th><th>What it does</th><th>Systems</th></tr></thead>
      <tbody>
        <tr><th>Backup node</th><td>Keeps the nightly copy of the whole panel off the server; one account or the whole panel comes back from it with one click, and Docker apps' backups go there too. On the panel: Module Admin &gt; Backup Config.</td><td>Ubuntu 26.04, Debian 13, AlmaLinux, Rocky Linux and RHEL 10, Fedora 45</td></tr>
        <tr><th>Docker node</th><td>Runs your customers' apps from Docker Hub with rootless Podman, behind HTTPS and a web firewall, each customer as their own user. With the <a href="/docker-hosting/">Docker Hosting</a> add-on.</td><td>Ubuntu 26.04, Debian 13, AlmaLinux, Rocky Linux and RHEL 10, Fedora 45</td></tr>
        <tr><th>Elk node</th><td>Elasticsearch, Logstash and Kibana 9 with <a href="/kibana-dashboards/">34 ready-made dashboards</a>, walls for a TV, and alerts in the panel; also reads a FortiGate, Veeam, Microsoft 365, Active Directory and vCenter. With the Log Forwarder add-on.</td><td>Ubuntu 26.04</td></tr>
      </tbody></table></div>""")
  + sec('The same three steps for every node', """    <ul class="ticks">
      <li><b>On the new server</b>, run that node's installer as root. It asks for the panel's address and shows <b>the panel's code</b>: answer yes only when it matches the code on the panel's page.</li>
      <li>It sets the node up and ends with <b>the node's key</b>, made from the node's own key.</li>
      <li><b>On the panel</b>, add the node with its address and that key. The panel checks the key the node really answers with, and trusts only that one from then on.</li>
    </ul>""")
  + sec('The commands', """    <p class="where">Backup node</p>
    """ + cmd('curl -fsSL https://raw.githubusercontent.com/RusTus/sentora-installers-2027/master2027/backup-node/sentora2027-backup-node -o sentora2027-backup-node &amp;&amp; sudo bash sentora2027-backup-node') + """
    <p class="where">Docker node</p>
    """ + cmd('curl -fsSL https://raw.githubusercontent.com/RusTus/sentora-installers-2027/master2027/docker-node/sentora2027-docker-node -o sentora2027-docker-node &amp;&amp; sudo bash sentora2027-docker-node') + """
    <p class="where">Elk node</p>
    """ + cmd(ELK_CMD) + """
    <p>Each runs on a server of its own, never the panel's. The guide for add-on makers who want a node of their own: <a href="https://github.com/RusTus/sentora-installers-2027/blob/master2027/NODES.md">NODES.md</a>.</p>""")
  + sec('Questions', '    <div class="faq">' + faqhtml(NODE_FAQ) + '</div>'),
  faq=NODE_FAQ)
