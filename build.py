#!/usr/bin/env python3
"""Static site generator for the Boldframe stage site.
Run: python3 build.py
Regenerates every HTML page from the data below into this same folder.
Only this script + assets/ are the source of truth — edit here, not the
generated *.html files directly, or your edits will be overwritten.
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://stage.boldframe.nl"  # bij livegang: https://boldframe.nl
LIVE = False  # bij livegang op True: haalt noindex weg en laat zoekmachines toe (robots.txt + meta)
GA_ID = "G-8N1ZFCB0FW"  # Google Analytics 4 meet-ID (G-XXXXXXXXXX). Leeg = geen analytics en geen cookiebanner.

PIN_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 3l7 7-3 1-3.5 3.5.5 4.5-1.5 1.5-4-4-5 5-1-1 5-5-4-4L6.5 10.5 11 11l3.5-3.5z"/></svg>'

import math
import random


def hero_art(seed, ridges=11, top=300, bottom=545, amp=(60, 110), sun=(1090, 300, 150), stars=36, band=False):
    """Genereert de hero-illustratie: lagen berglijnen (als groeicurves), een gestreepte zon en sterren.
    Alles is vectorlijnwerk in off-white op merkblauw en wordt met CSS geanimeerd."""
    rnd = random.Random(seed)
    W, H = 1600, 640
    layers = []
    for i in range(ridges):
        t = i / max(1, ridges - 1)
        base = top + (bottom - top) * (t ** 0.85)
        a = amp[0] + (amp[1] - amp[0]) * t
        comps = [(rnd.uniform(0.5, 1.2), rnd.uniform(0, 6.28), 0.55), (rnd.uniform(1.6, 3.2), rnd.uniform(0, 6.28), 0.3), (rnd.uniform(4.0, 7.0), rnd.uniform(0, 6.28), 0.15)]
        pts = []
        x = -40
        while x <= W + 40:
            f = sum(w * math.sin(x / W * 6.283 * fr + ph) for fr, ph, w in comps)
            f = 0.5 + 0.5 * f
            f = f * f * (3 - 2 * f)  # steilere flanken, plateaus
            pts.append((x, base - a * f))
            x += 16
        line = "M" + " L".join(f"{x},{y:.1f}" for x, y in pts)
        fill = line + f" L{W + 40},{H + 20} L-40,{H + 20} Z"
        op = 0.22 + 0.73 * t
        k = round(0.2 * (1 - t), 3)
        dl = round(-rnd.uniform(0, 9), 2)
        ab = round(-(2 + 5 * t), 1)
        dur = round(7 + 4 * (1 - t), 1)
        ds = round(0.12 * i, 2)
        layers.append(
            f'<g class="rg" style="--k:{k}"><g class="rb" style="--a:{ab}px;--dl:{dl}s;--dur:{dur}s">'
            f'<path class="rf" style="--ds:{ds}s" d="{fill}"/>'
            f'<path class="rh" style="--ds:{ds}s;--ho:{0.10 + 0.22 * t:.2f}" fill="url(#hatch-{seed})" d="{fill}"/>'
            f'<path class="rs" style="--ds:{ds}s;stroke-opacity:{op:.2f}" pathLength="1" d="{line}"/></g></g>'
        )
    sx, sy, sr = sun or (0, 0, 0)
    stripes = "".join(f'<line x1="{sx - sr}" x2="{sx + sr}" y1="{y}" y2="{y}"/>' for y in range(int(sy - sr) - 10, int(sy + sr) + 20, 9))
    sun_svg = (
        f'<clipPath id="sun-{seed}"><circle cx="{sx}" cy="{sy}" r="{sr}"/></clipPath>'
        f'<g class="sun"><circle cx="{sx}" cy="{sy}" r="{sr}" class="sun-glow"/><g clip-path="url(#sun-{seed})"><g class="stripes">{stripes}</g></g></g>'
    ) if sun else ""
    star_svg = "".join(
        f'<circle class="st" style="animation-delay:{-rnd.uniform(0, 6):.1f}s" cx="{rnd.randint(10, W - 10)}" cy="{rnd.randint(10, max(40, top - 40))}" r="{rnd.choice([0.8, 1.1, 1.5])}"/>'
        for _ in range(stars)
    )
    defs = f'<defs><pattern id="hatch-{seed}" width="5" height="5" patternUnits="userSpaceOnUse"><line x1="0.5" y1="0" x2="0.5" y2="5" stroke="#f6f4f0" stroke-width="1"/></pattern></defs>'
    return (f'<svg class="hero-art" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice" aria-hidden="true" focusable="false">{defs}'
            f'<g class="stars">{star_svg}</g>{sun_svg}{"".join(layers)}</svg>')


HERO_ART_BIG = hero_art(7, ridges=13, top=380, bottom=585, amp=(90, 190), sun=(1060, 395, 175), stars=44)
HERO_BG = hero_art(11, ridges=8, top=450, bottom=590, amp=(50, 110), sun=(1180, 470, 95), stars=22)
HERO_BAND = hero_art(5, ridges=6, top=430, bottom=600, amp=(40, 80), sun=None, stars=0)


NAV_ITEMS = [
    ("Cases", "/cases/"),
    ("Diensten", "/diensten/"),
    ("Werkwijze", "/werkwijze/"),
    ("Over ons", "/over-ons/"),
    ("Insights", "/insights/"),
]

# Kleine lijnicoon-set (stroke, currentColor) — standaard iconenbibliotheek voor de
# hele site. Nieuw icoon nodig? Voeg een key toe en gebruik icon("key") in build.py.
ICONS = {
    "search": '<circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    "bulb": '<path d="M9 18h6M10 21h4M12 3a6 6 0 00-3.6 10.8c.6.45 1.1 1.2 1.2 2.2h4.8c.1-1 .6-1.75 1.2-2.2A6 6 0 0012 3z"/>',
    "flask": '<path d="M9 2h6M10 2v6l-5.5 9.5A2 2 0 006.2 21h11.6a2 2 0 001.7-3.5L14 8V2"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>',
    "cross": '<circle cx="12" cy="12" r="9"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3.1 19.5 19.5 0 01-6-6A19.8 19.8 0 012.1 4.2 2 2 0 014 2h3a2 2 0 012 1.7c.1.9.3 1.8.6 2.7a2 2 0 01-.4 2.1L8 9.9a16 16 0 006 6l1.4-1.2a2 2 0 012.1-.4c.9.3 1.8.5 2.7.6A2 2 0 0122 16.9z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="2 7 12 14 22 7"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
    "arrow-right": '<line x1="5" y1="12" x2="19" y2="12"/><path d="M12 5l7 7-7 7"/>',
    "shield": '<path d="M12 3l8 3.5v5c0 5-3.4 8.7-8 9.5-4.6-.8-8-4.5-8-9.5v-5z"/><path d="M9 12l2 2 4-4"/>',
    "target": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r=".6" fill="currentColor"/>',
    "paw": '<circle cx="7" cy="8" r="1.6"/><circle cx="12" cy="6" r="1.6"/><circle cx="17" cy="8" r="1.6"/><circle cx="19.2" cy="13" r="1.8"/><ellipse cx="12" cy="16" rx="5.2" ry="4.2"/>',
    "hanger": '<path d="M12 3a2 2 0 10-2 2c0 .7.4 1.3 1 1.7V8L3.3 15c-1 .7-.5 2.2.7 2.2h16c1.2 0 1.7-1.5.7-2.2L13 8V6.7c.6-.4 1-1 1-1.7"/>',
    "palette": '<path d="M12 3a9 9 0 100 18c1 0 1.8-.8 1.8-1.8 0-.5-.2-.9-.5-1.2-.3-.3-.5-.7-.5-1.2 0-1 .8-1.8 1.8-1.8H17a4 4 0 004-4c0-4.4-4-8-9-8z"/><circle cx="7.5" cy="10.5" r="1" fill="currentColor"/><circle cx="7.5" cy="14.5" r="1" fill="currentColor"/><circle cx="12" cy="7.5" r="1" fill="currentColor"/><circle cx="16" cy="9.5" r="1" fill="currentColor"/>',
    "home": '<path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "bike": '<circle cx="6" cy="16" r="3.5"/><circle cx="18" cy="16" r="3.5"/><path d="M6 16l4-7h5l3 7M10 9L8.5 6H7M13 12.5h-4"/>',
    "leaf": '<path d="M5 19c0-8 5-14 15-14 0 10-6 15-14 15"/><path d="M5 19c3-5 6-8 10-10"/>',
    "gem": '<path d="M6 4h12l3 5-9 11L3 9z"/><path d="M3 9h18M9 4l3 5 3-5M12 9v11"/>',
    "tool": '<path d="M14.5 6.5a4 4 0 00-5 5L3.5 17.5a1.8 1.8 0 002.5 2.5l6-6a4 4 0 005-5l-2.5 2.5-2-.5-.5-2z"/>',
    "baby": '<circle cx="12" cy="12" r="8.5"/><circle cx="9" cy="11" r=".9" fill="currentColor"/><circle cx="15" cy="11" r=".9" fill="currentColor"/><path d="M9.5 15c1.4 1.2 3.6 1.2 5 0M12 3.5c0 1.5 1 2 2 2"/>',
    "bolt": '<path d="M13 3L5 13.5h6L10 21l8-10.5h-6z"/>',
    "cart": '<circle cx="9" cy="20" r="1.4"/><circle cx="17" cy="20" r="1.4"/><path d="M3 4h2.5l2.2 11h10.3L20 8H6.5"/>',
    "heart": '<path d="M12 21s-7-4.35-9.5-8.5C1 9 2.5 5 6 5c2 0 3.5 1.2 4 2.3C10.5 6.2 12 5 14 5c3.5 0 5 4 3.5 7.5C19 16.65 12 21 12 21z"/>',
}


def icon(key, cls="icon"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[key]}</svg>'


# Branches waar Boldframe voor webshops werkt — gebruikt op de homepage en Diensten.
# Uitbreiden: voeg een (naam, icoon-key, beschrijving) tuple toe.
BRANCHES = [
    ("Fashion & accessoires", "hanger", "Maattabellen, size-guides en productfoto's die retouren voorkomen."),
    ("Huisdieren", "paw", "Vertrouwen opbouwen rond kwaliteit en veiligheid van het product."),
    ("Hobby's & vrije tijd", "palette", "Een groot assortiment overzichtelijk maken voor een snellere keuze."),
    ("Care & gezondheid", "heart", "Twijfel wegnemen precies op het moment vóór de aankoop."),
    ("Wonen & interieur", "home", "Grote aankopen: maat, kleur en bezorging zo helder maken dat bezoekers durven bestellen."),
    ("Sport & outdoor", "bike", "Specificaties en maatadvies simpel uitleggen, zodat de juiste keuze snel gemaakt is."),
    ("Eten, drinken & supplementen", "leaf", "Herhaalaankopen en abonnementen stimuleren en vertrouwen opbouwen rond ingrediënten."),
    ("Sieraden & cadeaus", "gem", "Een emotionele aankoop ondersteunen met vertrouwen, presentatie en een soepele checkout."),
    ("Doe-het-zelf & techniek", "tool", "Technische producten begrijpelijk maken en bezoekers helpen de juiste variant te kiezen."),
    ("Baby & kind", "baby", "Ouders snel overtuigen met duidelijke maten, veiligheid en bezorgbeloftes."),
    ("Elektronica & gadgets", "bolt", "Vergelijkingen en specificaties zo tonen dat bezoekers zonder twijfel afrekenen."),
    ("En jouw branche?", "cart", "Geen beperking op branche: per aanvraag kijken we of er genoeg verkeer en potentieel is om samen resultaat te halen."),
]


def build_branches_section(id_attr=' id="branches"'):
    cards = "".join(
        f'<div class="branch" data-reveal style="--d:{i}">{icon(k)}<h3>{name}</h3><p>{desc}</p></div>'
        for i, (name, k, desc) in enumerate(BRANCHES)
    )
    return f'''<section{id_attr}><h2 data-reveal>Voor welke webshops?</h2><p class="lead" data-reveal>Boldframe werkt uitsluitend voor webwinkels, in elke branche. De aanpak is overal dezelfde: data, onderzoek en testen. Staat jouw branche er niet bij? Dan bekijken we per aanvraag of het een goede match is.</p>
<div class="branches">{cards}</div></section>'''

# Case-model
# ----------
# Een case is een dict. Zonder "blocks" krijgt hij de eenvoudige indeling (intro,
# optionele facts, testtijdlijn). Met "blocks" wordt het een uitgebreide
# verhaal-case (zie Ecodor): hero met headline + kerncijfers, daarna de blokken in
# de volgorde waarin ze hier staan. Beschikbare blokken (type):
#   text    h2, paras[]
#   bars    h2, lead, rows[(label, waarde, weergave, "act"|"est")], note
#   cards   h2, lead, items[(titel, icoon, tekst)]
#   phases  h2, lead, items[(titel, icoon, tekst, uitkomst)]
#   table   h2, lead, head[], rows[[...]]
#   tests   h2, lead            (de testtijdlijn met vastpinnen)
#   cta     h2, lead, other=(url, label)
# Test-velden: id, status (w/v/l), title, hyp, metrics[(waarde, label, sub)], learn, img, alt,
#   pinned; optioneel: date, duration, observation, principle, note, next.
CASES = {
    "ecodor": {
        "name": "Ecodor",
        "sub": "Van circa €40k naar een verwachte €325k omzet per jaar",
        "eyebrow": "Case · Huisdieren · WooCommerce",
        "headline": "Van circa €40k naar €325k omzet per jaar.",
        "intro": "Ecodor verkoopt enzymatische geurverwijderaars voor huisdieren. In juli 2024 bouwden we de webshop opnieuw, van OpenCart naar WooCommerce, en sindsdien optimaliseren we hem doorlopend met onderzoek en A/B-tests. De omzet van de eigen webshop groeide van circa €40k op jaarbasis (2024), via circa €75k in 2025, naar een verwachte €325k in 2026.",
        "hero": "/assets/img/cases/ecodor-hero.jpg",
        "facts": [],
        "stats": [
            {"count": 224157, "prefix": "€", "label": "omzet in 2026 t/m 5 oktober, incl. btw"},
            {"count": 325, "prefix": "≈ €", "suffix": "k", "label": "prognose voor heel 2026"},
            {"text": "79–82%", "label": "van de omzet komt via mobiel"},
            {"count": 45, "suffix": "%", "label": "winrate over 20 tests, waarvan een deel nog loopt"},
        ],
        "blocks": [
            {"type": "text", "h2": "Het uitgangspunt", "paras": [
                "Ecodor maakt een enzymatische urinegeurverwijderaar, bijvoorbeeld voor kattenpis. Dat betekent dat het product de geurdeeltjes afbreekt in plaats van de geur met parfum te maskeren. Klanten zijn er enthousiast over, en het product ligt bij dierenzaken als Pet’s Place, Ranzijn en Boerenbond en wordt verkocht via Bol.com en deels Amazon.",
                "Via het eigen kanaal ging het moeizaam. De oude OpenCart-webshop voldeed niet meer aan de normen voor gebruiksgemak en koppelingen met andere software, en werkte slecht op mobiel, terwijl 79 tot 82% van de omzet juist via mobiel binnenkomt. Daarbij was er weinig inzicht in data en weinig marketing.",
            ]},
            {"type": "bars", "h2": "Omzetgroei van de webshop",
             "lead": "Door de nieuwe site te bouwen en consequent nieuwe ontwikkelingen te testen werd marketing rendabeler, en kon die worden opgeschaald. Die combinatie zit achter de groei, en op dit moment zien we hem nog niet vertragen.",
             "rows": [
                 ("2024 (jun–dec)", 21420.56, "€21.421", "act"),
                 ("2024 op jaarbasis", 40000, "≈ €40.000", "est"),
                 ("2025 (heel jaar)", 74569.83, "€74.570", "act"),
                 ("2026 t/m 5 oktober", 224157.26, "€224.157", "act"),
                 ("2026 prognose", 325543.01, "≈ €325.543", "est"),
             ],
             "note": "Volle balk: gerealiseerde omzet. Gearceerde balk: omrekening of prognose. Omzet van de eigen webshop, inclusief btw (dus zonder Bol.com en Amazon). 2024 op jaarbasis is een omrekening van de omzet van juni tot en met december. De prognose voor 2026 is gebaseerd op de omzet tot en met 5 oktober 2026, aangevuld met het verwachte najaar: Black Friday, extra verkoop doordat katten en andere huisdieren in het najaar en de winter vaker binnen worden gehouden, en doorzetting van de groei."},
            {"type": "cards", "h2": "Vier uitdagingen", "lead": "Dit moest de webshop oplossen om bezoekers zeker te laten kopen.",
             "items": [
                 ("Laten zien dat het écht werkt", "shield", "Er zijn aanbieders die de geur alleen maskeren, waarna die terugkomt. De site moest vroeg in de klantreis duidelijk maken dat dit product de geur wél verwijdert."),
                 ("Geen schade aan de ondergrond", "check", "Een grote angst in de branche is dat een reiniger nieuwe vlekken maakt of de vloer beschadigt. We moesten tonen dat het een natuurlijk product is, en expliciet voor welke ondergronden het geschikt is."),
                 ("Snel bestellen op mobiel", "target", "Het merendeel van de omzet komt via mobiel. De shop moest daar zo soepel werken dat bestellen snel en zonder gedoe gaat."),
                 ("Beginnen met weinig data", "search", "Bij de start was er weinig inzicht in data. Eerst moest alle analytics goed worden ingericht, zodat zowel wij als Ecodor konden zien hoe de shop presteerde en wat er te verbeteren viel."),
             ]},
            {"type": "phases", "h2": "Onze aanpak", "lead": "Van fundament tot doorlopend testprogramma.",
             "items": [
                 ("Fundament", "target", "Een nieuwe WooCommerce-webshop (juli 2024), met mobiel als uitgangspunt: migratie van producten en vertalingen, dealerrollen met eigen prijzen, Mollie-betalingen, een Zoho CRM-koppeling en een lancering in 19 talen. Tegelijk zetten we alle analytics op die er nog niet waren.", "Uitkomst: een nieuw fundament om op door te ontwikkelen, en data om beslissingen op te baseren."),
                 ("Onderzoek", "search", "We keken niet alleen naar Google Analytics. We onderzochten ook de concurrentie, deden beoordelingsonderzoek naar wat klanten waarderen, en bekeken met heatmaps en sessieopnames hoe bezoekers door de shop klikken. Op de juiste momenten vragen we bezoekers of ze informatie missen, en na de checkout hoe de ervaring was.", "Uitkomst: onderbouwde knelpunten en kansen."),
                 ("Prioriteren", "bulb", "Uit het onderzoek volgden twee lijsten: een optimalisatiebacklog met ‘just do it’-aanpassingen, waarvan een test waarschijnlijk geen significant verschil zou tonen, en een testbacklog voor wijzigingen met hoog risico en grote impact. De volgorde bepaalden we samen met Ecodor, op basis van hoeveel een test raakt, de geschatte omzet en het gemak van implementatie.", "Uitkomst: een geprioriteerde backlog, afgestemd op de strategie van Ecodor."),
                 ("Testen", "flask", "We starten altijd meerdere tests met hoge impact tegelijk. In de beginjaren was er niet genoeg verkeer om kleine aanpassingen te testen; die voerden we deels direct door op basis van het onderzoek. Wat riskant en impactvol was, testten we altijd eerst.", "Uitkomst: een doorlopend programma, met de testtijdlijn hieronder."),
             ]},
            {"type": "quote", "h2": "Wat Ecodor zegt", "quote": ("Wij zijn ontzettend tevreden over de samenwerking met Boldframe […]. Vanaf het eerste contact verliep alles soepel en professioneel. […] Hij denkt mee, schakelt snel en weet technische wensen perfect te vertalen naar een gebruiksvriendelijke website.", "Robin Kanters", "Ecodor")},
            {"type": "table", "h2": "Van bevinding naar test", "lead": "Elke test begon met een observatie uit het onderzoek.",
             "head": ["Bevinding", "Test"],
             "rows": [
                 ["40% van de bezoekers haakte op de productpagina af voordat er iets in de winkelwagen ging, en onderweg was niet duidelijk onder welke voorwaarden er werd gekocht.", "Micro-garanties onder de winkelwagenknop"],
                 ["In heatmaps werden tekstlinks in blogs vaak gebruikt, maar bezoekers die op een blogbericht landen brachten verhoudingsgewijs weinig omzet op.", "Opvallendere tekstlinks"],
                 ["Interne zoekopdrachten, Google Ads en Search Console lieten zien dat ‘enzymatische reiniger’ een sleutelterm is, en AI-chatbots noemen dit type product vaak als oplossing voor kattengeur. Ook bleek er een breed scala aan toepassingen.", "Toepassingsgebied bij de productomschrijving"],
             ]},
            {"type": "tests", "h2": "Wat we testten", "lead": "Een selectie van de 20 tests die we draaiden, met hypothese, uitkomst en learning. Nieuwste bovenaan, vastgepinde tests eerst."},
            {"type": "cards", "h2": "Hoe we testen, en wat dat betekent", "lead": "Cijfers zijn pas bruikbaar als je weet hoe ze tot stand kwamen.",
             "items": [
                 ("Indicatief, niet absoluut", "flask", "Onze uitslagen komen vaak uit op een chance to beat van ongeveer 90 tot 95%. Dat is sterk genoeg om op te sturen, maar geen wetenschappelijk bewijs. Bij Ecodor kiezen we daar bewust voor: een hoge testsnelheid en snel winsten boeken weegt zwaarder dan 100% zekerheid."),
                 ("Niet elke test wint", "cross", "Over 20 tests, waarvan een deel nog loopt, is de winrate op dit moment 45%; de rest was negatief of onbeslist. Dat is precies waarom we testen: een verliezer gaat niet live, dus de shop wordt niet slechter. Een negatieve uitslag stuurt bovendien de volgende hypothese."),
                 ("Dit is een selectie", "search", "Hier staan vooral de tests met aanzienlijke winst, plus een verliezer als voorbeeld. Het zijn niet alle 20 tests die we hebben gedraaid."),
             ]},
            {"type": "text", "h2": "Wat het heeft opgeleverd", "paras": [
                "In een kleine twee jaar staat er een sterke webshop met veel learnings. Ecodor heeft in Nederland online een sterke marktpositie opgebouwd, bedient inkomend verkeer goed en overtuigt bezoekers dat dit het product is dat hen helpt.",
                "De rode draad in alle tests: gebruiksgemak, en het vertrouwen en de zelfverzekerdheid van de koper vergroten, zodat bestellen sneller en met meer zekerheid gaat. We zijn nooit gestopt met optimaliseren, en ook van tests die geen winnaar waren hebben we geleerd welke richting we op moesten.",
            ]},
            {"type": "cta", "h2": "Benieuwd wat dit voor jouw webshop kan betekenen?", "lead": "Plan een gesprek van 30 minuten, dan laten we zien waar jouw conversie-lekken zitten.", "other": ("/cases/schuurman/", "Bekijk ook de case van Schuurman →")},
        ],
        "tests": [
            {
                "id": "e5", "started": "2026-09-04", "status": "w", "duration": "",
                "title": "Toepassingsgebied bij de productomschrijving",
                "observation": "Interne zoekopdrachten, Google Ads en Search Console lieten zien dat ‘enzymatische reiniger’ een sleutelterm is, en AI-chatbots adviseren dit type product vaak als oplossing voor kattengeur. Ook kregen we inzicht in de uiteenlopende toepassingen van de producten.",
                "principle": "Zekerheid bij het bestellen: wie ziet dat het product op zijn ondergrond werkt, bestelt zekerder.",
                "hyp": "Als we alle toepassingen expliciet noemen op de productpagina’s en andere plekken, kan de klant zekerder bestellen.",
                "metrics": [("+9,98%", "Omzet per bezoeker, totaal", ""), ("+22,9%", "Omzet per bezoeker, mobiel", "793 tegen 800 gebruikers"), ("-7,1%", "Omzet per bezoeker, desktop", "162 tegen 156 gebruikers")],
                "note": "Op mobiel is de kans dat de variant de controleversie verslaat 91,7%. Op desktop bleef de conversieratio vrijwel gelijk (+0,6%), maar daalde de gemiddelde orderwaarde met 7,7%, op basis van 63 conversies in dat segment.",
                "learn": "Op mobiel, waar het merendeel van de bezoekers zit, werkt het expliciet benoemen van de toepassingen duidelijk. Op desktop daalde de orderwaarde; met 63 conversies in dat segment is dat nog geen harde conclusie. Daarom hebben we de aanpassing alleen op mobiel doorgevoerd.",
                "img": "/assets/img/tests/e5.jpg", "alt": "Ecodor productpagina voor en na: blok met toepassingsgebied bij de productomschrijving",
                "pinned": False,
            },
            {
                "id": "e2", "date": "2026-06-26", "status": "v", "duration": "",
                "title": "Groene tekstlinks in blogs",
                "hyp": "Met merkgroene links in plaats van blauwe vallen ze meer op, dus navigeren bezoekers sneller naar productpagina's.",
                "metrics": [("-12,55%", "Omzet per bezoeker", "€3,23 → €2,82"), ("-8,02%", "Orderwaarde", "€52,00 → €47,83")],
                "learn": "Groen wijkt af van de webconventie dat links blauw zijn, en was op mobiel bij fel licht slecht leesbaar.",
                "img": "/assets/img/tests/e2.jpg", "alt": "Ecodor blogtekst voor en na: groene tekstlinks",
                "pinned": False,
            },
            {
                "id": "e3", "date": "2026-06-02", "status": "w", "duration": "",
                "title": "Micro-garanties onder de winkelwagenknop",
                "observation": "Vanaf de productpagina zagen we 40% drop-off naar het toevoegen van producten aan de winkelwagen. Ook was tijdens het aankoopproces niet duidelijk onder welke voorwaarden er werd gekocht.",
                "principle": "Bezoekers moeten zelfverzekerd een aankoop kunnen doen.",
                "hyp": "Door de USP’s direct onder de winkelwagenknop te plaatsen, verhogen we het vertrouwen op het beslismoment, wat leidt tot een hogere conversie.",
                "metrics": [("+2,63%", "Omzet per bezoeker", "€7,12 → €7,31"), ("+7,39%", "Orderwaarde", "€52,13 → €55,98")],
                "note": "Op basis van 109 conversies uit 839 sessies.",
                "learn": "Op mobiel was de winst veel groter, maar die data is helaas verloren gegaan. We hebben de aanpassing doorgevoerd en kunnen met redelijk vertrouwen zeggen dat het een verbetering is.",
                "img": "/assets/img/tests/e3.jpg", "alt": "Ecodor productpagina voor en na: vertrouwensblok onder de knop",
                "pinned": False,
            },
            {
                "id": "e4", "started": "2026-05-25", "status": "w", "duration": "",
                "title": "Dikgedrukte groene tekstlinks in blogs",
                "observation": "In heatmaps werden tekstlinks in blogberichten regelmatig gebruikt, maar bezoekers die op een blogbericht landen brachten verhoudingsgewijs weinig omzet op.",
                "principle": "Links moeten meer opvallen, zodat tekst makkelijk te scannen is naar een vervolgactie.",
                "hyp": "Door de links een zwaarder gewicht te geven maken we de tekst beter scanbaar en de vervolgactie duidelijker, zodat bezoekers meer pagina’s bekijken en sneller naar een productpagina gaan.",
                "metrics": [("+12,08%", "Omzet per bezoeker", "€3,04 → €3,41"), ("-1,61%", "Orderwaarde", "€45,81 → €45,07")],
                "learn": "Bezoekers herkennen de groene links nu niet alleen als gemarkeerde tekst, maar ook als doorklikbare links. Doordat ze dikgedrukt zijn vallen ze extra op, ook op mobiel. Mogelijk speelt mee dat dikgedrukte tekst de gedachte oproept dat het belangrijk is.",
                "next": "Had deze test niet gewerkt, dan was de volgende stap een volledig conventionele linkkleur (#0645AD) geweest: lelijker, maar ‘ugly converts better’. Dat hadden we eerst met Ecodor overlegd.",
                "img": "/assets/img/tests/e4.jpg", "alt": "Ecodor blogtekst voor en na: dikgedrukte groene tekstlinks",
                "pinned": False,
            },
        ],
    },
    "bidet": {
        "name": "Bidet.nl",
        "sub": "Van €48k naar een verwachte €450k omzet in vier jaar",
        "eyebrow": "Case · Douche-wc's · WooCommerce",
        "headline": "Van €48k naar bijna €450k omzet in vier jaar.",
        "intro": "Bidet.nl verkoopt en installeert douche-wc's, en verkoopt online veel douche-wc-producten, op wens inclusief installatie. Boldframe bouwde de hele webshop en verbetert hem sinds 2022 doorlopend op basis van onderzoek naar reviews, chatberichten en data. De omzet groeide van €47.625 in 2022 naar €368.518 in 2025, en staat in 2026 na negen maanden al op €399.240.",
        "hero": "/assets/img/cases/bidet-hero.jpg",
        "facts": [],
        "stats": [
            {"count": 399240, "prefix": "€", "label": "omzet in 2026 t/m 7 oktober, incl. btw"},
            {"count": 450, "prefix": "≈ €", "suffix": "k", "label": "verwachte omzet voor heel 2026"},
            {"text": "7,7×", "label": "omzet in 2025 ten opzichte van 2022 (gerealiseerd)"},
        ],
        "blocks": [
            {"type": "text", "h2": "Het uitgangspunt", "paras": [
                "Bidet.nl is verkoper en installateur van douche-wc's, met een eigen showroom in Nieuwerkerk aan den IJssel en een eigen installatieteam. De webshop moest meer doen dan producten tonen: een douche-wc is een aankoop waar klanten over twijfelen, omdat het om water, stroom en installatie gaat.",
                "Boldframe bouwde de volledige webshop en blijft hem sinds 2022 verbeteren. Dit is een andere case dan die van Ecodor: er zijn geen A/B-tests uitgevoerd, omdat het verkeer daarvoor te beperkt was. In plaats daarvan baseerden we elke aanpassing op onderzoek, data en best practices. Het bewijs is dan ook niet een testuitslag, maar de verandering van de shop en de omzet over de jaren heen.",
            ]},
            {"type": "bars", "h2": "Omzetgroei van de webshop",
             "lead": "Elk jaar meer omzet dan het jaar ervoor, en 2026 ligt na negen maanden al boven het volledige jaar 2025.",
             "rows": [
                 ("2022", 47625.25, "€47.625", "act"),
                 ("2023", 143877.44, "€143.877", "act"),
                 ("2024", 188124.08, "€188.124", "act"),
                 ("2025", 368517.51, "€368.518", "act"),
                 ("2026 t/m 7 oktober", 399240.41, "€399.240", "act"),
                 ("2026 verwachting", 450000, "≈ €450.000", "est"),
             ],
             "note": "Volle balk: gerealiseerde omzet. Gearceerde balk: verwachting. Het gaat om de totale verkopen volgens de webshopstatistieken, inclusief btw en verzendkosten, over een kalenderjaar (1 januari tot en met 31 december). De verwachting voor 2026 is een inschatting op basis van de omzet tot en met 7 oktober en het najaar."},
            {"type": "cards", "h2": "Waar de groei vandaan komt", "lead": "De omzet is niet alleen het resultaat van optimalisatie. Dit zijn de factoren die samen meespelen.",
             "items": [
                 ("Een groeiende markt", "target", "Douche-wc's zijn in korte tijd een veel bekender product geworden. Die interesse in de markt zorgt voor meer zoekers en dus meer bezoekers."),
                 ("Een uitgebreider assortiment", "check", "Bidet.nl heeft de afgelopen jaren nieuwe modellen toegevoegd, waardoor er meer klanten met een passende keuze te bedienen zijn."),
                 ("Een sterkere webshop", "bulb", "Elke aanpassing hieronder komt voort uit onderzoek naar wat klanten twijfelen en zoeken. Zo zetten we het extra verkeer vaker om in bestellingen."),
                 ("Geen A/B-tests, wel onderzoek", "search", "Het verkeer was te laag om te testen. We kozen daarom bewust voor aanpassingen op basis van onderzoek, data en best practices, en volgden de omzet over de jaren heen."),
             ]},
            {"type": "cards", "h2": "Wat het onderzoek liet zien", "lead": "Bij de start, en gedurende het project, onderzochten we reviews, chatberichten en data.",
             "items": [
                 ("Vragen over installatie", "phone", "Klanten stelden veel vragen over installatie en productadvies. Stroom, water en technische specificaties kwamen steeds terug en zorgden voor twijfel."),
                 ("Onzekerheid over techniek", "shield", "Het was niet altijd duidelijk wat nodig is om een douche-wc aan te sluiten, zoals de afstand tot het stopcontact of de wateraansluiting. Veel klanten willen de installatie liever uit handen geven en zeker weten dat het goed gebeurt."),
                 ("Lastig kiezen en vergelijken", "search", "Klanten vonden het moeilijk om een model te kiezen en de functies van de modellen met elkaar te vergelijken."),
                 ("Behoefte aan persoonlijk advies", "target", "Klanten willen een adviseur die vertelt welk model past bij hun wensen, hoe de installatie eruit komt te zien en hoe het in zijn werk gaat. Een bezoek aan de showroom neemt die twijfel weg."),
             ]},
            {"type": "table", "h2": "Van inzicht naar aanpassing", "lead": "Elke grote wijziging begon met een bevinding uit het onderzoek.",
             "head": ["Bevinding", "Aanpassing"],
             "rows": [
                 ["Klanten twijfelen over installatie, stroom en water, en willen de installatie liever uit handen geven.", "Installatie-opties met prijs direct bij het product, een duidelijke levertijd en installatietijd, en een trustbox met showroom, installatieteam en garantie onder de knop."],
                 ["Klanten vinden het moeilijk om een model te kiezen en te vergelijken.", "Filters op merk, afstandsbediening, föhn, type, verwarmde zitting, stroomvoorziening en douchekop, een keuzehulp en standaard sorteren op populariteit."],
                 ["Klanten willen persoonlijk advies en de producten kunnen beleven.", "De showroom en het installatieteam prominent op de homepage, en de keuzehulp ook op de homepage aangeboden."],
                 ["De interne zoekfunctie wordt veel gebruikt.", "De zoekbalk op mobiel direct onder de header, en veel tijd besteed aan zoekresultaten die aansluiten bij wat klanten zoeken."],
                 ["Klanten verdwalen in vakjargon van merken en categorieën.", "Een menu dat producten direct toont en is ingedeeld op toepassing en functie."],
                 ["De belangrijkste informatie stond ver onder in de productpagina.", "Infographics bij het product, een grotere afbeelding op desktop, de beoordeling bovenaan op mobiel en de afmetingen van de zitting."],
             ]},
            {"type": "media", "h2": "De productpagina",
             "lead": "De pagina begint nu met wat klanten willen weten: beoordelingen, levertijd, installatie-opties en afmetingen. Onder de knop staat een trustbox met de showroom, het installatieteam en de garantie.",
             "items": [
                 ("/assets/img/cases/bidet-product-2022.jpg", "Bidet.nl productpagina in 2022", "Voor (2022): beschrijving en optie-keuze, weinig installatie-informatie", 1400, 1219),
                 ("/assets/img/cases/bidet-product-2026.jpg", "Bidet.nl productpagina in 2026", "Na (2026): beoordelingen, levertijd, installatie-opties en trustbox", 1400, 1111),
             ]},
            {"type": "media", "h2": "De categoriepagina",
             "lead": "Meer filters, een keuzehulp en sortering op populariteit helpen klanten sneller bij het product dat bij hen past.",
             "items": [
                 ("/assets/img/cases/bidet-categorie-2022.jpg", "Bidet.nl categoriepagina in 2022", "Voor (2022): beperkte filters", 1400, 1389),
                 ("/assets/img/cases/bidet-categorie-2026.jpg", "Bidet.nl categoriepagina in 2026", "Na (2026): meer filters, keuzehulp en sortering op populariteit", 1400, 1167),
             ]},
            {"type": "media", "h2": "De homepage",
             "lead": "De homepage laat nu zien dat Bidet.nl meer is dan een dozenschuiver: met een eigen installatieteam, een showroom en een keuzehulp.",
             "items": [
                 ("/assets/img/cases/bidet-home-2022.jpg", "Bidet.nl homepage in 2022", "Voor (2022): vooral producten en aanbiedingen", 1400, 1282),
                 ("/assets/img/cases/bidet-home-2026.jpg", "Bidet.nl homepage in 2026", "Na (2026): installatieteam, showroom en keuzehulp", 1400, 1158),
             ]},
            {"type": "media", "h2": "Het menu",
             "lead": "Het menu toont nu producten in plaats van alleen merken en categorieën. Klanten zien direct welk model bij hen past, zonder vakjargon.",
             "items": [
                 ("/assets/img/cases/bidet-menu-2022.jpg", "Bidet.nl menu in 2022", "Voor (2022): lijsten met merken en categorieën", 1400, 874),
                 ("/assets/img/cases/bidet-menu-2026.jpg", "Bidet.nl menu in 2026", "Na (2026): producten met afbeeldingen, op toepassing ingedeeld", 1400, 844),
             ]},
            {"type": "media", "h2": "Op mobiel", "cls": "phones",
             "lead": "De zoekbalk staat direct onder de header, omdat uit de data bleek dat die veel gebruikt wordt. Op de productpagina staat de klantbeoordeling bovenaan, en de bestaande content is naar beneden verschoven, met infographics om snel doorheen te klikken.",
             "items": [
                 ("/assets/img/cases/bidet-mobiel-2022.jpg", "Bidet.nl op mobiel in 2022", "Voor (2022): geen zoekbalk in beeld", 702, 1400),
                 ("/assets/img/cases/bidet-mobiel-2026.jpg", "Bidet.nl op mobiel in 2026", "Na (2026): zoekbalk direct onder de header, beoordeling bovenaan", 657, 1400),
             ]},
            {"type": "text", "h2": "Wat het heeft opgeleverd", "paras": [
                "De omzet groeide van €47.625 in 2022 naar €368.518 in 2025, ruim 7,7 keer zoveel. In 2026 staat de webshop na negen maanden op €399.240, en de verwachting voor het hele jaar is circa €450.000.",
                "Een deel van die groei is gedreven door de markt en het uitgebreidere assortiment. Wat de shop zelf doet is dat bezoekers sneller antwoord vinden op hun vragen over installatie, techniek en keuze, en daardoor vaker bestellen.",
            ]},
            {"type": "cta", "h2": "Benieuwd wat dit voor jouw webshop kan betekenen?", "lead": "Plan een gesprek van 30 minuten, dan laten we zien waar jouw conversie-lekken zitten.", "other": ("/cases/ecodor/", "Bekijk ook de case van Ecodor →")},
        ],
    },
    "schuurman": {
        "name": "Schuurman Dier & Hengelsport",
        "sub": "Lopend testtraject in dierenvoeding & hengelsport",
        "headline": "Testen waar de omzet echt vandaan komt.",
        "eyebrow": "Lopend testtraject",
        "intro": "Schuurman Dier & Hengelsport heeft een enorm assortiment, en het grootste deel van de omzet komt uit dierenvoeding. Samen bouwen we een testprogramma op dat daarop is afgestemd. De eerste test is afgerond, de tweede loopt op dit moment.",
        "hero": "/assets/img/cases/schuurman-hero.jpg",
        "stats": [
            {"count": 2, "label": "tests: één afgerond, één loopt nog"},
            {"count": 3, "label": "niveaus in het nieuwe menu"},
            {"count": 50, "suffix": "%", "label": "van de productpagina-bezoekers scrolt langs de add-to-cart-knop"},
            {"count": 70, "suffix": "%", "label": "van de productpagina-bezoekers voegt uiteindelijk niets toe aan de winkelwagen"},
        ],
        "blocks": [
            {"type": "text", "h2": "Het uitgangspunt", "paras": [
                "Bij de start van het traject zagen we dat een groot deel van de omzet van Schuurman uit dierenvoeding komt. De website presenteerde zich echter vooral als hengelsportwinkel. Daarbij is het assortiment zo groot dat bezoekers snel moeten kunnen vinden wat ze zoeken.",
                "Daarom begonnen we met een fundament: een webshop die laat zien wat er daadwerkelijk wordt verkocht, en waarin klanten sneller en makkelijker bij het juiste product komen. Daarop bouwen we het testprogramma.",
            ]},
            {"type": "media", "h2": "Fundament: een nieuw menu",
             "lead": "De menustructuur is opnieuw opgezet, zodat de dierenwinkel en de hengelsport allebei hun eigen plek hebben, met meer diepgang.",
             "items": [
                 ("/assets/img/cases/schuurman-menu-voor.jpg", "Schuurman desktopmenu vóór de wijziging: alleen hengelsportcategorieën zichtbaar", "Voor: een menu dat vooral hengelsport laat zien", 1600, 923),
                 ("/assets/img/cases/schuurman-menu-na.jpg", "Schuurman desktopmenu na de wijziging: dierenwinkel met drie niveaus", "Na: dierenwinkel en hengelsport gescheiden, met drie niveaus", 1600, 830),
                 ("/assets/img/cases/schuurman-menu-mobiel.jpg", "Schuurman mobiel menu na de wijziging met tabs Hengelsport en Dier", "Na, op mobiel: kies direct tussen Hengelsport en Dier", 800, 855),
             ]},
            {"type": "cards", "h2": "Wat het nieuwe menu oplost", "lead": "Vijf punten waarop het menu verbetert.",
             "items": [
                 ("Diepgang", "arrow-right", "Bezoekers klikken direct door naar de categorie die voor hen relevant is, met drie niveaus in het menu."),
                 ("Duidelijke scheiding", "check", "Er is nu een heldere scheiding tussen hengelsport en dierenwinkel."),
                 ("Totaaloverzicht", "target", "Klanten zien veel beter wat Schuurman allemaal te bieden heeft."),
                 ("Focus op dieren", "paw", "De meeste omzet komt uit dierenwinkelproducten, dus die krijgen nu voorrang."),
                 ("Ruimte voor de zoekfunctie", "search", "Zoeken werd op mobiel veel gebruikt, maar op desktop bleef het achter omdat het een klein icoontje was. Het is nu een groot veld. Zoekverkeer converteert doorgaans 2 tot 3 keer zo goed, mits de zoekfunctie goed werkt."),
             ]},
            {"type": "tests", "h2": "Testtijdlijn", "lead": "Elke test met hypothese en uitkomst, ook als er geen significant verschil uit komt. Zodra de lopende test is afgerond, voegen we het resultaat hier toe."},
            {"type": "text", "h2": "Waar Schuurman nu staat", "paras": [
                "Schuurman staat aan het begin van een testtraject. We tonen daarom geen omzetcijfers of groei: die kunnen we pas eerlijk benoemen na meerdere afgeronde winnende tests. Deze pagina wordt aangevuld zodra de resultaten binnen zijn.",
            ]},
            {"type": "cta", "h2": "Benieuwd wat een testtraject voor jouw webshop kan betekenen?", "lead": "Plan een gesprek van 30 minuten, dan laten we zien waar jouw conversie-lekken zitten.", "other": ("/cases/ecodor/", "Bekijk ook de case van Ecodor →")},
        ],
        "tests": [
            {
                "id": "s3", "started": "2026-09-29", "status": "l", "duration": "",
                "title": "Sticky add-to-cart op de productpagina (mobiel)",
                "observation": "Ongeveer 50% van de productpagina-bezoekers scrolt langs de add-to-cart-knop, waardoor de knop uit beeld verdwijnt. Dat kan betekenen dat klanten zich verder verdiepen in de productinformatie. Daarnaast voegt 70% van de bezoekers uiteindelijk geen product toe aan de winkelwagen.",
                "hyp": "Als we een ‘In winkelwagen’-balk onderaan het mobiele scherm fixeren zodra de originele knop uit beeld verdwijnt, nemen we de frictie weg op het moment dat de bezoeker overtuigd is. Dat leidt tot een hogere add-to-cart rate en een hogere algehele conversie.",
                "metrics": [],
                "learn": "Nog geen learning: de test loopt.",
                "img": "/assets/img/tests/s3.jpg", "alt": "Schuurman productpagina op mobiel voor en na: sticky add-to-cart-balk onderaan",
                "pinned": False,
            },
            {
                "id": "s2", "date": "2026-09-11", "status": "n", "duration": "18 dagen",
                "title": "Productpagina opschonen: filterknop en broodkruimelbalk (mobiel)",
                "hyp": "Als we de overbodige filterknop verwijderen en de massieve broodkruimelbalk op mobiel minimaliseren, stijgt het add-to-cart-percentage. Dat komt doordat we de cognitieve overbelasting verlagen en de kerninformatie (titel, prijs en bestelknop) direct in het eerste zichtbare scherm plaatsen.",
                "metrics": [("+3,91%", "Conversie (alle apparaten)", "7,82% → 8,13%"), ("-3,01%", "Omzet per bezoeker", "€8,18 → €7,93"), ("+1,86%", "Conversie mobiel", "7,87% → 8,01%"), ("+2,33%", "Orderwaarde mobiel", "€69,32 → €70,94")],
                "note": "De test liep van 11 t/m 29 september met 3.814 gebruikers en 304 conversies. De kans dat de variant beter presteert dan het origineel is 63,62%. Dat is ruim onder de gebruikelijke 90 tot 95%, dus de uitkomst is niet te onderscheiden van toeval.",
                "learn": "Het opschonen van de productpagina geeft geen betrouwbaar verschil: de conversie steeg licht, maar de omzet per bezoeker daalde licht.",
                "img": "/assets/img/tests/s2.jpg", "alt": "Schuurman productpagina op mobiel voor en na het opschonen",
                "pinned": False,
            },
        ],
    },
}
CASES_COMING_SOON = []

# Logo-muur: alle logo's zijn vooraf eenkleurig (merkblauw) en op gelijke visuele grootte gebracht.
# Nieuw logo toevoegen: afbeelding in assets/img/logos/ en een regel hieronder (naam, bestand, breedte, hoogte, optionele link).
CLIENT_LOGOS = [
    ("Schuurman Dier & Hengelsport", "schuurman.png", 120, 28, "/cases/schuurman/"),
    ("Ecodor", "ecodor.png", 68, 50, "/cases/ecodor/"),
    ("Hulpmiddelenspecialist.nl", "hulpmiddelenspecialist.png", 91, 37, None),
    ("Bidet.nl", "bidet.png", 111, 30, "/cases/bidet/"),
    ("Drempelhulp", "drempelhulp.png", 150, 22, None),
    ("Home Care Innovation", "home-care-innovation.png", 98, 35, None),
    ("Pro-Darts.be", "pro-darts.png", 129, 26, None),
    ("Camping Jagtveld", "jagtveld.png", 98, 35, None),
    ("Petite Zara", "petite-zara.png", 81, 42, None),
    ("Vestiti del Capo", "capo.png", 54, 54, None),
]


def row_logo(slug):
    for name, f, w, h, href in CLIENT_LOGOS:
        if href == f"/cases/{slug}/":
            return f'<img class="rowlogo" src="/assets/img/logos/{f}" alt="" width="{round(w*.62)}" height="{round(h*.62)}">'
    return ""


def build_logo_wall(h2="Webshops waarvoor we werken"):
    cells = []
    for i, (name, f, w, h, href) in enumerate(CLIENT_LOGOS):
        img = f'<img src="/assets/img/logos/{f}" alt="{name}" width="{w}" height="{h}" loading="lazy">'
        inner = f'<a href="{href}" aria-label="{name}: bekijk de case">{img}</a>' if href else img
        cells.append(f'<li data-reveal style="--d:{i}">{inner}</li>')
    return f'<section><h2 data-reveal>{h2}</h2><p class="lead" data-reveal>Webshops in onder meer huisdieren, hobby\u2019s en care. Bij een deel daarvan lees je hier de volledige case.</p><ul class="logos">{"".join(cells)}</ul></section>'


GOOGLE_REVIEWS_URL = "https://share.google/dzaxrX2aVZA24SoVb"
TESTIMONIALS = [
    ("Wij zijn ontzettend tevreden over de samenwerking met Boldframe […]. Vanaf het eerste contact verliep alles soepel en professioneel. […] Hij denkt mee, schakelt snel en weet technische wensen perfect te vertalen naar een gebruiksvriendelijke website.", "Robin Kanters", "Ecodor"),
    ("Van idee tot een werkende webshop voor onze camping: alles liep soepel. Er is goed meegedacht. Fijn contact en snel schakelen. Zeer tevreden met het eindresultaat.", "Mark Leerdam", "Camping Jagtveld"),
]


def build_offer(id_attr=' id="scan"'):
    return f'''<section{id_attr}><h2 data-reveal>Claim jouw gratis website scan</h2><p class="lead" data-reveal>Je krijgt twee dingen die je direct kunt gebruiken, ook als je daarna niet met mij verder wilt.</p>
<div class="offer">
<div data-reveal style="--d:0"><span class="tag">Onderdeel 1</span><h3>Volledige website conversiescan</h3><p>Ik bezoek je webshop en analyseer waar je conversie-lekken zitten. Geen vaag rapport, maar directe actiepunten waar je zelf mee aan de slag kunt.</p></div>
<div data-reveal style="--d:1"><span class="tag">Onderdeel 2</span><h3>Het ‘Van Gokken naar Groeien’ Playbook (PDF)</h3><ul><li>Mijn volledige stappenplan bij de onboarding van nieuwe klanten</li><li>Mijn Figma-template voor funnelbreakdowns</li><li>Een lijst met 20 van mijn favoriete A/B-tests voor shops in jouw branche</li></ul></div>
</div></section>'''


def build_testimonials():
    cards = "".join(
        f'<figure data-reveal style="--d:{i}"><blockquote>{q}</blockquote><figcaption><b>{n}</b>, {r}</figcaption></figure>'
        for i, (q, n, r) in enumerate(TESTIMONIALS)
    )
    return f'<section><h2 data-reveal>Wat klanten zeggen</h2><div class="quotes">{cards}</div><p data-reveal><a href="{GOOGLE_REVIEWS_URL}" target="_blank" rel="noopener">Lees alle reviews op Google →</a></p></section>'


STATUS_LABEL = {"w": "Winnaar", "v": "Verliezer", "l": "Loopt nog", "n": "Inconclusief"}

INSIGHTS = {
    "hoeveel-verkeer-om-te-testen": {
        "title": "Hoeveel verkeer heb je nodig om te testen?",
        "date": "2026-10-05",
        "dek": "Als vuistregel heb je minimaal zo\u2019n 500 meetbare conversies per maand nodig om snel te kunnen testen. Heb je minder, dan zijn er slimme alternatieven. Reken het hieronder uit voor jouw shop.",
        "body": [
            "## De vuistregel: 500 conversies per maand",
            "Wij gaan uit van minimaal zo\u2019n 500 conversies per maand die je kunt meten. Dan kun je redelijk snelle testtrajecten starten, waarbij een test maar twee tot drie weken hoeft te duren om iets aan te tonen. Let wel: hoe kleiner het effect dat je wilt aantonen, hoe meer verkeer of tijd je nodig hebt. Met 500 conversies per maand toon je in twee tot drie weken vooral grotere effecten aan.",
            "## Hoe zeker wil je zijn?",
            "Je kiest zelf hoe hoog de significantie moet zijn. Wil je een probability van 99%, dan kost je dat heel veel tijd en data. Voor een webshop is een probability van 90 tot 95% vaak voldoende: dan kun je ervan uitgaan dat de test een winnaar is.",
            "Het risico is bekend. Ga je voor 95%, dan voer je statistisch gezien eens in de 20 keer alsnog een wijziging door die geen wezenlijk effect had op je resultaten. Dat is een aannemelijk risico dat je als ondernemer moet kunnen en durven nemen. Het is vele malen beter dan je website op gevoel optimaliseren.",
            "## Te weinig verkeer? Kies een andere meetwaarde",
            "Heb je te weinig verkeer om te testen op bestellingen, dan kun je een test ook starten op basis van het aantal add-to-carts. Introduceer je een nieuwe, relevantere landingspagina voor de advertenties die je draait, dan kan de bounce rate een goede meetwaarde zijn. Daalt je bounce rate, dan is dat een sterke aanwijzing dat de landingspagina beter presteert.",
            "## Hoeveel tests kun je draaien?",
            "De hoeveelheid verkeer en conversies bepaalt ook hoeveel tests je ongeveer kunt draaien. Heb je weinig bezoekers en conversies, draai dan altijd brede tests die zoveel mogelijk impact maken op de bezoekers die je hebt: websitebrede tests, productpaginatests of optimalisaties in de winkelmand en checkout. Die raken alle bezoekers en dus alle conversies en bestellingen.",
            "Heb je heel veel bezoekers en data, dan kun je tests segmenteren. Je optimaliseert bijvoorbeeld \u00e9\u00e9n productlijstpagina (PLP) en draait in een fashionwinkel alleen een test voor klanten die op zoek zijn naar een broek. Door die segmentering overlappen tests niet met elkaar.",
            "## Pas op voor tests die elkaar beïnvloeden",
            "Draai je meerdere websitebrede tests tegelijk, dan kunnen die elkaar beïnvloeden. Presteert \u00e9\u00e9n test gigantisch goed en de andere twee matig of slecht, dan kan die grote winnaar de resultaten van de andere twee alsnog beïnvloeden. De uitkomsten kloppen dan niet helemaal.",
            "## Reken het uit voor jouw shop",
        ],
        "steps": [],
        "tool": "duration",
    },
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
            "Voor Ecodor, producent van geurverdrijvers tegen bijvoorbeeld kattenpis, realiseerde Boldframe onmiskenbare internationale groei: de website is via WPML vertaald in 19 talen op basis van DeepL, video's zijn meertalig ondertiteld, en dankzij een groeiend dealernetwerk in Europa kan Ecodor internationaal groeien zonder overal fysieke distributiepunten te hebben.",
            "Begin klein: richt je eerst op de landen met de grootste potentie, combineer geautomatiseerde vertaling met menselijke review voor nuance, en zorg dat marketing, content en logistiek aansluiten bij de lokale markt.",
        ],
        "steps": [],
        "tool": "reach",
    },
}
INSIGHT_ORDER = ["hoeveel-verkeer-om-te-testen", "ai-verkeer-meten-in-ga4", "ai-scan-landingspagina", "meertalige-ecommerce"]

DIENSTEN_STEPS = [
    ("Audit", "search", "We brengen de customer journey van je webshop in kaart en sporen de knelpunten op met heatmaps, sessieopnames en je eigen data — geen aannames."),
    ("Hypothese", "bulb", "Per knelpunt formuleren we een onderbouwde hypothese: welke aanpassing, waarom die het gedrag zou moeten veranderen, en wat we verwachten dat het oplevert."),
    ("A/B-test", "flask", "We testen de aanpassing tegen de huidige versie, met tools als Nelio A/B Testing, tot het resultaat statistisch betrouwbaar is."),
    ("Implementatie", "check", "Een bewezen winnaar voeren we definitief door. Een verliezer laten we vallen, ongeacht hoe logisch hij vooraf klonk — zoals je in onze testtijdlijnen kunt teruglezen."),
]
DIENSTEN_CHALLENGES = [
    ("Verkeer genoeg, omzet te weinig", "target", "Je steekt maandelijks budget in Google Ads, Meta of SEO. Er komen bezoekers binnen, maar onderaan de streep blijft er te weinig omzet over."),
    ("Afhakers vlak voor het afrekenen", "cross", "Bezoekers vullen hun winkelmand, en verlaten je site alsnog in de checkout. Vaak door twijfel die met een paar gerichte aanpassingen weg te nemen is."),
    ("Landingspagina's die de belofte van je advertentie niet waarmaken", "search", "Een advertentie trekt de juiste bezoeker, maar de pagina erachter beantwoordt niet de vraag waarmee hij kwam."),
    ("Beslissingen op onderbuikgevoel", "clock", "Wijzigingen worden doorgevoerd omdat ze logisch klinken, niet omdat ze getest zijn — met als risico dat je omzet juist inlevert."),
]
DIENSTEN_FAQ = [
    ("Moet ik mijn webbouwer ontslaan?", "Zeker niet. We kunnen de volledige development van je webshop op ons nemen, maar werken minstens zo graag samen met je huidige webbouwer om een bewezen winnaar structureel door te voeren."),
    ("Vertraagt dit mijn site?", "Nee. Een test draait via lichte A/B-testtools naast je bestaande webshop; pas een bewezen winnaar verwerken we structureel in de code."),
    ("Wat als de uplift uitblijft?", "Dan werken we kosteloos door. Halen we binnen zes maanden niet minimaal 10% uplift in omzet per bezoeker, dan vervallen de maandelijkse kosten van het traject totdat we dat wel hebben aangetoond. Het is dus geen geld-terug-garantie: we stoppen niet, maar blijven testen tot het resultaat er is. De meetmethode leggen we vooraf samen vast, op basis van de A/B-tests."),
    ("Moet ik direct duizenden euro's investeren in aanpassingen?", "Nee. We beginnen met de tests die het meeste opleveren tegen de minste ontwikkeltijd, en breiden pas uit zodra die hun waarde hebben bewezen."),
    ("Ik heb al andere marketingpartijen, werk jij hen niet tegen?", "Nee. Jouw advertentie- of SEO-partij zorgt voor het verkeer; wij zorgen dat een groter deel daarvan ook daadwerkelijk klant wordt."),
    ("Heb ik wel tijd om al die analyses door te nemen?", "Nauwelijks. Wij doen de analyse en het testen; jij krijgt korte, concrete updates — zoals de testtijdlijn die je bij elke case terugziet."),
]

OVER_ONS_STATS = [
    (20, "+", "Webshops geholpen met data-gedreven conversie-optimalisatie"),
    (5, "", "Nieuwe shops per maand, bewust — voor diepgang in plaats van volume"),
]

# Uitgebreide versie van de 4 stappen, voor de aparte Werkwijze-pagina.
WERKWIJZE_STEPS = [
    ("Audit", "search", "We starten met een technische en gedragsmatige audit van je webshop: heatmaps en sessieopnames laten zien wáár bezoekers vastlopen, GA4 laat zien wáár ze afhaken in de funnel, en een handmatige UX-review legt frictie bloot die data alleen niet altijd laat zien.", "Output: een lijst knelpunten, elk onderbouwd met data — geen onderbuikgevoel."),
    ("Hypothese & prioriteit", "bulb", "Elk knelpunt wordt een hypothese: welke aanpassing, welk mechanisme verklaart waarom die het gedrag zou veranderen, en wat verwachten we dat het oplevert. Hypotheses worden gewogen op verwachte impact, de zekerheid dat de aanpassing werkt, en de inspanning om 'm te bouwen — zodat we eerst testen wat het meeste oplevert tegen de minste moeite.", "Output: een geprioriteerde testbacklog, met de volgende test al vastgelegd voordat de huidige is afgerond."),
    ("A/B-test", "flask", "De aanpassing wordt tegen de huidige versie getest bij een representatief deel van je bezoekers, met tools als Nelio A/B Testing. We laten een test doorlopen tot het resultaat statistisch betrouwbaar is — niet tot het toevallig de goede kant op wijst.", "Output: een winnaar, verliezer, of 'geen significant verschil' — alle drie zijn een geldige uitkomst."),
    ("Implementatie & learning", "check", "Een bewezen winnaar voeren we structureel door, zelf of samen met je huidige webbouwer. Een verliezer laten we vallen, ongeacht hoe logisch hij vooraf klonk. Wat we leerden voeden we terug in de volgende hypothese — zo wordt elke test waardevol, ook de tests die niet 'wonnen'.", "Output: een doorgevoerde verandering en een testtijdlijn die groeit, zoals je die terugziet bij elke case."),
]
WERKWIJZE_PRIORITY = [
    ("Impact", "target", "Hoeveel omzet-effect verwachten we als de hypothese klopt? Een test op je productpagina's weegt zwaarder dan een test op een pagina die bijna niemand bezoekt."),
    ("Zekerheid", "shield", "Hoe onderbouwd is de hypothese? Data uit heatmaps, sessieopnames of eerdere tests geeft meer zekerheid dan een losse aanname."),
    ("Inspanning", "clock", "Hoeveel ontwikkeltijd kost de test? Een kleine aanpassing die veel oplevert gaat voor op een grote herbouw met een onzekere uitkomst."),
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
    robots_meta = "" if LIVE else '<meta name="robots" content="noindex,nofollow">\n'
    ga_attr = f' data-ga="{GA_ID}"' if GA_ID else ""
    cookie_link = '<a href="#" data-cookie-reset>Cookie-instellingen</a>' if GA_ID else ""
    jsonld = ""
    if path == "/":
        jsonld = '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "ProfessionalService", "name": "Boldframe",
            "url": SITE_URL.rstrip("/") + "/", "logo": SITE_URL.rstrip("/") + "/assets/img/logo-blue.png",
            "image": SITE_URL.rstrip("/") + "/assets/img/og.png",
            "description": "Conversie-optimalisatie met A/B-tests voor webshops.",
            "email": "roy@boldframe.nl", "telephone": "+31637617728",
            "address": {"@type": "PostalAddress", "streetAddress": "Zwarte Zee 98", "addressLocality": "Maassluis", "addressCountry": "NL"},
            "sameAs": ["https://www.linkedin.com/company/boldframenl/", "https://www.instagram.com/boldframe_nl", "https://www.facebook.com/people/Boldframe/61568444076737/"],
        }, ensure_ascii=False) + '</script>\n'
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
{robots_meta}<meta name="theme-color" content="#1800ad">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · Boldframe</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:locale" content="nl_NL">
<meta property="og:site_name" content="Boldframe">
<meta property="og:title" content="{title} · Boldframe">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE_URL.rstrip("/")}/assets/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
<link rel="icon" type="image/png" sizes="512x512" href="/assets/img/favicon-512.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=swap">
<link rel="stylesheet" href="/assets/css/style.css">
{jsonld}{extra_head}</head>
<body{ga_attr}>
<nav aria-label="Hoofdmenu">
<a class="logo" href="/"><img src="/assets/img/logo-blue.png" alt="Boldframe"></a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-menu" aria-label="Menu openen"><span></span><span></span><span></span></button>
<ul id="nav-menu">{nav_html}<li><a href="#afspraak"><strong>Contact</strong></a></li></ul>
</nav>
{body}
<div class="art-band" aria-hidden="true">{HERO_BAND}</div>
<section id="afspraak" class="wrap"><h2>Contact</h2>
<p class="lead">Bel of mail gerust direct, of kies hieronder zelf een moment.</p>
<div class="contact-direct"><a href="mailto:roy@boldframe.nl">{icon("mail")}roy@boldframe.nl</a><a href="tel:+31637617728">{icon("phone")}06-37617728</a></div>
<h3 class="cal-h">Of plan een gesprek van 30 minuten</h3>
<iframe src="https://calendly.com/roy-tc8/30min?embed_domain=boldframe.nl&amp;embed_type=Inline" frameborder="0" title="Selecteer een datum en tijd - Calendly"></iframe>
<p>Zie je de agenda niet? <a href="https://calendly.com/roy-tc8/30min" target="_blank" rel="noopener">Open hem in een nieuw tabblad</a>.</p></section>
{build_offer()}
<footer id="contact"><div class="wrap">
<img class="flogo" src="/assets/img/logo-white.png" alt="Boldframe">
<div class="fgrid">
<div><h3>Contact</h3><a href="mailto:roy@boldframe.nl">{icon("mail")}roy@boldframe.nl</a><br><a href="tel:+31637617728">{icon("phone")}06-37617728</a></div>
<div><h3>Kantoor</h3>Zwarte Zee 98<br>Maassluis</div>
<div><h3>Volg ons</h3><a href="https://www.linkedin.com/company/boldframenl/" target="_blank" rel="noopener">LinkedIn</a><br><a href="https://www.instagram.com/boldframe_nl" target="_blank" rel="noopener">Instagram</a><br><a href="https://www.facebook.com/people/Boldframe/61568444076737/" target="_blank" rel="noopener">Facebook</a></div>
<div><h3>Bedrijfsgegevens</h3>BTW NL002393881B08</div>
</div>
<div class="fine"><span>© 2026 Boldframe. Alle rechten voorbehouden.</span><a href="/privacy/">Privacyverklaring</a>{cookie_link}</div>
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


def test_card(t, i=0, order=0):
    dur = f'<span>{t["duration"]}</span>' if t.get("duration") else ""
    date = f'<span>Gestart {fmt_date(t["date"])}</span>' if t.get("date") else ""
    if t.get("started"):
        date = f'<span>Gestart {fmt_date(t["started"])}</span>'
    pinned = t["pinned"]
    cls = "item pinned" if pinned else "item"
    pressed = "true" if pinned else "false"
    label = "Losmaken" if pinned else "Vastpinnen"
    head = f'<div class="meta"><span class="tag {t["status"]}">{STATUS_LABEL[t["status"]]}</span>{date}{dur}<button class="pin" type="button" aria-pressed="{pressed}">{PIN_SVG}<span class="pin-label">{label}</span></button></div>'
    if t.get("observation"):
        why = f'<div class="why"><p><span class="lbl">Observatie</span>{t["observation"]}</p>'
        if t.get("principle"):
            why += f'<p><span class="lbl">Psychologisch principe</span>{t["principle"]}</p>'
        why += "</div>"
        hyp = f'<p class="hyp"><span class="lbl">Hypothese</span>{t["hyp"]}</p>'
        learn = f'<p><span class="lbl">Learning</span>{t["learn"]}</p>'
    else:
        why = ""
        hyp = f'<p class="hyp">Hypothese: {t["hyp"]}</p>'
        learn = f'<p>{t["learn"]}</p>'
    note = f'<p class="t-note">{t["note"]}</p>' if t.get("note") else ""
    nxt = f'<p><span class="lbl">Vervolgstap</span>{t["next"]}</p>' if t.get("next") else ""
    img = f'<img src="{t["img"]}" alt="{t["alt"]}" loading="lazy" width="1000" height="1000">'
    return f'<li class="{cls}" data-order="{order}" data-reveal style="--d:{i}">{head}<h3>{t["title"]}</h3>{why}{hyp}{metrics_html(t["metrics"])}{note}{learn}{nxt}{img}</li>'


def format_nl(n):
    return f"{int(n):,}".replace(",", ".")


def kpis_html(stats):
    cells = []
    for i, s in enumerate(stats):
        if s.get("count") is not None:
            attrs = f'data-count="{s["count"]}"'
            if s.get("prefix"):
                attrs += f' data-prefix="{s["prefix"]}"'
            if s.get("suffix"):
                attrs += f' data-suffix="{s["suffix"]}"'
            shown = s.get("prefix", "") + format_nl(s["count"]) + s.get("suffix", "")
            val = f'<b {attrs}>{shown}</b>'
        else:
            val = f'<b>{s["text"]}</b>'
        cells.append(f'<div data-reveal style="--d:{i}">{val}<span>{s["label"]}</span></div>')
    return '<section><div class="kpis">' + "".join(cells) + "</div></section>"


def phases_html(items):
    return "".join(
        f'''<li class="step-detail" data-reveal style="--d:{i}">
<div class="step-detail-head"><span class="num">{i+1}</span>{icon(k)}<h3>{t}</h3></div>
<p>{body}</p><p class="step-out"><strong>{out}</strong></p></li>'''
        for i, (t, k, body, out) in enumerate(items)
    )


def cards_html(items):
    return "".join(
        f'<div data-reveal style="--d:{i}">{icon(k)}<h3>{t}</h3><p>{d}</p></div>'
        for i, (t, k, d) in enumerate(items)
    )


def bars_html(rows):
    top = max(r[1] for r in rows)
    out = []
    for i, (label, val, shown, kind) in enumerate(rows):
        w = round(val / top * 100, 1)
        cls = "bar-row est" if kind == "est" else "bar-row"
        out.append(f'<li class="{cls}" data-reveal style="--d:{i};--w:{w}%"><span class="bar-label">{label}</span><span class="bar-track"><span class="bar-fill"></span></span><b class="bar-val">{shown}</b></li>')
    return "".join(out)


def table_html(head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    trs = []
    for i, r in enumerate(rows):
        tds = "".join(f'<td data-label="{head[j]}">{cell}</td>' for j, cell in enumerate(r))
        trs.append(f'<tr data-reveal style="--d:{i}">{tds}</tr>')
    return f'<table class="cmp"><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table>'


def tests_section(c, h2, lead):
    ordered = list(c["tests"])
    pinned = [(i, t) for i, t in enumerate(ordered) if t["pinned"]]
    rest = [(i, t) for i, t in enumerate(ordered) if not t["pinned"]]
    grp = f'<li class="grp">{PIN_SVG}Vastgepind</li>'
    if pinned:
        pinned_html = f'<div class="tl-pinned"><ul class="tl" style="margin-bottom:10px">{grp}{"".join(test_card(t, n, i) for n, (i, t) in enumerate(pinned))}</ul></div>'
    else:
        pinned_html = f'<div class="tl-pinned" hidden><ul class="tl" style="margin-bottom:10px">{grp}</ul></div>'
    rest_html = "".join(test_card(t, n, i) for n, (i, t) in enumerate(rest))
    return f'<section><h2 data-reveal>{h2}</h2><p class="lead" data-reveal>{lead}</p>{pinned_html}<div class="tl-rest"><ul class="tl">{rest_html}</ul></div></section>'


def render_block(b, c):
    t = b["type"]
    if t == "text":
        paras = "".join(f'<p class="lead" data-reveal style="max-width:66ch">{p}</p>' for p in b["paras"])
        return f'<section><h2 data-reveal>{b["h2"]}</h2>{paras}</section>'
    if t == "bars":
        return f'<section><h2 data-reveal>{b["h2"]}</h2><p class="lead" data-reveal>{b["lead"]}</p><ul class="bars">{bars_html(b["rows"])}</ul><p class="bar-note" data-reveal>{b["note"]}</p></section>'
    if t == "cards":
        return f'<section><h2 data-reveal>{b["h2"]}</h2><p class="lead" data-reveal>{b["lead"]}</p><div class="facts">{cards_html(b["items"])}</div></section>'
    if t == "phases":
        return f'<section><h2 data-reveal>{b["h2"]}</h2><p class="lead" data-reveal>{b["lead"]}</p><ul class="steps-detail">{phases_html(b["items"])}</ul></section>'
    if t == "table":
        return f'<section><h2 data-reveal>{b["h2"]}</h2><p class="lead" data-reveal>{b["lead"]}</p>{table_html(b["head"], b["rows"])}</section>'
    if t == "media":
        figs = "".join(
            f'<figure data-reveal style="--d:{i}"><img src="{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy"><figcaption>{cap}</figcaption></figure>'
            for i, (src, alt, cap, w, h) in enumerate(b["items"])
        )
        return f'<section><h2 data-reveal>{b["h2"]}</h2><p class="lead" data-reveal>{b["lead"]}</p><div class="media {b.get("cls", "")}">{figs}</div></section>'
    if t == "quote":
        q, n, r = b["quote"]
        return f'<section><h2 data-reveal>{b["h2"]}</h2><div class="quotes single"><figure data-reveal><blockquote>{q}</blockquote><figcaption><b>{n}</b>, {r}</figcaption></figure></div></section>'
    if t == "tests":
        return tests_section(c, b["h2"], b["lead"])
    if t == "cta":
        other = ""
        if b.get("other"):
            other = f' <a class="cta-other" href="{b["other"][0]}">{b["other"][1]}</a>'
        return f'<section><div class="cta-band" data-reveal><h2>{b["h2"]}</h2><p class="lead">{b["lead"]}</p><a class="btn" href="#afspraak">Claim jouw gratis website scan</a>{other}</div></section>'
    raise ValueError("onbekend blok: " + t)


def client_strip(slug, c):
    for name, f, w, h, href in CLIENT_LOGOS:
        if href == f"/cases/{slug}/":
            return f'<section class="client" data-reveal><img src="/assets/img/logos/{f}" alt="{name}" width="{round(w*1.3)}" height="{round(h*1.3)}"><p>Klant van Boldframe &middot; {c["eyebrow"].replace("Case · ", "")}</p></section>'
    return ""


def build_case(slug, c):
    if c.get("blocks"):
        eyebrow = f'<span class="meta">{c["eyebrow"]}</span>' if c.get("eyebrow") else ""
        headline = c.get("headline") or c["name"]
        kpis = kpis_html(c["stats"]) if c.get("stats") else ""
        blocks = "\n".join(render_block(b, c) for b in c["blocks"])
        body = f'''<a class="back" href="/cases/">← Alle cases</a>
<header class="hero" style="padding-top:32px">{HERO_BG}{eyebrow}<h1 class="case">{headline}</h1><p>{c['intro']}</p><img class="chero" src="{c['hero']}" alt="{c['name']} homepage" loading="lazy"></header>
{client_strip(slug, c)}
{kpis}
{blocks}'''
        return page(c["name"], c["sub"], f"/cases/{slug}/", body)
    # eenvoudige indeling (nog geen uitgewerkte verhaal-case)
    c = dict(c)
    c["tests"] = sorted(c["tests"], key=lambda t: t["date"], reverse=True)
    facts = ""
    if c["facts"]:
        fact_cells = "".join(f'<div data-reveal style="--d:{i}"><h3>{k}</h3><p>{v}</p></div>' for i, (k, v) in enumerate(c["facts"]))
        facts = f'<section><div class="facts">{fact_cells}</div></section>'
    body = f'''<a class="back" href="/cases/">← Alle cases</a>
<header class="hero" style="padding-top:32px">{HERO_BG}<h1 class="case">{c['name']}</h1><p>{c['intro']}</p><img class="chero" src="{c['hero']}" alt="{c['name']} homepage" loading="lazy"></header>
{facts}
{tests_section(c, "Testtijdlijn", "Elke test met hypothese, uitkomst en learning. Nieuwste bovenaan, vastgepinde tests eerst.")}'''
    return page(c["name"], c["sub"], f"/cases/{slug}/", body)


def build_cases_index():
    rows = "".join(
        f'<li data-reveal style="--d:{i}"><a class="row" href="/cases/{slug}/"><h3>{c["name"]}</h3><span>{c["sub"]}</span></a></li>'
        for i, (slug, c) in enumerate(CASES.items())
    ) + "".join(
        f'<li data-reveal style="--d:{i+len(CASES)}"><div class="row"><h3>{n}</h3><span>Case volgt</span></div></li>'
        for i, n in enumerate(CASES_COMING_SOON)
    )
    body = f'''<header class="hero">{HERO_BG}<h1>Cases.</h1><p>Open een case om te zien wat we testten, waarom, en wat het opleverde.</p></header>
<section><ul class="list">{rows}</ul></section>
{build_logo_wall()}'''
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
    elif tool == "duration":
        tool_html = '''<div class="tool"><h4>Tool: hoe lang moet jouw test duren?</h4><p class="tdesc">Indicatieve rekenhulp voor een A/B-test (tweezijdig, 80% power). Neem als meetwaarde bestellingen, add-to-carts of een bounce rate.</p>
<label for="dur-visitors">Bezoekers per maand (op de pagina\u2019s die je test)</label><input type="number" id="dur-visitors" min="0" value="30000">
<label for="dur-rate">Huidige waarde van je meetwaarde (%)</label><input type="number" id="dur-rate" min="0.1" max="99" step="0.1" value="2.5">
<label for="dur-mde">Minimaal effect dat je wilt aantonen (relatief, %)</label><input type="number" id="dur-mde" min="1" max="200" value="20">
<label for="dur-sig">Gewenste zekerheid</label><select id="dur-sig"><option value="1.645">90%</option><option value="1.96" selected>95%</option><option value="2.576">99%</option></select>
<label for="dur-var">Aantal versies (inclusief origineel)</label><select id="dur-var"><option value="2" selected>2</option><option value="3">3</option><option value="4">4</option></select>
<div class="tool-out" id="dur-out" aria-live="polite"></div></div>'''
    elif tool == "reach":
        tool_html = '''<div class="tool"><h4>Tool: schat je potentieel met meertaligheid</h4><p class="tdesc">Ruwe, indicatieve schatting op basis van sectorgemiddelden. Geen belofte, wel een startpunt voor het gesprek.</p><label for="rev-input">Huidige omzet per maand (€)</label><input type="number" id="rev-input" min="0" placeholder="10000"><div class="tool-out" id="rev-out">Vul je huidige omzet per maand in voor een indicatie.</div></div>'''
    else:
        tool_html = ""
    body = f'''<a class="back" href="/insights/">← Alle insights</a>
<header class="hero" style="padding-top:32px;padding-bottom:24px">{HERO_BG}<span class="meta">{fmt_date(x['date'])}</span><h1 class="case">{x['title']}</h1><p>{x['dek']}</p></header>
<section class="art">{"".join((f"<h2>{p[3:]}</h2>" if p.startswith("## ") else f"<p>{p}</p>") for p in x['body'])}{steps_html}{tool_html}</section>'''
    desc = x["dek"] if len(x["dek"]) <= 160 else x["dek"][:157].rsplit(" ", 1)[0] + "…"
    return page(x["title"], desc, f"/insights/{slug}/", body)


def build_insights_index():
    rows = "".join(
        f'<li data-reveal style="--d:{i}"><a class="row" href="/insights/{slug}/"><h3>{INSIGHTS[slug]["title"]}</h3><span>{fmt_date(INSIGHTS[slug]["date"])}</span></a></li>'
        for i, slug in enumerate(INSIGHT_ORDER)
    )
    body = f'''<header class="hero">{HERO_BG}<h1 style="font-size:clamp(36px,7vw,64px)">Insights.</h1><p>Wat we zien gebeuren in de markt, met steeds een tool erbij die je direct kunt gebruiken.</p></header>
<section class="art"><ul class="insight-list">{rows}</ul></section>'''
    return page("Insights", "Wat Boldframe ziet gebeuren in de markt, met een tool om direct mee aan de slag te gaan.", "/insights/", body)


def build_home():
    case_rows = "".join(
        f'<li data-reveal style="--d:{i}"><a class="row" href="/cases/{slug}/"><h3>{c["name"]}</h3><span>{c["sub"]}</span></a></li>'
        for i, (slug, c) in enumerate(CASES.items())
    ) + "".join(
        f'<li data-reveal style="--d:{i+len(CASES)}"><div class="row"><h3>{n}</h3><span>Case volgt</span></div></li>'
        for i, n in enumerate(CASES_COMING_SOON)
    )
    insight_rows = "".join(
        f'<li data-reveal style="--d:{i}"><a class="row" href="/insights/{slug}/"><h3>{INSIGHTS[slug]["title"]}</h3><span>{fmt_date(INSIGHTS[slug]["date"])}</span></a></li>'
        for i, slug in enumerate(INSIGHT_ORDER)
    )
    body = f'''<header class="hero hero-home">{HERO_ART_BIG}<h1>Van kliks naar klanten.</h1><p>Data-gedreven conversie-optimalisatie met A/B-tests voor webshops die meer omzet willen halen uit bezoekers die ze al hebben.</p><a class="btn" href="#afspraak">Claim jouw gratis website scan</a></header>
{build_logo_wall()}
<section><h2 data-reveal>Cases</h2><p class="lead" data-reveal>Open een case om te zien wat we testten, waarom, en wat het opleverde. <a href="/cases/">Alle cases →</a></p><ul class="list">{case_rows}</ul></section>
{build_testimonials()}
{build_branches_section()}
<section><h2 data-reveal>Insights</h2><p class="lead" data-reveal>Wat we zien gebeuren in de markt, met een tool om direct mee aan de slag te gaan. <a href="/insights/">Alle insights →</a></p><ul class="insight-list">{insight_rows}</ul></section>'''
    return page("Van kliks naar klanten", "Data-gedreven conversie-optimalisatie voor MKB-webshops. Boldframe dicht conversie-lekken op basis van A/B-tests, niet op onderbuikgevoel.", "/", body)


def build_stub(title, path):
    body = f'''<header class="hero"><h1 class="case">{title}</h1><p>Deze pagina is nog in opbouw. Neem gerust contact op als je hier specifieke content voor wilt.</p></header>'''
    return page(title, f"{title} — Boldframe", path, body)


def build_diensten():
    steps_html = "".join(
        f'<li data-reveal style="--d:{i}"><span class="num">{i+1}</span><div><h3>{icon(k)}{t}</h3><p>{d}</p></div></li>'
        for i, (t, k, d) in enumerate(DIENSTEN_STEPS)
    )
    challenges_html = "".join(
        f'<div data-reveal style="--d:{i}">{icon(k)}<h3>{t}</h3><p>{d}</p></div>'
        for i, (t, k, d) in enumerate(DIENSTEN_CHALLENGES)
    )
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in DIENSTEN_FAQ)
    body = f'''<header class="hero">{HERO_BG}<h1 class="case">Conversie-optimalisatie, geen giswerk.</h1><p>Je advertenties trekken bezoekers, maar als je landingspagina's en checkout ze niet vasthouden, betaal je voor verkeer dat nooit klant wordt. Wij herstellen die correlatie tussen advertentie en landingspagina met data-gedreven A/B-tests.</p></header>
<section><h2 data-reveal>Het Webshop Groei-Traject met uplift-garantie</h2><p class="lead" data-reveal>Meer rendement uit de bezoekers die je al hebt. Een hoge klikfrequentie is waardeloos als je checkout de verkoop blokkeert. Daarom nemen wij het risico: halen we binnen zes maanden niet minimaal 10% uplift, dan werken we gratis door totdat we het wel hebben aangetoond. Geen geld-terug-garantie, maar een traject dat doorgaat tot het resultaat er is.</p>
<div class="facts"><div data-reveal style="--d:0"><h3>Uplift-garantie</h3><p>Minimaal 10% uplift in zes maanden, anders werken we gratis door.</p></div><div data-reveal style="--d:1"><h3>Start</h3><p>Gratis website scan binnen 48 uur.</p></div><div data-reveal style="--d:2"><h3>Capaciteit</h3><p>Maximaal 5 nieuwe shops per maand, voor diepgang per klant.</p></div></div>
<p><a class="btn" href="#afspraak">Claim jouw gratis website scan</a></p></section>
{build_branches_section(id_attr="")}
<section><h2 data-reveal>Voor wie dit werkt</h2><p class="lead" data-reveal style="max-width:66ch">Wij werken met een doorlopend testprogramma: geen losse optimalisaties, maar een reeks onderbouwde experimenten die samen een strategie vormen. Dat werkt voor webshops met genoeg verkeer om betrouwbaar te testen, en die bereid zijn te leren van elke uitkomst, ook als een test verliest.</p></section>
<section><h2 data-reveal>Waar we conversie-lekken vinden</h2><p class="lead" data-reveal>Herkenbaar? Dit zijn de signalen waarmee webshopondernemers meestal bij ons aankloppen.</p>
<div class="facts">{challenges_html}</div></section>
<section><h2 data-reveal>Onze werkwijze</h2><p class="lead" data-reveal>Van vermoeden naar bewijs, in vier stappen — dezelfde stappen die je terugziet in elke testtijdlijn bij onze <a href="/cases/">cases</a>. <a href="/werkwijze/">Lees de volledige werkwijze →</a></p>
<ul class="steps">{steps_html}</ul></section>
<section><h2 data-reveal>Veelgestelde vragen</h2><div class="faq">{faq_html}</div></section>'''
    return page(
        "Diensten",
        "Data-gedreven conversie-optimalisatie voor MKB-webshops: het Webshop Groei-Traject met uplift-garantie van Boldframe.",
        "/diensten/",
        body,
    )


def build_werkwijze():
    steps_html = "".join(
        f'''<li class="step-detail" data-reveal style="--d:{i}">
<div class="step-detail-head"><span class="num">{i+1}</span>{icon(k)}<h3>{t}</h3></div>
<p>{body}</p><p class="step-out"><strong>{out}</strong></p></li>'''
        for i, (t, k, body, out) in enumerate(WERKWIJZE_STEPS)
    )
    priority_html = "".join(
        f'<div data-reveal style="--d:{i}">{icon(k)}<h3>{t}</h3><p>{d}</p></div>'
        for i, (t, k, d) in enumerate(WERKWIJZE_PRIORITY)
    )
    body = f'''<header class="hero">{HERO_BG}<h1 class="case">Van vermoeden naar bewijs.</h1><p>Dit is hoe een traject bij Boldframe er in de praktijk uitziet — dezelfde vier fases bij elke webshop, van de eerste audit tot de doorgevoerde winnaar.</p></header>
<section><h2 data-reveal>De vier fases</h2><p class="lead" data-reveal>Elke fase levert een concreet resultaat op voordat de volgende begint.</p>
<ul class="steps-detail">{steps_html}</ul></section>
<section><h2 data-reveal>Hoe we prioriteren</h2><p class="lead" data-reveal>Met meerdere knelpunten tegelijk is de vraag niet wát we testen, maar in welke volgorde. We wegen elke hypothese op drie punten.</p>
<div class="facts">{priority_html}</div></section>
<section><h2 data-reveal>Wat je kunt verwachten</h2><p class="lead" data-reveal>Korte lijnen, geen dikke rapporten. Na elke afgeronde test krijg je een update met de uitkomst, de learning, en wat we daarna gaan testen — terug te zien in de testtijdlijn van je eigen <a href="/cases/">case</a>. Blijft de afgesproken uplift uit? Dan werken we gratis door: lees de <a href="/diensten/">uplift-garantie</a>.</p>
<p><a class="btn" href="#afspraak">Claim jouw gratis website scan</a></p></section>'''
    return page(
        "Werkwijze",
        "Hoe een CRO-traject bij Boldframe werkt: audit, hypothese, A/B-test en implementatie, met prioritering op impact, zekerheid en inspanning.",
        "/werkwijze/",
        body,
    )


def build_over_ons():
    stats_html = "".join(
        f'<div data-reveal style="--d:{i}"><b data-count="{v}" data-suffix="{s}">{v}{s}</b><span>{l}</span></div>'
        for i, (v, s, l) in enumerate(OVER_ONS_STATS)
    )
    body = f'''<header class="hero">{HERO_BG}<h1 class="case">50% techniek, 50% gedrag.</h1><p>Conversie-optimalisatie zit precies tussen die twee in. Bij Boldframe combineren we ontwikkelaars die een test technisch correct bouwen met een strateeg die weet waaróm een bezoeker afhaakt.</p></header>
<section><h2 data-reveal>Onze visie</h2><p class="lead" data-reveal style="max-width:66ch">We geloven niet in giswerk of onderbuikgevoel. Elke aanpassing die we voorstellen is eerst een hypothese, dan een A/B-test tegen de huidige situatie, en pas daarna een implementatie — met een concreet omzet-effect als uitkomst. Precies zoals je in onze <a href="/cases/">testtijdlijnen</a> kunt teruglezen: ook de tests die niet werkten laten we zien, want ook dat is bewijs.</p>
<div class="stats">{stats_html}</div></section>
<section><div class="about"><img class="about-photo" src="/assets/img/roy.jpg" alt="Roy van Hees, oprichter van Boldframe" width="190" height="190" data-reveal><div><h2 data-reveal>Roy van Hees</h2>
<p class="lead" data-reveal style="max-width:66ch">Roy werkt al elf jaar in de e-commerce. Hij begon met het bouwen van webshops en richt zich inmiddels volledig op experimenttrajecten en conversie-optimalisatie met A/B-tests.</p>
<p class="lead" data-reveal style="max-width:66ch">Hij is gek op het uitpluizen van data en op het maken van meetbare impact voor webshops. Door de jaren heen bouwde hij een stevige basis: hij weet wat wel en niet werkt, en weet welke aanpassingen daadwerkelijk bijdragen aan meer omzet en meer winst.</p>
<p class="lead" data-reveal style="max-width:66ch">Roy is ervan overtuigd dat je met snel testen de concurrentie voorblijft. Zeker nu advertentiekosten stijgen en concurrenten zelf ook slimmer werken, is dat de enige manier.</p>
<p class="lead" data-reveal style="max-width:66ch">Roy is 28 en woont met zijn vrouw en twee zoontjes in Maassluis. <a href="mailto:roy@boldframe.nl">roy@boldframe.nl</a></p></div></div></section>
{build_testimonials()}
<section><h2 data-reveal>Hoe we werken</h2><p class="lead" data-reveal style="max-width:66ch">Audit, hypothese, A/B-test, implementatie — dezelfde vier stappen bij elke shop. Lees meer over onze <a href="/diensten/">werkwijze</a> of bekijk direct wat het heeft opgeleverd in onze <a href="/cases/">cases</a>.</p>
<p><a class="btn" href="#afspraak">Plan een kennismaking</a></p></section>'''
    return page(
        "Over ons",
        "Boldframe: conversie-optimalisatie op basis van data, niet onderbuikgevoel. 50% techniek, 50% gedrag.",
        "/over-ons/",
        body,
    )


def build_privacy():
    ga = ""
    if GA_ID:
        ga = "<h2>Statistieken</h2><p>Met jouw toestemming gebruiken we Google Analytics 4 om te meten hoe de website wordt gebruikt, zodat we hem kunnen verbeteren. Daarvoor worden cookies geplaatst en gegevens zoals je pagina\u2019s, apparaat en ongeveer locatie verwerkt door Google. Zonder toestemming laden we Google Analytics niet. Je kunt je keuze altijd wijzigen via \u2018Cookie-instellingen\u2019 onderaan de pagina.</p>"
    body = f'''<header class="hero">{HERO_BG}<h1 class="case">Privacyverklaring</h1><p>Hoe Boldframe omgaat met jouw gegevens. Laatst bijgewerkt: oktober 2026.</p></header>
<section class="art"><h2>Wie zijn wij</h2><p>Boldframe, Zwarte Zee 98, Maassluis. BTW-nummer NL002393881B08. Contact: <a href="mailto:roy@boldframe.nl">roy@boldframe.nl</a> of 06-37617728. Boldframe is verantwoordelijk voor de verwerking van de gegevens die in deze verklaring staan.</p>
<h2>Welke gegevens we verwerken</h2><p>Wij gebruiken op deze website geen contactformulieren. Je kunt ons mailen, bellen of een afspraak inplannen. Dan verwerken we alleen de gegevens die je zelf met ons deelt, zoals je naam, e-mailadres, telefoonnummer en de inhoud van je bericht. We gebruiken die om contact met je op te nemen en om een eventuele samenwerking voor te bereiden.</p>
<h2>Afspraak inplannen (Calendly)</h2><p>Voor het plannen van een gesprek gebruiken we Calendly. Als je een afspraak boekt, verwerkt Calendly je naam, e-mailadres en het gekozen tijdstip, volgens het eigen privacybeleid van Calendly.</p>
<h2>Lettertypen</h2><p>De website laadt het lettertype Archivo via Google Fonts. Daarbij ontvangt Google je IP-adres.</p>
{ga}
<h2>Bewaartermijn</h2><p>We bewaren gegevens niet langer dan nodig is voor het doel waarvoor je ze hebt gegeven, of zolang de wet dat vraagt.</p>
<h2>Je rechten</h2><p>Je kunt ons vragen om inzage in, correctie of verwijdering van je gegevens, of bezwaar maken tegen de verwerking. Stuur daarvoor een e-mail naar <a href="mailto:roy@boldframe.nl">roy@boldframe.nl</a>. Heb je een klacht? Dan kun je die indienen bij de Autoriteit Persoonsgegevens.</p></section>'''
    return page("Privacyverklaring", "Privacyverklaring van Boldframe: welke gegevens we verwerken en waarom.", "/privacy/", body)


def build_sitemap():
    base = SITE_URL.rstrip("/")
    paths = ["/", "/cases/", "/diensten/", "/werkwijze/", "/over-ons/", "/insights/"]
    paths += [f"/cases/{slug}/" for slug in CASES]
    paths += [f"/insights/{slug}/" for slug in INSIGHT_ORDER]
    urls = "".join(f"<url><loc>{base}{pth}</loc></url>" for pth in paths)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n'


def build_robots():
    if LIVE:
        return f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL.rstrip('/')}/sitemap.xml\n"
    return "User-agent: *\nDisallow: /\n\n# Stage-omgeving. Zet LIVE = True in build.py bij livegang.\n"


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
    write("/werkwijze/", build_werkwijze())
    write("/over-ons/", build_over_ons())
    write("/privacy/", build_privacy())
    for name, content in (("sitemap.xml", build_sitemap()), ("robots.txt", build_robots())):
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            f.write(content)
        print("wrote", name)

    # 404
    body = f'<header class="hero">{HERO_BG}<h1 class="case">Pagina niet gevonden</h1><p>Deze pagina bestaat niet (meer). <a href="/">Terug naar de homepage</a>.</p></header>'
    write("/404.html", page("Pagina niet gevonden", "404 — Boldframe", "/404.html", body))


if __name__ == "__main__":
    main()
