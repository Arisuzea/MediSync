"""SVG icon path data, copied from the prototype's `P` object.

Each value is the inner markup of a 24x24 stroke icon (no <svg> wrapper).
"""

ICONS = {
    "dashboard": (
        '<rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/>'
    ),
    "calplus": (
        '<rect x="3" y="4" width="18" height="18" rx="2.5"/><path d="M8 2v4M16 2v4M3 10h18M12 14v6M9 17h6"/>'
    ),
    "calcheck": (
        '<rect x="3" y="4" width="18" height="18" rx="2.5"/><path d="M8 2v4M16 2v4M3 10h18"/><path d="m9 15.5 2 2 4-4"/>'
    ),
    "list": (
        '<path d="M8 6h13M8 12h13M8 18h13"/><path d="M3 6h.01M3 12h.01M3 18h.01"/>'
    ),
    "history": (
        '<path d="M3 12a9 9 0 1 0 2.9-6.6L3 8"/><path d="M3 3v5h5"/><path d="M12 8v4.5l3 1.8"/>'
    ),
    "user": (
        '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>'
    ),
    "users": (
        '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>'
    ),
    "settings": (
        '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.6 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.6a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09A1.65 1.65 0 0 0 15 4.6a1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>'
    ),
    "bell": (
        '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>'
    ),
    "search": (
        '<circle cx="11" cy="11" r="7.5"/><path d="m21 21-4.3-4.3"/>'
    ),
    "menu": (
        '<path d="M4 6h16M4 12h16M4 18h16"/>'
    ),
    "x": (
        '<path d="M18 6 6 18M6 6l12 12"/>'
    ),
    "check": (
        '<path d="M20 6 9 17l-5-5"/>'
    ),
    "checkc": (
        '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/>'
    ),
    "left": (
        '<path d="m12 19-7-7 7-7M19 12H5"/>'
    ),
    "right": (
        '<path d="M5 12h14M12 5l7 7-7 7"/>'
    ),
    "cr": (
        '<path d="m9 18 6-6-6-6"/>'
    ),
    "cl": (
        '<path d="m15 18-6-6 6-6"/>'
    ),
    "cd": (
        '<path d="m6 9 6 6 6-6"/>'
    ),
    "clock": (
        '<circle cx="12" cy="12" r="9.5"/><path d="M12 6.5V12l4 2"/>'
    ),
    "steth": (
        '<path d="M5 3v6a5 5 0 0 0 10 0V3"/><path d="M10 14v1.5a5 5 0 0 0 10 0V14"/><circle cx="20" cy="11" r="2"/>'
    ),
    "tooth": (
        '<path d="M12 5.5C10.5 3.9 8.6 3 7 3 4.8 3 3 4.9 3 7.4c0 2.3.8 3.6 1.4 5.6.5 1.8.5 3.4 1 5.2.4 1.5 1 2.8 2.1 2.8 1.3 0 1.5-1.6 1.8-3.4.3-1.7.6-2.9 2.7-2.9s2.4 1.2 2.7 2.9c.3 1.8.5 3.4 1.8 3.4 1.1 0 1.7-1.3 2.1-2.8.5-1.8.5-3.4 1-5.2C20.2 11 21 9.7 21 7.4 21 4.9 19.2 3 17 3c-1.6 0-3.5.9-5 2.5z"/>'
    ),
    "shield": (
        '<path d="M12 22s8-4 8-10V5.5L12 2.5 4 5.5V12c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>'
    ),
    "alert": (
        '<path d="M10.3 3.9 1.9 18a2 2 0 0 0 1.7 3h16.8a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4.5M12 17h.01"/>'
    ),
    "info": (
        '<circle cx="12" cy="12" r="9.5"/><path d="M12 16.5V11M12 8h.01"/>'
    ),
    "refresh": (
        '<path d="M21 12a9 9 0 0 0-9-9 9 9 0 0 0-6.7 3L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9 9 0 0 0 6.7-3L21 16"/><path d="M21 21v-5h-5"/>'
    ),
    "sms": (
        '<path d="M21 14.5a2 2 0 0 1-2 2H8l-5 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><path d="M8 9h8M8 12.5h5"/>'
    ),
    "logout": (
        '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="m16 17 5-5-5-5M21 12H9"/>'
    ),
    "pin": (
        '<path d="M20 10.5c0 6-8 11.5-8 11.5S4 16.5 4 10.5a8 8 0 0 1 16 0z"/><circle cx="12" cy="10.5" r="3"/>'
    ),
    "zap": (
        '<path d="M13 2 3 14h7l-1 8 11-12h-8z"/>'
    ),
    "star": (
        '<path d="m12 2.5 2.9 5.9 6.6 1-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-1z"/>'
    ),
    "trend": (
        '<path d="m22 7-8.5 8.5-5-5L2 17"/><path d="M16 7h6v6"/>'
    ),
    "file": (
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 13h6M9 17h4"/>'
    ),
    "sliders": (
        '<path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6"/>'
    ),
    "lock": (
        '<rect x="3" y="11" width="18" height="11" rx="2.5"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>'
    ),
    "help": (
        '<circle cx="12" cy="12" r="9.5"/><path d="M9.6 9.3a2.6 2.6 0 0 1 5 .9c0 1.7-2.6 2.1-2.6 3.6"/><path d="M12 17.5h.01"/>'
    ),
    "hour": (
        '<path d="M5 22h14M5 2h14"/><path d="M17 22v-4.2a2 2 0 0 0-.6-1.4L12 12l-4.4 4.4A2 2 0 0 0 7 17.8V22M7 2v4.2a2 2 0 0 0 .6 1.4L12 12l4.4-4.4A2 2 0 0 0 17 6.2V2"/>'
    ),
    "act": (
        '<path d="M3 12h4l2.5-6 4 13 2.5-7h5"/>'
    ),
    "plus": (
        '<path d="M12 5v14M5 12h14"/>'
    ),
    "inbox": (
        '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>'
    ),
    "spark": (
        '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6.3 6.3l2.8 2.8M14.9 14.9l2.8 2.8M17.7 6.3l-2.8 2.8M9.1 14.9l-2.8 2.8"/>'
    ),
    "home": (
        '<path d="m3 10.5 9-7.5 9 7.5V21a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z"/><path d="M9 22V12h6v10"/>'
    ),
}


# Lucide icons (ISC licence, lucide-static) used by the Figma-matched shell and pages.
# Prefixed "lu-" so the prototype icons above keep working unchanged. Render with
# {% icon "lu-bell" 20 %}  (the icon tag draws "lu-" icons at Lucide's stroke width of 2).
ICONS.update({
    "lu-layout-dashboard": (
        '<rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>'
    ),
    "lu-calendar-plus": (
        '<path d="M16 18h6"/><path d="M16 2v3"/><path d="M19 15v6"/><path d="M21 11.5V5a2 2 0 00-2-2H5a2 2 0 00-2 2v14a2 2 0 002 2h8.3"/><path d="M3 9h18"/><path d="M8 2v3"/>'
    ),
    "lu-user-round": (
        '<circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 0 0-16 0"/>'
    ),
    "lu-circle-x": (
        '<circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/>'
    ),
    "lu-calendar-clock": (
        '<path d="M16 14v2.2l1.6 1"/><path d="M16 2v3"/><path d="M21 7.338V5a2 2 0 00-2-2H5a2 2 0 00-2 2v14a2 2 0 002 2h2.338"/><path d="M3 9h5.859"/><path d="M8 2v3"/><circle cx="16" cy="16" r="6"/>'
    ),
    "lu-award": (
        '<path d="m15.477 12.89 1.515 8.526a.5.5 0 0 1-.81.47l-3.58-2.687a1 1 0 0 0-1.197 0l-3.586 2.686a.5.5 0 0 1-.81-.469l1.514-8.526"/><circle cx="12" cy="8" r="6"/>'
    ),
    "lu-bottle-wine": (
        '<path d="M10 3a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v2a6 6 0 0 0 1.2 3.6l.6.8A6 6 0 0 1 17 13v8a1 1 0 0 1-1 1H8a1 1 0 0 1-1-1v-8a6 6 0 0 1 1.2-3.6l.6-.8A6 6 0 0 0 10 5z"/><path d="M17 13h-4a1 1 0 0 0-1 1v3a1 1 0 0 0 1 1h4"/>'
    ),
    "lu-bell-ring": (
        '<path d="M10.268 21a2 2 0 0 0 3.464 0"/><path d="M22 8c0-2.3-.8-4.3-2-6"/><path d="M3.262 15.326A1 1 0 0 0 4 17h16a1 1 0 0 0 .74-1.673C19.41 13.956 18 12.499 18 8A6 6 0 0 0 6 8c0 4.499-1.411 5.956-2.738 7.326"/><path d="M4 2C2.8 3.7 2 5.7 2 8"/>'
    ),
    "lu-user-circle": (
        '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="10" r="3"/><path d="M7 20.662V19a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v1.662"/>'
    ),
    "lu-log-out": (
        '<path d="m16 17 5-5-5-5"/><path d="M21 12H9"/><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>'
    ),
    "lu-bell": (
        '<path d="M10.268 21a2 2 0 0 0 3.464 0"/><path d="M3.262 15.326A1 1 0 0 0 4 17h16a1 1 0 0 0 .74-1.673C19.41 13.956 18 12.499 18 8A6 6 0 0 0 6 8c0 4.499-1.411 5.956-2.738 7.326"/>'
    ),
    "lu-clipboard-check": (
        '<rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/>'
    ),
    "lu-calendar": (
        '<path d="M8 2v3"/><path d="M16 2v3"/><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/>'
    ),
    "lu-clock": (
        '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>'
    ),
    "lu-users": (
        '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><path d="M16 3.128a4 4 0 0 1 0 7.744"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><circle cx="9" cy="7" r="4"/>'
    ),
    "lu-user-cog": (
        '<path d="M10 15H6a4 4 0 0 0-4 4v2"/><path d="m14.305 16.53.923-.382"/><path d="m15.228 13.852-.923-.383"/><path d="m16.852 12.228-.383-.923"/><path d="m16.852 17.772-.383.924"/><path d="m19.148 12.228.383-.923"/><path d="m19.53 18.696-.382-.924"/><path d="m20.772 13.852.924-.383"/><path d="m20.772 16.148.924.383"/><circle cx="18" cy="15" r="3"/><circle cx="9" cy="7" r="4"/>'
    ),
    "lu-calendar-off": (
        '<path d="M16 2v3"/><path d="m2 2 20 20"/><path d="M21 9h-5.5"/><path d="M3 9h6"/><path d="M3.586 3.586A2 2 0 003 5v14a2 2 0 002 2h14a2 2 0 001.414-.586"/><path d="M8.656 3H19a2 2 0 012 2v10.344"/>'
    ),
    "lu-list-todo": (
        '<path d="M13 5h8"/><path d="M13 12h8"/><path d="M13 19h8"/><path d="m3 17 2 2 4-4"/><rect x="3" y="4" width="6" height="6" rx="1"/>'
    ),
    "lu-bell-off": (
        '<path d="M10.268 21a2 2 0 0 0 3.464 0"/><path d="M17 17H4a1 1 0 0 1-.74-1.673C4.59 13.956 6 12.499 6 8a6 6 0 0 1 .258-1.742"/><path d="m2 2 20 20"/><path d="M8.668 3.01A6 6 0 0 1 18 8c0 2.687.77 4.653 1.707 6.05"/>'
    ),
    "lu-eye": (
        '<path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/><circle cx="12" cy="12" r="3"/>'
    ),
    "lu-eye-off": (
        '<path d="M10.733 5.076a10.744 10.744 0 0 1 11.205 6.575 1 1 0 0 1 0 .696 10.747 10.747 0 0 1-1.444 2.49"/><path d="M14.084 14.158a3 3 0 0 1-4.242-4.242"/><path d="M17.479 17.499a10.75 10.75 0 0 1-15.417-5.151 1 1 0 0 1 0-.696 10.75 10.75 0 0 1 4.446-5.143"/><path d="m2 2 20 20"/>'
    ),
    "lu-circle-alert": (
        '<circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/>'
    ),
    "lu-key-round": (
        '<path d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"/><circle cx="16.5" cy="7.5" r=".5" fill="currentColor"/>'
    ),
})


# Exact Lucide icons for the staff screens (Figma 01-03, 06), from lucide-static.
ICONS.update({
    "lu-shield-check": (
        '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/> <path d="m9 12 2 2 4-4"/>'
    ),
    "lu-search": (
        '<path d="m21 21-4.34-4.34"/> <circle cx="11" cy="11" r="8"/>'
    ),
    "lu-info": (
        '<circle cx="12" cy="12" r="10"/> <path d="M12 16v-4"/> <path d="M12 8h.01"/>'
    ),
    "lu-chevron-down": (
        '<path d="m6 9 6 6 6-6"/>'
    ),
    "lu-triangle-alert": (
        '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/> <path d="M12 9v4"/> <path d="M12 17h.01"/>'
    ),
    "lu-clock-3": (
        '<circle cx="12" cy="12" r="10"/> <path d="M12 6v6h4"/>'
    ),
    "lu-calendar-days": (
        '<path d="M8 2v3"/> <path d="M16 2v3"/> <rect x="3" y="3" width="18" height="18" rx="2"/> <path d="M3 9h18"/> <path d="M8 13h.01"/> <path d="M12 13h.01"/> <path d="M16 13h.01"/> <path d="M8 17h.01"/> <path d="M12 17h.01"/> <path d="M16 17h.01"/>'
    ),
    "lu-package": (
        '<path d="M11 21.73a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73z"/> <path d="M12 22V12"/> <polyline points="3.29 7 12 12 20.71 7"/> <path d="m7.5 4.27 9 5.15"/>'
    ),
    "lu-grid-2x2": (
        '<path d="M12 3v18"/> <path d="M3 12h18"/> <rect x="3" y="3" width="18" height="18" rx="2"/>'
    ),
    "lu-x": (
        '<path d="M18 6 6 18"/> <path d="m6 6 12 12"/>'
    ),
    "lu-check": (
        '<path d="M20 6 9 17l-5-5"/>'
    ),
})
