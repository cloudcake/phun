<p align="center">
  <img src=".github/readme/banner.svg" alt="Phun, your pocket-sized PHP playground, for macOS, Linux and Windows." width="100%">
</p>

Phun runs your PHP applications on your own machine. Every folder you link is
served at its own `.test` address over trusted HTTPS, with the PHP version it
needs, and the databases, cache, search and mail it uses run beside it as
native processes. It is one desktop app for macOS, Linux and Windows, with a
small background service and a `phun` command for the terminal. No Docker, no
virtual machine, and no password for everyday work.

## Download

<!-- latest-release:start -->
Latest release: **[v0.4.0](https://github.com/cloudcake/phun/releases/tag/v0.4.0)**

<a href="https://github.com/cloudcake/phun/releases/download/v0.4.0/Phun_0.4.0_apple-silicon.dmg"><img src=".github/readme/download/macos-apple-silicon.svg?v=0.4.0.7" alt="Download Phun 0.4.0 for macOS, Apple Silicon: Phun_0.4.0_apple-silicon.dmg" width="100%"></a>

<a href="https://github.com/cloudcake/phun/releases/download/v0.4.0/Phun_0.4.0_intel.dmg"><img src=".github/readme/download/macos-intel.svg?v=0.4.0.7" alt="Download Phun 0.4.0 for macOS, Intel: Phun_0.4.0_intel.dmg" width="100%"></a>

<a href="https://github.com/cloudcake/phun/releases/download/v0.4.0/Phun_0.4.0_windows-x64-setup.exe"><img src=".github/readme/download/windows-installer.svg?v=0.4.0.7" alt="Download Phun 0.4.0 for Windows, Installer: Phun_0.4.0_windows-x64-setup.exe" width="100%"></a>

<a href="https://github.com/cloudcake/phun/releases/download/v0.4.0/Phun_0.4.0_amd64.deb"><img src=".github/readme/download/linux-deb.svg?v=0.4.0.7" alt="Download Phun 0.4.0 for Linux, Debian package: Phun_0.4.0_amd64.deb" width="100%"></a>

<a href="https://github.com/cloudcake/phun/releases/download/v0.4.0/Phun_0.4.0_x86_64.pkg.tar.zst"><img src=".github/readme/download/linux-arch.svg?v=0.4.0.7" alt="Download Phun 0.4.0 for Linux, Arch package: Phun_0.4.0_x86_64.pkg.tar.zst" width="100%"></a>

<!-- latest-release:end -->

## Features

<img src=".github/readme/lists/serve.svg" alt="Serve every application: link or park folders on .test over trusted HTTPS, PHP per application, new applications, domains and proxies, public shares, no admin rights needed, an infrastructure canvas, several PHP versions, native databases and caches, caught mail, S3-compatible storage, Laravel workers and developer tools." width="100%">

<br>

<img src=".github/readme/lists/editor.svg" alt="A code editor that knows Laravel: highlighting, Laravel-aware completion, live PHP checks, navigation, refactoring with a preview, formatting, git and Markdown previews." width="100%">

<br>

<img src=".github/readme/lists/insight.svg" alt="See what your applications do: metrics, a request inspector, logs and terminals, a database browser, a schema canvas, dependency audits, a command palette, themes, an MCP server, the phun command, health checks and updates." width="100%">

<!--
Earlier feature artwork, kept for reuse elsewhere: a card per feature group
and a tile per feature. Rebuilt by .github/readme/build.py with the rest.

<img src=".github/readme/applications.svg" alt="Every application on .test: folders linked to .test addresses over HTTPS." width="100%">

<p align="center">
<img src=".github/readme/features/link-and-park.svg" alt="Link a folder, or park them all. Link a folder, or park a whole directory, and every project in it is served at name.test. The web root is found for you." width="49%">
<img src=".github/readme/features/https.svg" alt="Trusted HTTPS everywhere. Every application is served over HTTPS from Phun's own local certificate authority, trusted by your browsers." width="49%">
<img src=".github/readme/features/php-per-application.svg" alt="PHP per application. Each application picks its own PHP version, and the rest keep theirs. Switch from the app or with phun use." width="49%">
<img src=".github/readme/features/new-application.svg" alt="Start something new. Create a Laravel, WordPress, CodeIgniter, CakePHP, Slim, static or HTML application, or bring an existing project or a Git repository." width="49%">
<img src=".github/readme/features/domains-and-proxies.svg" alt="Domains and proxies. Add subdomains and wildcards, proxy a .test name to a local port, or send one path such as /reverb to another server." width="49%">
<img src=".github/readme/features/share.svg" alt="Share on a public URL. Share an application through Cloudflare Tunnel, for webhooks, demos and other devices." width="49%">
<img src=".github/readme/features/no-admin.svg" alt="Works without admin rights. No admin rights to hand? Every application is also reachable at http://localhost/~name.test." width="49%">
<img src=".github/readme/features/infrastructure.svg" alt="An infrastructure canvas. Each application's services drawn as a canvas. Add a database, cache or storage and Phun writes the settings into its .env." width="49%">
</p>

<img src=".github/readme/services.svg" alt="PHP and services, natively: an application joined to PHP, databases, cache, mail, search and storage." width="100%">

<p align="center">
<img src=".github/readme/features/php-versions.svg" alt="Every PHP version you need. Several PHP versions side by side, each with its own php.ini settings and extensions." width="49%">
<img src=".github/readme/features/services.svg" alt="Native services. MySQL, MariaDB, PostgreSQL, MongoDB, Redis and Meilisearch as native services, started with the app. No Docker, no VM." width="49%">
<img src=".github/readme/features/mail.svg" alt="Every email, caught. Every email your applications send is caught and readable in the Mail viewer: rendered, as plain text or as raw source." width="49%">
<img src=".github/readme/features/object-storage.svg" alt="S3-compatible storage. Object storage on your machine, with public or private buckets and a browser for what is in them." width="49%">
<img src=".github/readme/features/laravel-workers.svg" alt="Queues, scheduler and Reverb. Queue workers, as many as you need, the scheduler and Reverb, for each Laravel application." width="49%">
<img src=".github/readme/features/developer-tools.svg" alt="Developer tools on demand. Composer, Node.js, Bun, NVM, the Laravel installer and WP-CLI, installed when you need them, without a system package manager." width="49%">
</p>

<img src=".github/readme/editor.svg" alt="A code editor that knows Laravel: completion, live checks, refactors, formatting and git." width="100%">

<p align="center">
<img src=".github/readme/features/highlighting.svg" alt="A code editor in the app. Highlighting for PHP, Blade, JavaScript, TypeScript, Vue, HTML, CSS, JSON, YAML, Markdown, shell scripts and .env files." width="49%">
<img src=".github/readme/features/completion.svg" alt="Completion that knows Laravel. Your models' attributes and relations, routes, views, config, translations, validation rules and Blade components." width="49%">
<img src=".github/readme/features/problems.svg" alt="Problems as you type. PHP is checked by the application's own PHP as you type, with the message on hover and F2 to the next one." width="49%">
<img src=".github/readme/features/navigation.svg" alt="Jump anywhere. Ctrl-click a class to open it, see every usage of a method, go to any file, and search everywhere with a double Shift." width="49%">
<img src=".github/readme/features/refactoring.svg" alt="Refactor with a preview. Rename across the application, extract a variable, and move classes between namespaces with their references updated." width="49%">
<img src=".github/readme/features/formatting.svg" alt="Formatting your way. Format with the project's own Pint or Prettier. Its .editorconfig, .prettierrc and pint.json always win." width="49%">
<img src=".github/readme/features/git.svg" alt="Git, built in. Changed lines in the gutter, changed files in the tree, the branch in the status line and the diff in a tab." width="49%">
<img src=".github/readme/features/markdown-preview.svg" alt="Markdown, previewed. Markdown files show their rendered preview beside them, updated as you type, with code blocks in colour." width="49%">
</p>

<img src=".github/readme/insight.svg" alt="See what your applications do: metrics, requests, logs, terminals, a database browser and audits." width="100%">

<p align="center">
<img src=".github/readme/features/metrics.svg" alt="Metrics per application. Requests, response times, errors, memory and CPU for every application, charted as they happen." width="49%">
<img src=".github/readme/features/request-inspector.svg" alt="A request inspector. The newest requests with status, timing, query string and headers. Cookies and authorization headers are never kept." width="49%">
<img src=".github/readme/features/terminal-dock.svg" alt="Logs and terminals in a dock. Logs, Artisan, Tinker and a console at the bottom of the window. Artisan offers your models, tables and routes as you type." width="49%">
<img src=".github/readme/features/database-browser.svg" alt="A database browser. Browse any table in one grid, and write SQL that completes tables and columns. MySQL, MariaDB and PostgreSQL." width="49%">
<img src=".github/readme/features/schema-canvas.svg" alt="Draw your schema. For Laravel: tables and model relationships as blueprints. Drag one model onto another to relate them, and review the code first." width="49%">
<img src=".github/readme/features/dependency-audits.svg" alt="Dependency audits. Audit Composer and JavaScript dependencies, and make package managers wait before installing brand-new releases." width="49%">
</p>

<img src=".github/readme/around.svg" alt="Everything around it: a command palette, themes, an MCP server, the phun command, health checks and updates." width="100%">

<p align="center">
<img src=".github/readme/features/command-palette.svg" alt="A command palette. Every page, application, Artisan command and action, a few keystrokes away." width="49%">
<img src=".github/readme/features/themes.svg" alt="Two themes. Daybreak and Nightfall, or follow the system. Your choice reaches every window and the editor." width="49%">
<img src=".github/readme/features/mcp.svg" alt="An MCP server for AI agents. Turn it on and agents such as Claude Code can list sites, switch PHP, create databases and read caught mail." width="49%">
<img src=".github/readme/features/cli.svg" alt="The phun command. Link, park, secure, share and switch PHP from your terminal. The app and the command share one daemon." width="49%">
<img src=".github/readme/features/health-checks.svg" alt="Health checks with fixes. Built-in checks for DNS, certificates, ports and PHP, each with a one-click fix when something is off." width="49%">
<img src=".github/readme/features/updates.svg" alt="Updates itself. Phun checks for new versions and installs them from the app, with the release notes beside them." width="49%">
</p>
-->

## Install

**macOS.** Open the `.dmg` and drag Phun to Applications. Builds are not yet
notarised, so on first launch right-click Phun and choose Open, or run:

```sh
xattr -cr /Applications/Phun.app
```

Use the Apple Silicon build on M-series Macs and the Intel build on older ones.

**Linux.** Install the `.deb` on Debian, Ubuntu and their derivatives:

```sh
sudo apt install ./Phun_<version>_amd64.deb
```

On Arch Linux and its derivatives, install the `.pkg.tar.zst`:

```sh
sudo pacman -U ./Phun_<version>_x86_64.pkg.tar.zst
```

On Linux, `.test` names go through systemd-resolved, or NetworkManager with
dnsmasq. A base Arch install often has neither; Phun then opens applications at
`http://localhost/~<name>`. To use `.test` names there, enable systemd-resolved:

```sh
sudo systemctl enable --now systemd-resolved
sudo ln -sf ../run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
```

**Windows.** Run the installer. It is not yet signed, so SmartScreen may warn:
choose More info, then Run anyway.

The first launch walks you through installing a PHP version and trusting
Phun's certificate authority. That step asks for your password once; nothing
after it does.

## The phun command

Everything the app does is also available from the terminal:

```sh
phun link                    # serve the current folder at <folder>.test
phun park ~/Code             # serve every project in a folder
phun use blog <version>      # give blog.test its own PHP version
phun secure blog             # serve blog.test over HTTPS
phun share blog              # give blog.test a public URL
phun status                  # what is running
phun doctor fix              # check the setup and repair what it safely can
```

### Every command

Every command takes `--json` for machine-readable output, and
`phun help <command>` shows its options. `<app>` is an application's name.

<details>
<summary><b>Applications</b>: link, park, create, domains, proxies, routes, groups</summary>

| Command | What it does |
|---|---|
| `phun sites` | List every parked and linked application |
| `phun link [name] [path]` | Serve a folder as `<name>.test` (the current folder under its own name when given nothing) |
| `phun unlink <app>` | Stop serving a linked application |
| `phun park <path>` | Serve every folder inside `<path>` as its own `.test` application |
| `phun unpark <path>` | Stop serving a parked folder's projects (linked applications stay) |
| `phun list parked` | List the parked folders, empty ones included |
| `phun new <framework> <name>` | Create an application and follow it until it is ready: `laravel`, `wordpress`, `symfony`, `codeigniter`, `cakephp`, `slim`, `git` or `html` |
| `phun start <app>` / `phun stop <app>` | Serve an application again, or stop it and its processes |
| `phun secure <app>` / `phun unsecure <app>` | Serve an application over HTTPS, or stop |
| `phun root <app> [path]` | Set the folder an application is served from, e.g. `public`; `--auto` goes back to detecting it |
| `phun front-controller <app> on\|off` | Send every request through `index.php`, or run named `.php` files directly |
| `phun domain list [app]` | List an application's domains, or every application's |
| `phun domain add <app> <domain>` | Add a domain, subdomain or wildcard |
| `phun domain remove <app> <domain>` | Remove a domain |
| `phun domain primary <app> <domain>` | Choose the main domain |
| `phun domain reset <app>` | Go back to just `<app>.test` |
| `phun proxy add ...` | Proxy a `.test` name to a local port (`phun proxy add reverb http://localhost:8080`), or one path of an application to another server |
| `phun proxy remove ...` | Remove a whole-host proxy, or one application's path rule |
| `phun proxy list` | List proxies and path rules |
| `phun route add <app> <prefix> <target>` | Send unmatched URLs under a prefix to a file, e.g. `/api` to `api/index.php` or `/` to `index.html` for a single-page app |
| `phun route remove <app> <prefix>` | Remove a routing rule |
| `phun route list [app]` | List routing rules |
| `phun group list` | List groups, their applications and group folders |
| `phun group create <name>` / `rename <from> <to>` / `delete <name>` | Create, rename or delete a group |
| `phun group order [names...]` | Set the order groups are listed in |
| `phun group assign <app> [group]` | Put an application in a group, or take it out |
| `phun group add-folder <path>` / `remove-folder <path>` | Add or remove a group folder, served like a parked folder |
| `phun group folder-group <path> [group]` | Choose the group a group folder's applications join |
| `phun instance list <app>` | List an application's extra instances behind the load balancer |
| `phun instance add <app>` / `remove <app> <instance>` | Add or remove an instance |
| `phun instance restart <app> <instance>` | Restart an instance |
| `phun instance schedule <app> <instance> on\|off` | Run the scheduler on an instance, or stop it |

</details>

<details>
<summary><b>PHP</b>: versions, settings, extensions, shims</summary>

| Command | What it does |
|---|---|
| `phun use <version>` | Set the default PHP version, used by the terminal's `php` too |
| `phun use <app> <version>` | Give one application its own PHP version |
| `phun list php` | List installed PHP versions and the default |
| `phun install php <version>` | Install a PHP version |
| `phun update php [version]` | Update one PHP version, or all of them |
| `phun uninstall php <version>` | Remove a PHP version that nothing uses |
| `phun restart php [version]` | Restart one PHP pool, or every running one |
| `phun set php <setting> <value>` | Set a `php.ini` default for every version, e.g. `memory_limit 512M` |
| `phun unset php <setting>` | Put a `php.ini` default back to PHP's own |
| `phun php ext list` | List every extension for each installed version |
| `phun php ini set <version> <name> <value>` | Set any ini directive for one version, e.g. `xdebug.mode` |
| `phun php ini unset <version> <name>` | Remove one |
| `phun php ini list` | List per-version settings and directives |
| `phun php pool set <version> max_children <n>` | Set how many PHP workers one version may run |
| `phun php pool unset <version> max_children` | Put it back to the default |
| `phun php pool list` | List per-version pool settings |
| `phun exec [--site <app>] <tool> [args...]` | Run `php`, `composer` or another tool on the PHP version an application uses |
| `phun which <tool>` | Print the binary `phun exec` would run |
| `phun coverage [args...]` | Run a script on the default PHP with pcov coverage on |
| `phun path install` / `uninstall` | Add Phun's `php`, `composer` and friends to your shell's PATH, or take them out |
| `phun path print` | Print the PATH snippet without changing any file |

</details>

<details>
<summary><b>Services and tools</b>: databases, caches, search, mail, storage, dev tools</summary>

| Command | What it does |
|---|---|
| `phun services` | List services and whether they run |
| `phun service available` | List the versions each service can install |
| `phun service install <service> <version>` | Install a service: `redis`, `memcached`, `mysql`, `mariadb`, `postgres`, `mongodb`, `meilisearch`, `typesense`, `opensearch` or `mercure` |
| `phun service change-version <service> <version>` | Move a service to another version |
| `phun service uninstall <service> <version>` | Remove a version (`--purge` deletes its data too) |
| `phun service cancel-install <service>` | Stop a download that is still running |
| `phun service start` / `stop` / `restart <service>` | Start, stop or restart a service |
| `phun service set-autostart <service> on\|off` | Choose whether it starts with Phun |
| `phun service set-port <service> <port>` | Move it to another port |
| `phun service set <service> <key> <value>` / `unset <service> <key>` | Set or remove a configuration override |
| `phun service overrides <service>` | Show its overrides |
| `phun service logs <service>` | Show the end of its log |
| `phun service add --type <type>` | Add another instance, or a per-application server such as Reverb |
| `phun service remove <service>` | Remove a per-application instance |
| `phun service set-site <service> <app>` | Move a per-application instance to another application |
| `phun tools` | List the developer tools and which are installed |
| `phun install tool <id>` / `phun uninstall tool <id>` | Install or remove `composer`, `node`, `bun`, `laravel` or `wp-cli` |
| `phun db list <service>` | List the databases in MySQL, MariaDB or PostgreSQL |
| `phun db create` / `drop <service> <name>` | Create or drop a database |
| `phun db backup` / `restore <service> <name> <file>` | Back a database up to SQL, or restore it |
| `phun db provision <app>` | Create the database an application's `.env` names |
| `phun db tables <service> <database>` | List a database's tables |
| `phun db rows <service> <database> <table>` | Print a table's rows |
| `phun db schema <service> <database>` | Print tables, columns and foreign keys |
| `phun db query <service> <database> <sql>` | Run one SQL statement |
| `phun mail list` | List caught emails, newest first |
| `phun mail show <id>` / `source <id>` | Show an email, or its raw source |
| `phun mail read <ids...>` / `delete <ids...>` | Mark emails read, or delete them |
| `phun mail clear` | Delete every caught email |
| `phun mail enable` / `disable` | Turn mail capture on or off |
| `phun mail port <port>` | Move mail capture to another SMTP port |
| `phun storage enable` / `disable` | Turn the S3-compatible storage on or off |
| `phun storage port <port>` | Move it to another port |
| `phun storage buckets` | List buckets |
| `phun storage create-bucket <name>` / `delete-bucket <name>` | Create a bucket (public unless `--private`), or delete one with its files |
| `phun storage access <name> public\|private` | Make a bucket public or private |
| `phun storage objects <bucket>` | List a bucket's files |
| `phun storage delete-objects <bucket> <keys...>` | Delete files from a bucket |
| `phun storage object-path <bucket> <key>` | Print where a file is stored on disk |
| `phun storage install-driver <app>` | Add Laravel's S3 driver to an application |

</details>

<details>
<summary><b>Laravel, Symfony and WordPress</b>: workers, consoles, .env</summary>

| Command | What it does |
|---|---|
| `phun queue enable\|disable\|start\|stop\|status\|logs <app>` | Run Laravel queue workers, as many pools as you like (`--name`, `--processes`, `--queues`, ...) |
| `phun schedule enable\|disable\|start\|stop\|status\|logs <app>` | Run Laravel's scheduler |
| `phun reverb enable\|disable\|start\|stop\|status\|logs <app>` | Run Laravel Reverb |
| `phun messenger enable\|disable\|start\|stop\|status\|logs <app>` | Run Symfony Messenger workers |
| `phun npm enable <app> <script>` | Keep `npm run <script>` running for an application |
| `phun npm disable\|start\|stop\|status\|logs <app>` | Manage that script |
| `phun console <app> [args...]` | Run `artisan` or Symfony's `bin/console` on the application's PHP |
| `phun artisan <app> <step>` | Run `key-generate`, `storage-link`, `migrate` or `optimize-clear` |
| `phun filament upgrade\|optimize\|optimize-clear <app>` | Run a Filament command |
| `phun env <app> KEY=VALUE...` | Add `.env` entries and clear Laravel's cached config |
| `phun dotenv <app>` | Print an application's `.env` |
| `phun js-install <app>` | Install JavaScript dependencies with the application's package manager |
| `phun wordpress login-url <app>` | Print a one-time admin sign-in link |
| `phun wordpress users <app>` | List the site's administrators |
| `phun wordpress auto-login <app> on\|off` | Turn one-click admin sign-in on or off |
| `phun wordpress versions` | List the WordPress versions a new site can start from |

</details>

<details>
<summary><b>Code</b>: the editor and Composer from the terminal</summary>

| Command | What it does |
|---|---|
| `phun edit <app> [path[:line]]` | Open the app's code editor at a file and line |
| `phun editor ls <app> [path]` | List a folder |
| `phun editor cat <app> <path>` | Print a file |
| `phun editor write <app> <path>` | Write a file from standard input |
| `phun editor create <app> <path>` | Create a file, or a folder with `--dir` |
| `phun editor rename` / `copy <app> <from> <to>` | Rename, move or copy a file or folder |
| `phun editor rm <app> <path>` | Delete a file or folder |
| `phun editor find <app> <text>` | Find text in the application's files |
| `phun editor files <app>` | List every file |
| `phun editor symbols <app>` | List the PHP classes, functions and other names the project declares |
| `phun editor declaration <app> <name>` | Find where a PHP name is declared |
| `phun editor psr4 <app>` | Show Composer's PSR-4 map |
| `phun editor lint <app> <path>` | Check a PHP file with `php -l` |
| `phun editor format <app> <path>` | Format a file with the project's Pint or Prettier |
| `phun editor rename-symbol <app> <name> <to>` | Rename a symbol everywhere |
| `phun editor replace <app> <text> <replacement>` | Replace text in every file |
| `phun editor extract-variable <app> <path> <line> <expression> <name>` | Extract an expression to a variable |
| `phun editor tidy-imports <app> <path>` | Sort a PHP file's `use` lines and drop unused ones |
| `phun editor import <app> <path> <class>` | Add a `use` line for a class |
| `phun editor move <app> <from> <to>` | Move a class file and update its namespace and every reference |
| `phun editor git status\|head\|stage\|unstage\|commit\|blame <app> ...` | Git status, a file at HEAD, stage, unstage, commit and blame |
| `phun packages list <app>` | List the Composer packages an application requires |
| `phun packages update <app> <package>` | Update a package within its constraint |
| `phun packages require <app> <package> [constraint]` | Add a package, or move it to a new constraint |
| `phun packages remove <app> <package>` | Remove a package |

</details>

<details>
<summary><b>Insight and debugging</b>: logs, metrics, requests, Xdebug, audits</summary>

| Command | What it does |
|---|---|
| `phun logs <app> <log>` | Show the end of a log: `laravel`, `symfony`, `php`, `queue`, `schedule`, `reverb`, `messenger`, `npm`, `vite` or `tunnel` (`--clear` empties it) |
| `phun activity` | Requests each application has served, by status code |
| `phun metrics <app>` | Request counts per minute over the last 24 hours |
| `phun requests <app>` | Recent requests with method, path, status and time |
| `phun endpoints <app>` | How often each endpoint was hit, most-hit first |
| `phun history <app>` | Commands run in an application's terminals |
| `phun favicon <app>` | Show the icon an application's page declares |
| `phun debug <app> on\|off` | Debug an application's requests with Xdebug on port 9003 |
| `phun profile <app> on\|off` | Trace requests that carry the `XDEBUG_TRACE` cookie |
| `phun debugging` | List the applications being debugged |
| `phun security scan <app>` | Find outdated packages and known advisories |
| `phun security wait <app> on\|off` | Make package managers wait before installing brand-new releases (`--days`) |

</details>

<details>
<summary><b>Sharing and the network</b>: public URLs, tunnels, other devices</summary>

| Command | What it does |
|---|---|
| `phun share <app>` | Give an application a public HTTPS address through a Cloudflare Quick Tunnel |
| `phun share-access <app>` | Guard the next share with a password (`--password`) and a time limit (`--expires-in`) |
| `phun tunnel install` | Download `cloudflared` |
| `phun tunnel share <app>` / `stop <app>` | Start or stop a Quick Tunnel |
| `phun tunnel status` | Show live tunnels |
| `phun tunnel login` | Sign in to Cloudflare for named tunnels |
| `phun tunnel create <name>` / `delete <name>` | Create or delete a named tunnel |
| `phun tunnel list` | List named tunnels |
| `phun tunnel route <tunnel> <hostname>` | Point a public hostname at a named tunnel |
| `phun tunnel set-host <app> [hostname]` | Give an application a public hostname, or clear it |
| `phun tunnel publish` / `unpublish` | Put every application with a hostname online, or take them offline |
| `phun lan enable` / `disable` / `status` | Let other devices on your network reach your `.test` applications |
| `phun remote-setup` | Make a one-time command that sets up another device to use them |

</details>

<details>
<summary><b>Phun itself</b>: health, updates, settings, privileges</summary>

| Command | What it does |
|---|---|
| `phun ping` | Check the daemon is running |
| `phun status` | The daemon, ports, DNS, certificates and PHP at a glance |
| `phun doctor` | Check the setup for common problems |
| `phun doctor fix` | Repair what it safely can |
| `phun restart daemon` | Restart the daemon |
| `phun update` | Check for a new Phun (`--yes` installs it) |
| `phun uninstall` | Uninstall Phun |
| `phun settings dns-port <port>` | The port the `.test` DNS answers on |
| `phun settings fallback-ports <http> <https>` | The ports used when 80 and 443 are taken |
| `phun settings symlink-protection on\|off` | Refuse files reached through a symlink out of the application |
| `phun settings mcp on\|off` | Let AI agents reach Phun through `phun mcp` |
| `phun mcp` | Serve Phun's tools to AI agents over MCP, e.g. `claude mcp add --scope user phun -- phun mcp` |
| `phun request '<json>'` | Send any request to the daemon and print its JSON reply |
| `phun cancel-job <id>` | Cancel a running install or new application |
| `sudo phun elevate [trust\|resolver\|ports\|lan]` | Trust Phun's certificate authority, route `.test` to Phun, allow ports 80 and 443, and (macOS) let other devices reach them |
| `sudo phun unelevate [trust\|resolver\|ports\|lan]` | Undo any of those |

</details>

## Why Phun is closed source

Phun holds more trust on your machine than most apps. It installs a
certificate authority your browsers trust, a DNS resolver for `.test`, and a
small privileged helper for the few steps that need your password. Keeping the
source closed keeps that trust in one place:

- **One origin for privileged code.** Every installer comes from this
  repository's releases, built by a single pipeline from a single codebase, so
  you always know where the code holding a certificate authority on your
  machine came from.
- **Free, without strings.** Phun costs nothing and needs no account. A closed
  codebase is what lets a small team keep it that way, with our time going into
  the app and your feedback rather than into running a public project.
- **Your feedback still shapes it.** Every discussion started here is read,
  and the roadmap follows what people run into.

## Feedback

Found a bug or have an idea?
[Start a discussion](https://github.com/cloudcake/phun/discussions).
For a security problem, please use
[private vulnerability reporting](https://github.com/cloudcake/phun/security/advisories/new)
instead.
