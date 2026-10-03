// Mobile sidebar: toggled by [data-sidebar-toggle], closed by the scrim or Escape.
export function initSidebar() {
  const sidebar = document.getElementById("sidebar");
  const scrim = document.getElementById("scrim");
  if (!sidebar || !scrim) return;

  const setOpen = (open) => {
    sidebar.classList.toggle("open", open);
    scrim.hidden = !open;
    document.querySelectorAll("[data-sidebar-toggle]").forEach((b) =>
      b.setAttribute("aria-expanded", String(open))
    );
  };

  document.addEventListener("click", (ev) => {
    if (ev.target.closest("[data-sidebar-toggle]")) {
      setOpen(!sidebar.classList.contains("open"));
    } else if (ev.target === scrim) {
      setOpen(false);
    }
  });

  document.addEventListener("keydown", (ev) => {
    if (ev.key === "Escape") setOpen(false);
  });
}
