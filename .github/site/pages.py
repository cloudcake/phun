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
    "Phun runs your apps on your own machine: PHP, Node.js, C#, Go, Rust and Python. Every web app you add is served at its own "
    "<code>.test</code> address over trusted HTTPS, with the PHP version or toolchain it needs, and the "
    "databases, cache, search and mail it uses run beside it as native processes. It is one desktop app with a small background "
    "service and a <code>phun</code> command for the terminal. No Docker, no virtual machine, and no password "
    "for everyday work."
)

NAV = (
    ("Get started", ("install", "first-launch")),
    ("Applications", ("applications", "create", "projects", "frameworks", "php", "sharing")),
    ("Services", ("services", "quick-setup", "workers", "databases", "mail-storage", "developer-tools")),
    ("Working in Phun", ("editor", "git", "debugging", "terminals", "logs", "technical-debt", "issues")),
    ("Insight", ("metrics", "request-graph", "security", "diagnostics", "notifications")),
    ("You and Phun", ("account", "profiles", "community", "extensions")),
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
<p>Phun is ready. This step also offers <strong>Connect GitHub</strong> for the extras (your profile, achievements, leaderboards, Issues boards, settings sync and the extension hub) and a place for an invite code. Both are optional.</p></li>
</ol>
<p><strong>Back</strong> goes to the previous step, and the PHP step has <strong>Skip for now</strong>.</p>

<h2 id="no-admin">Without admin rights</h2>
<p>No admin rights to hand? Every application is also reachable at <code>http://localhost/~name.test</code>, with no resolver or certificate needed.</p>

<h2 id="finding-your-way">Finding your way</h2>
<ul>
<li><strong>The tabs.</strong> Community, Applications, Services, Extensions and Settings. Phun opens on <strong>Community</strong>: <strong>Around Phun</strong>, what Phun users with a public profile reached lately and new releases, beside the leaderboards and Discussions; see <a href="community.html">Community</a>.</li>
<li><strong>The header.</strong> The <strong>Daemon</strong> menu restarts or stops the background service and opens <strong>Diagnostics</strong>. <strong>Updates</strong> and <strong>Bug reports</strong> sit beside it.</li>
<li><strong>The title bar.</strong> The Account button, <strong>Search commands</strong>, the notifications bell and <strong>Collaborate</strong>.</li>
<li><strong>Your user card</strong>, at the top right, opens your <a href="profiles.html">profile</a>; its menu switches GitHub accounts and opens <a href="account.html">Account</a>.</li>
<li><strong>Keys.</strong> {k("Ctrl", "1")} to {k("Ctrl", "7")} open Community, Applications, Services, Diagnostics, Bug reports, Settings and Mail ({k("Cmd")} on macOS).</li>
<li><strong>The command palette</strong>, {k("Ctrl", "K")} ({k("Shift", "Cmd", "K")} on macOS), reaches every page, application, Artisan command and action. Matching is forgiving: "tnkr" finds Tinker.</li>
<li><strong>Themes and key binds</strong> live in Account › Appearance and Account › Key binds.</li>
<li><strong>The tray.</strong> Closing the window keeps Phun running in the tray, with the daemon's state and Start, Restart and Stop.</li>
</ul>

<h2 id="health">When something is off</h2>
<p>Diagnostics, in the header's Daemon menu, runs Phun's health checks for DNS, certificates, ports and PHP, each with a one-click fix. From the terminal:</p>
{sh("phun doctor       # check the setup", "phun doctor fix   # repair what it safely can")}
<p>Diagnostics › Report gathers what a problem report needs in one file: versions, services, Phun's processes, a <code>.test</code> lookup, health checks and recent logs. Passwords, tokens, keys, email addresses and your user name are removed before you see it.</p>
'''


# ── Applications ─────────────────────────────────────────────────────────
def applications():
    return f'''
{{{{figure:link-and-park}}}}
<h2 id="link">Link a folder</h2>
<p>Linking serves one folder as an application at <code>&lt;name&gt;.test</code>. In the app, choose Create on the Applications tab, then <strong>Existing project</strong>, and pick the folder. From the terminal, in the project's folder:</p>
{sh("phun link                 # serve this folder at <folder>.test", "phun link blog ~/Code/blog  # or name it and point at it")}
<p>The web root, such as <code>public</code>, is found for you. To set it yourself use <code>phun root &lt;app&gt; public</code>, and <code>--auto</code> to go back to detecting it.</p>

<h2 id="park">Park a directory</h2>
<p>Parking serves every project inside a folder, each at its own <code>.test</code> name, including projects you add to it later. Choose Create, then <strong>Park</strong>, or:</p>
{sh("phun park ~/Code", "phun unpark ~/Code   # linked applications stay", "phun list parked")}

<h2 id="create">Start something new</h2>
<p>Create makes an application and serves it: a PHP framework, a Node.js, C#, Go, Rust or Python project, a Unity game or an HTML app. <strong>Existing Project</strong> brings in a folder on this computer or clones a Git repository. <a href="create.html">Creating applications</a> goes through each one.</p>
{sh("phun new symfony shop --webapp", "phun new git blog --url git@github.com:acme/blog.git")}
<p>The Applications tab is just your applications, with <strong>Filter by name</strong> at the top. Rename one from its card or its page; its address stays the same.</p>

<h2 id="page">An application's page</h2>
<p>Click an application to open its page. The header has:</p>
<ul>
<li><strong>Open</strong>: the code editor, the browser and the folder. A WordPress application also has <strong>WP Admin</strong>.</li>
<li><strong>Terminal</strong>: Artisan, Console, Tinker and Logs, and AI agents such as Claude Code; see <a href="terminals.html">Terminals and the dock</a>.</li>
<li><strong>Tools</strong>: Sharing, Dependencies, the Live Request Graph, Trailed Request and Event Chains, where they apply.</li>
<li><strong>Settings</strong>, always last.</li>
</ul>
<p>The tabs, each where it applies:</p>
<ul>
<li><strong>Project</strong>: for Node.js, C#, Go, Rust, Python and Unity projects, their toolchain and actions; see <a href="projects.html">Node.js, C#, Go, Rust and Python</a>.</li>
<li><strong>Metrics</strong>: requests, response times, errors and the HTTP requests by endpoint; see <a href="metrics.html">Metrics and requests</a>.</li>
<li><strong>Infrastructure</strong>: the canvas of its services; see <a href="services.html">Services</a>.</li>
<li><strong>Schedule</strong> and <strong>Queue</strong>: for Laravel; see <a href="workers.html#schedule-tab">Workers and processes</a>.</li>
<li><strong>Technical Debt</strong>: see <a href="technical-debt.html">Technical Debt</a>.</li>
<li><strong>Issues</strong>: a board of issues and sticky notes for the application; see <a href="issues.html">Issues</a>.</li>
</ul>
<p>The Tools menu opens <a href="sharing.html">Sharing</a>, <a href="security.html">Dependencies</a> and the <a href="request-graph.html">Live Request Graph, Trailed Request and Event Chains</a>.</p>
<p><strong>Settings</strong> has a tab for each part down the side: under Application, <strong>General</strong> (group, path, URL, web root and, for WSL, ownership and networking), <strong>HTTPS</strong> and <strong>Environment variables</strong>; under Runtime, <strong>PHP</strong> and <strong>Node.js</strong>. See <a href="frameworks.html#environment">The environment</a>.</p>
<p>Every application shows its framework and the libraries it uses, with their versions. When its setup is wrong, such as an <code>APP_URL</code> that is not the address Phun serves it on or an empty <code>APP_KEY</code>, the page lists it with a one-click fix.</p>

<h2 id="https">HTTPS and domains</h2>
<p>Every application is served over HTTPS with a certificate from Phun's local certificate authority, trusted by your browsers; there is nothing to switch on. Add subdomains and wildcards, proxy a <code>.test</code> name to a local port, or send one path, such as <code>/reverb</code>, to another server:</p>
{sh("phun domain add blog api.blog.test", "phun proxy add reverb http://localhost:8080")}
<p>An HTML application is served straight from its folder, with no PHP version needed. Hidden files such as <code>.env</code> and <code>.git</code> are never served from any application.</p>

<h2 id="share">Share on a public URL</h2>
<p>Tools › Sharing gives an application a public HTTPS address through Cloudflare; see <a href="sharing.html">Sharing and the network</a> for passwords, time limits, your own hostname and other devices.</p>

<h2 id="groups">Groups and packages</h2>
<p><strong>Groups</strong> keep the Applications tab tidy: put applications in a group, order the groups, add a group folder, served like a parked one, and turn a whole group on or off from its heading. A <strong>package</strong> is a Composer package or repository your applications use, listed under a group (Create › Package). It opens in the code editor with its own dock badge and is never served.</p>
{sh("phun group create Clients", "phun group assign blog Clients")}

<h2 id="instances">More than one instance</h2>
<p>An application can run extra instances behind a load balancer, for scaling locally, and choose which one runs the scheduler.</p>
{sh("phun instance add blog", "phun instance list blog", "phun instance schedule blog <instance> on")}
'''


def create():
    return f'''
{{{{figure:new-application}}}}
<h2 id="menu">The Create menu</h2>
<p><strong>Create</strong>, on the Applications tab, holds everything that adds an application:</p>
<ul>
<li><strong>Existing Project</strong>: a folder on this computer, or a Git repository Phun clones.</li>
<li><strong>Park</strong>, <strong>Group</strong> and <strong>Package</strong>; see <a href="applications.html">Linking and parking</a>.</li>
<li><strong>PHP</strong>: <strong>Laravel</strong>, <strong>WordPress</strong>, <strong>Symfony</strong>, <strong>CodeIgniter</strong>, <strong>CakePHP</strong> and <strong>Slim</strong>.</li>
<li><strong>JavaScript</strong>: <strong>Node.js</strong> and <strong>HTML app</strong>.</li>
<li><strong>C#</strong>: <strong>.NET</strong> and <strong>Unity</strong>.</li>
<li><strong>Go</strong>, <strong>Rust</strong> and <strong>Python</strong>.</li>
</ul>
<p>Each PHP starter asks for a name, a folder and the PHP version the application runs on, and says when a version is too old for the framework. It checks first for what it needs, such as Composer or the Laravel installer, offers to install what is missing, then shows each step as it runs. Node.js, C#, Go, Rust, Python and Unity have <a href="projects.html">a page of their own</a>.</p>

<h2 id="existing">Existing Project</h2>
<p>Pick <strong>On this computer</strong> and a folder, and Phun looks at what it holds before adding it:</p>
<ul>
<li>A Composer or published npm package is added as a <strong>package</strong>, not served.</li>
<li>A Node.js, C#, Go, Rust or Python project is added as one, not as PHP.</li>
<li>A project that has not installed its packages yet gets them installed.</li>
<li>On Windows, a folder inside WSL, such as <code>\\\\wsl.localhost\\Ubuntu\\home\\you\\blog</code>, runs its PHP inside WSL. When its files belong to a different Linux user, Phun says so and offers <strong>Fix ownership</strong>.</li>
</ul>

<h2 id="github">Put it on GitHub</h2>
<p>The last step of each starter can create a GitHub repository for the new application, under your account or an organisation where Phun's GitHub app is installed, private or public. Once the application is ready, Phun creates the repository, makes the folder a git repository with a first commit if it is not one yet, and pushes it. Phun signs that push in with your GitHub sign-in for that one command; nothing is saved in the repository. Signed out, the same place offers to sign in to GitHub first.</p>

<h2 id="laravel">Laravel</h2>
<p>The Laravel starter runs the Laravel installer with the choices it would ask in a terminal:</p>
<ul>
<li><strong>Template</strong>: <strong>Full Stack</strong>, the regular Laravel app; <strong>Filament</strong>, which adds the latest Filament with an admin panel at <code>/admin</code> (add a user to sign in with <code>php artisan make:filament-user</code>); or <strong>Micro Service</strong>, an API with no frontend: no <code>package.json</code>, Vite, frontend resources or npm scripts, and its classes in <code>service/</code> under the <code>Service\\</code> namespace instead of <code>app/</code>. When git is on, the template's changes are committed after Laravel's first commit.</li>
<li><strong>Starter kit</strong>: none, React, Vue, Livewire or Svelte, or a community kit by its package name.</li>
<li><strong>Authentication</strong>: Laravel's built-in or WorkOS AuthKit, with team support, and standalone class components for Livewire.</li>
<li><strong>Frontend dependencies</strong>: install and build with npm or Bun, or skip them for later. Node.js or Bun is installed for you when missing.</li>
<li><strong>Testing</strong>: Pest or PHPUnit.</li>
<li><strong>Database</strong>: SQLite, MySQL, MariaDB, PostgreSQL or SQL Server.</li>
</ul>

<h2 id="wordpress">WordPress</h2>
<p>Choose the core version, the locale, the application title and the admin account, and the database name and table prefix. Phun creates the database in MySQL or MariaDB, downloads WordPress, writes <code>wp-config.php</code> and runs the install; see <a href="frameworks.html#wordpress">WordPress</a> for signing in.</p>

<h2 id="others">Symfony, CodeIgniter, CakePHP and Slim</h2>
<p>These start from each framework's own Composer skeleton. Symfony has a <strong>Web application</strong> switch for Twig, Doctrine, forms, security, mailer and Messenger; leave it off for the minimal skeleton, as for an API. Flex's Docker files are left out, mail goes to Phun's capture, and a web application starts on SQLite, all in <code>.env.local</code>.</p>

<h2 id="html">HTML app</h2>
<p>A folder with an <code>index.html</code>, from a <strong>Single-page app</strong> with a few client-side routes, a <strong>Plain page</strong>, or a small app in <strong>Vue</strong>, <strong>React</strong>, <strong>Preact</strong>, <strong>Alpine.js</strong> or <strong>Lit</strong>. The framework starters load a pinned version from a CDN, so there is still nothing to install or build, though the page needs the internet the first time it opens. It needs no PHP version; see <a href="frameworks.html#html">HTML applications</a>.</p>

<h2 id="clone">Clone from Git</h2>
<p>Existing Project › <strong>Clone from Git</strong> takes an <code>https://</code>, <code>ssh://</code> or <code>git@host:path</code> address and an optional branch. Phun clones it with the git on your PATH, so private repositories use the SSH keys and credential helpers git already has. Then it runs <code>composer install</code> when there is a <code>composer.json</code>, copies <code>.env.example</code> to <code>.env</code> when the project ships one, and for Laravel generates an <code>APP_KEY</code>, links public storage and installs the JavaScript dependencies. The command palette can start a clone too.</p>

<h2 id="cli">From the terminal</h2>
<p><code>phun new</code> creates an application in the current folder, or <code>--dir</code>, and follows it until it is ready. <code>--php</code> picks the version.</p>
{sh("phun new symfony shop --webapp", "phun new html landing --spa", "phun new html todo --starter vue", "phun new git blog --url git@github.com:acme/blog.git --branch main", "phun new codeigniter api --php 8.3")}
<p>Laravel and WordPress take their choices as JSON with <code>--options</code>, where Laravel's <code>"template"</code> is <code>full_stack</code>, <code>filament</code> or <code>micro_service</code>; the app's starters are the easier route for those. Node.js, C#, Go, Rust, Python and Unity projects are created in the app; an existing one is added with <code>phun link</code>.</p>
'''


def projects():
    return f'''
<h2 id="kinds">More than PHP</h2>
<p>Phun runs Node.js, C#, Go, Rust and Python projects, and opens Unity games, beside your PHP applications. Each one is an application like any other, in the same list, groups and command palette. A web project gets its own <code>.test</code> address over trusted HTTPS; anything else, such as a console app, a command-line tool, a library, a test project, a desktop app or a Unity game, has no address and is run, built and tested from its page.</p>

<h2 id="create">Create one</h2>
<p>Create › JavaScript › <strong>Node.js</strong>, C# › <strong>.NET</strong> or <strong>Unity</strong>, or <strong>Go</strong>, <strong>Rust</strong> or <strong>Python</strong> opens a short wizard, <strong>Basics</strong> then <strong>Review</strong>:</p>
<ul>
<li><strong>Node.js</strong>: an empty project, a Node.js server, Express, Vite, Next.js or Electron. Phun installs its packages.</li>
<li><strong>.NET</strong>: any template your .NET SDK has, with a filter.</li>
<li><strong>Unity</strong>: pick one of your installed Unity editors.</li>
<li><strong>Go</strong>: an empty module or an HTTP server.</li>
<li><strong>Rust</strong>: an empty package or an HTTP server, made with Cargo.</li>
<li><strong>Python</strong>: an empty project or an HTTP server, run with uv. Django, Flask, FastAPI and other projects you add are recognised too.</li>
</ul>
<p>Like the PHP starters, each can create a GitHub repository for the new project. To bring in a project you already have, use Existing Project; Phun recognises it from its files.</p>

<h2 id="toolchain">The toolchain</h2>
<p>When a project needs something you don't have, its page offers it: <strong>Install .NET SDK</strong>, <strong>Install Go</strong>, <strong>Install Rust</strong> or <strong>Install uv</strong>. Node.js comes from Phun's <a href="developer-tools.html#node">Node.js versions</a>. For a project inside WSL, Go, Rust and uv install there. Rust on Windows also needs Microsoft's C++ Build Tools, and the page says so.</p>

<h2 id="project-tab">The Project tab</h2>
<p>These projects open on a <strong>Project</strong> tab:</p>
<ul>
<li><strong>A web project</strong> shows whether it is running, with <strong>Start</strong>, <strong>Stop</strong>, <strong>Restart</strong> and <strong>Logs</strong>. Phun runs it on a port of its own, restarts it if it crashes, and shows a progress bar while it builds and starts. The <strong>Command</strong> row shows what it runs, with <strong>Change</strong>.</li>
<li><strong>Actions</strong> run what the project offers, each with a <strong>Run</strong> button and, where it takes them, arguments: Run, Build, Test and Pack for .NET; Install packages, Run and the <code>package.json</code> scripts for Node.js; Run, Build and Test for Go and Rust; Install packages, Run and Test for Python. The output shows below, with a progress bar and <strong>Stop</strong>.</li>
<li><strong>A Unity project</strong> shows its Unity version and has <strong>Open in Unity</strong> and Build. When that editor isn't installed, Phun says so and opens Unity Hub.</li>
</ul>

<h2 id="tabs">What else they get</h2>
<p>Infrastructure, Technical Debt and Issues work as for any application. A web project also has Metrics and Tools › Sharing, and a Node.js project Tools › Dependencies. PHP settings, Xdebug, Composer and extra PHP instances are left out, and Technical Debt skips the PHP checks.</p>
'''


def php():
    return f'''
{{{{figure:php-versions}}}}
<h2 id="versions">Install versions</h2>
<p>The installed PHP versions are under Services › PHP, with their updates and the default for new applications; each version's settings open from that table. The version you installed on the welcome screen is the default until you choose another.</p>
{sh("phun list php", "phun install php <version>", "phun uninstall php <version>   # only when nothing uses it")}
<p>When Phun ships a newer build of a version you have, such as one that gains an extension, it is offered as an update: <code>phun update php</code> updates every version.</p>

<h2 id="per-application">A version per application</h2>
<p>Each application picks its own PHP version in its Settings › PHP, and the rest keep theirs. From the terminal:</p>
{sh("phun use blog <version>   # just blog.test", "phun use <version>        # the default, used by the terminal's php too")}
<p>To run a tool on the version an application uses, use <code>phun exec</code>:</p>
{sh("phun exec --app blog composer install")}

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
<p>The Services tab has a tab for each part down the side: <strong>Managed services</strong>, then <strong>PHP</strong> and <strong>Node.js</strong> under Runtimes, and <strong>Developer tools</strong>. Managed services lists every service Phun can run in one table you can search by name, port or application, installed or not, with its state, port, auto-start and Install or Update in its row. They run natively, started with Phun: no Docker, no virtual machine.</p>
<ul>
<li><strong>Mail</strong> and <strong>Object storage</strong>, first.</li>
<li><strong>Databases</strong>: MySQL, MariaDB, PostgreSQL and MongoDB.</li>
<li><strong>Cache</strong>: Redis (Valkey) and Memcached.</li>
<li><strong>Search</strong>: Meilisearch, Typesense and OpenSearch.</li>
<li><strong>Live updates</strong>: Mercure.</li>
<li><strong>Cloudflare Tunnel</strong>, last, which sets up <code>cloudflared</code> for <a href="sharing.html">sharing</a>.</li>
</ul>
{sh("phun services", "phun service install redis <version>", "phun service set-port mysql 3307")}

<h2 id="more">Mail, storage and databases</h2>
<p>Caught mail and S3-compatible storage have their own page, <a href="mail-storage.html">Mail and storage</a>, and the database browser and schema canvas are in <a href="databases.html">Databases</a>.</p>

<h2 id="tools">Developer tools</h2>
<p>Composer, Node.js, Bun, the Laravel installer, WP-CLI, Chrome for Testing and Git install when you need them, without a system package manager, and Node.js versions sit side by side; see <a href="developer-tools.html">Developer tools and Node.js</a>.</p>
'''


def developer_tools():
    return f'''
{{{{figure:developer-tools}}}}
<h2 id="tools">Developer tools</h2>
<p>Services › <strong>Developer tools</strong> lists them. Each tool installs its latest release (the LTS for Node.js) into Phun's data folder, puts its commands on your PATH and updates from the same row. No system package manager is involved.</p>
<ul>
<li><strong>Composer</strong>, the PHP dependency manager.</li>
<li><strong>Node.js</strong>, with <code>npm</code> and <code>npx</code>, for building frontend assets. More versions are below.</li>
<li><strong>Bun</strong>, a JavaScript runtime and package manager.</li>
<li><strong>Node Version Manager</strong>, for installing and switching Node.js versions yourself (not on Windows).</li>
<li><strong>The Laravel installer</strong>, <code>laravel new</code>.</li>
<li><strong>WordPress CLI</strong>, the <code>wp</code> command.</li>
<li><strong>Chrome for Testing</strong> and the ChromeDriver built for it, as <code>chrome</code> and <code>chromedriver</code>, for browser tests with Laravel Dusk or Symfony Panther.</li>
<li><strong>Git</strong>: Phun's own on Windows. On macOS and Linux the row shows only while git is missing, and installs it the system's way.</li>
</ul>
<p>The Laravel installer and WordPress CLI need Phun's Composer; installing one without it offers to install Composer first. A tool already on your PATH from another install shows as <strong>External</strong>: Phun leaves that copy alone, <strong>Install managed copy</strong> adds Phun's, and its own copy takes precedence once you install it.</p>
<p>The .NET SDK, Go, Rust and uv are not listed: a project that needs one offers it on its page; see <a href="projects.html#toolchain">The toolchain</a>. Formatters such as shfmt and Ruff download the first time the editor needs them.</p>
{sh("phun tools", "phun install tool node     # the latest Node.js LTS", "phun install tool chrome", "phun uninstall tool bun")}

<h2 id="node">Node.js versions</h2>
<p>Install as many Node.js versions as your projects need, from the official nodejs.org builds, each checked against its published SHA-256. Name a major, an exact version, <code>lts</code>, an LTS line such as <code>lts/iron</code>, or <code>latest</code>. Services › Node.js lists them, installs more (Latest LTS, Latest or a release line) and sets the default.</p>
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
<p>Phun's bin folder comes before nvm's on your PATH, so Phun steps aside instead of fighting it. When nvm (or fnm) has a version active in your shell, after <code>nvm use</code> or from nvm's default alias, Phun's <code>node</code>, <code>npm</code> and <code>npx</code> run that version. Services › Node.js chooses between <strong>Step Aside for nvm</strong>, <strong>Always Phun</strong> and <strong>Leave to nvm</strong>; from the terminal:</p>
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

<h2 id="schedule-tab">The Schedule and Queue tabs</h2>
<p>A Laravel application's page has a tab for each:</p>
<ul>
<li><strong>Schedule</strong>: what is <strong>Running now</strong>, what is <strong>Upcoming</strong> with when each task runs next and last ran, and <strong>Recent runs</strong>. When the scheduler is off, a banner offers <strong>Start scheduler</strong>.</li>
<li><strong>Queue</strong>: jobs <strong>Running now</strong>, <strong>Waiting</strong>, <strong>Failed</strong> and <strong>Recent jobs</strong>. Retry a failed job or <strong>Retry all</strong>, or delete one for good.</li>
</ul>

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
<p>Every application opens in Phun's own code editor from <strong>Open › Editor</strong> at the top of its page. It fills the window; {k("Shift", "Esc")} hides it to its pill in the dock, which brings it back as it was. {k("Esc")} alone never hides it, so closing a suggestion list or popup keeps you in the editor. It remembers open tabs, cursors and the tree. From a terminal:</p>
{sh("phun edit blog app/Models/Post.php:42")}
<p>The bar left of the file tree holds the editor's tools: Files, Git, Preview, Show changes, Blame, Format code, Run tests, Debug, the application's terminals, Find in files and Editor settings.</p>

<h2 id="languages">Languages</h2>
<p>Highlighting for PHP, Blade, JavaScript and TypeScript, Vue, HTML, XML, CSS and Sass, JSON, Markdown, YAML, shell scripts and <code>.env</code>, recognised by name and by content. Markdown shows its preview beside it, updated as you type. Images, video and audio show as themselves. Colours in stylesheets, templates and scripts get a swatch; click a hex colour's swatch to pick a new one.</p>

<h2 id="completion">Completion and problems</h2>
<p>Completion comes from the application's own classes, functions and variables and, for Laravel, its models' attributes and relations, routes, views, config, translations, validation rules and Blade components. After <code>-&gt;</code>, <code>?-&gt;</code> and <code>::</code> it offers the methods and properties of what is on the left, through chains, parent classes, traits, <code>@mixin</code> and generics. Accepting a class adds its <code>use</code> line, and hover and parameter hints show a member's signature.</p>
<p>PHP is checked by the application's own PHP as you type, with a mark in the gutter, the message on hover and {k("F2")} to the next problem. A class that isn't imported is underlined, and {k("Alt", "Enter")} imports it. Methods, properties and constants a class doesn't have are underlined too.</p>

<h2 id="navigate">Find your way</h2>
<ul>
<li>{k("Ctrl")}-click a class, method, property, function or variable to go to its declaration ({k("Cmd")}-click on macOS). Find Usages lists real uses only, grouped by file and kind.</li>
<li>Tap {k("Shift")} twice to search everywhere.</li>
<li><strong>Find in Files</strong> is a floating window you can move and resize, with a <strong>Replace in Files</strong> switch: match case, whole words or a regular expression, scope it to the application, a folder or the open files, and tick the lines to replace, with undo afterwards. Searches leave <code>vendor</code>, <code>node_modules</code> and the other dependency folders out unless you ask. The file tree's right-click menu opens it for a folder.</li>
</ul>

<h2 id="editing">Editing</h2>
<ul>
<li><strong>Multiple cursors</strong>: {k("Alt", "Shift")}-click adds a cursor, and {k("Alt")}-drag selects a column.</li>
<li><strong>The Text menu</strong>, on right-click: sort, join and de-duplicate lines, change case, switch quotes, wrap for Laravel's translator, Base64 and URL encode or decode, format or compact JSON, timestamps to dates and back, and insert a UUID.</li>
<li><strong>Copy reference</strong> copies <code>App\\Models\\User::name</code> in PHP, or <code>path:line</code> elsewhere; <strong>Copy as Markdown</strong> copies the selection fenced in its language.</li>
<li><strong>Folding</strong>: a run of PHP <code>use</code> lines or JavaScript imports folds to its first line.</li>
<li>The status bar counts what is selected, and sums selected numbers.</li>
</ul>

<h2 id="refactor">Refactor and format</h2>
<p>Rename across the application with a preview, extract a variable, and move classes between namespaces with their references updated; renaming a class renames its file. <strong>Format code</strong> uses the project's own Pint for PHP, else Prettier, and formats JavaScript, TypeScript, Vue, HTML, CSS, JSON, Markdown, YAML, XML, SQL, <code>.env</code> and INI files, shell, Go, Rust, Python, C# and Caddyfiles, or just the selection. The project's <code>.editorconfig</code>, <code>.prettierrc</code> and <code>pint.json</code> always win. Formatting also sorts a PHP file's <code>use</code> lines and drops unused ones.</p>

<h2 id="saving">Saving</h2>
<p>Editor settings › General can save for you, as PhpStorm does: when you leave the window or hide the editor, and a moment after typing stops. Both are off until you turn them on. The same page can colour the name of a file with unsaved changes, and of one with uncommitted git changes, in the tabs and the tree; both stay gray unless you pick a colour.</p>
<p>Files changed outside Phun follow along: a file another tool writes reloads in its tab, a tab with unsaved edits asks whether to take the disk's version, and a deleted file's tab closes.</p>

<h2 id="git">Git</h2>
<p>Changed lines in the gutter, changed files in the tree, the branch in the status line and the diff in a tab. The Changes view beside the tree stages, unstages and commits ({k("Ctrl", "Enter")}, {k("Cmd", "Enter")} on macOS), and Blame shows who last changed each line. Branches, pulling, the log and worktrees are on <a href="git.html">Git</a>.</p>

<h2 id="tests">Tests</h2>
<p>A test file shows a run marker beside every Pest test, <code>describe</code> group and PHPUnit method. Run one, or debug it; results arrive in a panel under the editor as each test finishes, and a failure shows on the line where it stopped. {k("Ctrl", "Shift", "F10")} runs the test at the cursor.</p>

<h2 id="debugging">Debugging</h2>
<p>The bug button turns Xdebug on, and a click beside a line number sets a breakpoint; see <a href="debugging.html">Debugging and profiling</a>.</p>

<h2 id="settings">Settings and shortcuts</h2>
<p>{k("Ctrl", ",")} ({k("Cmd", ",")} on macOS) opens the editor settings: General, Formatting, Icons and Shortcuts, including the font and its size ({k("Ctrl", "=")} and {k("Ctrl", "-")} in the editor). The default keys follow PhpStorm's, and every editor shortcut can be rebound.</p>

<h2 id="sticky-notes">Sticky notes in the code</h2>
<p>Right-click a line and choose <strong>Add sticky note here</strong> to pin a note to it. A folded-paper mark sits beside each line with a note; hover it to read, edit or open the board. See <a href="issues.html#sticky-notes">Issues</a>.</p>
'''


def terminals():
    return f'''
{{{{figure:terminal-dock}}}}
<h2 id="dock">The dock</h2>
<p>An application's <strong>Terminal</strong> menu, in its page header, opens them:</p>
<ul>
<li><strong>Artisan</strong>: Laravel's commands with their forms. It offers your models, tables, views, components and route names as you type. A Symfony application has <code>bin/console</code> in the same place.</li>
<li><strong>Console</strong>: an interactive shell for the application.</li>
<li><strong>Tinker</strong>: Laravel's REPL.</li>
<li><strong>Logs</strong>: every log the application has, in one list; see <a href="logs.html">Logs</a>.</li>
<li><strong>AI agents</strong>: Claude Code, Codex, Gemini CLI or Grok, started in the application's folder.</li>
</ul>
<p>Tinker shows only for a Laravel application, and Artisan for Laravel and Symfony. Clicking anywhere outside an open terminal minimises it to its pill in the dock; the pill brings it back. The code editor goes there too.</p>
<p>The dock is a strip of pills, one for each terminal, editor and install that is open, grouped by kind behind a label: Artisan, Console (AI agents included, each named for its agent), Tinker, Logs, Editor and Installing. Drag a pill to reorder it in its group, or a group's label to move the whole group. When the dock is full, its pills scroll with back and forward buttons.</p>
<ul>
<li><strong>Minimise all</strong> puts the open terminal and editor back to their pills; nothing is ended.</li>
<li><strong>Close all</strong> ends every terminal and closes every editor; installs carry on. It always asks first.</li>
<li><strong>Move the dock</strong>: drag its handle and Phun shows where it can go, at the top or the bottom, left, centre or right, and snaps it to the nearest spot.</li>
<li><strong>Keep the editor clear</strong>, with the dock at the bottom, keeps it off the code instead of floating over it.</li>
<li><strong>Hide the dock</strong>, always on its outside edge, leaves a small handle that shows it again. Terminals keep running and their keys still open them.</li>
</ul>
<p>Account › Appearance sets what the dock shows.</p>

<h2 id="console-tabs">Console tabs</h2>
<p>The Console has tabs, each its own shell in the application's folder, so you can run commands in one and keep something like Claude Code running in another. Tabs keep running, at their size, while you are in another, in the dock or inside the editor.</p>
<ul>
<li><strong>+</strong> or {k("Ctrl", "Shift", "T")} ({k("Cmd", "Shift", "T")} on macOS) adds a tab.</li>
<li>{k("Ctrl", "PageDown")} and {k("Ctrl", "PageUp")} move between them ({k("Cmd", "Shift", "]")} and {k("Cmd", "Shift", "[")} on macOS).</li>
<li>Double-click a tab, or press {k("F2")}, to rename it.</li>
</ul>

<h2 id="in-editor">Inside the code editor</h2>
<p>The bar left of the code editor's file tree has a button for each of the application's terminals. They open over the editor. Turn on Editor settings › General › <strong>Open terminals inside the editor</strong> and they open as a resizable panel under the code instead. It is the same session as in the dock, so hiding the editor hands it back to the dock without restarting it, and keys typed in it never trigger the editor's shortcuts.</p>

<h2 id="cursor">The cursor</h2>
<p>Account › Appearance sets how terminals draw their cursor: a block, underscore or pipe, its colour, and whether it blinks, with a preview. Open terminals change at once.</p>

<h2 id="keys">Keys</h2>
<ul>
<li>{k("`")} opens the Console for the application you are on, and closes it again, even from inside it.</li>
<li>{k("Shift", "`")} moves to its next open terminal.</li>
<li>{k("Ctrl", "Up")} hides and shows the dock, on macOS too.</li>
<li>{k("Ctrl", "D")} ({k("Cmd", "D")} on macOS) after the shell ends hides the Console.</li>
<li>Account › Key binds can give your own keys to opening every terminal at once, the code editor and the dock's actions.</li>
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

<h2 id="conflicts">Conflicts</h2>
<p>A file with merge conflicts shows a bar above each one, with <strong>Keep yours</strong>, <strong>Keep theirs</strong> and <strong>Keep both</strong>, the two sides tinted apart. Settle them one by one or for the whole file, then mark it resolved.</p>

<h2 id="lfs">Git LFS</h2>
<p>A file still waiting in LFS opens as a notice with a <strong>Download</strong> button instead of its pointer text. Pull fetches LFS files too, diffs say when a file lives in LFS, and the Changes view says when <code>git-lfs</code> is missing.</p>

<h2 id="cli">From the terminal</h2>
<p><code>phun editor git</code> does the same for scripts and AI agents, inside the application's folder:</p>
{sh("phun editor git status blog", "phun editor git blame blog app/Models/Post.php")}
'''


def logs():
    return f'''
<h2 id="open">Open it</h2>
<p><strong>Logs</strong> is in the Terminal menu of an application's page, in the code editor's tool bar and in the command palette. It opens in the dock like the other terminals and stays there while you move around Phun.</p>

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


def issues():
    return f'''
<h2 id="board">The board</h2>
<p>Every application has an <strong>Issues</strong> tab: a board of columns for the work it needs. Add one from a column, or with <strong>Add a note</strong> at the top. The composer chooses between an <strong>Issue</strong> and a <strong>Sticky note</strong>, and between <strong>Only me</strong> and <strong>Team</strong>.</p>
<ul>
<li><strong>Move</strong> an issue by dragging it to another column or place, or with <strong>Move to</strong> in its menu.</li>
<li><strong>Assign</strong> it, give it labels, and <strong>Close</strong> it as Completed, Not planned or Duplicate; <strong>Reopen</strong> brings it back. Closed issues hide until you show them, and <strong>Mentions you</strong> narrows the board to what mentions you.</li>
<li><strong>Columns</strong> are yours to change: <strong>Add a column</strong>, rename one, move it or delete it.</li>
<li>Issues take details, comments and @mentions of other Phun users.</li>
</ul>

<h2 id="on-phun">A board on Phun</h2>
<p>Issues live on Phun, so you need to be signed in with GitHub. The board belongs to the application's git remote, so everyone with the same remote finds the same board. Choose whether it is yours alone or one of your <a href="account.html#teams">teams</a>'; a team's board is shared with everyone in it. The board's menu renames, deletes or switches boards, and Follow notifies you of new issues.</p>
<p>An application with no git remote keeps its notes with the code. <strong>Keep notes local</strong> does the same by choice, and <strong>Use a shared board</strong> moves to Phun later. Older notes files waiting in the project are offered with <strong>Move notes to the board</strong>.</p>

<h2 id="github">Move from GitHub</h2>
<p>An application whose issues are on a GitHub Projects board is offered <strong>Move from GitHub</strong>, also in the board's menu. Phun copies the board's issues across and only reads GitHub; nothing there changes, and running it again adds nothing twice.</p>

<h2 id="sticky-notes">Sticky notes in the code</h2>
<p>A <strong>Sticky note</strong> stays with the code instead of the board: in <code>.phun/notes/</code>, shared with the team through git, or in <code>.phun/notes.local/</code> for you alone. In the code editor, right-click a line and choose <strong>Add sticky note here</strong>; a folded-paper mark sits beside each line with a note, and hovering it shows the note with Edit, Details, Comments, Open board and Unlink. <strong>Make it an issue</strong> moves a sticky note to the board, and <strong>Share with the team</strong> or <strong>Keep to myself</strong> changes who sees it.</p>

<h2 id="reminders">Reminders</h2>
<p><strong>Remind me</strong> in a note's menu offers a few presets or any date and time you choose. When it is due, Phun sends a <a href="notifications.html">notification</a>. Only you get reminded.</p>
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
<p>Mark an item <strong>Not an issue</strong> to hide it for everyone. The list is kept in <code>.phun/debt-dismissed.json</code> in the application, so committing it shares it with your team. A hidden item follows its line if the line moves, and comes back if the line changes. The <strong>Not an issue</strong> filter shows them, with <strong>Restore</strong>, and <strong>No longer in the code</strong> lists the ones whose code is gone, to remove.</p>

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
<p><strong>Updates</strong>, in the header beside the Daemon menu, shows the version you run, checks for a new one and installs it with <strong>Update now</strong>, with the release notes below. A dot on the button means an update is out or there are notes you haven't read. The command palette opens it too (<strong>Open Updates</strong>, or <strong>Check for updates</strong>), and Phun tells you about a new release with a notification. From the terminal:</p>
{sh("phun update         # check for a new Phun", "phun update --yes   # and install it")}
<p>On Arch Linux, Phun updates its package with pacman.</p>

<h2 id="automatic">Automatic updates</h2>
<p>The <strong>Automatic updates</strong> switch installs new versions in the background, mostly without a restart; when one needs it, <strong>Restart to finish</strong> appears. It is off until you turn it on.</p>

<h2 id="beta">Beta updates</h2>
<p>The <strong>Beta updates</strong> switch offers new versions before their full release, while they are still being tested, and shows what's in a beta before you install it. It is there for users with the Beta Tester badge; signed in without it, <strong>Ask to join the beta</strong> asks the Phun team.</p>

<h2 id="rollback">Going back</h2>
<p>If the daemon will not start after an in-app update, its panel offers to go back to the version you had, for two weeks after the update. Phun downloads that release and installs it; your applications and settings stay as they are.</p>
<p>Every older release in the release notes has its own <strong>Go back to this version</strong> button, so you can install any earlier version, at any time. It asks first, and keeps your applications, databases and settings.</p>

<h2 id="checksums">Checked before installing</h2>
<p>Every update is checked against the installer's checksum on GitHub before it installs. When a release is rebuilt under the same version number, such as a fixed beta, the checksums differ and Updates offers the version you run again.</p>

<h2 id="whats-new">What's new</h2>
<p>The release notes for each version are in Updates, as Features, Changed and Fixed, newest first, with older ones loaded from the archive. Every release is also on <a href="https://github.com/cloudcake/phun/releases">GitHub</a>.</p>

<h2 id="php-and-services">PHP, services and tools</h2>
<p>PHP versions, services and developer tools update on their own rows in Services. A download that hits a server hiccup tries again by itself.</p>
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
<p>Create a WordPress application from Create, or <code>phun new wordpress</code>. Services are written into <code>wp-config.php</code>: MySQL or MariaDB, and Redis for the Redis Object Cache plugin. <strong>WP Admin</strong> in the application's header opens the dashboard; from the terminal:</p>
{sh("phun wordpress auto-login shop on", "phun wordpress login-url shop   # a one-time admin sign-in link", "phun wordpress users shop")}

<h2 id="others">CodeIgniter, Drupal, Magento and more</h2>
<p>CodeIgniter gets its databases, Redis, Memcached and mail in its own <code>.env</code> settings. WordPress, CodeIgniter (with <code>codeigniter4/tasks</code>), Drupal (with Drush) and Magento get scheduled tasks from Infrastructure › Processes, which run the application's own cron command every minute, with its output in the application's logs and a notification when a run fails.</p>

<h2 id="html">HTML applications</h2>
<p>Create › HTML app makes a folder with an <code>index.html</code>, served as it is, from a plain page or a single-page app with a few client-side routes. Phun answers any path that is not a file with <code>index.html</code>, so reloading <code>/about</code> still works. No PHP version has to be installed and no PHP process starts; a request that needs PHP, such as a <code>.php</code> script or a POST, still goes to PHP.</p>

<h2 id="environment">The environment</h2>
<p>An application's Settings › <strong>Environment variables</strong> edits its <code>.env</code>; Phun hides values until you reveal them. <strong>Environment profiles</strong>, at the top, are the <code>.env.&lt;name&gt;</code> files beside it (<code>.env.testing</code>, <code>.env.example</code> and so on): <strong>Compare and use</strong> shows one against the current <code>.env</code> key by key and uses it in its place, keeping the old one as <code>.env.backup</code> and clearing Laravel's cached config. <strong>Save current as…</strong> writes a new profile.</p>
{sh("phun env blog MAIL_FROM_ADDRESS=hello@blog.test", "phun dotenv blog")}

<h2 id="npm">JavaScript</h2>
<p><code>phun js-install blog</code> installs an application's JavaScript dependencies with its own package manager, and <code>phun npm enable blog dev</code> keeps an npm script running beside it.</p>
'''


def sharing():
    return f'''
{{{{figure:share}}}}
<h2 id="quick">Share on a public URL</h2>
<p>An application's Tools › <strong>Sharing</strong> gives it a public HTTPS address on <code>trycloudflare.com</code> through a Cloudflare Quick Tunnel, for webhooks, demos and other devices, with no account needed. The address changes every time you start one, and anyone with it can reach the application while it is shared and Phun is running. It is for development, not production. When <code>cloudflared</code> isn't installed yet, <strong>Set up cloudflared in Services</strong> takes you to its row.</p>
<ul>
<li><strong>A password and a time limit.</strong> A share can ask visitors for a password and stay open until you stop it, or for an hour, eight hours, a day or a week. People on your own machine are never asked.</li>
<li><strong>Who reached it.</strong> <strong>Visitors</strong> lists them with their address, country, path and status.</li>
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

<h2 id="snapshots">Snapshots</h2>
<p>A snapshot saves an application's database so you can put it back later, say before a migration you are not sure of. The database card's <strong>Snapshots</strong>, or the <strong>Snapshots</strong> tab of the database browser, lists them newest first with their size: <strong>Take snapshot</strong> with a name, <strong>Restore</strong> one, or delete it. Works with MySQL, MariaDB, PostgreSQL and SQLite.</p>
<ul>
<li><strong>Restoring</strong> puts the database back exactly: tables added since are dropped, and the application's database user keeps its access. Phun snapshots the current data first, so the newest <em>Before restoring</em> entry undoes a restore. If a restore fails part way, Phun puts the data from before back.</li>
<li><strong>Before migrating</strong>: running <code>migrate</code>, <code>migrate:fresh</code>, <code>migrate:refresh</code>, <code>migrate:reset</code>, <code>migrate:rollback</code> or <code>db:wipe</code> from the Artisan terminal snapshots the database first. Turn the switch off to skip it.</li>
<li>Snapshots you take stay until you delete them. Phun keeps its ten newest automatic ones per database. They live in Phun's data folder, under <code>db-snapshots</code>.</li>
</ul>

<h2 id="cli">From the terminal</h2>
{sh("phun db list mysql", "phun db create mysql blog", "phun db provision blog          # the database blog's .env names", "phun db backup mysql blog blog.sql", "phun db restore mysql blog blog.sql", "phun db query mysql blog 'select count(*) from users'")}
<p>Snapshots take an application name, or <code>&lt;service&gt;/&lt;database&gt;</code> for any database on a Phun server. Restore and delete take the id <code>phun db snapshots</code> prints, or just the number it starts with:</p>
{sh("phun db snapshot blog 'Before the orders migration'", "phun db snapshots blog", "phun db snapshot-restore blog 1794744204746", "phun db snapshot-delete mysql/shop 1794744204746")}
'''


def mail_storage():
    return f'''
{{{{figure:mail}}}}
<h2 id="mail">Every email, caught</h2>
<p>Phun catches every email your applications send, so nothing reaches a real inbox. The Mail viewer ({k("Ctrl", "Shift", "M")}, or the Mail row in Services, which {k("Ctrl", "7")} opens) reads each message rendered, as its plain-text part, or as the raw source exactly as the application sent it, with a Copy button. New mail can arrive as a desktop notification.</p>
<p>Applications are wired to it when you add mail on the Infrastructure canvas.</p>
{sh("phun mail list", "phun mail show <id>", "phun mail clear", "phun mail port 2525")}

<h2 id="storage">S3-compatible storage</h2>
{{{{figure:object-storage}}}}
<p>Phun serves object storage on <code>http://127.0.0.1:19000</code>, with buckets and files kept in Phun's data folder. Add <strong>Object storage</strong> to a Laravel application from its Infrastructure canvas and Phun creates its bucket and fills in its settings, so the <code>s3</code> disk works as it would against S3: uploads, downloads, listing, copying, deleting, multipart uploads and temporary URLs.</p>
<p>The bucket browser, from the Object storage row in Services, creates and deletes buckets, makes them public or private, and opens, reveals or deletes files. Its port is set under Diagnostics › Ports.</p>
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
<p>An application's <strong>Metrics</strong> tab opens with cards for its requests, response time, error rate, PHP memory, workers and logs. Below the HTTP requests, <strong>Time series</strong> charts requests, requests by instance, response time, PHP memory and CPU, queue jobs and log volume over the last 15 minutes, hour or day.</p>
{sh("phun metrics blog     # request counts per minute, last 24 hours", "phun activity         # requests each application served, by status")}

<h2 id="requests">HTTP requests</h2>
{{{{figure:request-inspector}}}}
<p>The requests the application has served, by endpoint: the method, the path and how many times it was hit, with its errors, average time, when it was last hit and its status. Filter by path, method or status, show only errors, and <strong>Clear</strong> the counts and the requests. Query strings are left out, so <code>/search?q=a</code> and <code>/search?q=b</code> are one endpoint.</p>
<p>An endpoint opens to its latest requests, with their query string and headers. Cookies, authorization headers and bodies are never kept. A request can be:</p>
<ul>
<li><strong>Replayed</strong>, signed out and without a body, since Phun keeps neither.</li>
<li><strong>Profiled</strong>; see <a href="debugging.html#profile">Profile a request</a>.</li>
<li><strong>Trailed</strong>, to see its path through the application; see <a href="request-graph.html#trails">Trailed Request</a>.</li>
<li><strong>Copied</strong> as a <code>curl</code> command.</li>
<li><strong>Shown with its log lines</strong>, what the application wrote while it ran.</li>
</ul>
{sh("phun requests blog", "phun endpoints blog", "phun endpoints blog --clear")}
'''


def request_graph():
    return f'''
<h2 id="live">Live Request Graph</h2>
<p>Tools › <strong>Live Request Graph</strong> watches each request travel through a Laravel application as it happens, in columns: the route, the middleware one by one, the controller action, the response, and everything it touched on the way, such as queries, cache calls, views, jobs, mail and events. Hover a step to light the whole path through it.</p>
<ul>
<li><strong>Pause</strong> and <strong>Resume</strong> stop and start watching.</li>
<li><strong>Step through</strong> holds each request at every step, from route to response, until you press <strong>Next</strong> ({k("Right")} or {k("Enter")}); <strong>Run to end</strong> lets it finish.</li>
<li><strong>Clear map</strong> clears the graph and the requests listed under it, without deleting them from the HTTP requests or Trailed Request.</li>
</ul>
<p>It needs request trails on; the graph offers to turn them on.</p>

<h2 id="trails">Trailed Request</h2>
<p>Tools › <strong>Trailed Request</strong> lists the requests that have a trail, with <strong>Record request trails</strong> and an errors filter. A trail shows the request's path and timings step by step: Phun, PHP, boot, global middleware, routing, route middleware, the controller action, the response and terminate. The time Phun takes to receive a request is shown but not counted. When the request failed, the trail shows the exception and its stack, a click from the editor, and it suggests <code>php artisan optimize</code> where that would speed Laravel up.</p>

<h2 id="events">Event Chains</h2>
<p>Tools › <strong>Event Chains</strong> draws a Laravel application's events as a map: where each one is dispatched, the event, and what listens to it. Search for an event or listener, and show Laravel's own events too.</p>
<p>The Live Request Graph and Event Chains are for Laravel applications; Trailed Request needs a PHP application with an address.</p>
'''


def security():
    return f'''
{{{{figure:dependency-audits}}}}
<h2 id="audit">Dependency audits</h2>
<p>An application's Tools › <strong>Dependencies</strong> audits its Composer and JavaScript dependencies: how far behind each package is, and the known advisories against it, with a card per package manager. <strong>Install</strong> puts in the packages your lock files pin, and <strong>Check again</strong> reads them afresh.</p>
{sh("phun security scan blog")}

<h2 id="wait">Wait before installing</h2>
<p>Brand-new releases are where supply-chain attacks land. <strong>Wait before installing</strong> makes package managers hold off on releases younger than the days you choose. For Composer it uses Composer's own cooldown setting, <code>config.policy.cooldown</code> in <code>composer.json</code> (Composer 2.11 and newer), so it works for any Composer application.</p>
{sh("phun security wait blog on --days 7")}

<h2 id="packages">Composer packages</h2>
<p>Dependencies lists every package <code>composer.json</code> requires, with its constraint, its installed and newest versions and its advisories, and a button to update it, upgrade it to a new major or remove it. Add packages from the same card. Every change runs Phun's Composer on the application's PHP.</p>
{sh("phun packages list blog", "phun packages require blog spatie/laravel-data", "phun packages update blog laravel/framework")}

<h2 id="update-all">Update all, and go back</h2>
<p><strong>Update all</strong> updates every Composer and JavaScript package within the versions your project allows (no new major versions), still waiting out new releases if Wait before installing is on, and lists what moved. The lock files are saved first: <strong>Restore previous versions</strong> puts them back and reinstalls.</p>
{sh("phun security update blog", "phun security restore blog")}
'''


def diagnostics():
    return f'''
{{{{figure:health-checks}}}}
<h2 id="checks">Health checks</h2>
<p><strong>Diagnostics</strong> opens from the header's <strong>Daemon</strong> menu, or its own button while the daemon is stopped, or {k("Ctrl", "4")}. At the top, <strong>Services</strong> shows every service at a glance: how many are running, a pill for each with the ones needing attention first, and the default PHP and its pools. Below it, Phun's checks for DNS, certificates, ports and PHP, each with a one-click fix when something is off, then <strong>Ports</strong>, to move Phun's ports, and, on macOS and Linux, <strong>Terminal CLI</strong>. The palette can run the safe fixes too.</p>
{sh("phun status       # the daemon, ports, DNS, certificates and PHP at a glance", "phun doctor", "phun doctor fix")}

<h2 id="ports">A port that is already taken</h2>
<p>When another program holds a port Phun needs, such as 80 or 443, the DNS port, or a database's port, Diagnostics names it with its process id and says what it is: Apache, nginx, Caddy, Herd, IIS, Skype, Docker, another MySQL, MariaDB, PostgreSQL or Redis, or a copy of one of Phun's own services left running. Then it offers the fix. <strong>Stop</strong> appears only when that is safe: a program you own that nothing will start again behind your back. A system service gets the command that really stops it instead, such as <code>sudo systemctl stop nginx</code>, <code>brew services stop mysql</code> or <code>docker stop</code>, ready to copy. <strong>Use port</strong> moves Phun's service to a free port and restarts it. A service that can't start for this reason says the same in its error.</p>

<h2 id="certificates">Certificates that are about to expire</h2>
<p>Phun warns 30 days before its local certificate authority or an application's certificate expires: in Diagnostics, and with one notice when it gets close, again in its last week, and once it has expired, never on every launch. Renewing an application's certificate takes one click and needs nothing trusted again. Renewing the certificate authority asks first, because the new one has to be trusted again, which may ask for your password.</p>
{sh("phun cert list               # certificates that expire within 30 days", "phun cert renew blog.test", "phun cert renew-ca --yes     # then trust it again: sudo phun elevate trust")}

<h2 id="report">A problem report</h2>
{{{{figure:diagnostics-report}}}}
<p>Diagnostics › <strong>Report</strong> gathers what a bug report needs in one file: versions, services, Phun's processes, a <code>.test</code> lookup, health checks and recent logs. Passwords, tokens, keys, email addresses, share links, card or ID numbers and your user name are removed before you see it. Copy it, or <strong>Save file</strong> puts it in Downloads. Copy diagnostics on the daemon panel is redacted the same way. <strong>Logs</strong>, beside it, shows the app's and the daemon's own logs.</p>

<h2 id="bug-reports">Bug reports</h2>
<p><strong>Bug reports</strong>, in the header beside Updates ({k("Ctrl", "5")}), sends a problem to the Phun team: a title, what happened, and <strong>Include diagnostics</strong>, on by default, which attaches the report above; <strong>See the report</strong> shows it first. Signed in with GitHub, <strong>Tell me when it is fixed</strong> sends a notification when it is. <strong>Your reports</strong> lists what you sent with the team's notes; edit one until it is fixed or turned down, or delete it. Accepted reports count towards the Bug Hunter badge.</p>

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
<p>Phun tells you what happens, in its own list under the bell in the title bar and as a desktop notification, even with its window closed:</p>
<ul>
<li><strong>In the background</strong>: queued jobs finishing or failing, scheduled tasks running or failing, caught mail, errors in an application's log, a service stopping, background tasks finishing or failing, and shares ending.</li>
<li><strong>Issues</strong>: mentions, comments and replies, issues assigned to you or new on a board you follow, and your own <a href="issues.html#reminders">reminders</a>.</li>
<li><strong>Community</strong>: mentions and replies in discussions, and reviews asked of you.</li>
<li><strong>Teams and the beta</strong>: team invitations, and being let into the beta.</li>
<li><strong>Extensions</strong>: yours approved or not, and suggested updates sent, accepted or declined.</li>
<li><strong>Phun itself</strong>: a new release, and news on your bug reports.</li>
</ul>
<p>A burst of one kind becomes one notification, such as "5 jobs finished in blog", and an application logging the same error over and over notifies once, then stays quiet for two minutes. Clicking a notification opens what it is about, such as the mail viewer for new email. The bell's menu has <strong>Mark all read</strong>, <strong>Clear all</strong> and <strong>Notification settings</strong>; each GitHub account keeps its own list.</p>

<h2 id="settings">Choose what you hear about</h2>
<p>Account › Notifications turns each kind on or off, <strong>In Phun</strong> and <strong>On the desktop</strong> separately. Scheduled tasks that succeed start switched off, since a task that runs every minute would notify every minute. <strong>Send a test notification</strong> checks that your system shows them.</p>
<ul>
<li><strong>Do not disturb</strong> silences the desktop and the chime until you turn it off; the list under the bell keeps filling.</li>
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
<p>{k("Ctrl", "K")} ({k("Shift", "Cmd", "K")} on macOS, since {k("Cmd", "K")} can open the system's search), or <strong>Search commands</strong> in the title bar, opens a search box for the whole app:</p>
<ul>
<li>Type an application's name to open it, its Artisan, Console, Tinker or Logs, its tabs, or copy its local URL.</li>
<li>Start, stop or restart any service; install, update or remove developer tools; make a PHP version the default or restart its pools.</li>
<li>Create or clone an application, run the diagnostics or their safe fixes, jump to any Settings section, and open Updates.</li>
<li><strong>Run again</strong> lists the Artisan commands you ran recently in each application, and <strong>Recent</strong> what you used last.</li>
</ul>
<p>Matching is forgiving: "tnkr" finds Tinker.</p>

<h2 id="keys">Key binds</h2>
{{{{figure:key-binds}}}}
<p>Account › Key binds gives any action in the command palette a key of your own, plus the dock's actions for the application you are on. Press a key cap to record; {k("Esc")} cancels and {k("Backspace")} clears it. Phun asks before taking a key another action has, refuses keys that typing needs, and can reset each one. {k("Ctrl", "/")} shows every shortcut.</p>
<div class="table-wrap"><table><thead><tr><th>Keys</th><th>What they do</th></tr></thead><tbody>
<tr><td>{k("Ctrl", "K")}</td><td>The command palette ({k("Shift", "Cmd", "K")} on macOS)</td></tr>
<tr><td>{k("Ctrl", "1")} to {k("Ctrl", "3")}</td><td>Community, Applications, Services</td></tr>
<tr><td>{k("Ctrl", "4")} and {k("Ctrl", "5")}</td><td>Diagnostics and Bug reports</td></tr>
<tr><td>{k("Ctrl", "6")} or {k("Ctrl", ",")}</td><td>Settings</td></tr>
<tr><td>{k("Ctrl", "7")}</td><td>Mail, in Services</td></tr>
<tr><td>{k("Ctrl", "Shift", "M")}</td><td>The Mail viewer</td></tr>
<tr><td>{k("Ctrl", "Shift", "N")} and {k("Ctrl", "Shift", "P")}</td><td>Link an application and park a folder</td></tr>
<tr><td>{k("Ctrl", "Shift", "L")}</td><td>Switch between light and dark</td></tr>
<tr><td>{k("Ctrl", "Shift", "R")}</td><td>Restart the daemon</td></tr>
<tr><td>{k("Ctrl", "Shift", "Right")} and {k("Ctrl", "Shift", "Left")}</td><td>Next and previous application, in the Applications tab's order, on the same tab ({k("Ctrl")} on macOS too)</td></tr>
<tr><td>{k("Ctrl", "Up")}</td><td>Hide or show the dock ({k("Ctrl")} on macOS too)</td></tr>
<tr><td>{k("`")}</td><td>Open or close the Console for the application you are on</td></tr>
<tr><td>{k("Shift", "`")}</td><td>Its next open terminal</td></tr>
<tr><td>{k("Ctrl", "/")}</td><td>Every shortcut</td></tr>
</tbody></table></div>
<p>On macOS, {k("Cmd")} takes the place of {k("Ctrl")} unless the table says otherwise. Extensions has no number key; the palette opens it.</p>

<h2 id="themes">Themes</h2>
{{{{figure:themes}}}}
<p>System, Light or Dark, under Account › Appearance, with the colour that leads the app and an <strong>Interface size</strong> that scales all of Phun down for more room or up for larger text. The choice reaches every window, the terminals and the editor. Theme <a href="extensions.html#themes">extensions</a> from the Hub can change Phun's colours, fonts, corners and tabs. When your system asks for reduced motion, nothing in Phun slides, pulses or spins.</p>
'''


def ai_agents():
    return f'''
{{{{figure:mcp}}}}
<h2 id="mcp">An MCP server for AI agents</h2>
<p>Phun can serve its tools to AI coding agents on your machine over MCP, the Model Context Protocol, so agents such as Claude Code can list your applications, switch PHP, create databases, snapshot a database before a migration and read caught mail. Agents cannot restore or delete snapshots; that stays with you.</p>
<ol class="steps">
<li><b>Turn it on</b><p>Settings › AI agents › <strong>Enable Phun's MCP server</strong>, or <code>phun settings mcp on</code>.</p></li>
<li><b>Register Phun with your agent</b><p>The same section registers Phun with your agent. For Claude Code by hand:</p>
{sh("claude mcp add --scope user phun -- phun mcp")}</li>
</ol>

<h2 id="consoles">Agents in the dock</h2>
<p>An application's Terminal menu starts <strong>Claude Code</strong>, <strong>Codex</strong>, <strong>Gemini CLI</strong> or <strong>Grok</strong> in its folder. Each runs in the dock with the other consoles, its pill named for its agent; see <a href="terminals.html">Terminals and the dock</a>.</p>

<h2 id="cli">The command line, for agents and scripts</h2>
<p>Every <code>phun</code> command takes <code>--json</code>, and <code>phun request '&lt;json&gt;'</code> sends any request to the daemon and prints its JSON reply. <code>phun editor</code> reads, writes, searches, formats and refactors an application's files the way the app's code editor does; see <a href="cli.html#code">the command reference</a>.</p>
'''


# ── You and Phun ─────────────────────────────────────────────────────────
def account():
    return f'''
<h2 id="open">Open it</h2>
<p><strong>Account</strong> is a page of its own. Open it from <strong>Account</strong> in your user card's menu, at the top right, or the Account button in the title bar. It has a tab for each part down the side, grouped under headings. Signed out, only GitHub, Appearance, Notifications and Key binds show.</p>

<h2 id="github">GitHub</h2>
<p>One GitHub sign-in for all of Phun: your profile, leaderboards, your name in collaboration, @mentions, Issues boards and pull requests in the code editor. Your settings sync across computers while GitHub is connected. You can sign in with more than one GitHub account and switch between them from your user card's menu (<strong>Add Account</strong>, <strong>Manage Accounts</strong>); each keeps its own notifications.</p>

<h2 id="teams">Teams</h2>
<p>Make a team, invite people with a link or by their GitHub login, and share <a href="issues.html#on-phun">Issues boards</a> with them. <strong>New team</strong>, <strong>Join a team</strong> and <strong>Invitations for you</strong> are at the top. Owners and admins can make members admins, hand over ownership, remove people, change the team's name and picture, and revoke invitations. Deleting a team deletes every board it owns.</p>

<h2 id="referrals">Referrals</h2>
<p>Invite people to Phun with your own link, and earn XP for each friend who sticks with Phun; five earn the Recruiter achievement.</p>

<h2 id="customise">Appearance, Notifications and Key binds</h2>
<p>Under <strong>Customise</strong>:</p>
<ul>
<li><strong>Appearance</strong>: the theme, the colour that leads the app, the interface size, what the dock shows and how terminals draw their cursor; see <a href="palette.html#themes">Themes</a>.</li>
<li><strong>Notifications</strong>: what reaches you, in Phun and on the desktop; see <a href="notifications.html">Notifications</a>.</li>
<li><strong>Key binds</strong>: your own keys for any action; see <a href="palette.html#keys">Key binds</a>.</li>
</ul>

<h2 id="privacy">Privacy and Your data</h2>
<p>Under <strong>Privacy and data</strong>:</p>
<ul>
<li><strong>Privacy</strong>: <strong>Public profile</strong> and <strong>Show my activity on my profile</strong>, and whether you take part in achievements and the leaderboards. A private profile also leaves the leaderboards and Around Phun.</li>
<li><strong>Your data</strong>: download or delete what Cloudcake keeps for your account.</li>
</ul>
<p>Settings, on its own tab, keeps the app-wide preferences: Startup and AI agents under Phun, and Security and Factory reset under Safety.</p>
'''


def profiles():
    return f'''
<h2 id="open">Your profile</h2>
<p>Click your user card, at the top right of every page, to open your profile. Anyone's name or avatar in Phun opens theirs, and <strong>Share</strong> copies a link that opens it in Phun. A profile is one page, each part under its own heading:</p>
<ul>
<li><strong>Level</strong>: your level and rank, the XP to the next level, your commit streak, best streak, commits this week, and how much of every achievement you've unlocked, secrets included.</li>
<li><strong>Badges</strong>: the badge shown next to your name, picked from the ones you hold, and the rest, each with its level, XP and when you got it.</li>
<li><strong>Activity</strong>: a year of activity as a calendar. Hide it, and <strong>Show it</strong> brings it back.</li>
<li><strong>Extensions</strong>: what someone has published on the <a href="extensions.html">extension hub</a>, once they have.</li>
<li><strong>Achievements</strong>: every one unlocked, newest first, with a search. Secrets stay hidden until you find them yourself.</li>
</ul>
<p>Your own profile also has <strong>Account</strong>. Signed out, <strong>Connect GitHub</strong> gives you one; a private profile is seen only by you.</p>

<h2 id="xp">Levels and achievements</h2>
<p>Using Phun earns XP: commits, achievements and badges all count, and your level climbs with it. There are over a thousand achievements for exploring Phun, its apps, code and services, plus secrets for the corners few people look in. Achievements are earned by doing things, not by opening a page or a single click.</p>

<h2 id="badges">Badges</h2>
<p>Badges mark who you are in Phun, and every badge earns XP. Some grow with what you do, and earning one, or a new level of one, is celebrated with its card. Among them:</p>
<ul>
<li><strong>Code Crafter</strong>, for writing code in the editor: XP for every line you save, with no top level, and an icon that grows richer with every level.</li>
<li><strong>Extension Contributor</strong>: a level and 250 XP for every extension of yours approved on the hub, a puzzle piece that gathers more every level.</li>
<li><strong>Bug Hunter</strong>, for accepted bug reports, and <strong>Community Voice</strong>, for taking part in discussions.</li>
<li><strong>Sponsor</strong>, with a level for every month you've sponsored Phun, and <strong>Past sponsor</strong>.</li>
<li><strong>Beta Tester</strong>, which brings beta updates, and <strong>Years of Service</strong>, a level for every year.</li>
</ul>

<h2 id="leaderboards">Leaderboards</h2>
<p>Community › Activity has the leaderboards: <strong>Levels</strong>, <strong>Commit streaks</strong>, <strong>Commits this week</strong> and <strong>Cleanest code this week</strong>, with medals for the top three. <strong>Join</strong> puts you on them, and Account › Privacy takes you off. The Phun team and moderators are on them like everyone.</p>
'''


def community():
    return f'''
<h2 id="tab">The Community tab</h2>
<p>Phun opens on <strong>Community</strong> ({k("Ctrl", "1")}). It has <strong>Activity</strong> and <strong>Discussions</strong>, and a Hall of Fame for sponsors. Signed out, it asks you to connect GitHub first.</p>

<h2 id="around">Around Phun</h2>
<p>Activity shows <strong>Around Phun</strong>: what Phun users reached lately, such as levels, achievements, badges, leaderboard milestones and newcomers, and new releases with their notes, grouped by day. It shows only users with a public profile and "Show my activity on my profile" on, and only public moments: never applications, paths or repositories. The <a href="profiles.html#leaderboards">leaderboards</a> sit beside it.</p>

<h2 id="discussions">Discussions</h2>
<p>Discussions live in Phun, in categories.<strong>New discussion</strong>, or <strong>Ask a question</strong> in a Q&amp;A category, starts one, with a preview before posting and <strong>Formatting</strong> to show the Markdown and tags you can use.</p>
<ul>
<li>Reply, @mention any Phun user, upvote, react, attach files, and copy a link to any post.</li>
<li>In Q&amp;A, mark the reply that answers the question; <strong>Unanswered</strong> finds the ones still waiting.</li>
<li><strong>Subscribe</strong> to a thread to hear about replies.</li>
<li>Moderators pin, lock and move threads, and work through reported posts; every moderator action shows in the thread.</li>
</ul>
<p>Upvotes and posts count towards the Community Voice badge.</p>

<h2 id="sponsor">Sponsoring</h2>
<p><strong>Sponsor</strong>, in the header, supports Phun's development. Sponsors get the Sponsor badge and a place in the Hall of Fame.</p>

<h2 id="more">Teams and bug reports</h2>
<p>Teams are in <a href="account.html#teams">Account › Teams</a>, and reporting a problem is in <a href="diagnostics.html#bug-reports">Bug reports</a>.</p>
'''


def extensions():
    return f'''
<h2 id="tab">The Extensions tab</h2>
<p>Extensions are your own commands, buttons, panels, themes and automations for Phun, written in Phun Script. The Extensions tab opens on the <strong>Hub</strong>, then <strong>Installed</strong>, <strong>Starred</strong> (signed in) and <strong>Create</strong>.</p>

<h2 id="hub">The Hub</h2>
<p>The Hub has extensions other users share. Search, sort by newest, name, stars or installs, and filter by tag (Theme, Services, CLI and more) or <strong>Official</strong>, for Phun's own. Each card shows what the extension does, its tags, who made it, its version and installs:</p>
<ul>
<li><strong>Install</strong> it, or <strong>Update</strong> when a newer version is out; <strong>See what changed</strong> shows the difference side by side.</li>
<li><strong>View code</strong>, in its menu, shows its code before you install it.</li>
<li>Star it to find it again on the Starred tab.</li>
</ul>
<p>Signed in, <strong>Yours</strong> lists what you published and where each review stands.</p>

<h2 id="installed">Installed</h2>
<p>Each installed extension has a switch to run it and says whether it is running, off or has a problem. Its menu has <strong>Edit code</strong>, <strong>Publish to the hub</strong> or <strong>Publish a new version</strong>, <strong>Take off the hub</strong>, and <strong>Delete</strong>, or <strong>Uninstall</strong> for one from the Hub. Installed has the Hub's search and filters too.</p>

<h2 id="create">Create</h2>
<p>Name it and pick a starting point: a blank extension or one of 23 templates, grouped by what they work with (user interface, themes, apps, services, the CLI and monitoring). Create switches it on and opens it in the code editor, with its console below and a guide and reference for Phun Script beside it.</p>
<p>Phun Script is PHP: an extension is one class that extends <code>Extension</code>, run in a sandbox, and its events are methods such as <code>onAppCreated</code>. Phun's API is classes such as <code>UI</code>, <code>Timer</code> and <code>Apps</code>, imported from the <code>Phun</code> namespace (<code>use Phun\\UI;</code>). The editor completes the API as you type and explains each method on hover. Saving reloads the extension, and problems show at their line and on its card.</p>

<h2 id="themes">Themes</h2>
<p>A theme extends <code>Theme</code> and can change Phun's colours, for light and dark separately, its fonts, how round its corners are, and its tabs' names, icons and order. Switching a theme on switches the others off. Phun's official Tokyo Night theme is on the Hub.</p>

<h2 id="publish">Publishing</h2>
<p><strong>Publish to the hub</strong> asks for a title, what it does, up to five tags and what changed, and checks first that the extension is formatted the hub's way and has no technical debt; <strong>Format it</strong> fixes the formatting. A moderator approves each version before others see it, and you're notified either way. Each approved extension counts towards the Extension Contributor badge.</p>
<p>On an extension someone else made, <strong>Suggest an update</strong> sends your changes to its author. Once they accept them, a moderator reviews them like any version.</p>

<h2 id="review">Review</h2>
<p>Moderators and the Phun team have a <strong>Review</strong> tab of versions waiting for a moderator, each with its changes side by side. <strong>Try</strong> installs the waiting version and turns it on, so they can use it before they <strong>Approve</strong> or <strong>Reject</strong> it with a reason.</p>
'''


PAGES = {
    "install": dict(title="Install", icon="developer-tools", summary="Download Phun for macOS, Windows or Linux and get it running.",
                    lede="Phun is one desktop app for macOS, Linux and Windows, with a small background service and the <code>phun</code> command.", body=install),
    "first-launch": dict(title="First launch", icon="https", summary="The welcome steps: the daemon, PHP and trust, then finding your way.",
                         lede="A few quick steps get your local PHP environment running. Only one of them asks for your password.", body=first_launch),
    "create": dict(title="Creating applications", icon="new-application", summary="Start a PHP, Node.js, C#, Go, Rust, Python or HTML app, or bring one in.",
                   lede="Start a new application from a starter, or bring in a folder or a Git repository, and Phun serves it straight away.", body=create),
    "projects": dict(title="Node.js, C#, Go, Rust and Python", icon="runtimes", summary="Projects beyond PHP, and Unity games, run, built and tested from Phun.",
                     lede="Node.js, C#, Go, Rust and Python projects, and Unity games, beside your PHP applications, with the toolchain installed when they need it.", body=projects),
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
    "terminals": dict(title="Terminals and the dock", icon="terminal-dock", summary="Artisan, Console, Tinker, Logs and AI agents, kept in the dock.",
                      lede="Artisan, a console, Tinker and every log, in a dock that floats where you put it, a key away.", body=terminals),
    "technical-debt": dict(title="Technical Debt", icon="technical-debt", summary="The work your team put off, the code smells and the deprecated PHP, with fixes.",
                           lede="The work your team put off and noted in the code, beside the code smells and deprecated PHP Phun finds, with a fix where one is safe.", body=technical_debt),
    "issues": dict(title="Issues", icon="issues", summary="A board of issues for each application, on Phun and shared with your teams, and sticky notes in the code.",
                   lede="A board of issues for each application, kept on Phun and shared with your teams, beside sticky notes that stay with the code.", body=issues),
    "frameworks": dict(title="Frameworks", icon="framework-stack", summary="Laravel, Symfony, WordPress, CodeIgniter and HTML applications, and their settings.",
                       lede="Phun knows each framework: its workers, its console, where it reads its settings, and the libraries it uses.", body=frameworks),
    "sharing": dict(title="Sharing and the network", icon="share", summary="A public URL, your own hostname, domains, proxies and other devices.",
                    lede="Share an application on a public URL, give it a hostname of your own, or open it on the devices around you.", body=sharing),
    "databases": dict(title="Databases", icon="database-browser", summary="MySQL, MariaDB, PostgreSQL, SQLite and MongoDB, browsed, drawn and snapshotted.",
                      lede="Add a database in a click, browse any table, write SQL that completes, draw a Laravel schema, and snapshot it before a migration.", body=databases),
    "mail-storage": dict(title="Mail and storage", icon="mail", summary="Every email caught, and S3-compatible storage on your machine.",
                         lede="Every email your applications send, caught and readable, and S3-compatible object storage beside them.", body=mail_storage),
    "debugging": dict(title="Debugging and profiling", icon="debugging", summary="Xdebug breakpoints in the editor, and a flame graph of any request.",
                      lede="Set a breakpoint, load the page and step through it, or profile a request to see where the time went.", body=debugging),
    "metrics": dict(title="Metrics and requests", icon="metrics", summary="Charts, the request inspector, replays and endpoints.",
                    lede="See what each application does: its requests, response times, errors, memory and CPU, and every recent request.", body=metrics),
    "request-graph": dict(title="Live Request Graph", icon="request-graph", summary="Watch requests travel through a Laravel app, read their trails, and map its events.",
                          lede="Watch each request travel through a Laravel application step by step, read where its time went, and see which listeners each event reaches.", body=request_graph),
    "security": dict(title="Dependencies", icon="dependency-audits", summary="Dependency audits, a wait before new releases, and Composer packages.",
                     lede="Audit an application's dependencies, wait out brand-new releases, and manage its Composer packages.", body=security),
    "diagnostics": dict(title="Diagnostics", icon="health-checks", summary="Health checks with fixes, a redacted report, and a daemon that won't start.",
                        lede="Health checks with a fix for each, a problem report with the secrets taken out, and what to do when the daemon will not start.", body=diagnostics),
    "notifications": dict(title="Notifications", icon="notifications", summary="Desktop notifications for jobs, mail, errors and more, with a chime.",
                          lede="What happens in the background arrives as a desktop notification, even with the window closed.", body=notifications),
    "account": dict(title="Account", icon="account", summary="Your GitHub sign-in, teams, referrals, appearance, notifications, key binds and data.",
                    lede="Your GitHub sign-in, teams, referrals, privacy, appearance and data, on one page with a tab for each.", body=account),
    "profiles": dict(title="Profiles and achievements", icon="achievements", summary="Your level, badges, activity and achievements, and the leaderboards.",
                     lede="Your level, badges, activity, extensions and achievements on one page, and the leaderboards you can join.", body=profiles),
    "community": dict(title="Community", icon="community", summary="Around Phun, the leaderboards and Discussions, where Phun opens.",
                      lede="What Phun users reached lately, the leaderboards, and discussions with the people who use Phun.", body=community),
    "extensions": dict(title="Extensions", icon="extensions", summary="Install extensions from the Hub, write your own in Phun Script, and publish them.",
                       lede="Add commands, buttons, panels, themes and automations to Phun, from the Hub or written yourself in Phun Script.", body=extensions),
    "palette": dict(title="Palette, keys and themes", icon="command-palette", summary="The command palette, key binds of your own, and light, dark and theme extensions.",
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
