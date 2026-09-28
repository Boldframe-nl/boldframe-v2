#!/usr/bin/env python3
"""Static site generator for the Boldframe stage site.
Run: python3 build.py
Regenerates every HTML page from the data below into this same folder.
Only this script + assets/ are the source of truth — edit here, not the
generated *.html files directly, or your edits will be overwritten.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://stage.boldframe.nl"  # update when the real domain is wired up

PIN_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 3l7 7-3 1-3.5 3.5.5 4.5-1.5 1.5-4-4-5 5-1-1 5-5-4-4L6.5 10.5 11 11l3.5-3.5z"/></svg>'

NAV_ITEMS = [
    ("Cases", "/cases/"),
    ("Diensten", "/diensten/"),
    ("Over ons", "/over-ons/"),
    ("Insights", "/insights/"),
]

CASES = {
    "ecodor": {
        "name": "Ecodor",
        "sub": "Webshop voor geurbestrijders, met dealerfunctionaliteit voor B2B",
        "intro": "Ecodor verkoopt geurbestrijders aan consumenten met huisdieren, via de eigen webshop, Bol.com en dealers. Boldframe bouwde de nieuwe webshop en optimaliseert die nu met A/B-tests.",
        "hero": "/assets/img/cases/ecodor-hero.jpg",
        "facts": [
            ("Vraag", "Van OpenCart naar WooCommerce, met een beter overzicht voor dealers, efficiëntere betalingen en klaar voor internationale groei."),
            ("Aanpak", "Migratie inclusief producten en vertalingen, dealerrollen met eigen prijzen, Mollie-betalingen en een lancering in 19 talen."),
            ("Resultaat", "Een snellere, toekomstbestendige webshop met Zoho CRM-koppeling, extra beveiliging en een eenvoudiger checkout."),
        ],
        "tests": [
            {
                "id": "e1", "date": "2026-07-15", "status": "w", "duration": "21 dagen",
                "title": "Een vlaggetje op de productfoto",
                "hyp": "Door lokale productie direct te claimen, stijgt de gepercipieerde kwaliteit en verdwijnt twijfel over productveiligheid.",
                "metrics": [("+10,43%", "Omzet per bezoeker", "€5,60 → €6,18"), ("+6,42%", "Orderwaarde", "€42,25 → €44,97"), ("-5,17%", "Conversieratio", "")],
                "learn": "Het label 'Gemaakt in Nederland' werkte als kwaliteitsfilter: iets minder kopers, maar met een hogere orderwaarde.",
                "img": "/assets/img/tests/e1.jpg", "alt": "Ecodor productpagina voor en na: label Gemaakt in Nederland",
                "pinned": True,
            },
            {
                "id": "e2", "date": "2026-06-26", "status": "v", "duration": "",
                "title": "Opvallendere tekstlinks in blogs",
                "hyp": "Met merkgroene links in plaats van blauwe vallen ze meer op, dus navigeren bezoekers sneller naar productpagina's.",
                "metrics": [("-12,55%", "Omzet per bezoeker", "€3,23 → €2,82"), ("-8,02%", "Orderwaarde", "€52,00 → €47,83")],
                "learn": "Groen wijkt af van de webconventie dat links blauw zijn, en was op mobiel bij fel licht slecht leesbaar.",
                "img": "/assets/img/tests/e2.jpg", "alt": "Ecodor blogtekst voor en na: groene tekstlinks",
                "pinned": False,
            },
            {
                "id": "e3", "date": "2026-06-02", "status": "w", "duration": "",
                "title": "Vertrouwensblok onder de winkelwagenknop",
                "hyp": "Levertijd, retour en beoordelingen direct onder de knop nemen twijfel op het beslismoment weg.",
                "metrics": [("+2,63%", "Omzet per bezoeker", "€7,12 → €7,31"), ("+7,39%", "Orderwaarde", "€52,13 → €55,98")],
                "learn": "Aanleiding: 40% van de bezoekers verliet de productpagina zonder iets in de winkelmand te leggen.",
                "img": "/assets/img/tests/e3.jpg", "alt": "Ecodor productpagina voor en na: vertrouwensblok onder de knop",
                "pinned": False,
            },
        ],
    },
    "schuurman": {
        "name": "Schuurman Dier & Hengelsport",
        "sub": "Webshop voor dierenvoeding en hengelsport",
        "intro": "Voor Schuurman lopen op dit moment twee tests. De resultaten komen hier zodra ze zijn afgerond.",
        "hero": "/assets/img/cases/schuurman-hero.jpg",
        "facts": [],
        "tests": [
            {
                "id": "s1", "date": "2026-09-01", "status": "l", "duration": "",
                "title": "Homepage: nieuwe hero", "hyp": "Hypothese volgt.", "metrics": [],
                "learn": "Test loopt nog.", "img": "/assets/img/tests/s1.jpg", "alt": "Schuurman homepage voor en na",
                "pinned": False,
            },
            {
                "id": "s2", "date": "2026-08-15", "status": "l", "duration": "",
                "title": "Productpagina: broodkruimelpad opschonen", "hyp": "Hypothese volgt.", "metrics": [],
                "learn": "Test loopt nog.", "img": "/assets/img/tests/s2.jpg", "alt": "Schuurman productpagina voor en na",
                "pinned": False,
            },
        ],
    },
}
CASES_COMING_SOON = ["Fikalights", "Joffs Administraties", "Rezoomy", "Orange Ant", "Jagtveld", "Cleanservice4you", "Luzcap", "Capo"]

STATUS_LABEL = {"w": "Winnaar", "v": "Verliezer", "l": "Loopt nog"}

INSIGHTS = {
    "ai-verkeer-meten-in-ga4": {
        "title": "AI-verkeer meten in GA4",
        "date": "2026-08-01",
        "dek": "AI-verkeer naar websites steeg in 2025 met 527%, en converteert volgens onderzoek tot 3x sneller dan andere kanalen. Voor de meeste sites is het nog maar 1-2% van het totaal, maar je kunt je nu al voorbereiden.",
        "body": [
            "Wist je dat AI-verkeer voor websites in 2025 met 527% is gestegen (Searchengineland.com) en dat verkeer via LLM's tot 3x sneller converteert volgens een studie van Microsoft Clarity? Voor de meeste websites gaat het nog maar om 1 tot 2% van het totale verkeer, maar je kunt je maar beter voorbereiden.",
            "In Google Analytics 4 (GA4) kun je binnen enkele stappen een eigen kanaalgroep aanmaken die AI-chatbots zoals ChatGPT, Gemini, Copilot, Perplexity en Claude herkent, zodat je ziet hoeveel bezoekers via AI binnenkomen en welke pagina's populair zijn bij de LLM's.",
        ],
        "steps": [
            "Log in bij je GA4-account en selecteer je property.",
            "Klik op Admin, en open Channel Groups.",
            "Maak een nieuwe Channel Group, bijvoorbeeld 'AI Tools' of 'LLM's'.",
            "Klik op 'Add new channel' en geef die een naam.",
            "Klik op '+Add condition group' → Source → Matches Regex, en plak de regex hieronder.",
            "Sla de kanaalgroep op en sleep hem via 'Reorder' boven 'Referral'.",
        ],
        "tool": "ga4",
    },
    "ai-scan-landingspagina": {
        "title": "Pas op: een AI-scan van je landingspagina is niet genoeg",
        "date": "2026-04-15",
        "dek": "Een AI-scan van je pagina levert binnen twee minuten nieuwe inzichten op, maar het Baymard Institute meet 50-75% nauwkeurigheid voor AI UX-evaluaties. Zonder menselijke blik erop kan klakkeloos doorvoeren schadelijk zijn.",
        "body": [
            "Een AI-scan van een landingspagina is nuttig: binnen twee minuten krijg je een nieuwe blik op een pagina die vaak organisch gegroeid is en nooit meer heroverwogen werd. Maar het Baymard Institute meet voor AI UX-evaluaties een nauwkeurigheid van 50 tot 75%. Klakkeloos doorvoeren van AI-adviezen kan daarom schadelijk zijn.",
            "Bij Boldframe combineren we daarom altijd een AI-scan met een 'human in the loop': de AI signaleert patronen en technische hiaten, de specialist filtert de ruis, weegt de adviezen af tegen de merkstrategie, en pas na een A/B-test voeren we een wijziging definitief door.",
        ],
        "steps": [],
        "tool": "prompt",
    },
    "meertalige-ecommerce": {
        "title": "Meertalige e-commerce: kansen voor Nederlandse webshops",
        "date": "2026-06-10",
        "dek": "75% van de consumenten koopt liever in de eigen taal, en 96% van de bedrijven met geautomatiseerde vertaaltechnologie ziet een positieve ROI. Voor webshops is internationale groei kosteneffectiever dan ooit.",
        "body": [
            "Google Translate is als eerste stap voor een meertalige website inmiddels achterhaald. Moderne vertaaltools maken het mogelijk om content direct professioneel, geautomatiseerd, consistent en schaalbaar te vertalen voor meerdere markten, zonder dat elke wijziging opnieuw een kostbare vertaalronde vraagt.",
            "Voor Ecodor, producent van geurverdrijvers tegen bijvoorbeeld kattenpis, realiseerde Boldframe onmiskenbare internationale groei: de website is via WPML vertaald in 18 talen op basis van DeepL, video's zijn meertalig ondertiteld, en dankzij een groeiend dealernetwerk in Europa kan Ecodor internationaal groeien zonder overal fysieke distributiepunten te hebben.",
            "Begin klein: richt je eerst op de landen met de grootste potentie, combineer geautomatiseerde vertaling met menselijke review voor nuance, en zorg dat marketing, content en logistiek aansluiten bij de lokale markt.",
        ],
        "steps": [],
        "tool": "reach",
    },
}
INSIGHT_ORDER = ["ai-verkeer-meten-in-ga4", "ai-scan-landingspagina", "meertalige-ecommerce"]

DIENSTEN_STEPS = [
    ("Audit", "We brengen de customer journey van je webshop in kaart en sporen de knelpunten op met heatmaps, sessieopnames en je eigen data — geen aannames."),
    ("Hypothese", "Per knelpunt formuleren we een onderbouwde hypothese: welke aanpassing, waarom die het gedrag zou moeten veranderen, en wat we verwachten dat het oplevert."),
    ("A/B-test", "We testen de aanpassing tegen de huidige versie, met tools als Nelio A/B Testing, tot het resultaat statistisch betrouwbaar is."),
    ("Implementatie", "Een bewezen winnaar voeren we definitief door. Een verliezer laten we vallen, ongeacht hoe logisch hij vooraf klonk — zoals je in onze testtijdlijnen kunt teruglezen."),
]
DIENSTEN_CHALLENGES = [
    ("Verkeer genoeg, omzet te weinig", "Je steekt maandelijks budget in Google Ads, Meta of SEO. Er komen bezoekers binnen, maar onderaan de streep blijft er te weinig omzet over."),
    ("Afhakers vlak voor het afrekenen", "Bezoekers vullen hun winkelmand, en verlaten je site alsnog in de checkout. Vaak door twijfel die met een paar gerichte aanpassingen weg te nemen is."),
    ("Landingspagina's die de belofte van je advertentie niet waarmaken", "Een advertentie trekt de juiste bezoeker, maar de pagina erachter beantwoordt niet de vraag waarmee hij kwam."),
    ("Beslissingen op onderbuikgevoel", "Wijzigingen worden doorgevoerd omdat ze logisch klinken, niet omdat ze getest zijn — met als risico dat je omzet juist inlevert."),
]
DIENSTEN_FAQ = [
    ("Moet ik mijn webbouwer ontslaan?", "Zeker niet. We kunnen de volledige development van je webshop op ons nemen, maar werken minstens zo graag samen met je huidige webbouwer om een bewezen winnaar structureel door te voeren."),
    ("Vertraagt dit mijn site?", "Nee. Een test draait via lichte A/B-testtools naast je bestaande webshop; pas een bewezen winnaar verwerken we structureel in de code."),
    ("Wat als ik niet tevreden ben?", "Dan betaal je niets. Het Webshop Groei-Traject werkt op no-cure-no-pay-basis, met 100% geld-terug-garantie."),
    ("Moet ik direct duizenden euro's investeren in aanpassingen?", "Nee. We beginnen met de tests die het meeste opleveren tegen de minste ontwikkeltijd, en breiden pas uit zodra die hun waarde hebben bewezen."),
    ("Ik heb al andere marketingpartijen, werk jij hen niet tegen?", "Nee. Jouw advertentie- of SEO-partij zorgt voor het verkeer; wij zorgen dat een groter deel daarvan ook daadwerkelijk klant wordt."),
    ("Heb ik wel tijd om al die analyses door te nemen?", "Nauwelijks. Wij doen de analyse en het testen; jij krijgt korte, concrete updates — zoals de testtijdlijn die je bij elke case terugziet."),
]

OVER_ONS_STATS = [
    ("20+", "Webshops geholpen met data-gedreven conversie-optimalisatie"),
    ("5", "Nieuwe shops per maand, bewust — voor diepgang in plaats van volume"),
]


def fmt_date(d):
    months = ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december"]
    y, m, day = d.split("-")
    return f"{int(day)} {months[int(m)-1]} {y}"


def page(title, description, path, body, extra_head=""):
    """path: root-relative canonical path, e.g. '/', '/cases/ecodor/'"""
    canonical = SITE_URL.rstrip("/") + path
    nav_links = []
    for label, href in NAV_ITEMS:
        current = ' aria-current="page"' if path.startswith(href) and href != "/" else ""
        nav_links.append(f'<li><a href="{href}"{current}>{label}</a></li>')
    nav_html = "".join(nav_links)
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex,nofollow">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · Boldframe</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="/assets/img/logo-blue.png">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=swap">
<link rel="stylesheet" href="/assets/css/style.css">
{extra_head}</head>
<body>
<nav aria-label="Hoofdmenu">
<a class="logo" href="/"><img src="/assets/img/logo-blue.png" alt="Boldframe"></a>
<ul>{nav_html}<li><a href="#afspraak"><strong>Contact</strong></a></li></ul>
</nav>
{body}
<section id="afspraak" class="wrap"><h2>Plan een kennismaking</h2>
<p class="lead">Kies zelf een moment voor een gesprek van 30 minuten.</p>
<iframe src="https://calendly.com/roy-tc8/30min?embed_domain=boldframe.nl&amp;embed_type=Inline" frameborder="0" title="Selecteer een datum en tijd - Calendly"></iframe>
<p>Zie je de agenda niet? <a href="https://calendly.com/roy-tc8/30min" target="_blank" rel="noopener">Open hem in een nieuw tabblad</a>.</p></section>
<footer id="contact"><div class="wrap">
<img class="flogo" src="/assets/img/logo-white.png" alt="Boldframe">
<div class="fgrid">
<div><h3>Contact</h3><a href="mailto:roy@boldframe.nl">roy@boldframe.nl</a><br><a href="tel:+31637617728">06-37617728</a></div>
<div><h3>Kantoor</h3>Zwarte Zee 98<br>Maassluis</div>
<div><h3>Volg ons</h3><a href="https://www.linkedin.com/company/boldframenl/" target="_blank" rel="noopener">LinkedIn</a><br><a href="https://www.instagram.com/boldframe_nl" target="_blank" rel="noopener">Instagram</a><br><a href="https://www.facebook.com/people/Boldframe/61568444076737/" target="_blank" rel="noopener">Facebook</a></div>
<div><h3>Bedrijfsgegevens</h3>BTW NL002393881B08</div>
</div>
<div class="fine"><span>© 2026 Boldframe. Alle rechten voorbehouden.</span></div>
</div></footer>
<script src="/assets/js/site.js"></script>
</body>
</html>
"""


def metrics_html(m):
    if not m:
        return ""
    cells = "".join(f'<div><b>{v}</b>{label}<small>{sub}</small></div>' for v, label, sub in m)
    return f'<div class="metrics">{cells}</div>'


def test_card(t):
    dur = f'<span>{t["duration"]}</span>' if t["duration"] else ""
    return f'''<li class="item{' pinned' if t['pinned'] else ''}" data-date="{t['date']}"><div class="meta"><span class="tag {t['status']}">{STATUS_LABEL[t['status']]}</span><span>{fmt_date(t['date'])}</span>{dur}<button class="pin" type="button" aria-pressed="{'true' if t['pinned'] else 'false'}">{PIN_SVG}<span class="pin-label">{'Losmaken' if t['pinned'] else 'Vastpinnen'}</span></button></div>
<h3>{t['title']}</h3><p class="hyp">Hypothese: {t['hyp']}</p>{metrics_html(t['metrics'])}<p>{t['learn']}</p><img src="{t['img']}" alt="{t['alt']}" loading="lazy" width="1000" height="600"></li>'''


def build_case(slug, c):
    pinned = [t for t in c["tests"] if t["pinned"]]
    rest = sorted([t for t in c["tests"] if not t["pinned"]], key=lambda t: t["date"], reverse=True)
    facts = ""
    if c["facts"]:
        facts = '<div class="facts">' + "".join(f"<div><h3>{k}</h3><p>{v}</p></div>" for k, v in c["facts"]) + "</div>"
    pinned_html = ""
    if pinned:
        pinned_html = f'<div class="tl-pinned"><ul class="tl" style="margin-bottom:10px"><li class="grp">{PIN_SVG}Vastgepind</li>{"".join(test_card(t) for t in pinned)}</ul></div>'
    else:
        pinned_html = '<div class="tl-pinned" hidden><ul class="tl" style="margin-bottom:10px"><li class="grp">' + PIN_SVG + 'Vastgepind</li></ul></div>'
    body = f'''<a class="back" href="/cases/">← Alle cases</a>
<header class="hero" style="padding-top:32px"><h1 class="case">{c['name']}</h1><p>{c['intro']}</p><img class="chero" src="{c['hero']}" alt="{c['name']} homepage" loading="lazy"></header>
{facts}
<section><h2>Testtijdlijn</h2><p class="lead">Elke test met hypothese, uitkomst en learning. Nieuwste bovenaan, vastgepinde tests eerst.</p>
{pinned_html}
<div class="tl-rest"><ul class="tl">{"".join(test_card(t) for t in rest)}</ul></div></section>'''
    return page(c["name"], c["sub"], f"/cases/{slug}/", body)


def build_cases_index():
    rows = "".join(
        f'<li><a class="row" href="/cases/{slug}/"><h3>{c["name"]}</h3><span>{c["sub"]}</span></a></li>'
        for slug, c in CASES.items()
    ) + "".join(f'<li><div class="row"><h3>{n}</h3><span>Case volgt</span></div></li>' for n in CASES_COMING_SOON)
    body = f'''<header class="hero"><h1>Cases.</h1><p>Open een case om te zien wat we testten, waarom, en wat het opleverde.</p></header>
<section><ul class="list">{rows}</ul></section>'''
    return page("Cases", "Cases van Boldframe: wat we testten, waarom, en wat het opleverde.", "/cases/", body)


def build_insight(slug, x):
    steps_html = ""
    if x["steps"]:
        steps_html = "<ol>" + "".join(f"<li>{s}</li>" for s in x["steps"]) + "</ol>"
    tool = x["tool"]
    if tool == "ga4":
        base_regex = ".*chatgpt\\.com.*|.*openai\\.com.*|.*gemini\\.google\\.com.*|.*bard\\.google\\.com.*|.*copilot\\.microsoft\\.com.*|.*perplexity.*|.*claude\\.ai.*"
        tool_html = f'''<div class="tool"><h4>Tool: bouw je AI-kanaalgroep</h4><p class="tdesc">Vul optioneel extra AI-tools toe (komma-gescheiden) en kopieer de kant-en-klare regex voor stap 6 hierboven.</p><label for="ga4-extra">Extra AI-bots (optioneel)</label><input type="text" id="ga4-extra" placeholder="bijv. you.com, deepseek.com"><pre id="ga4-out">{base_regex}</pre><button type="button" class="btn small" data-copy="#ga4-out">Kopieer regex</button></div>'''
    elif tool == "prompt":
        default_prompt = "Handel nu als een Senior Conversie Optimalisatie (CRO) en SEO Expert. Analyseer de volgende pagina: {jouw pagina}.\n\nGeef een kritische beoordeling op de volgende 5 punten:\n\n1. De 3-seconden test: Is direct duidelijk wat ze doen, voor wie, en wat de volgende stap is?\n2. Conversie-killers: Zie je afleidingen, onduidelijke knoppen of ontbrekende 'social proof' (reviews/logo's)?\n3. SEO & Inhoud: Is de H1 logisch? Mist de pagina belangrijke onderwerpen die een bezoeker zou verwachten?\n4. User Experience (UX): Hoe schat je de leesbaarheid en mobiele bruikbaarheid in op basis van de tekststructuur.\n5. Het 'Gouden Advies': Wat is de #1 aanpassing die direct voor meer aanvragen/verkopen zou zorgen?\n\nPresenteer dit in een kort overzicht dat ik direct als advies naar mijn klant kan sturen."
        tool_html = f'''<div class="tool"><h4>Tool: genereer jouw Gouden Prompt</h4><p class="tdesc">Vul de URL van je pagina in en kopieer de volledige prompt naar Gemini, ChatGPT of Claude.</p><label for="prompt-url">URL van je pagina</label><input type="url" id="prompt-url" placeholder="https://jouwsite.nl/landingspagina"><textarea id="prompt-out" rows="9" readonly>{default_prompt}</textarea><button type="button" class="btn small" data-copy="#prompt-out">Kopieer prompt</button></div>'''
    elif tool == "reach":
        tool_html = '''<div class="tool"><h4>Tool: schat je potentieel met meertaligheid</h4><p class="tdesc">Ruwe, indicatieve schatting op basis van sectorgemiddelden. Geen belofte, wel een startpunt voor het gesprek.</p><label for="rev-input">Huidige omzet per maand (€)</label><input type="number" id="rev-input" min="0" placeholder="10000"><div class="tool-out" id="rev-out">Vul je huidige omzet per maand in voor een indicatie.</div></div>'''
    else:
        tool_html = ""
    body = f'''<a class="back" href="/insights/">← Alle insights</a>
<header class="hero" style="padding-top:32px;padding-bottom:24px"><span class="meta">{fmt_date(x['date'])}</span><h1 class="case">{x['title']}</h1><p>{x['dek']}</p></header>
<section class="art">{"".join(f"<p>{p}</p>" for p in x['body'])}{steps_html}{tool_html}</section>'''
    return page(x["title"], x["dek"], f"/insights/{slug}/", body)


def build_insights_index():
    rows = "".join(
        f'<li><a class="row" href="/insights/{slug}/"><h3>{INSIGHTS[slug]["title"]}</h3><span>{fmt_date(INSIGHTS[slug]["date"])}</span></a></li>'
        for slug in INSIGHT_ORDER
    )
    body = f'''<header class="hero" style="padding:56px 24px 40px"><h1 style="font-size:clamp(36px,7vw,64px)">Insights.</h1><p>Wat we zien gebeuren in de markt, met steeds een tool erbij die je direct kunt gebruiken.</p></header>
<section class="art"><ul class="insight-list">{rows}</ul></section>'''
    return page("Insights", "Wat Boldframe ziet gebeuren in de markt, met een tool om direct mee aan de slag te gaan.", "/insights/", body)


def build_home():
    case_rows = "".join(
        f'<li><a class="row" href="/cases/{slug}/"><h3>{c["name"]}</h3><span>{c["sub"]}</span></a></li>'
        for slug, c in CASES.items()
    ) + "".join(f'<li><div class="row"><h3>{n}</h3><span>Case volgt</span></div></li>' for n in CASES_COMING_SOON)
    insight_rows = "".join(
        f'<li><a class="row" href="/insights/{slug}/"><h3>{INSIGHTS[slug]["title"]}</h3><span>{fmt_date(INSIGHTS[slug]["date"])}</span></a></li>'
        for slug in INSIGHT_ORDER
    )
    body = f'''<header class="hero"><h1>Van kliks naar klanten.</h1><p>Data-gedreven conversie-optimalisatie met A/B-tests voor webshops die meer omzet willen halen uit bezoekers die ze al hebben.</p><a class="btn" href="#afspraak">Claim mijn gratis Conversie Audit</a></header>
<section><h2>Cases</h2><p class="lead">Open een case om te zien wat we testten, waarom, en wat het opleverde. <a href="/cases/">Alle cases →</a></p><ul class="list">{case_rows}</ul></section>
<section><h2>Insights</h2><p class="lead">Wat we zien gebeuren in de markt, met een tool om direct mee aan de slag te gaan. <a href="/insights/">Alle insights →</a></p><ul class="insight-list">{insight_rows}</ul></section>'''
    return page("Van kliks naar klanten", "Data-gedreven conversie-optimalisatie voor MKB-webshops. Boldframe dicht conversie-lekken op basis van A/B-tests, niet op onderbuikgevoel.", "/", body)


def build_stub(title, path):
    body = f'''<header class="hero"><h1 class="case">{title}</h1><p>Deze pagina is nog in opbouw. Neem gerust contact op als je hier specifieke content voor wilt.</p></header>'''
    return page(title, f"{title} — Boldframe", path, body)


def build_diensten():
    steps_html = "".join(
        f'<li><span class="num">{i+1}</span><div><h3>{t}</h3><p>{d}</p></div></li>'
        for i, (t, d) in enumerate(DIENSTEN_STEPS)
    )
    challenges_html = "".join(f"<div><h3>{t}</h3><p>{d}</p></div>" for t, d in DIENSTEN_CHALLENGES)
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in DIENSTEN_FAQ)
    body = f'''<header class="hero"><h1 class="case">Conversie-optimalisatie, geen giswerk.</h1><p>Je advertenties trekken bezoekers, maar als je landingspagina's en checkout ze niet vasthouden, betaal je voor verkeer dat nooit klant wordt. Wij herstellen die correlatie tussen advertentie en landingspagina met data-gedreven A/B-tests.</p></header>
<section><h2>Het No-cure-no-pay Webshop Groei-Traject</h2><p class="lead">Meer rendement uit de bezoekers die je al hebt. Een hoge klikfrequentie is waardeloos als je checkout de verkoop blokkeert. Wij nemen het risico: geen extra omzet, geen kosten. Jij krijgt de data en de extra verkopen.</p>
<div class="facts"><div><h3>Risico</h3><p>No-cure-no-pay, met 100% geld-terug-garantie.</p></div><div><h3>Start</h3><p>Gratis conversie-audit binnen 48 uur.</p></div><div><h3>Capaciteit</h3><p>Maximaal 5 nieuwe shops per maand, voor diepgang per klant.</p></div></div>
<p><a class="btn" href="#afspraak">Claim mijn gratis Conversie Audit</a></p></section>
<section><h2>Waar we conversie-lekken vinden</h2><p class="lead">Herkenbaar? Dit zijn de signalen waarmee webshopondernemers meestal bij ons aankloppen.</p>
<div class="facts">{challenges_html}</div></section>
<section><h2>Onze werkwijze</h2><p class="lead">Van vermoeden naar bewijs, in vier stappen — dezelfde stappen die je terugziet in elke testtijdlijn bij onze <a href="/cases/">cases</a>.</p>
<ul class="steps">{steps_html}</ul></section>
<section><h2>Veelgestelde vragen</h2><div class="faq">{faq_html}</div></section>'''
    return page(
        "Diensten",
        "Data-gedreven conversie-optimalisatie voor MKB-webshops: het No-cure-no-pay Webshop Groei-Traject van Boldframe.",
        "/diensten/",
        body,
    )


def build_over_ons():
    stats_html = "".join(f"<div><b>{v}</b><span>{l}</span></div>" for v, l in OVER_ONS_STATS)
    body = f'''<header class="hero"><h1 class="case">50% techniek, 50% gedrag.</h1><p>Conversie-optimalisatie zit precies tussen die twee in. Bij Boldframe combineren we ontwikkelaars die een test technisch correct bouwen met een strateeg die weet waaróm een bezoeker afhaakt.</p></header>
<section><h2>Onze visie</h2><p class="lead" style="max-width:66ch">We geloven niet in giswerk of onderbuikgevoel. Elke aanpassing die we voorstellen is eerst een hypothese, dan een A/B-test tegen de huidige situatie, en pas daarna een implementatie — met een concreet omzet-effect als uitkomst. Precies zoals je in onze <a href="/cases/">testtijdlijnen</a> kunt teruglezen: ook de tests die niet werkten laten we zien, want ook dat is bewijs.</p>
<div class="stats">{stats_html}</div></section>
<section><h2>Roy van Hees</h2><p class="lead" style="max-width:66ch">E-commerce strateeg en oprichter van Boldframe. Roy combineert een achtergrond in sales consultancy met hands-on CRO-werk: hij weet waar bezoekers in de klantreis afhaken, en bouwt vandaaruit de hypothese die we vervolgens testen. <a href="mailto:roy@boldframe.nl">roy@boldframe.nl</a></p></section>
<section><h2>Hoe we werken</h2><p class="lead" style="max-width:66ch">Audit, hypothese, A/B-test, implementatie — dezelfde vier stappen bij elke shop. Lees meer over onze <a href="/diensten/">werkwijze</a> of bekijk direct wat het heeft opgeleverd in onze <a href="/cases/">cases</a>.</p>
<p><a class="btn" href="#afspraak">Plan een kennismaking</a></p></section>'''
    return page(
        "Over ons",
        "Boldframe: conversie-optimalisatie op basis van data, niet onderbuikgevoel. 50% techniek, 50% gedrag.",
        "/over-ons/",
        body,
    )


def write(path, content):
    full = os.path.join(ROOT, path.lstrip("/"), "index.html") if path.endswith("/") else os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", os.path.relpath(full, ROOT))


def main():
    write("/", build_home())
    write("/cases/", build_cases_index())
    for slug, c in CASES.items():
        write(f"/cases/{slug}/", build_case(slug, c))
    write("/insights/", build_insights_index())
    for slug in INSIGHT_ORDER:
        write(f"/insights/{slug}/", build_insight(slug, INSIGHTS[slug]))
    write("/diensten/", build_diensten())
    write("/over-ons/", build_over_ons())

    # 404
    body = '<header class="hero"><h1 class="case">Pagina niet gevonden</h1><p>Deze pagina bestaat niet (meer). <a href="/">Terug naar de homepage</a>.</p></header>'
    write("/404.html", page("Pagina niet gevonden", "404 — Boldframe", "/404.html", body))


if __name__ == "__main__":
    main()
