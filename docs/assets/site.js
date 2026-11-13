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
})();
