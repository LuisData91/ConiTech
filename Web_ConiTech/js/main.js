/* ConiTech — interacciones de la web (sin dependencias). */
(() => {
  "use strict";

  const WHATSAPP = "51941393854";
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

  /* ---------- Cabecera: sombra al hacer scroll ---------- */
  const header = $("#header");
  const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 8);
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Menú móvil ---------- */
  const toggle = $("#nav-toggle");
  const nav = $("#nav");
  const setMenu = (open) => {
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
    nav.classList.toggle("is-open", open);
  };
  toggle.addEventListener("click", () => setMenu(toggle.getAttribute("aria-expanded") !== "true"));
  $$("a", nav).forEach((a) => a.addEventListener("click", () => setMenu(false)));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") setMenu(false); });

  /* ---------- Enlace activo según la sección visible ---------- */
  const links = $$(".nav__list a");
  const sections = links.map((a) => $(a.getAttribute("href"))).filter(Boolean);
  if ("IntersectionObserver" in window) {
    const spy = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        links.forEach((a) => a.classList.toggle("is-active", a.getAttribute("href") === `#${entry.target.id}`));
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    sections.forEach((s) => spy.observe(s));
  }

  /* ---------- Pestañas de proyectos (patrón ARIA tabs) ---------- */
  const tabs = $$('[role="tab"]');
  const selectTab = (tab, focus = false) => {
    tabs.forEach((t) => {
      const selected = t === tab;
      t.setAttribute("aria-selected", String(selected));
      t.tabIndex = selected ? 0 : -1;
      $(`#${t.getAttribute("aria-controls")}`).hidden = !selected;
    });
    if (focus) tab.focus();
    tab.scrollIntoView({ block: "nearest", inline: "nearest" });
  };
  tabs.forEach((tab, i) => {
    tab.addEventListener("click", () => selectTab(tab));
    tab.addEventListener("keydown", (e) => {
      const moves = { ArrowRight: 1, ArrowLeft: -1 };
      if (e.key in moves) {
        e.preventDefault();
        selectTab(tabs[(i + moves[e.key] + tabs.length) % tabs.length], true);
      } else if (e.key === "Home") { e.preventDefault(); selectTab(tabs[0], true); }
      else if (e.key === "End") { e.preventDefault(); selectTab(tabs[tabs.length - 1], true); }
    });
  });

  // "Ver desarrollo" en las tarjetas abre la pestaña correspondiente
  $$("[data-goto]").forEach((link) => {
    link.addEventListener("click", () => {
      const tab = $(`#tab-${link.dataset.goto}`);
      if (tab) selectTab(tab);
    });
  });

  /* ---------- Visor de capturas ---------- */
  const lightbox = $("#lightbox");
  const lightboxImg = $("img", lightbox);
  $$("[data-zoom]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const img = $("img", btn);
      lightboxImg.src = img.currentSrc || img.src;
      lightboxImg.alt = img.alt;
      if (typeof lightbox.showModal === "function") lightbox.showModal();
      else window.open(lightboxImg.src, "_blank", "noopener");
    });
  });
  $(".lightbox__close").addEventListener("click", () => lightbox.close());
  lightbox.addEventListener("click", (e) => { if (e.target === lightbox) lightbox.close(); });

  /* ---------- Formulario → WhatsApp ---------- */
  const form = $("#form-contacto");
  const error = $("#form-error");
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    const required = ["nombre", "mensaje"];
    let valid = true;
    required.forEach((name) => {
      const field = form.elements[name];
      const empty = !String(data[name] || "").trim();
      field.setAttribute("aria-invalid", String(empty));
      if (empty) valid = false;
    });
    error.hidden = valid;
    if (!valid) { form.querySelector('[aria-invalid="true"]').focus(); return; }

    const lines = [
      "Hola ConiTech 👋",
      `Soy ${data.nombre.trim()}${data.empresa.trim() ? ` de ${data.empresa.trim()}` : ""}.`,
      `Me interesa: ${data.interes}.`,
      "",
      data.mensaje.trim(),
    ];
    const url = `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(lines.join("\n"))}`;
    window.open(url, "_blank", "noopener");
  });
  $$("input, textarea", form).forEach((el) =>
    el.addEventListener("input", () => el.removeAttribute("aria-invalid")));

  /* ---------- Aparición suave al hacer scroll ---------- */
  const revealables = $$(".section__head, .compare__col, .pillar, .card, .custom, .step, .client, .faq details, .form");
  if ("IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    revealables.forEach((el) => el.classList.add("reveal"));
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        io.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    revealables.forEach((el) => io.observe(el));
  }

  /* ---------- Año del pie ---------- */
  $("#year").textContent = new Date().getFullYear();
})();
