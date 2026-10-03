// Entry point loaded on every page. Page-specific scripts load from their own templates.
import { initSidebar } from "./ui/sidebar.js";
import { initDropdowns } from "./ui/dropdown.js";
import { initToasts } from "./ui/toast.js";

initSidebar();
initDropdowns();
initToasts();
