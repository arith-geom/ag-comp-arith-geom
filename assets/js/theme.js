// Has to be in the head tag, otherwise a flicker effect will occur.

let toggleThemeSetting = () => {
  let themeSetting = determineThemeSetting();
  if (themeSetting == "system") {
    setThemeSetting("light");
  } else if (themeSetting == "light") {
    setThemeSetting("dark");
  } else {
    setThemeSetting("system");
  }
};

let setThemeSetting = (themeSetting) => {
  localStorage.setItem("theme", themeSetting);

  document.documentElement.setAttribute("data-theme-setting", themeSetting);

  applyTheme();
};

let applyTheme = () => {
  let theme = determineComputedTheme();

  transTheme();

  document.documentElement.setAttribute("data-theme", theme);
};

let transTheme = () => {
  document.documentElement.classList.add("transition");
  window.setTimeout(() => {
    document.documentElement.classList.remove("transition");
  }, 500);
};

let determineThemeSetting = () => {
  let themeSetting = localStorage.getItem("theme");
  if (themeSetting != "dark" && themeSetting != "light" && themeSetting != "system") {
    themeSetting = "system";
  }
  return themeSetting;
};

let determineComputedTheme = () => {
  let themeSetting = determineThemeSetting();
  if (themeSetting == "system") {
    const userPref = window.matchMedia;
    if (userPref && userPref("(prefers-color-scheme: dark)").matches) {
      return "dark";
    } else {
      return "light";
    }
  } else {
    return themeSetting;
  }
};

let initTheme = () => {
  let themeSetting = determineThemeSetting();

  setThemeSetting(themeSetting);

  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", ({ matches }) => {
    applyTheme();
  });
};

initTheme();

if (document.documentElement) {
  const currentTheme = determineComputedTheme();
  document.documentElement.setAttribute("data-theme", currentTheme);
}

document.addEventListener("DOMContentLoaded", function () {
  const mode_toggle = document.getElementById("light-toggle");
  if (mode_toggle) {
    mode_toggle.addEventListener("click", function () {
      toggleThemeSetting();
    });
  }

  const theme_toggle = document.getElementById("theme-toggle");
  if (theme_toggle) {
    theme_toggle.addEventListener("click", function () {
      toggleThemeSetting();
    });
  }
});
