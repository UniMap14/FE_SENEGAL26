(function () {
  var btn = document.querySelector(".nav-toggle");
  var header = document.querySelector(".site-header");
  if (!btn || !header) return;
  function set(open) {
    header.classList.toggle("nav-open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  }
  btn.addEventListener("click", function () { set(!header.classList.contains("nav-open")); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") set(false); });
  header.querySelectorAll(".main-nav a").forEach(function (a) {
    a.addEventListener("click", function () { set(false); });
  });
  window.addEventListener("resize", function () { if (window.innerWidth > 1200) set(false); });
})();
