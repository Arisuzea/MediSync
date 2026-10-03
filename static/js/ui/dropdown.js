// Generic dropdowns (notifications, user menu).
// Markup: <div data-dropdown> <button data-dropdown-trigger> ... <div data-dropdown-menu hidden>
export function initDropdowns() {
  const dropdowns = () => document.querySelectorAll("[data-dropdown]");

  const closeAll = (except = null) => {
    dropdowns().forEach((dd) => {
      if (dd === except) return;
      const menu = dd.querySelector("[data-dropdown-menu]");
      const trigger = dd.querySelector("[data-dropdown-trigger]");
      if (menu) menu.hidden = true;
      if (trigger) trigger.setAttribute("aria-expanded", "false");
    });
  };

  document.addEventListener("click", (ev) => {
    const trigger = ev.target.closest("[data-dropdown-trigger]");
    if (!trigger) {
      // Clicks inside an open menu keep it open; anywhere else closes everything.
      if (!ev.target.closest("[data-dropdown-menu]")) closeAll();
      return;
    }
    const dd = trigger.closest("[data-dropdown]");
    const menu = dd.querySelector("[data-dropdown-menu]");
    const willOpen = menu.hidden;
    closeAll(dd);
    menu.hidden = !willOpen;
    trigger.setAttribute("aria-expanded", String(willOpen));
  });

  document.addEventListener("keydown", (ev) => {
    if (ev.key === "Escape") closeAll();
  });
}
