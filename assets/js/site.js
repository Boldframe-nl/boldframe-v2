// Boldframe site — kleine interactieve onderdelen, geen framework nodig.

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
      // herplaats op datum (data-date, aflopend)
      const d = item.dataset.date;
      const items = Array.from(rest.children);
      const next = items.find((li) => li.dataset.date < d);
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
