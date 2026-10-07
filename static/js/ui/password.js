// Show/hide password. Markup: .pw > input + button[data-pw-toggle] > [data-pw-off] (eye-off) + [data-pw-on] (eye)
export function initPasswordToggles() {
  document.addEventListener("click", (ev) => {
    const btn = ev.target.closest("[data-pw-toggle]");
    if (!btn) return;
    const input = btn.closest(".pw").querySelector("input");
    const show = input.type === "password";
    input.type = show ? "text" : "password";
    btn.setAttribute("aria-pressed", String(show));
    btn.setAttribute("aria-label", show ? "Hide password" : "Show password");
    btn.querySelector("[data-pw-off]").hidden = show;
    btn.querySelector("[data-pw-on]").hidden = !show;
  });
}
