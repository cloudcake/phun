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
    ("Applications", ("applications", "php", "services")),
    ("Working in Phun", ("editor", "terminals", "technical-debt")),
    ("Phun itself", ("updates", "collaboration", "cli")),
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
<p>Every release is on GitHub. Pick the file for your system from the latest release:</p>
<div class="downloads">
<a class="download" href="{RELEASES}"><b>macOS, Apple Silicon</b><span>M-series Macs</span><code>Phun_&lt;version&gt;_apple-silicon.dmg</code></a>
<a class="download" href="{RELEASES}"><b>macOS, Intel</b><span>Older Macs</span><code>Phun_&lt;version&gt;_intel.dmg</code></a>
<a class="download" href="{RELEASES}"><b>Windows</b><span>Windows 10 and 11, x64</span><code>Phun_&lt;version&gt;_windows-x64-setup.exe</code></a>
<a class="download" href="{RELEASES}"><b>Debian and Ubuntu</b><span>And their derivatives</span><code>Phun_&lt;version&gt;_amd64.deb</code></a>
<a class="download" href="{RELEASES}"><b>Arch Linux</b><span>And its derivatives</span><code>Phun_&lt;version&gt;_x86_64.pkg.tar.zst</code></a>
</div>

<h2 id="macos">macOS</h2>
<p>Open the <code>.dmg</code> and drag Phun to Applications. Use the Apple Silicon build on M-series Macs and the Intel build on older ones.</p>
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
<p>Create makes an application and serves it: Laravel, WordPress, Symfony, CodeIgniter, CakePHP, Slim, a static site or plain HTML. <strong>Existing project</strong> brings in a folder on this computer, a Git repository, or a Laravel Cloud application. A cloned Laravel application gets Composer, its <code>.env</code>, its key, its public storage link and its JavaScript dependencies.</p>
{sh("phun new laravel blog", "phun new symfony shop --webapp")}
<p><strong>Groups</strong> keep the Overview tidy: put applications in a group, order the groups, and add a group folder that is served like a parked one.</p>

<h2 id="page">An application's page</h2>
<p>Click an application to open its page. The header has <strong>Open</strong> (the code editor, the browser, the folder), the terminals and <strong>Share</strong>. The tabs:</p>
<ul>
<li><strong>Metrics</strong>: requests, response times, errors, memory and CPU, the latest requests and the endpoints hit.</li>
<li><strong>Infrastructure</strong>: the canvas of its services; see <a href="services.html">Services</a>.</li>
<li><strong>Security</strong>: dependency audits and Composer packages.</li>
<li><strong>Technical Debt</strong>: see <a href="technical-debt.html">Technical Debt</a>.</li>
<li><strong>Sharing</strong>: a public URL through Cloudflare.</li>
<li><strong>Settings</strong>: General, PHP, HTTPS and the Environment editor.</li>
</ul>
<p>Every application shows its framework and the libraries it uses, with their versions. When its setup is wrong, such as an <code>APP_URL</code> that is not the address Phun serves it on or an empty <code>APP_KEY</code>, the page lists it with a one-click fix.</p>

<h2 id="https">HTTPS and domains</h2>
<p>Every application is served over HTTPS with a certificate from Phun's local certificate authority, trusted by your browsers. Add subdomains and wildcards, proxy a <code>.test</code> name to a local port, or send one path, such as <code>/reverb</code>, to another server:</p>
{sh("phun domain add blog api.blog.test", "phun proxy add reverb http://localhost:8080")}
<p>An HTML application is served straight from its folder, with no PHP version needed. Hidden files such as <code>.env</code> and <code>.git</code> are never served from any application.</p>

<h2 id="share">Share on a public URL</h2>
<p>Share gives an application a public HTTPS address through a Cloudflare Quick Tunnel, for webhooks, demos and other devices. It can ask visitors for a password and close itself after an hour, a day or a week, and the Sharing tab lists who reached it. While it is shared, a QR code opens it on your phone.</p>
{sh("phun share blog")}
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
<p>For Laravel, the canvas runs queue workers (as many as you need, each with its own queues and log), the scheduler and Reverb. Symfony gets Messenger workers. WordPress, CodeIgniter, Drupal and Magento get scheduled tasks, which run the application's own cron command every minute.</p>
{sh("phun queue enable blog", "phun schedule enable blog", "phun messenger enable shop")}

<h2 id="services-page">The Services page</h2>
<p>Services, on the Overview, lists every service Phun can run, installed or not, with Install or Update in its row. They run natively, started with Phun: no Docker, no virtual machine.</p>
<ul>
<li><strong>Databases</strong>: MySQL, MariaDB, PostgreSQL and MongoDB.</li>
<li><strong>Cache</strong>: Redis and Memcached.</li>
<li><strong>Search</strong>: Meilisearch, Typesense and OpenSearch.</li>
<li><strong>Live updates</strong>: Mercure.</li>
</ul>
{sh("phun services", "phun service install redis <version>", "phun service set-port mysql 3307")}

{{{{figure:mail}}}}
<h2 id="mail">Mail</h2>
<p>Every email your applications send is caught and readable in the Mail viewer ({k("Ctrl", "5")}): rendered, as plain text or as the raw source. Nothing leaves your machine.</p>

<h2 id="storage">S3-compatible storage</h2>
<p>Object storage on your machine, with public or private buckets and a browser for what is in them. Added to a Laravel application from the canvas, Phun creates its bucket and fills in its settings, so the <code>s3</code> disk works as it would against S3.</p>

<h2 id="data">Databases, browsed</h2>
<p>A database card opens the database browser: one grid for any table, and SQL that completes tables and columns, for MySQL, MariaDB and PostgreSQL. For Laravel, <strong>Open Schema</strong> draws the tables and model relationships as blueprints; drag one model onto another to relate them, and review the change to each model before it is written.</p>

<h2 id="tools">Developer tools</h2>
<p>Composer, Node.js, Bun, the Laravel installer, WP-CLI and Chrome for Testing install when you need them, without a system package manager.</p>
{sh("phun tools", "phun install tool node")}

<h2 id="cloud">Laravel Cloud</h2>
<p>From a Laravel application's Infrastructure › Laravel Cloud, sign in with an API token, link it to a Cloud application, see what Cloud is missing compared with Phun, create it after confirming what Cloud bills for, and deploy. Phun keeps no copy of your token.</p>
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

<h2 id="git">Git</h2>
<p>Changed lines in the gutter, changed files in the tree, the branch in the status line and the diff in a tab. The Changes view beside the tree stages, unstages and commits ({k("Ctrl", "Enter")}, {k("Cmd", "Enter")} on macOS), and Blame shows who last changed each line.</p>

<h2 id="tests">Tests</h2>
<p>A test file shows a run marker beside every Pest test, <code>describe</code> group and PHPUnit method. Run one, or debug it; results arrive in a panel under the editor as each test finishes, and a failure shows on the line where it stopped. {k("Ctrl", "Shift", "F10")} runs the test at the cursor.</p>

<h2 id="debugging">Debugging</h2>
{{{{figure:debugging}}}}
<p>The bug button turns Xdebug on for the application. Click beside a line number to set a breakpoint, load the page, and it stops there. The panel under the editor steps over ({k("F8")}), into ({k("F7")}) and out ({k("Shift", "F8")}), continues on {k("F9")}, shows the stack and opens arrays and objects in the variables.</p>

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
<li><strong>Logs</strong>: every log the application has, each in its own tab.</li>
</ul>
<p>Artisan and Tinker show only for a Laravel application. Clicking anywhere outside an open terminal minimises it to its badge in the dock; the badge brings it back. The code editor minimises there too.</p>

<h2 id="keys">Keys</h2>
<ul>
<li>{k("`")} opens the Console for the application you are on, and closes it again, even from inside it.</li>
<li>{k("Shift", "`")} moves to its next open terminal.</li>
<li>Settings › Key binds can give your own keys to opening every terminal at once, the code editor, minimising the terminal and hiding the dock.</li>
</ul>

<h2 id="logs">Logs</h2>
<p>Logs shows the application's own log (Laravel's, or Symfony's <code>var/log</code>), PHP's, and those of its queue workers, scheduler, Reverb, Messenger and tunnel. Every file and line in a stack trace inside the application opens the editor there. <strong>Exceptions</strong> lists each exception once, with how often it was thrown and when last. Each log can be emptied.</p>
{sh("phun logs blog laravel", "phun logs blog queue --clear")}

<h2 id="history">History and Run again</h2>
<p>Commands run in an application's terminals are kept in its history (<code>phun history blog</code>). The command palette's <strong>Run again</strong> group lists the Artisan commands you ran recently, so a repeat is {k("Ctrl", "K")}, a few letters and {k("Enter")}.</p>
{sh("phun console blog migrate:status   # artisan or bin/console, on the application's PHP")}
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

<h2 id="act">Act on an item</h2>
<p>Select an item to see its code with the line marked, then open the editor at that line or apply its fix. A <strong>Fix</strong> button makes the change where it is safe, such as a nullable parameter type, a cast's new name, a <code>${{}}</code> in a string or the missing blank line.</p>
<p>Each line names who last changed it, from git, and you can search by that name. Changes not committed yet say so.</p>

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
{next_note("Updates gains a <strong>Previous version</strong> row with a <strong>Go back</strong> button. It installs the version your last update replaced, or else the release before the one you run, at any time, not only when the daemon fails to start.")}

<h2 id="whats-new">What's new</h2>
<p>The release notes for each version are in Updates, as Features, Changed and Fixed. Every release is also on <a href="https://github.com/cloudcake/phun/releases">GitHub</a>.</p>

<h2 id="php-and-services">PHP, services and tools</h2>
<p>PHP versions, services and developer tools update on their own rows: Settings for PHP, Services for the rest. A download that hits a server hiccup tries again by itself.</p>
'''


def collaboration():
    return f'''
{next_note("Collaboration arrives with the next Phun release. This page describes it as it will ship.")}
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


PAGES = {
    "install": dict(title="Install", icon="developer-tools", summary="Download Phun for macOS, Windows or Linux and get it running.",
                    lede="Phun is one desktop app for macOS, Linux and Windows, with a small background service and the <code>phun</code> command.", body=install),
    "first-launch": dict(title="First launch", icon="https", summary="The welcome steps: the daemon, PHP and trust, then finding your way.",
                         lede="A few quick steps get your local PHP environment running. Only one of them asks for your password.", body=first_launch),
    "applications": dict(title="Linking and parking", icon="link-and-park", summary="Serve a folder, or every project in one, at its own .test address.",
                         lede="Link a folder, or park a whole directory, and every project in it is served at <code>name.test</code> over trusted HTTPS.", body=applications),
    "php": dict(title="PHP versions", icon="php-versions", summary="Several PHP versions side by side, one per application.",
                lede="Several PHP versions side by side, each with its own <code>php.ini</code> settings and extensions, and each application on the one it needs.", body=php),
    "services": dict(title="Services and infrastructure", icon="infrastructure", summary="Databases, cache, search, mail and storage on the infrastructure canvas.",
                     lede="Databases, cache, search, mail and storage run beside your applications as native processes, and the infrastructure canvas wires them in.", body=services),
    "editor": dict(title="The code editor", icon="highlighting", summary="Completion that knows Laravel, live checks, refactors, git, tests and debugging.",
                   lede="A code editor inside Phun that knows your application: completion, live PHP checks, refactors, formatting, git, tests and Xdebug.", body=editor),
    "terminals": dict(title="Terminals and the dock", icon="terminal-dock", summary="Artisan, Console, Tinker and Logs at the bottom of the window.",
                      lede="Artisan, a console, Tinker and every log, in a dock at the bottom of the window, a key away.", body=terminals),
    "technical-debt": dict(title="Technical Debt", icon="technical-debt", summary="The work your team put off, the code smells and the deprecated PHP, with fixes.",
                           lede="The work your team put off and noted in the code, beside the code smells and deprecated PHP Phun finds, with a fix where one is safe.", body=technical_debt),
    "updates": dict(title="Updates and rollback", icon="updates", summary="Update Phun from the app, try betas, and go back if a version gives you trouble.",
                    lede="Phun checks for new versions and installs them from the app, with the release notes beside them.", body=updates),
    "collaboration": dict(title="Collaboration", icon="share", next=True, summary="Invite teammates into your Phun, end-to-end encrypted.",
                          lede="Invite teammates into your Phun over the internet or your network, and choose what each one may do.", body=collaboration),
    "cli": dict(title="The phun command", icon="cli", summary="Link, park, secure, share and switch PHP from your terminal.",
                lede="Link, park, secure, share and switch PHP from your terminal. Everything the app does, the command does too.", body=cli),
}


def page(slug):
    return PAGES[slug]
