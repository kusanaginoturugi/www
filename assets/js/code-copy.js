(function () {
  "use strict";

  // Reveal the copy buttons once the DOM is ready. This script is included in
  // the <head>, so the code blocks may not exist yet when it first runs.
  function revealButtons() {
    var buttons = document.querySelectorAll(".code-block .code-copy[hidden]");
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].hidden = false;
    }
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", revealButtons);
  } else {
    revealButtons();
  }

  function flash(button) {
    var label = button.querySelector(".code-copy-label");
    var previous = label ? label.textContent : null;
    button.classList.add("is-copied");
    if (label) label.textContent = "Copied";
    window.setTimeout(function () {
      button.classList.remove("is-copied");
      if (label && previous !== null) label.textContent = previous;
    }, 2000);
  }

  function legacyCopy(text) {
    var area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.style.position = "absolute";
    area.style.left = "-9999px";
    document.body.appendChild(area);
    area.select();
    var ok = false;
    try {
      ok = document.execCommand("copy");
    } catch (e) {
      ok = false;
    }
    document.body.removeChild(area);
    return ok;
  }

  function copyFrom(button) {
    var container = button.closest(".code-block");
    if (!container) return;
    var pre = container.querySelector("pre");
    if (!pre) return;
    var source = pre.querySelector("code") || pre;
    var text = source.innerText;

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(
        function () { flash(button); },
        function () { if (legacyCopy(text)) flash(button); }
      );
    } else if (legacyCopy(text)) {
      flash(button);
    }
  }

  document.addEventListener("click", function (event) {
    var button = event.target.closest(".code-copy");
    if (button) copyFrom(button);
  });
})();
