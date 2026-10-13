// Theme (device setting until the visitor picks), theme-aware images, copy buttons, tabs, demo pause, blog search.
(function () {
  var root = document.documentElement, saved = null;
  try { saved = localStorage.getItem("theme"); } catch (e) {}
  if (saved === "light" || saved === "dark") root.dataset.theme = saved;
  var mq = matchMedia("(prefers-color-scheme: dark)");
  var dark = function () { return root.dataset.theme ? root.dataset.theme === "dark" : mq.matches; };
  var $$ = function (s) { return Array.prototype.slice.call(document.querySelectorAll(s)); };

  function paint() {
    $$("img[data-dark]").forEach(function (img) { img.src = dark() ? img.dataset.dark : img.dataset.light; });
    $$(".theme").forEach(function (b) { b.setAttribute("aria-label", dark() ? "Switch to light mode" : "Switch to dark mode"); });
  }
  mq.addEventListener("change", paint);

  document.addEventListener("DOMContentLoaded", function () {
    paint();
    $$(".theme").forEach(function (b) {
      b.addEventListener("click", function () {
        root.dataset.theme = dark() ? "light" : "dark";
        try { localStorage.setItem("theme", root.dataset.theme); } catch (e) {}
        paint();
      });
    });

    $$(".copy").forEach(function (b) {
      b.addEventListener("click", function () {
        var label = b.textContent;
        navigator.clipboard.writeText(b.dataset.copy).then(function () {
          b.textContent = "Copied"; b.classList.add("done");
          setTimeout(function () { b.textContent = label; b.classList.remove("done"); }, 1600);
        });
      });
    });

    $$('.tabs [role="tab"]').forEach(function (tab) {
      tab.addEventListener("click", function () {
        $$('.tabs [role="tab"]').forEach(function (t) {
          var on = t === tab;
          t.setAttribute("aria-selected", on);
          document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
        });
      });
    });

    $$(".pause").forEach(function (b) {
      b.addEventListener("click", function () {
        var on = root.classList.toggle("paused");
        b.setAttribute("aria-pressed", on);
        b.setAttribute("aria-label", on ? "Play animation" : "Pause animation");
      });
    });

    // How it works: a story player. Plays once on screen; tap, swipe, keys or the step list to move.
    var hiw = document.querySelector(".hiw");
    if (hiw) {
      var scenes = $$(".hiw .sc"), steps = $$(".hiw .st"), stage = hiw.querySelector(".stage"), cap = hiw.querySelector(".cap");
      var i = 0, running = false;
      if (matchMedia("(prefers-reduced-motion: reduce)").matches) hiw.classList.add("stopped");
      var go = function (n) {
        i = (n + scenes.length) % scenes.length;
        scenes.forEach(function (sc) { sc.classList.remove("on"); });
        void hiw.offsetWidth;  // restart the scene's animations
        scenes[i].classList.add("on");
        steps.forEach(function (b, k) {
          b.classList.toggle("done", k < i); b.classList.toggle("now", k === i);
          b.setAttribute("aria-selected", k === i);
          var bar = b.querySelector(".bar b"); bar.style.animation = "none"; void bar.offsetWidth; bar.style.animation = "";
        });
        cap.querySelector("strong").textContent = scenes[i].dataset.t;
        cap.querySelector("span").textContent = scenes[i].dataset.d;
      };
      steps.forEach(function (b, k) {
        b.querySelector(".bar b").addEventListener("animationend", function () { if (k === i && running) go(i + 1); });
        b.addEventListener("click", function () { go(k); });
      });
      // A quick tap moves (left third back, the rest forward); a swipe moves; a press-and-hold pauses until let go.
      // Hovering, touching to scroll and scrolling never pause it. The pause button is the other way to stop it.
      var x0 = 0, y0 = 0, timer = null, held = false, moved = false;
      stage.addEventListener("pointerdown", function (e) {
        if (e.target.closest(".pause")) return;
        x0 = e.clientX; y0 = e.clientY; held = false; moved = false;
        timer = setTimeout(function () { held = true; hiw.classList.add("hold"); }, 350);
      });
      stage.addEventListener("pointermove", function (e) {
        if (timer && (Math.abs(e.clientX - x0) > 10 || Math.abs(e.clientY - y0) > 10)) { clearTimeout(timer); timer = null; moved = true; }
      });
      var release = function (e) {
        clearTimeout(timer); timer = null;
        if (held) { held = false; hiw.classList.remove("hold"); return; }
        if (!e || e.type !== "pointerup" || e.target.closest(".pause")) return;
        var dx = e.clientX - x0;
        if (moved && Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(e.clientY - y0)) { go(dx < 0 ? i + 1 : i - 1); return; }
        if (moved) return;  // a scroll, not a tap
        var r = stage.getBoundingClientRect();
        go(e.clientX - r.left < r.width * 0.35 ? i - 1 : i + 1);
      };
      stage.addEventListener("pointerup", release);
      stage.addEventListener("pointercancel", release);
      stage.addEventListener("pointerleave", function () { if (held) release(); else { clearTimeout(timer); timer = null; } });
      stage.addEventListener("contextmenu", function (e) { e.preventDefault(); });
      stage.addEventListener("keydown", function (e) {
        if (e.key === "ArrowRight") go(i + 1);
        if (e.key === "ArrowLeft") go(i - 1);
      });
      go(0);
      hiw.classList.add("hold");
      if ("IntersectionObserver" in window) {
        new IntersectionObserver(function (es) {
          es.forEach(function (en) {
            if (en.isIntersecting && !running) { running = true; hiw.classList.remove("hold"); go(0); }
            else if (!en.isIntersecting && running) { hiw.classList.add("hold"); }
            else if (en.isIntersecting) { hiw.classList.remove("hold"); }
          });
        }, { threshold: 0.5 }).observe(stage);
      } else { running = true; hiw.classList.remove("hold"); }
    }

    var heroCta = document.querySelector(".hero .cta"), start = document.getElementById("start"), mcta = document.querySelector(".mcta");
    if (mcta && heroCta && "IntersectionObserver" in window) {
      // Hidden while the hero button, the How it works hint or the Get started section is on screen.
      var hint = document.querySelector("#how .hint"), seen = new Map();
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (en) { seen.set(en.target, en.isIntersecting); });
        var any = false; seen.forEach(function (v) { any = any || v; });
        document.body.classList.toggle("show-mcta", !any);
      });
      [heroCta, hint, start].forEach(function (el) { if (el) { seen.set(el, el === heroCta); io.observe(el); } });
    } else if (mcta) { document.body.classList.add("show-mcta"); }

    var q = document.getElementById("q");
    if (q) {
      var tag = "";
      var filter = function () {
        var text = q.value.trim().toLowerCase(), shown = 0;
        $$("#posts .post").forEach(function (c) {
          var ok = (!text || c.dataset.text.indexOf(text) > -1) && (!tag || c.dataset.tags.split("|").indexOf(tag) > -1);
          c.hidden = !ok; if (ok) shown++;
        });
        document.getElementById("empty").hidden = shown > 0;
      };
      q.addEventListener("input", filter);
      $$(".chip").forEach(function (c) {
        c.addEventListener("click", function () {
          tag = c.dataset.tag;
          $$(".chip").forEach(function (x) { x.classList.toggle("on", x === c); });
          filter();
        });
      });
    }
  });
})();
