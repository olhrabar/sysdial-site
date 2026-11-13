# i18n contract — translate sysdial.app into one locale

You are translating the ENTIRE marketing site (`index.html` + `privacy.html`) into **{{LANG_NAME}}** (`{{LANG_CODE}}`, html lang attribute: `{{HTML_LANG}}`).

Source files to copy from (English, root of the repo): `index.html`, `privacy.html`.
Destination: create `{{LANG_CODE}}/index.html` and `{{LANG_CODE}}/privacy.html` in this repo (`/Users/ohrabar/SysDial_pet/sysdial-site/`). Do not touch any other file. Do not commit.

## 1. Structural changes every locale copy needs (mechanical, same for everyone)

- `<html lang="en">` → `<html lang="{{HTML_LANG}}">`
- Any asset path that currently has no leading `../` (`images/...`, `style.css`) → prefix with `../` (your files live one directory deeper than the English root). Anchor links (`#memory`, `#story`, etc.), `mailto:` links and the `privacy.html` footer link (same directory, no prefix needed) stay as they are.
- `<a class="site" href="/">` (logo, in both files) → `href="/{{LANG_CODE}}/"`.
- Add a `<link rel="canonical" href="https://sysdial.app/{{LANG_CODE}}/">` in `index.html`'s `<head>` (and `.../{{LANG_CODE}}/privacy.html` in `privacy.html`'s `<head>`) — the English root currently has no canonical tag either; add one there too if you notice it's missing, but that's a side detail, not your main job.
- `<meta property="og:url" content="https://sysdial.app/">` → `.../{{LANG_CODE}}/` (index.html only, it has og tags; privacy.html doesn't).
- Add `<meta property="og:locale" content="{{OG_LOCALE}}">` right after `og:url` (index.html only).
- Paste this **exact** hreflang block (same on every single locale page, do not customize it) right after the `<link rel="canonical">` line in **both** files — for `index.html` use block A, for `privacy.html` use block B:

**Block A (index.html — paste verbatim, all locales including this one):**
```html
<link rel="alternate" hreflang="en" href="https://sysdial.app/">
<link rel="alternate" hreflang="uk" href="https://sysdial.app/uk/">
<link rel="alternate" hreflang="de" href="https://sysdial.app/de/">
<link rel="alternate" hreflang="fr" href="https://sysdial.app/fr/">
<link rel="alternate" hreflang="es" href="https://sysdial.app/es/">
<link rel="alternate" hreflang="it" href="https://sysdial.app/it/">
<link rel="alternate" hreflang="nl" href="https://sysdial.app/nl/">
<link rel="alternate" hreflang="pt-BR" href="https://sysdial.app/pt/">
<link rel="alternate" hreflang="pl" href="https://sysdial.app/pl/">
<link rel="alternate" hreflang="cs" href="https://sysdial.app/cs/">
<link rel="alternate" hreflang="sk" href="https://sysdial.app/sk/">
<link rel="alternate" hreflang="hr" href="https://sysdial.app/hr/">
<link rel="alternate" hreflang="ro" href="https://sysdial.app/ro/">
<link rel="alternate" hreflang="x-default" href="https://sysdial.app/">
```

**Block B (privacy.html — paste verbatim, all locales including this one):**
```html
<link rel="alternate" hreflang="en" href="https://sysdial.app/privacy.html">
<link rel="alternate" hreflang="uk" href="https://sysdial.app/uk/privacy.html">
<link rel="alternate" hreflang="de" href="https://sysdial.app/de/privacy.html">
<link rel="alternate" hreflang="fr" href="https://sysdial.app/fr/privacy.html">
<link rel="alternate" hreflang="es" href="https://sysdial.app/es/privacy.html">
<link rel="alternate" hreflang="it" href="https://sysdial.app/it/privacy.html">
<link rel="alternate" hreflang="nl" href="https://sysdial.app/nl/privacy.html">
<link rel="alternate" hreflang="pt-BR" href="https://sysdial.app/pt/privacy.html">
<link rel="alternate" hreflang="pl" href="https://sysdial.app/pl/privacy.html">
<link rel="alternate" hreflang="cs" href="https://sysdial.app/cs/privacy.html">
<link rel="alternate" hreflang="sk" href="https://sysdial.app/sk/privacy.html">
<link rel="alternate" hreflang="hr" href="https://sysdial.app/hr/privacy.html">
<link rel="alternate" hreflang="ro" href="https://sysdial.app/ro/privacy.html">
<link rel="alternate" hreflang="x-default" href="https://sysdial.app/privacy.html">
```

- **privacy.html only** — the current English nav in `privacy.html` is stale (links to `/#features` and `/#pro`, sections that no longer exist). Fix it in your copy to match the real `index.html` nav structure, translated:
  ```html
  <nav aria-label="Sections">
    <a href="/{{LANG_CODE}}/#memory">{{T:Memory}}</a>
    <a href="/{{LANG_CODE}}/#plans">{{T:Plans}}</a>
    <a href="mailto:support@sysdial.app">{{T:Support}}</a>
  </nav>
  ```
- **privacy.html only** — right under the `<h1>`, add one italic/muted line (wrap it in `<p><em>…</em></p>` or similar, match the doc's existing style) saying this translation is provided for convenience and the English version at `https://sysdial.app/privacy.html` is the authoritative text. Translate that sentence into {{LANG_NAME}} too.
- **privacy.html only** — the footer currently has `<a href="/">SysDial</a>`; change to `<a href="/{{LANG_CODE}}/">SysDial</a>`.

### Language switcher
A language-switcher component will be added to the nav of every page (English root + all locales) in a **separate pass after all translations land** — you do not need to build it. Just leave the nav as a normal `<nav>` with your translated links; it will be edited in place afterward.

### Font — Cyrillic only
{{FONT_NOTE}}

## 2. What to translate vs. what to leave in English

Everything that is **live HTML/JS text** gets translated. Everything **baked into a screenshot image** (`images/app/sc-*.webp`, `moments-card.webp`, `alerts-card.webp`, `watch-card.webp`, and all the big `.webp` screenshots in `#memory`/`#themes`) stays in English — the app itself is English-only, so an English screenshot under translated captions is normal and expected. Do not touch any image file.

The same goes for two live-HTML stand-ins for app UI in the story scene: the context menu `<div class="sc-cm">` ("Quit “mDNSResponder”", "Force Quit “mDNSResponder”…", "Copy PID", "Copy Name") and the card `<div class="sc-mh">` ("Notable moments", "15:52–15:57", "5 min", "peak 93%", "mDNSResponder", "LOAD"). They replace screenshots of the app, so they stay in English in every language.

Keep these **as literal English/brand terms in every language**, do not translate them:
- The product name **SysDial**.
- **Free** / **Pro** as the two tier/pill labels (`<em class="tier free">Free</em>` / `<em class="tier pro">Pro</em>`) — these are short badge labels that appear ~10 times across the page (tri cards, `#story` captions, `#plans` table header). Keep them as the English words "Free" and "Pro" everywhere, unchanged — do not translate these two words, so they read as a consistent product-tier brand pair in every locale. This is a hard rule, not a style preference.
- The 9 theme proper names: **Amber, Lime, Ocean, Coral, Mint, Mono, Neon, Acid, Violet** — these match the actual (English-only) in-app Settings names, so translating them would create a mismatch between the site and the real app UI. Translate the sentence around them, not the names themselves (e.g. "SysDial Overview in the Amber theme" → translate everything except the word "Amber").
- `mDNSResponder` (a real macOS process name, in the `#story` banner) — universal, not translated.
- Email addresses, the mailto subject query string, and the website URL.
- The effective date value in privacy.html ("October 25, 2026") — reformat to your locale's normal date convention (day/month order, spacing) but keep it the same calendar date.

Everything else — headings, body copy, button labels, alt text, figcaptions, aria-labels, table cells, list items, tooltip `title=` attributes — gets translated. Below is every location, section by section, matching the current English `index.html`/`privacy.html`. Use it as a checklist; don't skip the `aria-label`/`alt`/`title` attributes, they matter for accessibility and SEO in every language too.

### `<head>` (index.html)
`<title>`, `<meta name="description">`, `<meta property="og:title">`, `<meta property="og:description">` — translate all four (write natural, idiomatic marketing copy for {{LANG_NAME}}, not a literal word-for-word translation).

### `<head>` (privacy.html)
`<title>`, `<meta name="description">`.

### Header / nav (both files, `<header class="menubar">`)
- `aria-label="Sections"`
- Nav link text: Memory, Menu bar, Themes, Plans, Privacy, Support (index.html has all six; privacy.html gets the fixed 3-item nav described above)
- `aria-label="Example of SysDial in the menu bar"`
- `title="Processor"`, `title="Memory"`, `title="Disk"`, `title="Internet latency"` (four tooltip `title=` attributes on the little menu-bar mockup icons)

### Hero (`<section class="hero">`)
- Eyebrow: "Watches · Warns · Follows · Remembers" (same order as the four `.hx-chip` buttons below it; since 12.11.2026 — use the same words as the chips)
- The `<h1 aria-label="...">` — translate the `aria-label` attribute (the full sentence) **and** the word-by-word `<span class="w">`/`<span class="w acc">` markup inside it. The English version reveals the sentence word by word, with the back half in an accent colour (the "twist": "SysDial already knows why" is highlighted). Keep that same idea — split your translated sentence into a sensible number of `<span class="w" style="--i:N">` chunks (don't force exactly 8 words if your language's syntax doesn't split that way) and put `class="w acc"` on the back portion that carries the "aha" reveal, matching the English structure's intent, not its literal word count. Keep `style="--i:N"` indices sequential (0, 1, 2…) over however many spans you end up with.
- Lede paragraph (long sentence about watching, following, warning, 30 days of history)
- CTA button text: "Download for Mac"
- Note: "Coming soon for macOS 14 and later." and the link text "Tell me when it's out" (leave the `mailto:...?subject=...` query string itself in English, just translate the visible link text)
- Fine print: "Watching and alerts are free. Following apps, history and insights are part of SysDial Pro." (remember: "Free"/"Pro" stay English if they appear as the tier words, but this sentence uses them as plain adjectives/nouns in prose, not as the pill badges — translate this sentence naturally, it's fine if the words "free"/"Pro" end up translated here since it's not the badge)
- Three proof-figure `alt` texts (long, descriptive — these describe what's in the screenshot for screen readers, translate fully)
- Four `.tri` cards: each has an `<h3>` title (Watches / Follows any app / Warns / Remembers — translate these, they're not brand terms) + a `<em class="tier free|pro">Free|Pro</em>` tier badge (leave as English "Free"/"Pro", see hard rule above) + a body paragraph (translate)

### `#story` section
- h2: "Your Mac slows down. Here is what happens next."
- Intro paragraph
- Inside the fake "Dashboard" mock app (all live text, not images): the word "Dashboard" itself (it's a generic placeholder app name, not SysDial's own UI — translate it as an ordinary word), "Live" / "Not responding" (two pill states), "Throughput", "Response time", "Capacity" (three card headers), "Queue", "Cache", "Workers" (three capacity-bar labels)
- The two notification banners (`.sc-ban`) — these ARE live text, not images: "DNS isn't responding" + "The network is up, but website names can't be resolved, so pages won't open. Since 15:54." / "High CPU load" + "CPU load has been above 50% for 1 min. Top process: mDNSResponder (93%)." (leave `mDNSResponder` untranslated, it's a real process name; the time "15:54" stays as-is, it's just a clock)
- Six step `aria-label`s on the dot buttons: "All quiet", "Then something goes wrong", "SysDial warns you", "One click opens the panel", "It already knows why", "One click, calm again"
- The matching six `<p><b>…</b><span>…</span></p>` captions below (title + body text for each of the same six steps — note two of them also carry a `<em class="tier pro">Pro</em>` badge, which stays English)
- "Replay" (button text)
- Footnote: "The CPU alert and the panel are free. Internet alerts, the window, quitting from the process list and History are part of SysDial Pro."

### `#memory` section
- h2: "It remembers, so you don't have to"
- Intro paragraph
- Seven steps, each with: a `<span class="t">` title (e.g. "Look back through 30 days"), a body paragraph, and an `alt=` text on its screenshot. **Each of the seven screenshots appears TWICE in the HTML** (once in the `<ol class="steps">` list, once again in the `<div class="stage">` block below it) — both copies of each `alt=` must get the identical translated text, keep them in sync.

### `#glance` section
- h2: "And right now, at a glance"
- Intro paragraph (mentions "Pro" and "free" in prose — translate naturally)
- `aria-label="What SysDial reads"`
- The 7-item tag list: Processor, Memory, GPU, Disk, Battery, Network speed, Data used — translate these as plain nouns (they're not in-app strings, just descriptive labels); since 2026-11-05 each tag shows only an icon, and the word lives twice per item — in `title="…"` and in `<span class="sr-only">…</span>` (translate both, keep them identical); keep the same translation choices for these words everywhere else they recur on the page (see the glossary note at the end of this file)
- Figure `alt=` text

### `#menubar` section (static HTML part)
- h2: "Your menu bar, your way"
- Intro paragraph
- Figure `alt=` text + `<figcaption>The same thing in a real menu bar.</figcaption>`
- Second figure `alt=` text (panel-settings screenshot)

### `#menubar` section (JS-generated part — read carefully, this is the risky part)
This section's visible UI is built by JavaScript from data arrays inside the big `<script>` block near the end of `index.html`. You must edit **only the human-readable string values**, never the surrounding code (ids, booleans, numbers, CSS classes, SVG paths). Two arrays to edit:

1. **`MODS` array** (`const MODS = [ ... ]`) — nine objects, each has an `id:` (do not touch) and a `name:` (translate this). The nine names are: `'CPU'`, `'Memory'`, `'GPU'`, `'Disk'`, `'Internet'`, `'Network'`, `'Data today'`, `'Battery'`, `'Alerts'`. These names render as tooltips, chip labels and aria-labels throughout the live demo — use the **same** translation for each as you use everywhere else on the page for that concept (CPU/Processor, Memory, Disk, Battery, Network, Internet, Alerts all recur elsewhere — stay consistent, see the glossary note).
2. **`SCRIPT` array** (`const SCRIPT = [ ... ]`) — seven objects, each has a `title:` and a `text:` (translate both), and some have an `a: [...]` tuple (do not touch — that's logic, not text). The seven title/text pairs: "Compact info" / "Live values sit right in the menu bar.", "Switch a module on" / "One tap, and GPU joins the bar.", "Switch one off" / "Tap again to hide it. Nothing else moves.", "Add the battery" / "Battery, Data today and Alerts work the same way.", "Drag to reorder" / "Hold ≡ and move a module. The bar follows right away.", "Or just the icon" / "Prefer it quiet? Show only the SysDial icon.", "Back to the numbers" / "Switch back whenever you like."

Also inside that same JS-built template (template-literal strings, still just text to translate, logic untouched):
- `aria-label="Menu bar preview"`
- Segmented control button labels: "Icon", "Compact info"
- `aria-label="Menu bar style"`
- Hint: "Press any button, try it yourself"
- Demo button (`#bldPlay`): "Watch how it works" (since 2026-11-05 the demo plays only on this button; the section is no longer scroll-pinned, so the intro no longer has a "Scroll to watch how it works." sentence)
- `aria-label="Menu bar modules"`
- "Now it is yours" + "You took over, so the demo stopped. Keep tapping, drag ≡, or switch the style. Scroll on whenever you are done."
- Hint paragraph: "Drag ≡ to change the order. From the keyboard, press Space to switch a module and Alt with an arrow key to move it."

### `#themes` section
- h2: "Nine themes, one tap"
- Intro paragraph
- Nine `alt=` texts on the theme screenshots: "SysDial Overview in the {Theme} theme" — translate the sentence, **keep the theme proper name in English** (see hard rule above: Amber/Lime/Ocean/Coral/Mint/Mono/Neon/Acid/Violet stay as-is)
- JS: the `T` array (`const T = [ ['amber', 'Amber', ...], ... ]`) — each inner array is `[id, name, color, color, color]`. Do **not** touch the `id` (first item) or the three hex colors; the `name` (second item, e.g. `'Amber'`) must also stay in English for the same reason (matches the real app's Settings screen) — so for this specific array, leave every string exactly as-is, there is nothing to translate here. (This is the one array in the whole file where you change nothing.)
- `role="radiogroup" aria-label="Theme"` → translate "Theme" to the generic word for it in your language
- Button (`#thNext`, cycles to the next theme): "Try the next theme" (since 2026-11-05; replaced the old "Tap any theme, try it yourself · scroll flips through all nine" hint — themes no longer change on scroll or by themselves)

### `#widgets` section
- h2: "On your desktop, and in your shortcuts"
- Intro paragraph
- Four list items (translate the full sentences; "Small widget"/"Medium widget"/"Shortcuts"/"Siri" are Apple/SysDial feature names — translate them if your language has an obviously natural equivalent commonly used on macOS, otherwise it's fine to leave them in English, your judgement)
- Fine print: "Right-click the desktop, choose Edit Widgets and search for SysDial. macOS refreshes widgets about every 15 minutes."
- `aria-label="SysDial widgets on a Mac desktop"`
- Two widget image `alt=` texts

### `.light` section
- `aria-label="Under 1 percent CPU in the background"` (on the `<svg>`)
- The `<text>` inside the SVG: "CPU in the background" (the `<1%`/percentage text next to it is written by JS as just digits/%, nothing to translate there)
- h2: "Light enough to forget it's running"
- Body paragraph

### `#plans` section
- h2: "Free, with Pro when you need more"
- Intro paragraph
- Table headers: "Feature", "Free", "Pro" — **"Free" and "Pro" here stay English** (column headers for the tier badges, same hard rule), translate "Feature"
- 14 table rows — each has a main `<td>` sentence and most have a `<small>` sub-line; translate both for all 14 rows. The ✓ and — symbols in the Free/Pro columns stay as-is, don't touch those cells.

### `#privacy` teaser section (on the homepage, not the policy page itself)
- h2: "Your data stays on your Mac"
- Paragraph (mentions public IP and internet-quality checks)
- Link text: "Read the privacy policy"

### Footer (both files)
- index.html: "© 2026 Oleksandr Hrabar. Requires macOS 14 Sonoma or later." (translate "Requires macOS 14 Sonoma or later", keep the name and year), footer nav link text "Privacy" (the email link itself stays as the literal email address, not translated)
- privacy.html: "© 2026 Oleksandr Hrabar" (keep as-is, nothing to translate) — just fix the logo link href as noted above

### `privacy.html` full policy body
Translate every heading and paragraph in the document: the `<h1>`, all `<h2>` headings, all body paragraphs, all `<li>` items, the full data-retention table (3 column headers + 5 rows × 3 cells), and the bold lead-in phrases inside list items (e.g. "**Public IP address.**", "**Direct edition:**" — keep the `<strong>` emphasis, translate the words). Do not translate: the product name SysDial, "Oleksandr Hrabar", "support@sysdial.app", "sysdial.app", "api.ipify.org", "1.1.1.1", "8.8.8.8", file paths like `~/Library/Application Support/app.sysdial.mac/`, or `app.sysdial.mac`. This is a legal/policy document — prioritize clarity and accuracy over flourish; if a legal term doesn't have a clean one-word equivalent in {{LANG_NAME}}, use the closest common phrase used in other software privacy policies in that language rather than inventing one.

### Added 11.11.2026 (already translated in all 12 languages by the tech lead; keep in sync if the English changes)
- `#glance`: the `.tags` icon pills were replaced by 7 `.gl-tile` buttons (name + one-line description of the panel card) and `aria-label` "Cards in the panel". Names reuse the glossary words for Processor, Memory, Battery, Disk, Data used; "Network" and "Alerts" use the words from `#plans`.
- `.light`: timeline `.lt` — heading "What SysDial reads, second by second", 4 row labels, lock band "Screen locked: nothing is read", axis unit `s` (`с` in `uk`), and 4 facts (`<b>` lead + sentence). "Settings → This App" stays in English (it is app UI).
- `#privacy`: diagram `.pv` — "Your Mac", 3 file descriptions (file names `history.json`/`watched.json`/`traffic.json` and "Application Support" stay in English), 3 destination descriptions (`api.ipify.org`, `1.1.1.1 · 8.8.8.8` stay as-is; "Your DNS server" is translated) and "Analytics, ads, accounts" / "None. Nothing else leaves your Mac."
- Source of the translations: `scratchpad/i18n_blocks.py` of that session (temporary); the pages themselves are the source of truth.

## 3. Consistency glossary (use the same translation every time these recur)

These technical nouns appear repeatedly across different sections (nav, hero tri-cards, `#glance` tags, `#menubar` MODS array, `#plans` table). Pick one natural translation per concept and reuse it everywhere on the page, so the site doesn't contradict itself with two different words for the same thing: Processor/CPU, Memory, GPU, Disk, Battery, Network, Network speed, Internet, Data used/Data today, Alerts, History, Storage, Settings, Overview, Processes, Theme(s), Widgets, Shortcuts.

## 4. After you're done — verification

1. Serve the repo locally (e.g. `python3 -m http.server` from the repo root) and open `/{{LANG_CODE}}/index.html` and `/{{LANG_CODE}}/privacy.html` in a browser (or headless Chrome + screenshot) at **1440px** and **390px** widths.
2. Check for text overflow in anything with a fixed/tight width: the nav bar (your translated nav labels are often longer than the English ones — "Memory", "Menu bar" etc. — make sure they still fit in a single row at 1440px; if German/Polish/etc. genuinely doesn't fit, that's useful information to flag back, don't silently truncate or shrink font-size yourself), the "Free"/"Pro" tier pills, the segmented-control buttons ("Icon"/"Compact info"), the `#plans` table's Free/Pro column headers, the theme swatch name labels.
3. Confirm every image still loads (paths are `../images/...`, not broken).
4. For `uk/` only: confirm the page visibly renders in a font that actually draws Cyrillic letters (not a generic fallback serif) — check the font note above.
5. Report back: list of files changed, and explicitly flag anything you weren't confident translating, anything that didn't fit in the UI at 1440/390px, and anything in the glossary where you made a judgement call.

Do not modify `style.css`, the English root `index.html`/`privacy.html`, or any file outside your own `{{LANG_CODE}}/` directory. Do not commit.

## Added 12.11.2026: hero scenes (MacBook)
The `.proof` cards and the `.tri-row` under the hero were replaced by the 3D MacBook scene (`[data-hx]`); `#story` was removed (its Dashboard, CPU and DNS banners now live in the hero's "Warns & fixes" scene).
- Reused from the page itself: chip names (split from the `.eyebrow`), captions for Watches / Follows / Remembers (former `.tri` texts), the Dashboard window strings, CPU and DNS banners, "The culprit, already found" and "Calm again, and saved to History" (former `#story`).
- New strings: memory banner title and body (Google Chrome Helper at 19.4 GB), tags "Live, in your menu bar", "Over the limit you set", "The app behind it, named", "One click, calm again", "Every spike, with the app behind it", the `sc-window` alt, the word "fixes" in the second chip, the combined "Warns & fixes" caption, `aria-label` "What SysDial does", Pause / Play.
- Stay English: "Top processes", "Quit", "Overview", "Internet quality" (app UI), "Free" / "Pro" badges.


## Added 12.11.2026: design-review fixes
- Eyebrow order changed to Watches · Warns · Follows · Remembers in all 13 pages (words unchanged, only the order; same words as the hero chips).
- **"Insights" must not share a word with "analytics" (the privacy section: "no analytics, ads, accounts").** `uk`: "Аналітика" -> "Підказки" / "Підказки пояснюють…" (plans row, hero note, `#memory` step 03, alt text of the Alerts screenshot); "Аналітика" stays in the privacy section. `ro`: "Analize/analiză" (Insights) -> "Indicii/indiciu" (privacy keeps "analize/Analiză"). Other languages use a different word already (de Einblicke, it approfondimenti, nl inzichten, pt insights, cs/sk/hr own words). **Close calls left unchanged, owner/native check welcome:** `fr` "analyses" (Insights) vs "analytique" (privacy); `es` "análisis" vs "analíticas"; `pl` "analizy" vs "analityka" — same root, different words. Suggested alternatives if wanted: fr "Explications", es "Explicaciones"/"Pistas", pl "Wskazówki".
- No new or changed visible strings otherwise (the `#glance` tile descriptions are now visually hidden at <=560 px but stay in the DOM for screen readers).

## Added 12.11.2026: header nav link "Panel" (`#glance`)
New nav item between "Memory" and "Menu bar" in all 13 `index.html` (not in `privacy.html`, whose reduced nav stays Memory · Plans · Support). Use the page's own word for the SysDial panel (the word already used in the `#glance` aria-label and copy):
en Panel · uk Панель · de Panel · fr Panneau · es Panel · it Pannello · nl Paneel · pt Painel · pl Panel · cs Panel · sk Panel · hr Panel · ro Panou.
Nav is hidden at max-width 1130px (was 1040px) so the longest labels (uk, nl, fr) fit without overlapping the menu-bar modules.

## Added 13.11.2026: `#glance` GPU tile (8th tile, `data-i="7"`)
Title "GPU" (not translated); description EN "Load, memory used, renderer and tiler." ("renderer" and "tiler" stay English, as in the app UI). "Load" and "memory used" reuse each page's Processor / Memory tile words:
uk Навантаження, використана пам’ять, renderer і tiler. · de Last, belegter Speicher, Renderer und Tiler. · fr Charge, mémoire utilisée, renderer et tiler. · es Carga, memoria usada, renderer y tiler. · it Carico, memoria usata, renderer e tiler. · nl Belasting, gebruikt geheugen, renderer en tiler. · pt Carga, memória usada, renderer e tiler. · pl Obciążenie, zajęta pamięć, renderer i tiler. · cs Zátěž, využitá paměť, renderer a tiler. · sk Záťaž, využitá pamäť, renderer a tiler. · hr Opterećenje, zauzeta memorija, renderer i tiler. · ro Încărcare, memorie folosită, renderer și tiler.
