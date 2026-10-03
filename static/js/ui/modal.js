// Modals. Markup comes from {% modal %}; triggers use [data-modal-open="id"].
// Close with [data-modal-close], a click on the backdrop, or Escape.
export function initModals() {
  let lastTrigger = null;

  const open = (id, trigger) => {
    const el = document.getElementById(`modal-${id}`);
    if (!el) return;
    lastTrigger = trigger;
    el.hidden = false;
    const focusable = el.querySelector("input:not([type=hidden]), textarea, select, button");
    if (focusable) focusable.focus();
  };

  const closeAll = () => {
    document.querySelectorAll("[data-modal]").forEach((m) => (m.hidden = true));
    if (lastTrigger) lastTrigger.focus();
    lastTrigger = null;
  };

  document.addEventListener("click", (ev) => {
    const opener = ev.target.closest("[data-modal-open]");
    if (opener) {
      // Close any open dropdown first so the menu doesn't sit behind the modal.
      document.querySelectorAll("[data-dropdown-menu]").forEach((m) => (m.hidden = true));
      open(opener.dataset.modalOpen, opener);
      return;
    }
    if (ev.target.closest("[data-modal-close]") || ev.target.matches("[data-modal]")) closeAll();
  });

  document.addEventListener("keydown", (ev) => {
    if (ev.key === "Escape") closeAll();
  });

  // A modal that must show on load (e.g. after a form error): <div data-modal data-modal-autoopen>
  document.querySelectorAll("[data-modal][data-modal-autoopen]").forEach((m) => (m.hidden = false));
}
