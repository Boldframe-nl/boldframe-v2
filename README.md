# Boldframe — stage site

Statische, meerdere-pagina's website. Geen framework, geen build-stap nodig
om te bekijken — wel om te *genereren*: alle content (cases, insights)
staat in `build.py`, en dat script schrijft de losse `index.html`-bestanden.

## Bewerken

Bewerk **niet** de gegenereerde `*/index.html`-bestanden direct — je
wijzigingen verdwijnen bij de volgende build. Pas in plaats daarvan
`build.py` aan (de `CASES`- en `INSIGHTS`-dictionaries bovenaan) en run:

```bash
python3 build.py
```

Dit regenereert alle pagina's op basis van de data in het script.

## Lokaal bekijken

```bash
python3 -m http.server 8000
```

en open <http://localhost:8000>.

## Structuur

```
index.html              Homepage
cases/                   Case-overzicht + losse case-pagina's
insights/                Insight-overzicht + losse insight-pagina's (met tools)
diensten/, over-ons/     Placeholder-pagina's, nog in te vullen
assets/css/style.css     Alle styling
assets/js/site.js        Vastpinnen, kopieer-knoppen, insight-tools
assets/img/              Logo, case-hero's, testscreenshots
build.py                 Generator — enige bron van waarheid voor de content
netlify.toml             Netlify build-config (draait build.py bij elke deploy)
robots.txt               Blokkeert indexering — dit is de stage-omgeving
```

## Deployen naar Netlify via GitHub

1. Maak een lege GitHub-repository aan (bijv. `boldframe-site`).
2. Push deze map:
   ```bash
   git init
   git add .
   git commit -m "Eerste versie van de Boldframe stage site"
   git branch -M main
   git remote add origin git@github.com:<jouw-account>/boldframe-site.git
   git push -u origin main
   ```
3. Log in op [Netlify](https://app.netlify.com) → **Add new site → Import an
   existing project** → kies GitHub → selecteer de repository.
4. Build command: `python3 build.py` (staat al in `netlify.toml`, hoeft niet
   opnieuw ingevuld). Publish directory: `.` (ook al ingesteld).
5. Onder **Domain settings** → voeg `stage.boldframe.nl` toe als custom
   domain, en maak bij je DNS-beheer de CNAME aan die Netlify aangeeft.

Elke push naar `main` bouwt en publiceert automatisch opnieuw.

## Nog te doen

- `diensten/` en `over-ons/` zijn placeholders — content volgt.
- `robots.txt` blokkeert indexering bewust; verwijder dit zodra de site
  op het definitieve domein staat.
- Logo staat nu als PNG (`assets/img/logo-*.png`); een SVG-versie geeft
  scherpere weergave op alle schermdichtheden.
