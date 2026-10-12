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
