(() => {
  const root = document.documentElement;
  const toggle = document.querySelector("[data-theme-toggle]");
  const media = window.matchMedia("(prefers-color-scheme: dark)");

  if (!toggle) return;

  const currentTheme = () => root.dataset.theme || (media.matches ? "dark" : "light");
  const update = () => toggle.setAttribute("aria-pressed", String(currentTheme() === "dark"));

  toggle.addEventListener("click", () => {
    const theme = currentTheme() === "dark" ? "light" : "dark";
    root.dataset.theme = theme;
    try {
      localStorage.setItem("showway-theme", theme);
    } catch (_) {}
    update();
  });

  media.addEventListener("change", () => {
    if (!root.dataset.theme) update();
  });

  update();
})();
