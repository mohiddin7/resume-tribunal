// Theme: follows the device setting until the visitor picks one. Theme-aware images swap with it.
(function () {
  var root = document.documentElement, saved = null;
  try { saved = localStorage.getItem("theme"); } catch (e) {}
  if (saved === "light" || saved === "dark") root.dataset.theme = saved;
  var dark = function () {
    return root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  };
  var paint = function () {
    document.querySelectorAll("img[data-dark]").forEach(function (img) {
      img.src = dark() ? img.dataset.dark : img.dataset.light;
    });
    var b = document.querySelector(".theme");
    if (b) b.textContent = dark() ? "Light mode" : "Dark mode";
  };
  document.addEventListener("DOMContentLoaded", function () {
    paint();
    var b = document.querySelector(".theme");
    if (b) b.addEventListener("click", function () {
      root.dataset.theme = dark() ? "light" : "dark";
      try { localStorage.setItem("theme", root.dataset.theme); } catch (e) {}
      paint();
    });
  });
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", paint);
})();
