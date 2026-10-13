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

    $$('[role="tab"]').forEach(function (tab) {
      tab.addEventListener("click", function () {
        $$('[role="tab"]').forEach(function (t) {
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
      stage.addEventListener("click", function (e) {
        if (e.target.closest(".pause")) return;
        var r = stage.getBoundingClientRect();
        go(e.clientX - r.left < r.width * 0.35 ? i - 1 : i + 1);
      });
      var x0 = null;
      stage.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; hiw.classList.add("hold"); }, { passive: true });
      stage.addEventListener("touchend", function (e) {
        hiw.classList.remove("hold");
        if (x0 === null) return;
        var dx = e.changedTouches[0].clientX - x0; x0 = null;
        if (Math.abs(dx) > 40) { e.preventDefault(); go(dx < 0 ? i + 1 : i - 1); }
      });
      stage.addEventListener("mouseenter", function () { hiw.classList.add("hold"); });
      stage.addEventListener("mouseleave", function () { hiw.classList.remove("hold"); });
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
