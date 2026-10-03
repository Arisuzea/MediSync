// Toasts. Django `messages` are rendered into #troot by the server;
// this module auto-dismisses them and exposes showToast() for JS-triggered ones.
const DISMISS_MS = 4200;

function dismiss(el) {
  el.style.transition = "opacity .25s, transform .25s";
  el.style.opacity = "0";
  el.style.transform = "translateX(20px)";
  setTimeout(() => el.remove(), 260);
}

export function showToast(kind, title, message = "") {
  const root = document.getElementById("troot");
  if (!root) return;
  const el = document.createElement("div");
  el.className = `toast ${kind}`;
  const body = document.createElement("div");
  const strong = document.createElement("strong");
  strong.textContent = title; // textContent => no HTML injection
  body.append(strong);
  if (message) {
    const p = document.createElement("p");
    p.textContent = message;
    body.append(p);
  }
  el.append(body);
  root.append(el);
  setTimeout(() => dismiss(el), DISMISS_MS);
}

export function initToasts() {
  document.querySelectorAll("#troot .toast").forEach((el) => {
    setTimeout(() => dismiss(el), DISMISS_MS);
  });
}
