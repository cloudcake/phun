"""Outline icons from Tabler Icons 3.50.0 (https://tabler.io/icons), 24 by 24,
drawn with a 2px round stroke. Used under the MIT licence below; only the
shapes the feature lists use are kept.

MIT License

Copyright (c) 2020-2026 Paweł Kuna

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

ICONS = {
    "link-and-park": ["M9 3h3l2 2h5a2 2 0 0 1 2 2v7a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2v-9a2 2 0 0 1 2 -2", "M17 16v2a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2v-9a2 2 0 0 1 2 -2h2"],
    "https": ["M5 13a2 2 0 0 1 2 -2h10a2 2 0 0 1 2 2v6a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2v-6", "M11 16a1 1 0 1 0 2 0a1 1 0 0 0 -2 0", "M8 11v-4a4 4 0 1 1 8 0v4"],
    "php-per-application": ["M2 12a10 9 0 1 0 20 0a10 9 0 1 0 -20 0", "M5.5 15l.395 -1.974l.605 -3.026h1.32a1 1 0 0 1 .986 1.164l-.167 1a1 1 0 0 1 -.986 .836h-1.653", "M15.5 15l.395 -1.974l.605 -3.026h1.32a1 1 0 0 1 .986 1.164l-.167 1a1 1 0 0 1 -.986 .836h-1.653", "M12 7.5l-1 5.5", "M11.6 10h2.4l-.5 3"],
    "new-application": ["M16 18a2 2 0 0 1 2 2a2 2 0 0 1 2 -2a2 2 0 0 1 -2 -2a2 2 0 0 1 -2 2m0 -12a2 2 0 0 1 2 2a2 2 0 0 1 2 -2a2 2 0 0 1 -2 -2a2 2 0 0 1 -2 2m-7 12a6 6 0 0 1 6 -6a6 6 0 0 1 -6 -6a6 6 0 0 1 -6 6a6 6 0 0 1 6 6"],
    "domains-and-proxies": ["M3 19a2 2 0 1 0 4 0a2 2 0 0 0 -4 0", "M19 7a2 2 0 1 0 0 -4a2 2 0 0 0 0 4", "M11 19h5.5a3.5 3.5 0 0 0 0 -7h-8a3.5 3.5 0 0 1 0 -7h4.5"],
    "share": ["M20.94 13.045a9 9 0 1 0 -8.953 7.955", "M3.6 9h16.8", "M3.6 15h9.4", "M11.5 3a17 17 0 0 0 0 18", "M12.5 3a16.991 16.991 0 0 1 2.529 10.294", "M16 22l5 -5", "M21 21.5v-4.5h-4.5"],
    "no-admin": ["M10.17 6.159l2.316 -2.316a2.877 2.877 0 0 1 4.069 0l3.602 3.602a2.877 2.877 0 0 1 0 4.069l-2.33 2.33", "M14.931 14.948a2.863 2.863 0 0 1 -1.486 -.79l-.301 -.302l-6.558 6.558a2 2 0 0 1 -1.239 .578l-.175 .008h-1.172a1 1 0 0 1 -.993 -.883l-.007 -.117v-1.172a2 2 0 0 1 .467 -1.284l.119 -.13l.414 -.414h2v-2h2v-2l2.144 -2.144l-.301 -.301a2.863 2.863 0 0 1 -.794 -1.504", "M15 9h.01", "M3 3l18 18"],
    "infrastructure": ["M10 19a2 2 0 1 0 -4 0a2 2 0 0 0 4 0", "M18 5a2 2 0 1 0 -4 0a2 2 0 0 0 4 0", "M10 5a2 2 0 1 0 -4 0a2 2 0 0 0 4 0", "M6 12a2 2 0 1 0 -4 0a2 2 0 0 0 4 0", "M18 19a2 2 0 1 0 -4 0a2 2 0 0 0 4 0", "M14 12a2 2 0 1 0 -4 0a2 2 0 0 0 4 0", "M22 12a2 2 0 1 0 -4 0a2 2 0 0 0 4 0", "M6 12h4", "M14 12h4", "M15 7l-2 3", "M9 7l2 3", "M11 14l-2 3", "M13 14l2 3"],
    "php-versions": ["M12 4l-8 4l8 4l8 -4l-8 -4", "M4 12l8 4l8 -4", "M4 16l8 4l8 -4"],
    "services": ["M4 6a8 3 0 1 0 16 0a8 3 0 1 0 -16 0", "M4 6v6a8 3 0 0 0 16 0v-6", "M4 12v6a8 3 0 0 0 16 0v-6"],
    "mail": ["M3 7a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v10a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-10", "M3 7l9 6l9 -6"],
    "object-storage": ["M4 7a8 4 0 1 0 16 0a8 4 0 1 0 -16 0", "M4 7c0 .664 .088 1.324 .263 1.965l2.737 10.035c.5 1.5 2.239 2 5 2s4.5 -.5 5 -2c.333 -1 1.246 -4.345 2.737 -10.035a7.45 7.45 0 0 0 .263 -1.965"],
    "laravel-workers": ["M3 17l8 5l7 -4v-8l-4 -2.5l4 -2.5l4 2.5v4l-11 6.5l-4 -2.5v-7.5l-4 -2.5l0 11.5", "M11 18v4", "M7 15.5l7 -4", "M14 7.5v4", "M14 11.5l4 2.5", "M11 13v-7.5l-4 -2.5l-4 2.5", "M7 8l4 -2.5", "M18 10l4 -2.5"],
    "developer-tools": ["M7 10h3v-3l-3.5 -3.5a6 6 0 0 1 8 8l6 6a2 2 0 0 1 -3 3l-6 -6a6 6 0 0 1 -8 -8l3.5 3.5"],
    "highlighting": ["M7 8l-4 4l4 4", "M17 8l4 4l-4 4", "M14 4l-4 16"],
    "completion": ["M10 12h4", "M9 4a3 3 0 0 1 3 3v10a3 3 0 0 1 -3 3", "M15 4a3 3 0 0 0 -3 3v10a3 3 0 0 0 3 3"],
    "problems": ["M12 9v4", "M10.363 3.591l-8.106 13.534a1.914 1.914 0 0 0 1.636 2.871h16.214a1.914 1.914 0 0 0 1.636 -2.87l-8.106 -13.536a1.914 1.914 0 0 0 -3.274 0", "M12 16h.01"],
    "navigation": ["M7.904 17.563a1.2 1.2 0 0 0 2.228 .308l2.09 -3.093l4.907 4.907a1.067 1.067 0 0 0 1.509 0l1.047 -1.047a1.067 1.067 0 0 0 0 -1.509l-4.907 -4.907l3.113 -2.09a1.2 1.2 0 0 0 -.309 -2.228l-13.582 -3.904l3.904 13.563"],
    "refactoring": ["M3 4a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -4", "M15 16a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -4", "M21 11v-3a2 2 0 0 0 -2 -2h-6l3 3m0 -6l-3 3", "M3 13v3a2 2 0 0 0 2 2h6l-3 -3m0 6l3 -3"],
    "formatting": ["M4 6l16 0", "M4 12l10 0", "M4 18l14 0"],
    "git": ["M5 18a2 2 0 1 0 4 0a2 2 0 1 0 -4 0", "M5 6a2 2 0 1 0 4 0a2 2 0 1 0 -4 0", "M15 6a2 2 0 1 0 4 0a2 2 0 1 0 -4 0", "M7 8l0 8", "M9 18h6a2 2 0 0 0 2 -2v-5", "M14 14l3 -3l3 3"],
    "markdown-preview": ["M3 7a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v10a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-10", "M7 15v-6l2 2l2 -2v6", "M14 13l2 2l2 -2m-2 2v-6"],
    "metrics": ["M4 19l16 0", "M4 15l4 -6l4 2l4 -5l4 4"],
    "request-inspector": ["M8 11a3 3 0 1 0 6 0a3 3 0 0 0 -6 0", "M16 16l-2.5 -2.5", "M3 7v-2a2 2 0 0 1 2 -2h2", "M3 17v2a2 2 0 0 0 2 2h2", "M17 3h2a2 2 0 0 1 2 2v2", "M17 21h2a2 2 0 0 0 2 -2v-2"],
    "terminal-dock": ["M8 9l3 3l-3 3", "M13 15l3 0", "M3 6a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2l0 -12"],
    "database-browser": ["M3 5a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v14a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-14", "M3 10h18", "M10 3v18"],
    "schema-canvas": ["M5 2h5v4h-5l0 -4", "M15 10h5v4h-5l0 -4", "M5 18h5v4h-5l0 -4", "M5 10h5v4h-5l0 -4", "M10 12h5", "M7.5 6v4", "M7.5 14v4"],
    "dependency-audits": ["M11.46 20.846a12 12 0 0 1 -7.96 -14.846a12 12 0 0 0 8.5 -3a12 12 0 0 0 8.5 3a12 12 0 0 1 -.09 7.06", "M15 19l2 2l4 -4"],
    "command-palette": ["M7 9a2 2 0 1 1 2 -2v10a2 2 0 1 1 -2 -2h10a2 2 0 1 1 -2 2v-10a2 2 0 1 1 2 2h-10"],
    "themes": ["M12 21a9 9 0 0 1 0 -18c4.97 0 9 3.582 9 8c0 1.06 -.474 2.078 -1.318 2.828c-.844 .75 -1.989 1.172 -3.182 1.172h-2.5a2 2 0 0 0 -1 3.75a1.3 1.3 0 0 1 -1 2.25", "M7.5 10.5a1 1 0 1 0 2 0a1 1 0 1 0 -2 0", "M11.5 7.5a1 1 0 1 0 2 0a1 1 0 1 0 -2 0", "M15.5 10.5a1 1 0 1 0 2 0a1 1 0 1 0 -2 0"],
    "mcp": ["M6 6a2 2 0 0 1 2 -2h8a2 2 0 0 1 2 2v4a2 2 0 0 1 -2 2h-8a2 2 0 0 1 -2 -2l0 -4", "M12 2v2", "M9 12v9", "M15 12v9", "M5 16l4 -2", "M15 14l4 2", "M9 18h6", "M10 8v.01", "M14 8v.01"],
    "cli": ["M5 7l5 5l-5 5", "M13 17l6 0"],
    "health-checks": ["M19.5 13.572l-7.5 7.428l-2.896 -2.868m-6.117 -8.104a5 5 0 0 1 9.013 -3.022a5 5 0 1 1 7.5 6.572", "M3 13h2l2 3l2 -6l1 3h3"],
    "updates": ["M20 11a8.1 8.1 0 0 0 -15.5 -2m-.5 -4v4h4", "M4 13a8.1 8.1 0 0 0 15.5 2m.5 4v-4h-4"],
    "laravel-cloud": ["M7 18a4.6 4.4 0 0 1 0 -9a5 4.5 0 0 1 11 2h1a3.5 3.5 0 0 1 0 7h-1", "M9 15l3 -3l3 3", "M12 12l0 9"],
    "key-binds": ["M2 8a2 2 0 0 1 2 -2h16a2 2 0 0 1 2 2v8a2 2 0 0 1 -2 2h-16a2 2 0 0 1 -2 -2l0 -8", "M6 10l0 .01", "M10 10l0 .01", "M14 10l0 .01", "M18 10l0 .01", "M6 14l0 .01", "M18 14l0 .01", "M10 14l4 .01"],
    "notifications": ["M10 5a2 2 0 0 1 4 0a7 7 0 0 1 4 6v3a4 4 0 0 0 2 3h-16a4 4 0 0 0 2 -3v-3a7 7 0 0 1 4 -6", "M9 17v1a3 3 0 0 0 6 0v-1", "M21 6.727a11.05 11.05 0 0 0 -2.794 -3.727", "M3 6.727a11.05 11.05 0 0 1 2.792 -3.727"],
    "framework-stack": ["M7 16.5l-5 -3l5 -3l5 3v5.5l-5 3l0 -5.5", "M2 13.5v5.5l5 3", "M7 16.545l5 -3.03", "M17 16.5l-5 -3l5 -3l5 3v5.5l-5 3l0 -5.5", "M12 19l5 3", "M17 16.5l5 -3", "M12 13.5v-5.5l-5 -3l5 -3l5 3v5.5", "M7 5.03v5.455", "M12 8l5 -3"],
    "diagnostics-report": ["M13 3v4a.997 .997 0 0 0 1 1h4", "M11 21h-5a2 2 0 0 1 -2 -2v-14a2 2 0 0 1 2 -2h7l5 5v3.5", "M8 9h1", "M8 12.994l3 0", "M8 16.997l2 0", "M21 15.994c0 4 -2.5 6 -3.5 6s-3.5 -2 -3.5 -6c1 0 2.5 -.5 3.5 -1.5c1 1 2.5 1.5 3.5 1.5"],
    "debugging": ["M9 9v-1a3 3 0 0 1 6 0v1", "M8 9h8a6 6 0 0 1 1 3v3a5 5 0 0 1 -10 0v-3a6 6 0 0 1 1 -3", "M3 13l4 0", "M17 13l4 0", "M12 20l0 -6", "M4 19l3.35 -2", "M20 19l-3.35 -2", "M4 7l3.75 2.4", "M20 7l-3.75 2.4"],
    "technical-debt": ["M9 5h-2a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-12a2 2 0 0 0 -2 -2h-2", "M9 5a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2a2 2 0 0 1 -2 2h-2a2 2 0 0 1 -2 -2", "M9 12l.01 0", "M13 12l2 0", "M9 16l.01 0", "M13 16l2 0"],
}
