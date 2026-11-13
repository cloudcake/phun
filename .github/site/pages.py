"""The documentation's words. Every statement follows the app as released and
its CHANGELOG; a page or note marked `next` describes what arrives with the
next release (CHANGELOG `## Unreleased`) and says so on the page. When that
release ships, drop the marks.

`{{figure:<banner stem>|caption}}` places a feature banner's drawing.
"""
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
README = os.path.join(os.path.dirname(os.path.dirname(HERE)), "README.md")

RELEASES = "https://github.com/cloudcake/phun/releases/latest"

INTRO = (
    "Phun runs your PHP applications on your own machine. Every folder you link is served at its own "
    "<code>.test</code> address over trusted HTTPS, with the PHP version it needs, and the databases, cache, "
    "search and mail it uses run beside it as native processes. It is one desktop app with a small background "
    "service and a <code>phun</code> command for the terminal. No Docker, no virtual machine, and no password "
    "for everyday work."
)

NAV = (
    ("Get started", ("install", "first-launch")),
    ("Applications", ("applications", "create", "frameworks", "php", "sharing", "laravel-cloud")),
    ("Services", ("services", "quick-setup", "workers", "databases", "mail-storage", "developer-tools")),
    ("Working in Phun", ("editor", "git", "debugging", "terminals", "logs", "technical-debt")),
    ("Insight", ("metrics", "security", "diagnostics", "notifications")),
    ("Phun itself", ("palette", "ai-agents", "updates", "collaboration", "cli")),
)

HOME_FEATURES = (
    ("link-and-park", "applications"),
    ("infrastructure", "services"),
    ("completion", "editor"),
    ("terminal-dock", "terminals"),
    ("technical-debt", "technical-debt"),
    ("cli", "cli"),
)


def k(*keys):
    return "+".join(f"<kbd>{html.escape(x)}</kbd>" for x in keys)


def sh(*lines):
    out = []
    for line in lines:
        if "#" in line and not line.startswith("#"):
            cmd, _, comment = line.partition("  #")
            out.append(f'{html.escape(cmd.rstrip())}  <span class="c"># {html.escape(comment.strip())}</span>' if comment else html.escape(line))
        else:
            out.append(html.escape(line))
    return "<pre><code>" + "\n".join(out) + "</code></pre>"


def next_note(text):
    return f'<div class="note next"><span class="label">In the next release</span><p>{text}</p></div>'


# ── Get started ──────────────────────────────────────────────────────────
def install():
    return f'''
<h2 id="download">Download</h2>
{{{{downloads}}}}
<p>Use the Apple Silicon build on M-series Macs and the Intel build on older ones. Every release, older ones included, is on <a href="https://github.com/cloudcake/phun/releases">GitHub</a>.</p>

<h2 id="macos">macOS</h2>
<p>Open the <code>.dmg</code> and drag Phun to Applications.</p>
<p>Builds are not notarised yet, so on first launch right-click Phun and choose <strong>Open</strong>, or run:</p>
{sh("xattr -cr /Applications/Phun.app")}
<p>Phun's background service runs as a login item. If macOS asks, allow Phun under <strong>Login Items</strong> in System Settings and the app connects by itself.</p>

<h2 id="windows">Windows</h2>
<p>Run the installer. It is not signed yet, so SmartScreen may warn: choose <strong>More info</strong>, then <strong>Run anyway</strong>.</p>
<p>Uninstalling asks whether to delete Phun's data as well: PHP versions, databases, certificates, settings and logs. Choose No to keep them for a later install.</p>

<h2 id="linux">Linux</h2>
<h3>Debian, Ubuntu and their derivatives</h3>
{sh("sudo apt install ./Phun_<version>_amd64.deb")}
<h3>Arch Linux and its derivatives</h3>
{sh("sudo pacman -U ./Phun_<version>_x86_64.pkg.tar.zst")}
<p>The Arch package brings the libraries MySQL, MariaDB and Chrome for Testing need, and Phun updates it with pacman.</p>

<h3 id="test-names">.test names on Linux</h3>
<p>On Linux, <code>.test</code> names go through systemd-resolved, or NetworkManager with dnsmasq. A base Arch install often has neither; Phun then opens applications at <code>http://localhost/~&lt;name&gt;</code>. To use <code>.test</code> names there, enable systemd-resolved:</p>
{sh("sudo systemctl enable --now systemd-resolved", "sudo ln -sf ../run/systemd/resolve/stub-resolv.conf /etc/resolv.conf")}

<h2 id="next">Next</h2>
<p>Open Phun. The first launch walks you through starting its background service, installing a PHP version and trusting its certificate authority; <a href="first-launch.html">First launch</a> goes through each step.</p>
<p>To remove Phun later, <code>phun uninstall</code> does it from the terminal.</p>
'''


def first_launch():
    return f'''
<p>Phun opens with a short intro: the P gathers from the dots, the name settles in, and it fades once Phun is ready. If your system asks for reduced motion, it holds still.</p>
<p>The welcome screen comes next. It stays until you finish it: quitting or restarting part-way brings you back to the step you need.</p>

<ol class="steps">
<li><b>Daemon</b>
<p>Phun installs its daemon, the small background service that serves your <code>.test</code> applications, answers DNS and runs databases. It never runs as root; the app only talks to it.</p>
<p>If ports 80 and 443 are already taken by another program, the step offers free ports to use instead, and the same for the DNS port. You can skip this and change them later in Settings.</p></li>
<li><b>PHP</b>
<p>The latest PHP version is selected for you and becomes your default. The download can take a few minutes; you can add more versions later.</p>
<p>This step can also add <code>phun</code> to your PATH, so <code>phun</code>, <code>php</code> and the tools Phun installs run directly in your terminal. It is optional.</p></li>
<li><b>Trust</b>
<p>For a green padlock on <code>.test</code>, Phun trusts its local certificate authority, which signs your HTTPS certificates, and installs the DNS resolver that points <code>.test</code> names at Phun. This asks for your password once; nothing after it does.</p>
<p>If it cannot finish, retry there or run this in a terminal:</p>
{sh("phun elevate")}</li>
<li><b>Done</b>
<p>Phun is ready. Applications, PHP and services are managed from the Overview.</p></li>
</ol>

<h2 id="no-admin">Without admin rights</h2>
<p>No admin rights to hand? Every application is also reachable at <code>http://localhost/~name.test</code>, with no resolver or certificate needed.</p>

<h2 id="finding-your-way">Finding your way</h2>
<ul>
<li><strong>The Overview</strong> lists your applications, with Services, Diagnostics and Settings beside them. {k("Ctrl", "1")} to {k("Ctrl", "4")} open those four in order ({k("Cmd")} on macOS), and {k("Ctrl", "5")} opens Mail.</li>
<li><strong>The command palette</strong>, {k("Ctrl", "K")} ({k("Cmd", "K")} on macOS), reaches every page, application, Artisan command and action. Matching is forgiving: "tnkr" finds Tinker.</li>
<li><strong>Themes.</strong> Daybreak and Nightfall, or follow the system, under Settings › Appearance. The choice reaches every window and the editor.</li>
<li><strong>Key binds.</strong> Settings › Key binds gives any action in the command palette a key of your own.</li>
<li><strong>The tray.</strong> Closing the window keeps Phun running in the tray, with the daemon's state and Start, Restart and Stop.</li>
</ul>

<h2 id="health">When something is off</h2>
<p>Diagnostics runs Phun's health checks for DNS, certificates, ports and PHP, each with a one-click fix. From the terminal:</p>
{sh("phun doctor       # check the setup", "phun doctor fix   # repair what it safely can")}
<p>Diagnostics › Report gathers what a problem report needs in one file: versions, services, Phun's processes, a <code>.test</code> lookup, health checks and recent logs. Passwords, tokens, keys, email addresses and your user name are removed before you see it.</p>
'''


# ── Applications ─────────────────────────────────────────────────────────
def applications():
    return f'''
{{{{figure:link-and-park}}}}
<h2 id="link">Link a folder</h2>
<p>Linking serves one folder as an application at <code>&lt;name&gt;.test</code>. In the app, choose Create on the Overview, then <strong>Existing project</strong>, and pick the folder. From the terminal, in the project's folder:</p>
{sh("phun link                 # serve this folder at <folder>.test", "phun link blog ~/Code/blog  # or name it and point at it")}
<p>The web root, such as <code>public</code>, is found for you. To set it yourself use <code>phun root &lt;app&gt; public</code>, and <code>--auto</code> to go back to detecting it.</p>

<h2 id="park">Park a directory</h2>
<p>Parking serves every project inside a folder, each at its own <code>.test</code> name, including projects you add to it later. Choose Create, then <strong>Park</strong>, or:</p>
{sh("phun park ~/Code", "phun unpark ~/Code   # linked applications stay", "phun list parked")}

<h2 id="create">Start something new</h2>
<p>Create makes an application and serves it: Laravel, WordPress, Symfony, CodeIgniter, CakePHP, Slim or an HTML app. <strong>Existing project</strong> brings in a folder on this computer, a Git repository, or a Laravel Cloud application. <a href="create.html">Creating applications</a> goes through each one.</p>
{sh("phun new symfony shop --webapp", "phun new git blog --url git@github.com:acme/blog.git")}

<h2 id="page">An application's page</h2>
<p>Click an application to open its page. The header has <strong>Open</strong> (the code editor, the browser, the folder), the terminals and <strong>Share</strong>. The tabs:</p>
<ul>
<li><strong>Metrics</strong>: requests, response times, errors, memory and CPU, the latest requests and the endpoints hit; see <a href="metrics.html">Metrics and requests</a>.</li>
<li><strong>Infrastructure</strong>: the canvas of its services; see <a href="services.html">Services</a>.</li>
<li><strong>Security</strong>: dependency audits and Composer packages; see <a href="security.html">Security and packages</a>.</li>
<li><strong>Technical Debt</strong>: see <a href="technical-debt.html">Technical Debt</a>.</li>
<li><strong>Sharing</strong>: a public URL through Cloudflare; see <a href="sharing.html">Sharing and the network</a>.</li>
<li><strong>Settings</strong>: General, PHP, HTTPS and the Environment editor; see <a href="frameworks.html#environment">The environment</a>.</li>
</ul>
<p>Every application shows its framework and the libraries it uses, with their versions. When its setup is wrong, such as an <code>APP_URL</code> that is not the address Phun serves it on or an empty <code>APP_KEY</code>, the page lists it with a one-click fix.</p>

<h2 id="https">HTTPS and domains</h2>
<p>Every application is served over HTTPS with a certificate from Phun's local certificate authority, trusted by your browsers; there is nothing to switch on. Add subdomains and wildcards, proxy a <code>.test</code> name to a local port, or send one path, such as <code>/reverb</code>, to another server:</p>
{sh("phun domain add blog api.blog.test", "phun proxy add reverb http://localhost:8080")}
<p>An HTML application is served straight from its folder, with no PHP version needed. Hidden files such as <code>.env</code> and <code>.git</code> are never served from any application.</p>

<h2 id="share">Share on a public URL</h2>
<p>Share gives an application a public HTTPS address through Cloudflare; see <a href="sharing.html">Sharing and the network</a> for passwords, time limits, your own hostname and other devices.</p>

<h2 id="groups">Groups and packages</h2>
<p><strong>Groups</strong> keep the Overview tidy: put applications in a group, order the groups, and add a group folder, served like a parked one. A <strong>package</strong> is a Composer package or repository your applications use, listed under a group (Create › Package). It opens in the code editor with its own dock badge and is never served.</p>
{sh("phun group create Clients", "phun group assign blog Clients")}

<h2 id="instances">More than one instance</h2>
<p>An application can run extra instances behind a load balancer, for scaling locally, and choose which one runs the scheduler.</p>
{sh("phun instance add blog", "phun instance list blog", "phun instance schedule blog <instance> on")}
'''


def create():
    return f'''
{{{{figure:new-application}}}}
<h2 id="menu">The Create menu</h2>
<p><strong>Create</strong>, on the Overview, holds everything that adds an application:</p>
<ul>
<li><strong>Existing Project</strong>: a folder on this computer, a Git repository Phun clones, or a Laravel Cloud application.</li>
<li><strong>Park</strong>, <strong>Group</strong> and <strong>Package</strong>; see <a href="applications.html">Linking and parking</a>.</li>
<li>The starters: <strong>Laravel</strong>, <strong>WordPress</strong>, <strong>Symfony</strong>, <strong>CodeIgniter</strong>, <strong>CakePHP</strong>, <strong>Slim</strong> and <strong>HTML app</strong>.</li>
</ul>
<p>Each starter asks for a name, a folder and the PHP version the application runs on, and says when a version is too old for the framework. It checks first for what it needs, such as Composer or the Laravel installer, then shows each step as it runs.</p>

<h2 id="laravel">Laravel</h2>
<p>The Laravel starter runs the Laravel installer with the choices it would ask in a terminal:</p>
<ul>
<li><strong>Starter kit</strong>: none, React, Vue, Livewire or Svelte, or a community kit by its package name.</li>
<li><strong>Authentication</strong>: Laravel's built-in or WorkOS AuthKit, with team support, and standalone class components for Livewire.</li>
<li><strong>Frontend dependencies</strong>: install and build with npm or Bun, or skip them for later. Node.js or Bun is installed for you when missing.</li>
<li><strong>Testing</strong>: Pest or PHPUnit.</li>
<li><strong>Database</strong>: SQLite, MySQL, MariaDB, PostgreSQL or SQL Server.</li>
</ul>

<h2 id="wordpress">WordPress</h2>
<p>Choose the core version, the locale, the site title and the admin account, and the database name and table prefix. Phun creates the database in MySQL or MariaDB, downloads WordPress, writes <code>wp-config.php</code> and runs the install; see <a href="frameworks.html#wordpress">WordPress</a> for signing in.</p>

<h2 id="others">Symfony, CodeIgniter, CakePHP and Slim</h2>
<p>These start from each framework's own Composer skeleton. Symfony has a <strong>Web application</strong> switch for Twig, Doctrine, forms, security, mailer and Messenger; leave it off for the minimal skeleton, as for an API. Flex's Docker files are left out, mail goes to Phun's capture, and a web application starts on SQLite, all in <code>.env.local</code>.</p>

<h2 id="html">HTML app</h2>
<p>A folder with an <code>index.html</code>, from a <strong>Single-page app</strong> with a few client-side routes or a <strong>Plain page</strong>. It needs no PHP version; see <a href="frameworks.html#html">HTML applications</a>.</p>

<h2 id="clone">Clone from Git</h2>
<p>Existing Project › <strong>Clone from Git</strong> takes an <code>https://</code>, <code>ssh://</code> or <code>git@host:path</code> address and an optional branch. Phun clones it with the git on your PATH, so private repositories use the SSH keys and credential helpers git already has. Then it runs <code>composer install</code> when there is a <code>composer.json</code>, copies <code>.env.example</code> to <code>.env</code> when the project ships one, and for Laravel generates an <code>APP_KEY</code>, links public storage and installs the JavaScript dependencies. The command palette can start a clone too.</p>

<h2 id="cloud">From Laravel Cloud</h2>
<p>Existing Project › <strong>Laravel Cloud</strong> clones a Cloud application's repository and sets up the same infrastructure locally; see <a href="laravel-cloud.html#bring-home">Laravel Cloud</a>.</p>

<h2 id="cli">From the terminal</h2>
<p><code>phun new</code> creates an application in the current folder, or <code>--dir</code>, and follows it until it is ready. <code>--php</code> picks the version.</p>
{sh("phun new symfony shop --webapp", "phun new html site --spa", "phun new git blog --url git@github.com:acme/blog.git --branch main", "phun new codeigniter api --php 8.3")}
<p>Laravel and WordPress take their choices as JSON with <code>--options</code>; the app's starters are the easier route for those.</p>
'''


def php():
    return f'''
{{{{figure:php-versions}}}}
<h2 id="versions">Install versions</h2>
<p>The installed PHP versions sit at the top of Settings, and each version's settings and the defaults open in a dialog from that table. The version you installed on the welcome screen is the default until you choose another.</p>
{sh("phun list php", "phun install php <version>", "phun uninstall php <version>   # only when nothing uses it")}
<p>When Phun ships a newer build of a version you have, such as one that gains an extension, it is offered as an update: <code>phun update php</code> updates every version.</p>

<h2 id="per-application">A version per application</h2>
<p>Each application picks its own PHP version in its Settings › PHP, and the rest keep theirs. From the terminal:</p>
{sh("phun use blog <version>   # just blog.test", "phun use <version>        # the default, used by the terminal's php too")}
<p>To run a tool on the version an application uses, use <code>phun exec</code>:</p>
{sh("phun exec --site blog composer install")}

<h2 id="settings">Settings and extensions</h2>
<p>Set <code>php.ini</code> values for every version at once or for one version, and see each version's extensions:</p>
{sh("phun set php memory_limit 512M", "phun php ini set <version> xdebug.mode debug", "phun php ext list", "phun php pool set <version> max_children 8")}

<h2 id="xdebug">Xdebug</h2>
<p>Xdebug comes with Phun. Turn it on for one application with the editor's bug button or <code>phun debug blog on</code>, and Phun listens on port 9003; see <a href="editor.html#debugging">debugging in the editor</a>.</p>

<h2 id="terminal">PHP in your terminal</h2>
<p><code>phun path install</code> adds Phun's <code>php</code>, <code>composer</code> and friends to your shell's PATH; <code>phun path print</code> shows the snippet without changing any file.</p>
'''


def services():
    return f'''
{{{{figure:infrastructure}}}}
<h2 id="canvas">The infrastructure canvas</h2>
<p>An application's <strong>Infrastructure</strong> tab draws its services as a canvas: PHP, its databases, cache, mail, search, storage and processes, joined to the application.</p>
<p>Add a database and Phun asks which engine: MySQL, MariaDB, PostgreSQL, SQLite or MongoDB. <strong>Add MySQL</strong> (or whichever you pick) installs and starts it, writes the settings and creates the database; <strong>Install only</strong> leaves your settings alone. An application can use more than one database; each gets a card with the connection name to use.</p>
<p>Phun only offers the services an application can use, and writes them where its framework reads them:</p>
<ul>
<li><strong>Laravel</strong>: <code>.env</code>.</li>
<li><strong>Symfony</strong>: <code>.env.local</code>, one DSN each, such as <code>DATABASE_URL</code> and <code>MAILER_DSN</code>.</li>
<li><strong>CodeIgniter</strong>: its own <code>.env</code> settings for databases, Redis, Memcached and mail.</li>
<li><strong>WordPress</strong>: <code>wp-config.php</code>, MySQL or MariaDB, and Redis for the Redis Object Cache plugin.</li>
</ul>
<p>An HTML application gets no services. One Phun cannot wire yet, such as CakePHP, Slim or plain PHP, is told so instead of being offered settings it would ignore.</p>
<p>A shared service's card on the canvas offers what belongs to the application: its logs, the database browser, <strong>Global Config</strong> and Remove. Starting, stopping, ports and versions live on the Services page, since they affect every application.</p>

<h2 id="processes">Processes</h2>
<p>For Laravel, the canvas runs queue workers (as many as you need, each with its own queues and log), the scheduler and Reverb. Symfony gets Messenger workers. WordPress, CodeIgniter, Drupal and Magento get scheduled tasks, which run the application's own cron command every minute. <a href="workers.html">Workers and processes</a> covers each one.</p>
{sh("phun queue enable blog", "phun schedule enable blog", "phun messenger enable shop")}

<h2 id="quick-setup">Quick setup</h2>
<p>A Laravel application's Infrastructure header has <strong>Quick setup</strong>, which sets it up from a typical stack and shows every change first; see <a href="quick-setup.html">Quick setup</a>.</p>

<h2 id="services-page">The Services page</h2>
<p>Services, on the Overview, lists every service Phun can run, installed or not, with Install or Update in its row. They run natively, started with Phun: no Docker, no virtual machine.</p>
<ul>
<li><strong>Databases</strong>: MySQL, MariaDB, PostgreSQL and MongoDB.</li>
<li><strong>Cache</strong>: Redis and Memcached.</li>
<li><strong>Search</strong>: Meilisearch, Typesense and OpenSearch.</li>
<li><strong>Live updates</strong>: Mercure.</li>
</ul>
{sh("phun services", "phun service install redis <version>", "phun service set-port mysql 3307")}

<h2 id="more">Mail, storage and databases</h2>
<p>Caught mail and S3-compatible storage have their own page, <a href="mail-storage.html">Mail and storage</a>, and the database browser and schema canvas are in <a href="databases.html">Databases</a>.</p>

<h2 id="tools">Developer tools</h2>
<p>Composer, Node.js, Bun, the Laravel installer, WP-CLI and Chrome for Testing install when you need them, without a system package manager, and Node.js versions sit side by side; see <a href="developer-tools.html">Developer tools and Node.js</a>.</p>

<h2 id="cloud">Laravel Cloud</h2>
<p>A Laravel application can link to Laravel Cloud from Infrastructure › Laravel Cloud; see <a href="laravel-cloud.html">Laravel Cloud</a>.</p>
'''


def developer_tools():
    return f'''
{{{{figure:developer-tools}}}}
<h2 id="tools">Developer tools</h2>
<p>Services, on the Overview, has a <strong>Developer tools</strong> card. Each tool installs its latest release (the LTS for Node.js) into Phun's data folder, puts its commands on your PATH and updates from the same row. No system package manager is involved.</p>
<ul>
<li><strong>Composer</strong>, the PHP dependency manager.</li>
<li><strong>Node.js</strong>, with <code>npm</code> and <code>npx</code>, for building frontend assets. More versions are below.</li>
<li><strong>Bun</strong>, a JavaScript runtime and package manager.</li>
<li><strong>Node Version Manager</strong>, for installing and switching Node.js versions yourself.</li>
<li><strong>The Laravel installer</strong>, <code>laravel new</code>.</li>
<li><strong>WordPress CLI</strong>, the <code>wp</code> command.</li>
<li><strong>Chrome for Testing</strong> and the ChromeDriver built for it, as <code>chrome</code> and <code>chromedriver</code>, for browser tests with Laravel Dusk or Symfony Panther.</li>
</ul>
<p>The Laravel installer and WordPress CLI need Phun's Composer; installing one without it offers to install Composer first. A tool already on your PATH from another install shows as <strong>External</strong>: Phun leaves that copy alone, and its own copy takes precedence once you install it.</p>
{sh("phun tools", "phun install tool node     # the latest Node.js LTS", "phun install tool chrome", "phun uninstall tool bun")}

<h2 id="node">Node.js versions</h2>
<p>Install as many Node.js versions as your projects need, from the official nodejs.org builds, each checked against its published SHA-256. Name a major, an exact version, <code>lts</code>, an LTS line such as <code>lts/iron</code>, or <code>latest</code>. The Node.js versions card under Developer tools lists them and installs more.</p>
{sh("phun install node 20", "phun install node lts/jod", "phun list node", "phun uninstall node v20.11.1")}
<p>Phun's <code>node</code>, <code>npm</code> and <code>npx</code> pick a version for the folder you run them in, and so do the Vite and npm workers Phun starts for an application. The first of these wins:</p>
<ul>
<li><strong>The application's own version</strong>, set in its Settings › Node.js or with <code>phun use blog node 20</code>.</li>
<li><strong>The project's files</strong>: the nearest <code>.nvmrc</code>, then <code>.node-version</code>, then <code>package.json</code>'s <code>engines.node</code>, looking upward from the folder.</li>
<li><strong>The default</strong>, set on the card or with <code>phun use node 22</code>.</li>
<li><strong>The newest installed version.</strong></li>
</ul>
<p>The highest installed version that matches is used. A version an application, <code>.nvmrc</code> or <code>.node-version</code> asks for that is not installed stops with the command to install it; an <code>engines.node</code> range nothing matches only warns. Settings › Node.js shows only for applications with a <code>package.json</code>. <code>phun use blog node auto</code> clears an application's version.</p>
{sh("phun use node 22        # the default", "phun use blog node 20   # just blog.test", "phun use blog node auto # back to blog's .nvmrc or the default")}

<h3 id="nvm">With nvm</h3>
<p>Phun's bin folder comes before nvm's on your PATH, so Phun steps aside instead of fighting it. When nvm (or fnm) has a version active in your shell, after <code>nvm use</code> or from nvm's default alias, Phun's <code>node</code>, <code>npm</code> and <code>npx</code> run that version. Two settings change this:</p>
<ul>
<li><code>phun set node manager phun</code>: always run Phun's versions, even with nvm loaded.</li>
<li><code>phun set node manager external</code>: take <code>node</code>, <code>npm</code> and <code>npx</code> out of Phun's bin folder altogether and leave them to nvm. Phun keeps its versions for its own use.</li>
</ul>
{sh("phun set node manager auto   # the default: step aside when nvm is active")}
<p>On Windows, Phun's bin folder holds a copy of the default version and that is the one that runs: the per-application and project-file choices apply on macOS and Linux.</p>

<h2 id="path">On your PATH</h2>
<p>The tools, <code>php</code> and the Node.js versions are in Phun's bin folder. <code>phun path install</code> adds it to your shell's PATH, and <code>phun path print</code> shows the snippet without changing any file. The welcome screen offers the same.</p>
'''


def quick_setup():
    return f'''
<h2 id="open">Open it</h2>
<p>On a Laravel application's Infrastructure tab, <strong>Quick setup</strong> in the header sets the application up from a typical Laravel stack. Phun compares the stack with what the application runs now and shows every change before it makes one. Nothing is uninstalled and no data is deleted.</p>

<h2 id="templates">The stacks</h2>
<ul>
<li><strong>Starter</strong>: SQLite, mail capture, a queue worker on the database driver and the scheduler.</li>
<li><strong>Standard</strong>: MySQL, Valkey for cache, sessions and queues, mail capture, a queue worker and the scheduler.</li>
<li><strong>Postgres</strong>: Standard with PostgreSQL as the database.</li>
<li><strong>Queue-heavy</strong>: Standard plus workers of their own for the <code>high</code> and <code>low</code> queues.</li>
<li><strong>Realtime</strong>: Standard plus a Reverb server for broadcasting over WebSockets.</li>
<li><strong>Search</strong>: Standard plus Meilisearch for full-text search with Scout.</li>
</ul>
<p>Each one names the engines this machine would use. Where MySQL cannot run, the stacks use MariaDB, and Search uses Typesense where Meilisearch cannot. A stack whose main service Phun cannot run here at all, such as Postgres without PostgreSQL, is not offered.</p>

<h2 id="extras">More workers and instances</h2>
<p>Beside the stack, add up to eight more queue workers, each on its own queue. A worker takes its name on the canvas from its first queue. Add up to seven more app instances too: more PHP pools behind the load balancer; see <a href="applications.html#instances">More than one instance</a>.</p>

<h2 id="plan">The plan</h2>
<p>Before anything runs, the plan lists each step under <strong>Add</strong>, <strong>Change</strong>, <strong>Keep</strong> or <strong>Turn off</strong>. When the application already runs everything the stack has, it says there is nothing to change.</p>
<ul>
<li>What you have stays unless you ask. <strong>Turn off what the template doesn't use</strong> stops extra workers and instances and detaches services from this application.</li>
<li>It never deletes a database or uninstalls an engine; turned-off engines stay installed and keep their data.</li>
<li>Running workers restart when their database, queue or mail settings move.</li>
</ul>
<p>The steps run one by one, through the same actions as the canvas, so the result is what you would have built by hand. Quick setup is offered only on Laravel applications; see <a href="services.html">Services and infrastructure</a> for adding services one at a time.</p>
'''


def workers():
    return f'''
{{{{figure:laravel-workers}}}}
<h2 id="processes">Processes</h2>
<p>The long-running processes an application needs run beside it, started and watched by Phun on the application's own PHP. Add them from the Processes menu on its Infrastructure canvas. Phun offers only what the framework uses:</p>
<ul>
<li><strong>Laravel</strong>: queue workers, the scheduler and Reverb.</li>
<li><strong>Symfony</strong>: Messenger workers.</li>
<li><strong>WordPress, CodeIgniter, Drupal and Magento</strong>: scheduled tasks.</li>
</ul>
<p>Each process gets a card on the canvas with its state and settings, and its own place in the application's <a href="logs.html">Logs</a>. They start again with Phun.</p>

<h2 id="queue">Queue workers</h2>
<p>A queue worker runs <code>php artisan queue:work</code>. Its settings are the connection, the queues it takes, how many processes to run, the timeout, the tries and a memory limit; anything left empty uses Artisan's default. A clean exit, <code>queue:restart</code> included, starts the worker again and does not count as a failure. Repeated crashes stop it.</p>
<p>Once one worker runs, <strong>Queue workers</strong> adds another, with its own name, queues and connection, such as one for <code>emails</code> beside the main one. Each worker has its own card, settings and log, and can be removed on its own.</p>
{sh("phun queue enable blog --queues default --processes 2", "phun queue enable blog --name emails --queues emails,notifications", "phun queue status blog --name emails", "phun queue logs blog")}
<p>Jobs finishing or failing can arrive as <a href="notifications.html">notifications</a>.</p>

<h2 id="scheduler">The scheduler</h2>
<p>The scheduler runs <code>php artisan schedule:work</code>, so your scheduled commands run as they would under cron. An application with more than one instance can run a scheduler on each, against the shared cache, so <code>onOneServer</code> and <code>withoutOverlapping</code> can be tested locally.</p>
{sh("phun schedule enable blog", "phun instance schedule blog <instance> on")}

<h2 id="reverb">Reverb</h2>
<p>Reverb runs <code>php artisan reverb:start</code>. Browsers reach it at <code>wss://blog.test/app</code> through Phun's proxy, over the same trusted HTTPS as the application. A crash restarts the server; after three failures it stays stopped until you start it again.</p>
{sh("phun reverb enable blog", "phun reverb status blog")}

<h2 id="messenger">Messenger workers</h2>
<p>For Symfony, Messenger workers run <code>php bin/console messenger:consume</code> for the transports you choose, <code>async</code> by default. Set how many processes, a time limit, a memory limit and how many messages before a worker restarts. Workers start again at their time limit, so code changes are picked up. A Doctrine transport needs <code>messenger:setup-transports</code> once.</p>
{sh("phun messenger enable shop", "phun messenger logs shop")}

<h2 id="cron">Scheduled tasks</h2>
<p>WordPress, CodeIgniter (with <code>codeigniter4/tasks</code>), Drupal (with Drush) and Magento get <strong>Scheduled tasks</strong>: Phun runs the application's own cron command every minute, as cron would. The output goes to the application's logs, and a failed run sends a notification.</p>

<h2 id="npm">npm scripts</h2>
<p>Phun can keep an npm script, such as <code>dev</code>, running beside an application, with its own log:</p>
{sh("phun npm enable blog dev", "phun npm status blog")}
'''


# ── Working in Phun ──────────────────────────────────────────────────────
def editor():
    return f'''
{{{{figure:completion}}}}
<h2 id="open">Open it</h2>
<p>Every application opens in Phun's own code editor from <strong>Open › Editor</strong> at the top of its page. It fills the window; {k("Esc")} minimises it to a badge in the dock that brings it back as it was. It remembers open tabs, cursors and the tree. From a terminal:</p>
{sh("phun edit blog app/Models/Post.php:42")}

<h2 id="languages">Languages</h2>
<p>Highlighting for PHP, Blade, JavaScript and TypeScript, Vue, HTML, XML, CSS and Sass, JSON, Markdown, YAML, shell scripts and <code>.env</code>, recognised by name and by content. Markdown shows its preview beside it, updated as you type. Images, video and audio show as themselves.</p>

<h2 id="completion">Completion and problems</h2>
<p>Completion comes from the application's own classes, functions and variables and, for Laravel, its models' attributes and relations, routes, views, config, translations, validation rules and Blade components. Accepting a class adds its <code>use</code> line.</p>
<p>PHP is checked by the application's own PHP as you type, with a mark in the gutter, the message on hover and {k("F2")} to the next problem.</p>

<h2 id="navigate">Find your way</h2>
<ul>
<li>{k("Ctrl")}-click a class to open it, or a method, property or variable to see every usage ({k("Cmd")}-click on macOS). {k("Ctrl", "B")} and {k("Alt", "F7")} do the same from the keyboard.</li>
<li>Tap {k("Shift")} twice to search everywhere.</li>
<li>Go to file, and find and replace in files. Searches leave <code>vendor</code>, <code>node_modules</code> and the other dependency folders out unless the Deps chip is on.</li>
</ul>

<h2 id="refactor">Refactor and format</h2>
<p>Rename across the application with a preview, extract a variable, and move classes between namespaces with their references updated. Format with the project's own Pint, else Prettier; its <code>.editorconfig</code>, <code>.prettierrc</code> and <code>pint.json</code> always win. Formatting also sorts a PHP file's <code>use</code> lines and drops unused ones.</p>

<h2 id="saving">Saving</h2>
<p>Editor settings › General can save for you, as PhpStorm does: when you leave the window or minimise the editor, and once typing stops for a few seconds you choose. Both are off until you turn them on. The same page can colour the name of a file with unsaved changes, and of one with uncommitted git changes, in the tabs and the tree; both stay gray unless you pick a colour.</p>
<p>Files changed outside Phun follow along: a file another tool writes reloads in its tab, a tab with unsaved edits asks whether to take the disk's version, and a deleted file's tab closes.</p>

<h2 id="git">Git</h2>
<p>Changed lines in the gutter, changed files in the tree, the branch in the status line and the diff in a tab. The Changes view beside the tree stages, unstages and commits ({k("Ctrl", "Enter")}, {k("Cmd", "Enter")} on macOS), and Blame shows who last changed each line. Branches, pulling, the log and worktrees are on <a href="git.html">Git</a>.</p>

<h2 id="tests">Tests</h2>
<p>A test file shows a run marker beside every Pest test, <code>describe</code> group and PHPUnit method. Run one, or debug it; results arrive in a panel under the editor as each test finishes, and a failure shows on the line where it stopped. {k("Ctrl", "Shift", "F10")} runs the test at the cursor.</p>

<h2 id="debugging">Debugging</h2>
<p>The bug button turns Xdebug on, and a click beside a line number sets a breakpoint; see <a href="debugging.html">Debugging and profiling</a>.</p>

<h2 id="settings">Settings and shortcuts</h2>
<p>{k("Ctrl", ",")} ({k("Cmd", ",")} on macOS) opens the editor settings: General, Formatting, Icons and Shortcuts. Every editor shortcut can be rebound.</p>
'''


def terminals():
    return f'''
{{{{figure:terminal-dock}}}}
<h2 id="dock">The dock</h2>
<p>Terminals live in a dock at the bottom of the window. An application's page header opens them:</p>
<ul>
<li><strong>Artisan</strong>: Laravel's commands with their forms. It offers your models, tables, views, components and route names as you type. A Symfony application has <code>bin/console</code> in the same place.</li>
<li><strong>Console</strong>: an interactive shell for the application.</li>
<li><strong>Tinker</strong>: Laravel's REPL.</li>
<li><strong>Logs</strong>: every log the application has, in one list; see <a href="logs.html">Logs</a>.</li>
</ul>
<p>Artisan and Tinker show only for a Laravel application. Clicking anywhere outside an open terminal minimises it to its badge in the dock; the badge brings it back. The code editor minimises there too.</p>
<p>The dock's hide button tucks it behind a small handle that shows how many items it holds, and the dock remembers whether you hid it. Settings › Appearance › <strong>Show other applications in the dock</strong> is on by default; turn it off and an application's page docks only its own terminals and editors, while the others keep running.</p>

<h2 id="console-tabs">Console tabs</h2>
<p>The Console has tabs, each its own shell in the application's folder, so you can run commands in one and keep something like Claude Code running in another. Tabs keep running, at their size, while you are in another, in the dock or inside the editor.</p>
<ul>
<li><strong>+</strong> or {k("Ctrl", "Shift", "T")} ({k("Cmd", "Shift", "T")} on macOS) adds a tab.</li>
<li>{k("Ctrl", "PageDown")} and {k("Ctrl", "PageUp")} move between them ({k("Cmd", "Shift", "]")} and {k("Cmd", "Shift", "[")} on macOS).</li>
<li>Double-click a tab, or press {k("F2")}, to rename it.</li>
</ul>

<h2 id="in-editor">Inside the code editor</h2>
<p>The code editor's toolbar has Console, Artisan, Tinker and Logs buttons for the application you are editing, each showing your key bind for it. They open over the editor. Turn on Editor settings › General › <strong>Open terminals inside the editor</strong> and they open as a resizable panel under the code instead. It is the same session as in the dock, so minimising the editor hands it back to the dock without restarting it, and keys typed in it never trigger the editor's shortcuts.</p>

<h2 id="cursor">The cursor</h2>
<p>Settings › Appearance › <strong>Terminal cursor</strong> sets a block, underscore or pipe, in Phun's red or the text colour, and whether it blinks, with a preview. Open terminals change at once.</p>

<h2 id="keys">Keys</h2>
<ul>
<li>{k("`")} opens the Console for the application you are on, and closes it again, even from inside it.</li>
<li>{k("Shift", "`")} moves to its next open terminal.</li>
<li>{k("Ctrl", "Up")} hides and shows the dock, on macOS too.</li>
<li>Settings › Key binds can give your own keys to opening every terminal at once, the code editor, minimising the terminal and hiding the dock.</li>
</ul>

<h2 id="logs">Logs</h2>
<p>Logs gathers every log the application has into one list you can filter and search, with stack traces that open the editor; see <a href="logs.html">Logs</a>.</p>

<h2 id="history">History and Run again</h2>
<p>Commands run in an application's terminals are kept in its history (<code>phun history blog</code>). The command palette's <strong>Run again</strong> group lists the Artisan commands you ran recently, so a repeat is {k("Ctrl", "K")}, a few letters and {k("Enter")}.</p>
{sh("phun console blog migrate:status   # artisan or bin/console, on the application's PHP")}
'''


def git():
    return f'''
{{{{figure:git}}}}
<h2 id="editor">In the editor</h2>
<p>The code editor knows git. Changed files show in the tree and on their tabs, a folder with changes below it is marked, a bar in the gutter marks added, changed and removed lines, and the branch sits in the status line. Opening a change shows the diff against the last commit as a tab, in the file's own colours. <strong>Blame</strong> in the toolbar shows who last changed each run of lines, and when.</p>

<h2 id="changes">The Changes view</h2>
<p><strong>Changes</strong>, beside Files, lists staged and unstaged files with a button to move each across, and a box to commit what is staged ({k("Ctrl", "Enter")}, {k("Cmd", "Enter")} on macOS). With nothing staged, the commit takes every change.</p>
<ul>
<li><strong>Branches</strong>: switch to a branch, local or remote, or create one.</li>
<li><strong>Pull</strong>: only fast-forwards, so it never makes a merge. It stops with a clear message instead of waiting on a password or host-key prompt.</li>
<li><strong>Discard</strong>: tick the files to throw away, or discard everything since the last commit, with or without new files. It always asks first and says which files will be deleted.</li>
</ul>

<h2 id="window">The Git window</h2>
<p>The clock button beside Files and Changes opens the Git window.</p>
<ul>
<li><strong>Log</strong> shows every branch's commits beside a coloured graph, one line per branch, with arms where branches split off and merge. Filter by text or hash, branch, user and date. A commit's files open as diffs.</li>
<li><strong>Branches and tags</strong> sit in a tree, with favourites listed first. Local branches show how many commits they have to pull and to push from their upstream, as small arrows with counts; hover one for the details.</li>
<li><strong>Console</strong> lists the git commands the editor ran, with their output.</li>
<li><strong>Worktrees</strong> lists, adds and removes worktrees.</li>
</ul>

<h2 id="branches">Branch menu</h2>
<p>Right-click a branch in the tree, or press {k("Shift", "F10")} or the menu key on it. A local branch can be:</p>
<ul>
<li>Checked out, or used to start a new branch.</li>
<li>Merged into the checked-out branch; conflicts stay in Changes for you to resolve.</li>
<li>Updated from its remote without switching to it.</li>
<li>Pushed. Its first push sets the upstream.</li>
<li>Renamed with {k("F2")}, deleted, or made a favourite.</li>
</ul>
<p>Remote branches offer check out, new branch and merge. Branches can also be compared, fetched and cherry-picked from the window.</p>

<h2 id="lfs">Git LFS</h2>
<p>A file still waiting in LFS opens as a notice with a <strong>Download</strong> button instead of its pointer text. Pull fetches LFS files too, diffs say when a file lives in LFS, and the Changes view says when <code>git-lfs</code> is missing.</p>

<h2 id="cli">From the terminal</h2>
<p><code>phun editor git</code> does the same for scripts and AI agents, inside the application's folder:</p>
{sh("phun editor git status blog", "phun editor git blame blog app/Models/Post.php")}
'''


def logs():
    return f'''
<h2 id="open">Open it</h2>
<p><strong>Logs</strong> is in the header of an application's page, in the code editor's toolbar and in the command palette. It opens in the dock like the other terminals and stays there while you move around Phun.</p>

<h2 id="sources">Every log in one list</h2>
<p>Logs merges every log the application has into one list, each line marked with its level and where it came from:</p>
<ul>
<li>The application's own log: Laravel's, or Symfony's <code>var/log/&lt;APP_ENV&gt;.log</code>.</li>
<li>PHP's log, one per instance when the application runs more than one.</li>
<li>Each running queue worker, the scheduler, Reverb, Messenger, scheduled tasks, Vite and npm.</li>
<li>The tunnel, while the application is shared.</li>
</ul>
<p>Narrow it by component, by level (errors, warnings, notices, info or debug) or with the search box.</p>

<h2 id="traces">Stack traces</h2>
<p>An entry with an exception opens to show its class, its message and where it was thrown. Every file and line inside the application is a link that opens the code editor there. Frames in <code>vendor</code> fold into one line you can open, and previous exceptions follow underneath.</p>

<h2 id="exceptions">Exceptions</h2>
<p>The <strong>Exceptions</strong> button lists each exception once, with how often it was thrown and when last. Open one to see its latest trace.</p>

<h2 id="clear">Clear</h2>
<p><strong>Clear logs</strong> empties every log shown, after asking. The PHP log belongs to the PHP version, so other applications on that version lose their PHP lines too.</p>

<h2 id="cli">From the terminal</h2>
{sh("phun logs blog laravel", "phun logs blog queue --clear", "phun logs shop symfony")}
<p>The logs are <code>laravel</code>, <code>symfony</code>, <code>php</code>, <code>queue</code>, <code>schedule</code>, <code>reverb</code>, <code>messenger</code>, <code>npm</code>, <code>vite</code> and <code>tunnel</code>. Errors written to an application's log can also arrive as <a href="notifications.html">notifications</a>.</p>
'''


def technical_debt():
    return f'''
{{{{figure:technical-debt}}}}
<h2 id="notes">What your team noted</h2>
<p>Each application has a <strong>Technical Debt</strong> tab. It lists the work your team put off and noted in the code: unfinished work, needed fixes, workarounds, things needing attention and known bugs. Each item shows its file and line, who it is for and what it says, grouped by file. Filter by kind, or search. An application with nothing noted gets a small celebration instead.</p>

<h2 id="smells">What Phun finds</h2>
<p>Beside your team's notes, Phun lists:</p>
<ul>
<li>Unused imports, and formatting that does not match the application's own Pint when it has one. An application not formatted with its Pint shows as one item.</li>
<li>Debugging calls left in, errors caught and dropped, commented-out code and silenced warnings.</li>
<li>Very long functions and files, and, in Laravel, <code>env()</code> read outside a config folder.</li>
<li>A missing blank line after a variable, or a run of them, before the next statement.</li>
<li>Deprecated PHP, from PHP 8.1 to 8.5, saying whether it already warns on the application's PHP or only will on a newer one. Deprecated PHP shows as high severity, in red.</li>
<li>A <code>composer.json</code> that requires a PHP the application does not run on, or pins Composer to a different PHP.</li>
</ul>

<h2 id="comments">Comments that sound like debt</h2>
<p>Plain comments count too, not only TODO-style markers. Phun lists comments such as "for now", "hack", "quick fix", "not sure why", "don't touch", "we'll fix this later" and <code>@deprecated</code> as possible debt, each with a short reason.</p>

<h2 id="act">Act on an item</h2>
<p>Select an item to see its code with the line marked, then open the editor at that line or apply its fix. A <strong>Fix</strong> button makes the change where it is safe, such as a nullable parameter type, a cast's new name, a <code>${{}}</code> in a string or the missing blank line.</p>
<p>Fix works on one item, a whole file, or everything at once; <strong>Fix all</strong> asks first. It formats files, removes unused imports, updates deprecated PHP, and deletes commented-out code and leftover debugging calls. PHP is formatted with the application's Pint; without it, Phun offers to install Pint or formats with the editor's own formatter.</p>
<p>Each line names who last changed it, from git, and you can search by that name. Changes not committed yet say so.</p>

<h2 id="not-an-issue">Not an issue</h2>
<p>Mark an item <strong>Not an issue</strong> to hide it for everyone. The list is kept in <code>.phun/debt-dismissed.json</code> in the application, so committing it shares it with your team. A hidden item follows its line if the line moves, and comes back if the line changes.</p>

<h2 id="settings">What counts as debt</h2>
<p>The tab's settings, <strong>What counts as debt</strong>, are saved in <code>.phun/debt.json</code> so your team shares them:</p>
<ul>
<li>Turn any check or note marker off.</li>
<li>Add markers of your own, such as <code>REVIEW</code> or <code>@internal</code>, and phrases that make a plain comment possible debt, such as "slow query".</li>
<li>Set the limits for long functions, long files and commented-out code.</li>
<li>List files and folders not to check.</li>
<li>Run the application's own ESLint, with a <strong>Fix with ESLint</strong> button.</li>
</ul>

<h2 id="speed">Results</h2>
<p>The list shows straight away, while the application's own Pint runs beside it, and the tab says what it is still reading. Results stay when you leave the tab and come back; <strong>Read again</strong>, a fix or a new PHP version reads afresh.</p>
'''


# ── Phun itself ──────────────────────────────────────────────────────────
def updates():
    return f'''
{{{{figure:updates}}}}
<h2 id="update">Update Phun</h2>
<p><strong>Updates</strong> shows the version you run, checks for a new one and installs it from the app, with the release notes beside it. Open it from the command palette (<strong>Open Updates</strong>, or <strong>Check for updates</strong>). Phun also tells you about a new release with a notification. From the terminal:</p>
{sh("phun update         # check for a new Phun", "phun update --yes   # and install it")}
<p>On Arch Linux, Phun updates its package with pacman.</p>

<h2 id="beta">Beta updates</h2>
<p>The <strong>Beta updates</strong> switch in Updates offers new versions before their full release, while they are still being tested. Turn it off to wait for the next full release.</p>

<h2 id="rollback">Going back</h2>
<p>If the daemon will not start after an in-app update, its panel offers to go back to the version you had, for two weeks after the update. Phun downloads that release and installs it; your applications and settings stay as they are.</p>
<p>Updates also has a <strong>Previous version</strong> row with a <strong>Go back</strong> button. It installs the version your last update replaced, or else the release before the one you run, at any time, not only when the daemon fails to start.</p>
<p>Every older release in Updates has its own <strong>Go back to this</strong> button, so you can install any earlier version. It asks first, and keeps your applications, databases and settings.</p>

<h2 id="checksums">Checked before installing</h2>
<p>Every update is checked against the installer's checksum on GitHub before it installs. When a release is rebuilt under the same version number, such as a fixed beta, the checksums differ and Updates offers the version you run again.</p>

<h2 id="whats-new">What's new</h2>
<p>The release notes for each version are in Updates, as Features, Changed and Fixed. Every release is also on <a href="https://github.com/cloudcake/phun/releases">GitHub</a>.</p>

<h2 id="php-and-services">PHP, services and tools</h2>
<p>PHP versions, services and developer tools update on their own rows: Settings for PHP, Services for the rest. A download that hits a server hiccup tries again by itself.</p>
'''


def collaboration():
    return f'''
<h2 id="invite">Invite a teammate</h2>
<p>The <strong>Collaborate</strong> button in the title bar, or <strong>Collaborate: invite or join a teammate</strong> in the command palette, invites up to eight people into your Phun. Each one joins with a code.</p>
<p>The code works over the internet, through a temporary Cloudflare tunnel, and on your network or VPN alike: each invite offers your LAN and VPN addresses and the internet route, and your teammate's Phun tries them all at once. Phun fetches <code>cloudflared</code> itself when it is missing.</p>

<h2 id="let-in">Let them in</h2>
<ol class="steps">
<li><b>Check the code together</b><p>Before each person gets in, you and they check a six-digit code together.</p></li>
<li><b>Choose what they may do</b><p>From watching, through to editing code or opening terminals.</p></li>
<li><b>Work together</b><p>Everyone sees everyone's pointer, each in its own colour.</p></li>
</ol>
<p>You can change what each person may do, remove one, or end the session at any time.</p>

<h2 id="mirror">What a guest sees</h2>
<p>Each guest sees a live mirror of your window, dialogs and Settings included. Secrets such as <code>.env</code> files, keys and credentials stay hidden unless you allow them. Pointers sit on the same spot whatever size each window is, and a ring pings out wherever anyone clicks.</p>

<h2 id="permissions">What they may do</h2>
<p>Three presets cover most sessions: <strong>View only</strong>, <strong>Pair</strong>, which lets them click and type and run app actions, and <strong>Full control</strong>, which adds editing code, terminals and settings. Each permission is also a tick of its own:</p>
<ul>
<li><strong>Click and type</strong>: drive your window with their mouse and keyboard.</li>
<li><strong>App actions</strong>: start and stop applications and services, run jobs.</li>
<li><strong>Edit code</strong>: save files in the editor.</li>
<li><strong>Terminals</strong>: open shells and run Artisan, which is full shell access on your machine.</li>
<li><strong>Settings</strong>: change Phun and application settings.</li>
<li><strong>Destructive actions</strong>: delete applications, files, databases or data.</li>
<li><strong>Secrets</strong>: see what the mirror otherwise hides.</li>
</ul>
<p>A list at the bottom right shows who is here and who is driving. From it you switch someone between View, Pair and Full with one click, pause their clicks and keys (or everyone's) without removing them, or remove them.</p>

<h2 id="privacy">Privacy</h2>
<p>Everything between the Phuns is end-to-end encrypted.</p>
'''


def _cli_reference():
    """The README's command tables, as HTML."""
    with open(README, encoding="utf-8") as fh:
        text = fh.read()
    out = []
    for block in re.findall(r"<details>(.*?)</details>", text, re.S):
        summary = re.search(r"<summary><b>(.*?)</b>:\s*(.*?)</summary>", block)
        if not summary:
            continue
        rows = []
        for line in block.splitlines():
            if not line.startswith("| `"):
                continue
            cells = re.split(r"(?<!\\)\|", line.strip())[1:-1]
            if len(cells) != 2:
                continue
            rows.append(tuple(_md(c.strip()) for c in cells))
        title = summary.group(1)
        anchor = re.sub(r"[^a-z]+", "-", title.lower()).strip("-")
        body = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows)
        out.append(
            f'<h3 id="{anchor}">{html.escape(title)}</h3><p>{html.escape(summary.group(2))}</p>'
            f'<div class="table-wrap"><table><thead><tr><th>Command</th><th>What it does</th></tr></thead><tbody>{body}</tbody></table></div>'
        )
    return "".join(out)


def _md(cell):
    cell = cell.replace("\\|", "|")
    parts = re.split(r"(`[^`]+`)", cell)
    return "".join(
        f"<code>{html.escape(p[1:-1])}</code>" if p.startswith("`") else html.escape(p)
        for p in parts
    )


def cli():
    return f'''
{{{{figure:cli}}}}
<p>Everything the app does is also available from the terminal. The app and the command share one daemon, so a change in one shows in the other.</p>
{sh("phun link                    # serve the current folder at <folder>.test",
    "phun park ~/Code             # serve every project in a folder",
    "phun use blog <version>      # give blog.test its own PHP version",
    "phun secure blog             # serve blog.test over HTTPS",
    "phun share blog              # give blog.test a public URL",
    "phun status                  # what is running",
    "phun doctor fix              # check the setup and repair what it safely can")}
<p>To have <code>phun</code> on your PATH, choose it on the welcome screen or run <code>phun path install</code> from the app's own copy.</p>

<h2 id="json">For scripts and AI agents</h2>
<p>Every command takes <code>--json</code> for machine-readable output, and <code>phun help &lt;command&gt;</code> shows its options. <code>phun request '&lt;json&gt;'</code> sends any request to the daemon and prints its JSON reply.</p>
<p>With Phun's MCP server enabled in Settings › AI agents, or <code>phun settings mcp on</code>, <code>phun mcp</code> serves Phun's tools to AI agents over MCP, so agents such as Claude Code can list applications, switch PHP, create databases and read caught mail:</p>
{sh("claude mcp add --scope user phun -- phun mcp")}

<h2 id="reference">Every command</h2>
<p><code>&lt;app&gt;</code> is an application's name.</p>
{_cli_reference()}
'''


# ── More pages ───────────────────────────────────────────────────────────
def frameworks():
    return f'''
{{{{figure:framework-stack}}}}
<h2 id="stack">Your stack, recognised</h2>
<p>Every application shows its framework and the libraries it uses, with their versions: Laravel, Livewire, Filament, Vue, React, Svelte, Alpine.js, Inertia, Tailwind and Vite, plus Symfony, CodeIgniter, CakePHP, Slim, Drupal, Magento, Yii and WordPress. Versions come from what is installed, else from the version your project asks for.</p>

<h2 id="laravel">Laravel</h2>
<ul>
<li><strong>Queue workers</strong>, as many as you need, <strong>the scheduler</strong> and <strong>Reverb</strong>, each with its own log; see <a href="workers.html">Workers and processes</a>.</li>
<li><strong>Quick setup</strong>, a typical stack in one go; see <a href="quick-setup.html">Quick setup</a>.</li>
<li><strong>Artisan</strong> and <strong>Tinker</strong> in the dock; see <a href="terminals.html">Terminals and the dock</a>.</li>
<li><strong>Setup checks</strong> with a one-click fix: an <code>APP_URL</code> that is not the address Phun serves the application on, an empty <code>APP_KEY</code>, a missing public storage link, and a cache, session, queue or database pointing at a Phun service that is stopped or not installed.</li>
</ul>
{sh("phun queue enable blog --processes 2", "phun schedule enable blog", "phun reverb enable blog", "phun artisan blog migrate      # key-generate, storage-link, migrate or optimize-clear", "phun filament optimize blog")}

<h2 id="symfony">Symfony</h2>
<p>Phun writes a Symfony application's settings to <code>.env.local</code> and leaves <code>.env</code> for the defaults you commit; services added on the canvas write one DSN each. <code>bin/console</code> sits where Artisan does, with the command list and forms. Messenger workers consume the transports you choose (<code>async</code> by default) with process, time, memory and message limits, and Symfony's own log has its tab.</p>
{sh("phun new symfony shop --webapp", "phun messenger enable shop", "phun console shop cache:clear")}

<h2 id="wordpress">WordPress</h2>
<p>Create a WordPress site from Create, or <code>phun new wordpress</code>. Services are written into <code>wp-config.php</code>: MySQL or MariaDB, and Redis for the Redis Object Cache plugin. Turn on one-click admin sign-in under the application's Settings › HTTPS, or from the terminal:</p>
{sh("phun wordpress auto-login site on", "phun wordpress login-url site   # a one-time admin sign-in link", "phun wordpress users site")}

<h2 id="others">CodeIgniter, Drupal, Magento and more</h2>
<p>CodeIgniter gets its databases, Redis, Memcached and mail in its own <code>.env</code> settings. WordPress, CodeIgniter (with <code>codeigniter4/tasks</code>), Drupal (with Drush) and Magento get scheduled tasks from Infrastructure › Processes, which run the application's own cron command every minute, with its output in the application's logs and a notification when a run fails.</p>

<h2 id="html">HTML applications</h2>
<p>Create › HTML app makes a folder with an <code>index.html</code>, served as it is, from a plain page or a single-page app with a few client-side routes. Phun answers any path that is not a file with <code>index.html</code>, so reloading <code>/about</code> still works. No PHP version has to be installed and no PHP process starts; a request that needs PHP, such as a <code>.php</code> script or a POST, still goes to PHP.</p>

<h2 id="environment">The environment</h2>
<p>An application's Settings › Environment edits its <code>.env</code>; Phun hides values until you reveal them. <strong>Profiles</strong> are the <code>.env.&lt;name&gt;</code> files beside it (<code>.env.testing</code>, <code>.env.example</code> and so on): compare one with the current <code>.env</code> key by key and use it in its place, keeping the old one as <code>.env.backup</code> and clearing Laravel's cached config. <strong>Save current as</strong> writes a new profile.</p>
{sh("phun env blog MAIL_FROM_ADDRESS=hello@blog.test", "phun dotenv blog")}

<h2 id="npm">JavaScript</h2>
<p><code>phun js-install blog</code> installs an application's JavaScript dependencies with its own package manager, and <code>phun npm enable blog dev</code> keeps an npm script running beside it.</p>
'''


def sharing():
    return f'''
{{{{figure:share}}}}
<h2 id="quick">Share on a public URL</h2>
<p>An application's <strong>Sharing</strong> tab gives it a public HTTPS address on <code>trycloudflare.com</code> through a Cloudflare Quick Tunnel, for webhooks, demos and other devices, with no account needed. The address changes every time you start one, and anyone with it can reach the application while it is shared and Phun is running. It is for development, not production. Phun fetches <code>cloudflared</code> when it is missing.</p>
<ul>
<li><strong>A password and a time limit.</strong> A share can ask visitors for a password and close itself after an hour, a day or a week. People on your own machine are never asked.</li>
<li><strong>Who reached it.</strong> The Sharing tab lists visitors with their address, country, path and status.</li>
<li><strong>On your phone.</strong> A QR code opens the share with your phone's camera on any network, with nothing to install or trust. Pages opened through the share reload by themselves when the application's files change.</li>
</ul>
{sh("phun share blog", "phun share-access blog   # a password and time limit for the next share", "phun tunnel status", "phun tunnel stop blog")}

<h2 id="named">Your own hostname</h2>
<p>With a Cloudflare account, a named tunnel puts an application on a hostname of your own that stays the same:</p>
{sh("phun tunnel login", "phun tunnel create phun", "phun tunnel route phun blog.example.com", "phun tunnel set-host blog blog.example.com", "phun tunnel publish     # every application with a hostname goes online")}

<h2 id="domains">Domains and proxies</h2>
{{{{figure:domains-and-proxies}}}}
<p>Add subdomains and wildcards, proxy a <code>.test</code> name to a local port, or send one path, such as <code>/reverb</code>, to another server. Routing rules send unmatched URLs under a prefix to a file, such as <code>/api</code> to <code>api/index.php</code>.</p>
{sh("phun domain add blog api.blog.test", "phun proxy add vite http://localhost:5173", "phun route add blog /api api/index.php")}

<h2 id="lan">Other devices on your network</h2>
<p>Let phones, tablets and other computers on your network reach your <code>.test</code> applications, and make a one-time command that sets another device up to use them:</p>
{sh("phun lan enable", "phun remote-setup")}
<p>On macOS this needs <code>sudo phun elevate lan</code> once.</p>

<h2 id="no-admin">Without admin rights</h2>
<p>Every application is also reachable at <code>http://localhost/~name.test</code>, with no resolver or certificate needed.</p>
'''


def laravel_cloud():
    return f'''
{{{{figure:laravel-cloud}}}}
<h2 id="link">Link an application</h2>
<p>From a Laravel application's Infrastructure › Laravel Cloud, sign in with a Laravel Cloud API token and link the application to a Cloud application and environment. Phun installs the Laravel Cloud CLI as a tool and keeps no copy of your token.</p>

<h2 id="compare">See what Cloud is missing</h2>
<p>Phun compares the application's local infrastructure with the Cloud environment: database, cache, bucket, WebSockets, queue workers, scheduler, cron and PHP version. Create what Cloud is missing there, after confirming what Cloud bills for.</p>

<h2 id="deploy">Deploy</h2>
<p>Deploy from the same panel and follow the deployment's progress in Phun.</p>

<h2 id="bring-home">Bring a Cloud application home</h2>
<p>Create › Existing project › Laravel Cloud clones a Cloud application's repository and sets up the same infrastructure locally.</p>
<p>Laravel Cloud is offered only on Laravel applications.</p>
'''


def databases():
    return f'''
{{{{figure:database-browser}}}}
<h2 id="add">Add a database</h2>
<p>On an application's Infrastructure canvas, <strong>Database</strong> asks which engine: MySQL, MariaDB, PostgreSQL, SQLite or MongoDB. Phun installs and starts it, writes the connection into the application's settings and creates the database. A second engine gets its own prefixed block (<code>DB_PGSQL_HOST</code> and so on, <code>MONGODB_URI</code>, or <code>DB_SQLITE_DATABASE</code>), so it never shares <code>DB_HOST</code> with the first, and its card shows the connection name to use in <code>config/database.php</code>. A Laravel application on SQLite keeps its database at <code>database/database.sqlite</code>.</p>

<h2 id="browse">Browse and query</h2>
<p>A database card opens the database browser. One grid shows a page of the picked table or what the last statement returned, and the SQL box starts with a query for that table and completes tables and columns. For MySQL, MariaDB and PostgreSQL.</p>

<h2 id="schema">Draw your schema</h2>
{{{{figure:schema-canvas}}}}
<p>For a Laravel application the database card offers <strong>Open Schema</strong>. It reads every table, column and foreign key and the relationships the models declare, and draws them as blueprints: drag to pan, {k("Ctrl")} and the wheel to zoom. Draw a relationship by dragging one model onto another, change or remove one from its line, or accept one a foreign key suggests. Changes show as a diff of each model file and are written only when you apply them.</p>

<h2 id="cli">From the terminal</h2>
{sh("phun db list mysql", "phun db create mysql blog", "phun db provision blog          # the database blog's .env names", "phun db backup mysql blog blog.sql", "phun db restore mysql blog blog.sql", "phun db query mysql blog 'select count(*) from users'")}
'''


def mail_storage():
    return f'''
{{{{figure:mail}}}}
<h2 id="mail">Every email, caught</h2>
<p>Phun catches every email your applications send, so nothing reaches a real inbox. The Mail viewer ({k("Ctrl", "5")}, or Services › Mail) reads each message rendered, as its plain-text part, or as the raw source exactly as the application sent it, with a Copy button. New mail can arrive as a desktop notification.</p>
<p>Applications are wired to it when you add mail on the Infrastructure canvas.</p>
{sh("phun mail list", "phun mail show <id>", "phun mail clear", "phun mail port 2525")}

<h2 id="storage">S3-compatible storage</h2>
{{{{figure:object-storage}}}}
<p>Phun serves object storage on <code>http://127.0.0.1:19000</code>, with buckets and files kept in Phun's data folder. Add <strong>Object storage</strong> to a Laravel application from its Infrastructure canvas and Phun creates its bucket and fills in its settings, so the <code>s3</code> disk works as it would against S3: uploads, downloads, listing, copying, deleting, multipart uploads and temporary URLs.</p>
<p>The bucket browser on the Services page creates and deletes buckets, makes them public or private, and opens, reveals or deletes files. The port can be changed in Settings, and the server turned off.</p>
{sh("phun storage buckets", "phun storage create-bucket uploads --private", "phun storage access uploads public", "phun storage install-driver blog   # Laravel's S3 driver")}
'''


def debugging():
    return f'''
{{{{figure:debugging}}}}
<h2 id="xdebug">Step through a request</h2>
<p>Xdebug comes with Phun, so there is nothing to install. In the code editor, the bug button turns it on for the application. Click beside a line number to set a breakpoint, load the page, and it stops there with the line highlighted. The panel under the editor steps over ({k("F8")}), into ({k("F7")}) and out ({k("Shift", "F8")}), continues on {k("F9")} ({k("Cmd", "Alt", "R")} on macOS), shows the stack and opens arrays and objects in the variables.</p>
<p>Breakpoints are remembered, and breakpoints in a listed package count too, so you can stop inside a package an application uses.</p>
{sh("phun debug blog on     # Xdebug on port 9003", "phun debugging         # what is being debugged")}

<h2 id="tests">Debug a test</h2>
<p>A test file's run markers can debug a single Pest test or PHPUnit method, stopping at your breakpoints. {k("Ctrl", "Shift", "F9")} debugs the test at the cursor ({k("Ctrl", "Shift", "D")} on macOS).</p>

<h2 id="profile">Profile a request</h2>
<p>A logged request on the Metrics tab has a <strong>Profile</strong> button. Phun sends it again with Xdebug tracing it and shows where the time went as a flame graph, with the application's code, packages and PHP's own functions in their own colours; click a call to look inside it. Every database query the request ran is listed, and a query run three times or more from one line is marked as a likely N+1, with its line, or the Blade view it came from, a click away in the editor.</p>
{sh("phun profile blog on   # trace requests that carry the XDEBUG_TRACE cookie")}

<h2 id="exceptions">Exceptions</h2>
<p>Every file and line in a stack trace in an application's log opens the editor at that line, and the Logs panel's <strong>Exceptions</strong> button lists each exception once with how often it was thrown and when last.</p>
'''


def metrics():
    return f'''
{{{{figure:metrics}}}}
<h2 id="charts">Metrics</h2>
<p>An application's <strong>Metrics</strong> tab charts its requests, response times, errors, memory and CPU as they happen.</p>
{sh("phun metrics blog     # request counts per minute, last 24 hours", "phun activity         # requests each application served, by status")}

<h2 id="requests">The request inspector</h2>
{{{{figure:request-inspector}}}}
<p>The newest two hundred requests, with their status, timing, query string and a few headers, a filter, an errors-only switch and Clear. Cookies, authorization headers and bodies are never kept. A request opens with a click, {k("Enter")} or {k("Space")}, and can be:</p>
<ul>
<li><strong>Replayed</strong>, signed out and without a body, since Phun keeps neither.</li>
<li><strong>Copied</strong> as a <code>curl</code> command.</li>
<li><strong>Shown with its log lines</strong>, what the application wrote while it ran.</li>
<li><strong>Profiled</strong>; see <a href="debugging.html#profile">Profile a request</a>.</li>
</ul>
{sh("phun requests blog")}

<h2 id="endpoints">Endpoints</h2>
<p>A table of the endpoints the application has served: the method, the path and how many times it was hit, with its errors, average response time and when it was last hit. Sort by any heading, filter by path, and clear the counts. Query strings are left out, so <code>/search?q=a</code> and <code>/search?q=b</code> are one endpoint.</p>
{sh("phun endpoints blog", "phun endpoints blog --clear")}
'''


def security():
    return f'''
{{{{figure:dependency-audits}}}}
<h2 id="audit">Dependency audits</h2>
<p>An application's <strong>Security</strong> tab audits its Composer and JavaScript dependencies: how far behind each package is, and the known advisories against it, with a card per package manager.</p>
{sh("phun security scan blog")}

<h2 id="wait">Wait before installing</h2>
<p>Brand-new releases are where supply-chain attacks land. <strong>Wait before installing</strong> makes package managers hold off on releases younger than the days you choose. For Composer it uses Composer's own cooldown setting, <code>config.policy.cooldown</code> in <code>composer.json</code> (Composer 2.11 and newer), so it works for any Composer application.</p>
{sh("phun security wait blog on --days 7")}

<h2 id="packages">Composer packages</h2>
<p>The Security tab lists every package <code>composer.json</code> requires, with its constraint, its installed and newest versions and its advisories, and a button to update it, upgrade it to a new major or remove it. Add packages from the same card. Every change runs Phun's Composer on the application's PHP.</p>
{sh("phun packages list blog", "phun packages require blog spatie/laravel-data", "phun packages update blog laravel/framework")}

<h2 id="update-all">Update all, and go back</h2>
<p><strong>Update all</strong> updates every Composer and JavaScript package within the versions your project allows (no new major versions), still waiting out new releases if Wait before installing is on, and lists what moved. The lock files are saved first: <strong>Restore previous versions</strong> puts them back and reinstalls.</p>
{sh("phun security update blog", "phun security restore blog")}
'''


def diagnostics():
    return f'''
{{{{figure:health-checks}}}}
<h2 id="checks">Health checks</h2>
<p><strong>Diagnostics</strong>, on the Overview ({k("Ctrl", "3")}), runs Phun's checks for DNS, certificates, ports and PHP, each with a one-click fix when something is off. The palette can run the safe fixes too.</p>
{sh("phun status       # the daemon, ports, DNS, certificates and PHP at a glance", "phun doctor", "phun doctor fix")}

<h2 id="report">A problem report</h2>
{{{{figure:diagnostics-report}}}}
<p>Diagnostics › Report gathers what a bug report needs in one file: versions, services, Phun's processes, a <code>.test</code> lookup, health checks and recent logs. Passwords, tokens, keys, email addresses, share links, card or ID numbers and your user name are removed before you see it. Copy it, or Save file puts it in Downloads. Copy diagnostics on the daemon panel is redacted the same way. Problems and ideas are welcome in <a href="https://github.com/cloudcake/phun/discussions">Discussions</a>.</p>

<h2 id="daemon">When the daemon will not start</h2>
<p>Phun checks, stops what is left and starts it directly. Copy diagnostics lists every start attempt with its time, so a report shows what was tried. After an in-app update, the daemon's panel can also go back to the version you had; see <a href="updates.html#rollback">Going back</a>.</p>
{sh("phun ping", "phun restart daemon")}

<h2 id="notifications">Notifications</h2>
<p>What happens in the background arrives as a desktop notification, even with the window closed; see <a href="notifications.html">Notifications</a>.</p>
'''


def notifications():
    return f'''
{{{{figure:notifications}}}}
<h2 id="what">What arrives</h2>
<p>Phun tells you about what happens in the background with a desktop notification, even with its window closed:</p>
<ul>
<li>Queued jobs finishing or failing, Messenger messages handled or given up on, and scheduled tasks running or failing.</li>
<li>Caught mail, and errors in an application's log.</li>
<li>A service or worker stopping.</li>
<li>Installs and new applications finishing or failing, and shares ending.</li>
<li>A new Phun release.</li>
</ul>
<p>A burst of one kind becomes one notification, such as "5 jobs finished in blog".</p>

<h2 id="settings">Choose what you hear about</h2>
<p>Settings › Notifications turns each kind on or off. Scheduled tasks that succeed start switched off, since a task that runs every minute would notify every minute. <strong>Send a test notification</strong> checks that your system shows them.</p>
<ul>
<li><strong>Do not disturb</strong> silences every notification until you turn it off.</li>
<li><strong>Play a sound</strong> plays Phun's own short chime with each one. On Windows it stays quiet while Windows is holding notifications back.</li>
</ul>

<h2 id="events">From the terminal</h2>
<p>The same events are kept by the daemon, so you can read what happened while you were away:</p>
{sh("phun events      # the recent background events")}
'''


def palette():
    return f'''
{{{{figure:command-palette}}}}
<h2 id="palette">The command palette</h2>
<p>{k("Ctrl", "K")} ({k("Cmd", "K")} on macOS), or <strong>Search commands</strong> in every page header, opens a search box for the whole app:</p>
<ul>
<li>Type an application's name to open it, its Artisan, Console, Tinker or Logs, its tabs, or copy its local URL.</li>
<li>Start, stop or restart any service; install, update or remove developer tools; make a PHP version the default or restart its pools.</li>
<li>Create or clone an application, run the diagnostics or their safe fixes, jump to any Settings section, and open Updates.</li>
<li><strong>Run again</strong> lists the Artisan commands you ran recently in each application, and <strong>Recent</strong> what you used last.</li>
</ul>
<p>Matching is forgiving: "tnkr" finds Tinker.</p>

<h2 id="keys">Key binds</h2>
{{{{figure:key-binds}}}}
<p>Settings › Key binds gives any action in the command palette a key of your own, plus the dock's actions for the application you are on. Press a key cap to record. Phun asks before taking a key another action has, refuses keys that typing needs, and can clear or reset each one. {k("Ctrl", "/")} shows every shortcut.</p>
<div class="table-wrap"><table><thead><tr><th>Keys</th><th>What they do</th></tr></thead><tbody>
<tr><td>{k("Ctrl", "K")}</td><td>The command palette</td></tr>
<tr><td>{k("Ctrl", "1")} to {k("Ctrl", "4")}</td><td>Overview, Services, Diagnostics, Settings</td></tr>
<tr><td>{k("Ctrl", "5")}</td><td>Mail</td></tr>
<tr><td>{k("Ctrl", ",")}</td><td>Settings</td></tr>
<tr><td>{k("Ctrl", "Shift", "L")}</td><td>Switch between light and dark</td></tr>
<tr><td>{k("Ctrl", "Shift", "R")}</td><td>Restart the daemon</td></tr>
<tr><td>{k("Ctrl", "Shift", "Right")} and {k("Ctrl", "Shift", "Left")}</td><td>Next and previous application, in the Overview's order, on the same tab ({k("Ctrl")} on macOS too)</td></tr>
<tr><td>{k("Ctrl", "Up")}</td><td>Hide or show the dock ({k("Ctrl")} on macOS too)</td></tr>
<tr><td>{k("`")}</td><td>Open or close the Console for the application you are on</td></tr>
<tr><td>{k("Shift", "`")}</td><td>Its next open terminal</td></tr>
<tr><td>{k("Ctrl", "/")}</td><td>Every shortcut</td></tr>
</tbody></table></div>
<p>On macOS, {k("Cmd")} takes the place of {k("Ctrl")}.</p>

<h2 id="themes">Themes</h2>
{{{{figure:themes}}}}
<p>Daybreak and Nightfall, or follow the system, under Settings › Appearance. The choice reaches every window, the terminals and the editor. When your system asks for reduced motion, nothing in Phun slides, pulses or spins.</p>
'''


def ai_agents():
    return f'''
{{{{figure:mcp}}}}
<h2 id="mcp">An MCP server for AI agents</h2>
<p>Phun can serve its tools to AI coding agents on your machine over MCP, the Model Context Protocol, so agents such as Claude Code can list your applications, switch PHP, create databases and read caught mail.</p>
<ol class="steps">
<li><b>Turn it on</b><p>Settings › AI agents › <strong>Enable Phun's MCP server</strong>, or <code>phun settings mcp on</code>.</p></li>
<li><b>Register Phun with your agent</b><p>The same section registers Phun with your agent. For Claude Code by hand:</p>
{sh("claude mcp add --scope user phun -- phun mcp")}</li>
</ol>

<h2 id="cli">The command line, for agents and scripts</h2>
<p>Every <code>phun</code> command takes <code>--json</code>, and <code>phun request '&lt;json&gt;'</code> sends any request to the daemon and prints its JSON reply. <code>phun editor</code> reads, writes, searches, formats and refactors an application's files the way the app's code editor does; see <a href="cli.html#code">the command reference</a>.</p>
'''


PAGES = {
    "install": dict(title="Install", icon="developer-tools", summary="Download Phun for macOS, Windows or Linux and get it running.",
                    lede="Phun is one desktop app for macOS, Linux and Windows, with a small background service and the <code>phun</code> command.", body=install),
    "first-launch": dict(title="First launch", icon="https", summary="The welcome steps: the daemon, PHP and trust, then finding your way.",
                         lede="A few quick steps get your local PHP environment running. Only one of them asks for your password.", body=first_launch),
    "create": dict(title="Creating applications", icon="new-application", summary="Start a Laravel, WordPress, Symfony or HTML application, or clone one.",
                   lede="Start a new application from a framework's starter, or bring one in from Git or Laravel Cloud, and Phun serves it straight away.", body=create),
    "applications": dict(title="Linking and parking", icon="link-and-park", summary="Serve a folder, or every project in one, at its own .test address.",
                         lede="Link a folder, or park a whole directory, and every project in it is served at <code>name.test</code> over trusted HTTPS.", body=applications),
    "php": dict(title="PHP versions", icon="php-versions", summary="Several PHP versions side by side, one per application.",
                lede="Several PHP versions side by side, each with its own <code>php.ini</code> settings and extensions, and each application on the one it needs.", body=php),
    "quick-setup": dict(title="Quick setup", icon="services", summary="A typical Laravel stack in one go, with every change shown first.",
                        lede="Pick a typical Laravel stack and Phun shows what it will add, change, keep or turn off before it touches anything.", body=quick_setup),
    "workers": dict(title="Workers and processes", icon="laravel-workers", summary="Queue workers, the scheduler, Reverb, Messenger and scheduled tasks.",
                    lede="Queue workers, the scheduler, Reverb, Messenger and cron run beside each application, watched by Phun.", body=workers),
    "developer-tools": dict(title="Developer tools and Node.js", icon="developer-tools", summary="Composer, Node.js, Bun, Chrome for Testing and Node.js versions side by side.",
                            lede="Composer, Node.js, Bun and the rest install from Phun when you need them, and every project gets the Node.js version it asks for.", body=developer_tools),
    "services": dict(title="Services and infrastructure", icon="infrastructure", summary="Databases, cache, search, mail and storage on the infrastructure canvas.",
                     lede="Databases, cache, search, mail and storage run beside your applications as native processes, and the infrastructure canvas wires them in.", body=services),
    "editor": dict(title="The code editor", icon="highlighting", summary="Completion that knows Laravel, live checks, refactors, git, tests and debugging.",
                   lede="A code editor inside Phun that knows your application: completion, live PHP checks, refactors, formatting, git, tests and Xdebug.", body=editor),
    "git": dict(title="Git", icon="git", summary="Changes, branches, the log graph, worktrees and LFS in the editor.",
                lede="Stage, commit, branch, pull and read the history without leaving the code editor.", body=git),
    "logs": dict(title="Logs", icon="problems", summary="Every log in one list, with filters, stack traces and exceptions.",
                 lede="Every log an application writes, in one list you can filter and search, with stack traces that open the editor.", body=logs),
    "terminals": dict(title="Terminals and the dock", icon="terminal-dock", summary="Artisan, Console, Tinker and Logs at the bottom of the window.",
                      lede="Artisan, a console, Tinker and every log, in a dock at the bottom of the window, a key away.", body=terminals),
    "technical-debt": dict(title="Technical Debt", icon="technical-debt", summary="The work your team put off, the code smells and the deprecated PHP, with fixes.",
                           lede="The work your team put off and noted in the code, beside the code smells and deprecated PHP Phun finds, with a fix where one is safe.", body=technical_debt),
    "frameworks": dict(title="Frameworks", icon="framework-stack", summary="Laravel, Symfony, WordPress, CodeIgniter and HTML applications, and their settings.",
                       lede="Phun knows each framework: its workers, its console, where it reads its settings, and the libraries it uses.", body=frameworks),
    "sharing": dict(title="Sharing and the network", icon="share", summary="A public URL, your own hostname, domains, proxies and other devices.",
                    lede="Share an application on a public URL, give it a hostname of your own, or open it on the devices around you.", body=sharing),
    "laravel-cloud": dict(title="Laravel Cloud", icon="laravel-cloud", summary="Link, compare, create and deploy, or bring a Cloud application home.",
                          lede="Link a Laravel application to Laravel Cloud, create what Cloud is missing and deploy, or bring a Cloud application home with the same infrastructure.", body=laravel_cloud),
    "databases": dict(title="Databases", icon="database-browser", summary="MySQL, MariaDB, PostgreSQL, SQLite and MongoDB, browsed and drawn.",
                      lede="Add a database in a click, browse any table, write SQL that completes, and draw a Laravel schema.", body=databases),
    "mail-storage": dict(title="Mail and storage", icon="mail", summary="Every email caught, and S3-compatible storage on your machine.",
                         lede="Every email your applications send, caught and readable, and S3-compatible object storage beside them.", body=mail_storage),
    "debugging": dict(title="Debugging and profiling", icon="debugging", summary="Xdebug breakpoints in the editor, and a flame graph of any request.",
                      lede="Set a breakpoint, load the page and step through it, or profile a request to see where the time went.", body=debugging),
    "metrics": dict(title="Metrics and requests", icon="metrics", summary="Charts, the request inspector, replays and endpoints.",
                    lede="See what each application does: its requests, response times, errors, memory and CPU, and every recent request.", body=metrics),
    "security": dict(title="Security and packages", icon="dependency-audits", summary="Dependency audits, a wait before new releases, and Composer packages.",
                     lede="Audit an application's dependencies, wait out brand-new releases, and manage its Composer packages.", body=security),
    "diagnostics": dict(title="Diagnostics", icon="health-checks", summary="Health checks with fixes, a redacted report, and a daemon that won't start.",
                        lede="Health checks with a fix for each, a problem report with the secrets taken out, and what to do when the daemon will not start.", body=diagnostics),
    "notifications": dict(title="Notifications", icon="notifications", summary="Desktop notifications for jobs, mail, errors and more, with a chime.",
                          lede="What happens in the background arrives as a desktop notification, even with the window closed.", body=notifications),
    "palette": dict(title="Palette, keys and themes", icon="command-palette", summary="The command palette, key binds of your own, and Daybreak and Nightfall.",
                    lede="Every page, application and action a few keystrokes away, on keys of your own, in the theme you like.", body=palette),
    "ai-agents": dict(title="AI agents", icon="mcp", summary="An MCP server so agents such as Claude Code can work with Phun.",
                      lede="Let AI coding agents on your machine manage Phun over MCP.", body=ai_agents),
    "updates": dict(title="Updates and rollback", icon="updates", summary="Update Phun from the app, try betas, and go back if a version gives you trouble.",
                    lede="Phun checks for new versions and installs them from the app, with the release notes beside them.", body=updates),
    "collaboration": dict(title="Collaboration", icon="share", summary="Invite teammates into your Phun, end-to-end encrypted.",
                          lede="Invite teammates into your Phun over the internet or your network, and choose what each one may do.", body=collaboration),
    "cli": dict(title="The phun command", icon="cli", summary="Link, park, secure, share and switch PHP from your terminal.",
                lede="Link, park, secure, share and switch PHP from your terminal. Everything the app does, the command does too.", body=cli),
}


def page(slug):
    return PAGES[slug]
