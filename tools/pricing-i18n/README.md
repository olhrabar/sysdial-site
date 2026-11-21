# pricing-i18n

Generates the 13 pricing pages (`pricing.html` and `{sk,pl,it,cs,ro,pt,uk,hr,nl,de,fr,es}/pricing.html`)
from one template plus per-language strings. Plain Python 3, no dependencies.

    python3 tools/pricing-i18n/build.py           # regenerate the 13 files (overwrites them)
    python3 tools/pricing-i18n/build.py --check   # regenerate to a temp folder, exit 1 if any page differs

**It overwrites the 13 pricing.html files.** Never edit those by hand: put the change in
`template.html` (markup, scripts, layout) or `strings/<lang>.py` (text), then rebuild.

## Files
- `template.html`: the English page with `{{key}}` placeholders where text is translatable.
  The JS price dictionary (`const D = {...}`) uses the same keys; apostrophes in those values are escaped automatically.
- `strings/en.py`: English value of every key, plus `FEATURE_TABLE` (the English Free/Pro table).
- `strings/<lang>.py`: translation of every key for that language (`L = dict(...)`).
- `build.py`: fills the template, then applies the locale wiring: `lang`, canonical, hreflang, `../` asset paths, logo/nav links,
  language switcher (stays on pricing), links to the English legal pages with " (EN)".

## Reused from other pages (do not translate here)
For each language the build reads `{lang}/index.html` and `{lang}/privacy.html`: the Free/Pro feature table
(so features always match the homepage), the "Tell me when it's out" label, the "Requires macOS 14..." line,
nav labels and the footer/Privacy labels. Change those on the homepage or privacy page, then rebuild.
Two derived defaults: the "All prices" column and row labels reuse the toggle and card labels, and the "Prices in US dollars"
fine print reuses `usd_note`.

## Add or change a string
1. Edit the text in `template.html` and replace it with `{{newkey}}` (or just edit the English text in `strings/en.py`).
2. Add `newkey` to `strings/en.py` and to every `strings/<lang>.py`. The build fails with a list of missing keys otherwise.
3. Rebuild, then `--check`.

## Add a language
1. Add `strings/<code>.py` with every key (copy `strings/de.py` as a start).
2. Add the language to `LANGS` in `build.py` (code, native name, html lang), create `<code>/index.html` and `<code>/privacy.html` first (the build reads them).
3. Add the new language to the hreflang block in the other pages and to `sitemap.xml` (the build only writes pricing pages).

Prices, the currency and product names (Pro, Free, Direct, App Store, Paddle) stay in English in every language.
