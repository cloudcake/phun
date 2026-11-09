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
<a href="https://github.com/cloudcake/phun/releases/tag/v0.2.0"><img src=".github/readme/download/macos.svg?v=0.2.0" alt="Phun 0.2.0 for macOS" width="100%"></a>

<a href="https://github.com/cloudcake/phun/releases/download/v0.2.0/Phun_0.2.0_windows-x64-setup.exe"><img src=".github/readme/download/windows.svg?v=0.2.0" alt="Phun 0.2.0 for Windows" width="100%"></a>

<a href="https://github.com/cloudcake/phun/releases/download/v0.2.0/Phun_0.2.0_amd64.deb"><img src=".github/readme/download/linux.svg?v=0.2.0" alt="Phun 0.2.0 for Linux" width="100%"></a>
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
<img src=".github/readme/features/themes.svg" alt="Three themes. Daybreak, Nightfall and Tokyo Night, or follow the system. Your choice reaches every window and the editor." width="49%">
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

Run `phun --help` for the full list.

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
