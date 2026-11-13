/* Phun documentation: the theme toggle, the phone menu, scroll-in, and the
   home page's P gathering from the dots, as the app's launch intro does.
   The theme is set before first paint by the inline script in <head>. */
(function () {
  "use strict";
  var root = document.documentElement;
  var KEY = "phun-docs-theme";
  var system = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function stored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function apply(theme) {
    root.setAttribute("data-theme", theme);
    var btn = document.querySelector(".theme-toggle");
    if (btn) {
      var other = theme === "dark" ? "Daybreak" : "Nightfall";
      btn.setAttribute("data-tip", "Switch to " + other);
      btn.setAttribute("aria-label", "Switch to " + other);
    }
  }
  apply(root.getAttribute("data-theme") || (system && system.matches ? "dark" : "light"));
  if (system && system.addEventListener) {
    system.addEventListener("change", function (e) {
      if (!stored()) apply(e.matches ? "dark" : "light");
    });
  }
  var toggle = document.querySelector(".theme-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      var follows = (system && system.matches ? "dark" : "light") === next;
      try {
        if (follows) localStorage.removeItem(KEY); else localStorage.setItem(KEY, next);
      } catch (e) { /* private mode: the choice lasts for this page */ }
      apply(next);
    });
  }

  var menu = document.querySelector(".menu-toggle");
  var scrim = document.querySelector(".scrim");
  function closeMenu() {
    document.body.classList.remove("nav-open");
    if (menu) menu.setAttribute("aria-expanded", "false");
  }
  if (menu) {
    menu.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      menu.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }
  if (scrim) scrim.addEventListener("click", closeMenu);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeMenu(); });

  var reveals = document.querySelectorAll(".reveal");
  if (!still && "IntersectionObserver" in window) {
    var seen = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          seen.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (el) { seen.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  var canvas = document.querySelector(".app-icon canvas");
  if (canvas && !still && canvas.getContext && typeof Path2D !== "undefined") gather(canvas);

  /* Dots on the ground's 20px grid glide onto the icon's lines with a slight
     overshoot, turning from the ground's colour to the logo's red, and fade
     as the drawn P resolves at 1.15s (CSS). The lines are read from the icon
     itself. */
  function gather(canvas) {
    var ctx = canvas.getContext("2d");
    var icon = canvas.parentNode.querySelector("svg.icon");
    var mark = icon && icon.querySelector(".mark");
    if (!mark) return;
    var edges = [];
    mark.querySelectorAll("line").forEach(function (l) {
      edges.push(["x1", "y1", "x2", "y2"].map(function (k) { return Number(l.getAttribute(k)); }));
    });
    mark.querySelectorAll("polygon[fill=none]").forEach(function (poly) {
      var pts = poly.getAttribute("points").trim().split(/\s+/).map(function (pt) { return pt.split(",").map(Number); });
      pts.forEach(function (pt, i) {
        var next = pts[(i + 1) % pts.length];
        edges.push([pt[0], pt[1], next[0], next[1]]);
      });
    });
    var box = canvas.getBoundingClientRect();
    var size = box.width || 404;
    var tile = size - (size > 300 ? 300 : 220);
    var origin = (size - tile) / 2;
    var scale = tile / 200;
    var dpr = window.devicePixelRatio || 1;
    canvas.width = size * dpr;
    canvas.height = size * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var dots = [];
    var centre = origin + tile / 2;
    edges.forEach(function (e) {
      var length = Math.hypot(e[2] - e[0], e[3] - e[1]);
      var steps = Math.max(1, Math.round(length / 3.4));
      for (var i = 0; i <= steps; i++) {
        var x = e[0] + ((e[2] - e[0]) * i) / steps;
        var y = e[1] + ((e[3] - e[1]) * i) / steps;
        var angle = Math.random() * Math.PI * 2;
        var reach = tile * (0.85 + Math.random());
        dots.push({
          sx: Math.round((centre + Math.cos(angle) * reach) / 20) * 20,
          sy: Math.round((centre + Math.sin(angle) * reach) / 20) * 20,
          tx: origin + (x + 100) * scale,
          ty: origin + (y + 100) * scale,
          delay: 120 + Math.random() * 520,
          travel: 700 + Math.random() * 260
        });
      }
    });
    var dark = root.getAttribute("data-theme") === "dark";
    var ink = dark ? [255, 255, 255] : [21, 23, 28];
    var red = (getComputedStyle(icon).color.match(/\d+/g) || [229, 72, 77]).slice(0, 3).map(Number);
    function colour(k, alpha) {
      var c = ink.map(function (v, i) { return Math.round(v + (red[i] - v) * k); });
      return "rgba(" + c[0] + "," + c[1] + "," + c[2] + "," + alpha + ")";
    }
    function back(t) { return 1 + 2.35 * Math.pow(t - 1, 3) + 1.35 * Math.pow(t - 1, 2); }
    var RESOLVE = 1250, FADE = 380, start = performance.now();
    function frame(now) {
      var t = now - start;
      ctx.clearRect(0, 0, size, size);
      var fade = t < RESOLVE ? 1 : Math.max(0, 1 - (t - RESOLVE) / FADE);
      dots.forEach(function (d) {
        var k = Math.min(1, Math.max(0, (t - d.delay) / d.travel));
        var e = back(k);
        var px = d.sx + (d.tx - d.sx) * e;
        var py = d.sy + (d.ty - d.sy) * e;
        ctx.fillStyle = colour(Math.min(1, k), (0.35 + 0.65 * k) * fade);
        ctx.beginPath();
        ctx.arc(px, py, 1.1 + k * 0.4, 0, Math.PI * 2);
        ctx.fill();
      });
      if (fade > 0) requestAnimationFrame(frame);
      else canvas.remove();
    }
    requestAnimationFrame(frame);
  }
})();
