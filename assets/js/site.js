// Boldframe site — kleine interactieve onderdelen, geen framework nodig.

// 0a) Scroll-reveal: alles met [data-reveal] faded/schuift in zodra het in beeld komt.
// Dit is de standaard voor nieuwe pagina's/onderdelen — voeg data-reveal toe
// (en optioneel style="--d:0..n" voor een staggered volgorde binnen een groep).
const reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const revealEls = document.querySelectorAll("[data-reveal]");
if (revealEls.length) {
  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealEls.forEach((el) => el.classList.add("is-visible"));
  } else {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            animateCount(entry.target);
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -40px 0px" }
    );
    // Tellers starten op 0 (HTML bevat de eindwaarde voor no-JS en zoekmachines).
    document.querySelectorAll("[data-count]").forEach((el) => {
      el.textContent = (el.getAttribute("data-prefix") || "") + "0" + (el.getAttribute("data-suffix") || "");
    });
    revealEls.forEach((el) => io.observe(el));
  }
}

// 0b) Count-up voor statistieken: <b data-count="20" data-suffix="+">0+</b>
function animateCount(container) {
  const el = container.matches && container.matches("[data-count]") ? container : container.querySelector("[data-count]");
  if (!el || el.dataset.counted) return;
  el.dataset.counted = "1";
  const target = parseFloat(el.getAttribute("data-count"));
  const suffix = el.getAttribute("data-suffix") || "";
  const prefix = el.getAttribute("data-prefix") || "";
  if (!isFinite(target)) return;
  const fmt = (n) => prefix + Math.round(n).toLocaleString("nl-NL") + suffix;
  if (reduceMotion) {
    el.textContent = fmt(target);
    return;
  }
  const dur = 900;
  const start = performance.now();
  function step(now) {
    const p = Math.min(1, (now - start) / dur);
    const eased = 1 - Math.pow(1 - p, 3);
    el.textContent = fmt(target * eased);
    if (p < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

// 0c) Lichte schaduw onder de nav zodra er gescrold is.
const siteNav = document.querySelector("nav");
if (siteNav) {
  const onScroll = () => siteNav.classList.toggle("nav-scrolled", window.scrollY > 8);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
}

// 1) Vastpinnen van tests binnen een case (client-side, per bezoek).
document.addEventListener("click", (e) => {
  const p = e.target.closest(".pin");
  if (!p) return;
  const item = p.closest(".item");
  const list = item.closest(".tl");
  const pinnedGroup = document.querySelector(".tl-pinned");
  const willPin = p.getAttribute("aria-pressed") !== "true";
  p.setAttribute("aria-pressed", willPin ? "true" : "false");
  p.querySelector(".pin-label").textContent = willPin ? "Losmaken" : "Vastpinnen";
  item.classList.toggle("pinned", willPin);
  if (willPin && pinnedGroup) {
    pinnedGroup.querySelector("ul").appendChild(item);
    pinnedGroup.hidden = false;
  } else if (!willPin) {
    const rest = document.querySelector(".tl-rest ul");
    if (rest) {
      // herplaats op volgorde (data-order, oplopend = nieuwste eerst)
      const o = parseInt(item.dataset.order || "0", 10);
      const items = Array.from(rest.children);
      const next = items.find((li) => parseInt(li.dataset.order || "0", 10) > o);
      rest.insertBefore(item, next || null);
    }
    if (pinnedGroup && !pinnedGroup.querySelector(".item")) pinnedGroup.hidden = true;
  }
});

// 2) Kopieer-knoppen voor de insight-tools.
document.addEventListener("click", (e) => {
  const cp = e.target.closest("[data-copy]");
  if (!cp) return;
  const el = document.querySelector(cp.getAttribute("data-copy"));
  const text = el ? ("value" in el ? el.value : el.textContent) : "";
  const orig = cp.textContent;
  const done = () => {
    cp.textContent = "Gekopieerd ✓";
    setTimeout(() => (cp.textContent = orig), 1500);
  };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(done).catch(done);
  } else {
    done();
  }
});

// 3) Tool: AI-kanaalgroep regex-generator (insights/ai-verkeer-meten-in-ga4)
const GA4_BASE = [
  "chatgpt\\.com", "openai\\.com", "gemini\\.google\\.com", "bard\\.google\\.com",
  "copilot\\.microsoft\\.com", "perplexity", "claude\\.ai",
];
function ga4Regex(extra) {
  const ex = (extra || "")
    .split(",")
    .map((x) => x.trim())
    .filter(Boolean)
    .map((x) => x.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
  return [...GA4_BASE, ...ex].map((x) => `.*${x}.*`).join("|");
}
const ga4Extra = document.getElementById("ga4-extra");
if (ga4Extra) {
  ga4Extra.addEventListener("input", () => {
    document.getElementById("ga4-out").textContent = ga4Regex(ga4Extra.value);
  });
}

// 4) Tool: Gouden Prompt generator (insights/ai-scan-landingspagina)
function goldenPrompt(url) {
  const u = url && url.trim() ? url.trim() : "{jouw pagina}";
  return `Handel nu als een Senior Conversie Optimalisatie (CRO) en SEO Expert. Analyseer de volgende pagina: ${u}.

Geef een kritische beoordeling op de volgende 5 punten:

1. De 3-seconden test: Is direct duidelijk wat ze doen, voor wie, en wat de volgende stap is?
2. Conversie-killers: Zie je afleidingen, onduidelijke knoppen of ontbrekende 'social proof' (reviews/logo's)?
3. SEO & Inhoud: Is de H1 logisch? Mist de pagina belangrijke onderwerpen die een bezoeker zou verwachten?
4. User Experience (UX): Hoe schat je de leesbaarheid en mobiele bruikbaarheid in op basis van de tekststructuur.
5. Het 'Gouden Advies': Wat is de #1 aanpassing die direct voor meer aanvragen/verkopen zou zorgen?

Presenteer dit in een kort overzicht dat ik direct als advies naar mijn klant kan sturen.`;
}
const promptUrl = document.getElementById("prompt-url");
if (promptUrl) {
  promptUrl.addEventListener("input", () => {
    document.getElementById("prompt-out").value = goldenPrompt(promptUrl.value);
  });
}

// 5) Tool: indicatieve schatting meertalig omzetpotentieel (insights/meertalige-ecommerce)
function reachEstimate(rev) {
  const r = parseFloat(rev);
  if (!r || r <= 0) return "Vul je huidige omzet per maand in voor een indicatie.";
  const lo = Math.round((r * 0.15) / 50) * 50;
  const hi = Math.round((r * 0.3) / 50) * 50;
  return `Indicatief extra omzetpotentieel bij succesvolle internationale uitbreiding: €${lo.toLocaleString("nl-NL")} – €${hi.toLocaleString("nl-NL")} per maand. Gebaseerd op sectorgemiddelden (75% koopt liever in eigen taal), geen garantie.`;
}
const revInput = document.getElementById("rev-input");
if (revInput) {
  revInput.addEventListener("input", () => {
    document.getElementById("rev-out").textContent = reachEstimate(revInput.value);
  });
}

// 6) Analytics met toestemming: alleen als <body data-ga="G-..."> is gezet. Zonder keuze wordt er niets geladen.
(function () {
  const gaId = document.body.getAttribute("data-ga");
  if (!gaId) return;
  const KEY = "bf-consent";
  const read = () => { try { return localStorage.getItem(KEY); } catch (e) { return null; } };
  const write = (v) => { try { localStorage.setItem(KEY, v); } catch (e) {} };
  function loadGA() {
    if (window.__gaLoaded) return;
    window.__gaLoaded = true;
    const s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(gaId);
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    gtag("js", new Date());
    gtag("config", gaId, { anonymize_ip: true });
  }
  function banner() {
    if (document.querySelector(".cookie")) return;
    const b = document.createElement("div");
    b.className = "cookie";
    b.setAttribute("role", "dialog");
    b.setAttribute("aria-label", "Cookies");
    b.innerHTML = '<p>We gebruiken analytische cookies om de site te verbeteren, alleen met jouw toestemming. <a href="/privacy/">Privacyverklaring</a></p><div class="cookie-btns"><button type="button" class="no">Weigeren</button><button type="button" class="yes">Accepteren</button></div>';
    b.querySelector(".yes").addEventListener("click", () => { write("yes"); loadGA(); b.remove(); });
    b.querySelector(".no").addEventListener("click", () => { write("no"); b.remove(); });
    document.body.appendChild(b);
  }
  const c = read();
  if (c === "yes") loadGA();
  else if (c !== "no") banner();
  document.addEventListener("click", (e) => {
    if (e.target.closest("[data-cookie-reset]")) { e.preventDefault(); write(""); banner(); }
  });
})();

// 7) Hamburgermenu op mobiel.
(function () {
  const btn = document.querySelector(".nav-toggle");
  const menu = document.getElementById("nav-menu");
  if (!btn || !menu) return;
  const set = (open) => {
    menu.classList.toggle("open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    btn.setAttribute("aria-label", open ? "Menu sluiten" : "Menu openen");
  };
  btn.addEventListener("click", () => set(!menu.classList.contains("open")));
  menu.addEventListener("click", (e) => { if (e.target.closest("a")) set(false); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") set(false); });
})();

// 8) Tool: testduur (insights/hoeveel-verkeer-om-te-testen)
function testDuration(visitors, ratePct, mdePct, z, variants) {
  const p = ratePct / 100;
  const delta = p * (mdePct / 100);
  if (!(visitors > 0) || !(p > 0 && p < 1) || !(delta > 0)) return null;
  const zb = 0.8416; // 80% power
  const nPer = (2 * Math.pow(z + zb, 2) * p * (1 - p)) / (delta * delta);
  const total = nPer * variants;
  const perDay = visitors / 30;
  const days = Math.ceil(total / perDay);
  return { nPer: Math.ceil(nPer), total: Math.ceil(total), days, conv: Math.round(visitors * p) };
}
(function () {
  const out = document.getElementById("dur-out");
  if (!out) return;
  const ids = ["dur-visitors", "dur-rate", "dur-mde", "dur-sig", "dur-var"];
  const el = (i) => document.getElementById(i);
  const fmt = (n) => n.toLocaleString("nl-NL");
  function update() {
    const sigPct = { "1.645": 90, "1.96": 95, "2.576": 99 }[el("dur-sig").value];
    const r = testDuration(parseFloat(el("dur-visitors").value), parseFloat(el("dur-rate").value), parseFloat(el("dur-mde").value), parseFloat(el("dur-sig").value), parseInt(el("dur-var").value, 10));
    if (!r) { out.textContent = "Vul alle velden in voor een indicatie."; return; }
    const weeks = (r.days / 7).toFixed(1).replace(".", ",");
    let verdict;
    if (r.days <= 21) verdict = "Past in een test van twee tot drie weken.";
    else if (r.days <= 42) verdict = "Haalbaar, maar langzaam. Een breder effect of een meetwaarde die vaker voorkomt (zoals add-to-carts) maakt de test sneller.";
    else verdict = "Te lang voor een gewone test. Kies een bredere test, een groter minimaal effect of een meetwaarde die vaker voorkomt, zoals add-to-carts.";
    const low = r.conv < 500 ? " Je meetwaarde komt per maand minder dan 500 keer voor: weinig voor een snel testprogramma." : "";
    const risk = 1 / (1 - sigPct / 100);
    out.innerHTML = "Je meet ongeveer " + fmt(r.conv) + " keer per maand. Je hebt " + fmt(r.nPer) + " bezoekers per versie nodig (" + fmt(r.total) + " in totaal): ongeveer <strong>" + fmt(r.days) + " dagen (" + weeks + " weken)</strong>. " + verdict + low + "<br><small>Bij " + sigPct + "% zekerheid voer je gemiddeld eens in de " + fmt(Math.round(risk)) + " keer een wijziging door zonder wezenlijk effect.</small>";
  }
  ids.forEach((i) => el(i).addEventListener("input", update));
  update();
})();
