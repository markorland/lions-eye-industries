# Lions Eye Industries

A one-page corporate site for a fictional multinational, deployed with GitHub Pages.
Plain static HTML and CSS — no build step, no dependencies.

```
index.html                 the whole site
figures.config.js          the group figures — the one file you edit routinely
404.html                   deadpan not-found page
assets/css/site.css        all styles (CSS custom properties at the top)
assets/img/logo.svg        eye device / favicon
assets/img/logo-email.png  the same logo for email signatures
assets/signatures.html     the three signatures, rendered for copying
tools/make-logo.py         redraws logo-email.png; no dependencies
tools/make-signatures.py   rewrites assets/signatures.html
CNAME                      custom domain for GitHub Pages
```

## Moving the numbers

Open `figures.config.js` and change them. That is the whole procedure:

```js
window.LEI_FIGURES = {
  figures: [
    { label: 'Jurisdictions of operation', value: 41, key: 'jurisdictions' },
    { label: 'Personnel under direction',  value: 68400 },
    { label: 'Facilities & installations',  value: 212 },
    { label: 'Assets under direction',     value: '94.6', unit: 'B USD' }
  ]
};
```

A numeric `value` gets thousands separators automatically (`68400` → `68,400`); a string is
printed verbatim, which is how `94.6` keeps its decimal. `unit` is optional and renders in gold
beside the number. Entries can be added or removed — the grid reflows, though four or five tiles
read best alongside the fixed "Year established" one.

The reporting date above the band is **computed**, not configured. It is the quarter end of the
period the current group bulletin reports on, so the date and the bulletin numeral always advance
together — in the final month of each quarter the numeral ticks up and the date moves to that
quarter's end (September 2026 → bulletin `CCCXIX`, "as at 30 September 2026"). Uncomment `asAt` in
the config only if you want to pin it to some other date.

The hero line at the top of the page ("Established 1947 · Operating in 41 jurisdictions") quotes
the jurisdiction count, so that figure carries `key: 'jurisdictions'` and the line follows it
automatically. No other prose on the page cites a figure.

"Year established 1947" is deliberately **not** in the config — it is hardcoded in `index.html`,
because it does not change. Everything else lives *only* in the config: there is no second copy in
the markup to keep in step. The figures are therefore rendered by JavaScript, and with scripts
disabled the band degrades to the single "Year established" tile, the hero line reads just
"Established 1947", and the reporting date is omitted. Nothing stale is ever shown.

## Local preview

```sh
python3 -m http.server 8000
# then open http://localhost:8000
```

## Deploy

1. Push to `main`.
2. Repo → **Settings → Pages** → Source: **Deploy from a branch**, Branch: `main`, folder: `/ (root)`.
3. `CNAME` holds the custom domain, `lionseyeindustries.com`. GitHub manages this file when you
   set the domain in the Pages UI, so edit it there rather than here.

### DNS

The site is served from the apex domain, which needs `A` and `AAAA` records rather than a `CNAME`.
At the registrar for `lionseyeindustries.com`:

| Type   | Name  | Value                   |
| ------ | ----- | ----------------------- |
| A      | `@`   | `185.199.108.153`       |
| A      | `@`   | `185.199.109.153`       |
| A      | `@`   | `185.199.110.153`       |
| A      | `@`   | `185.199.111.153`       |
| AAAA   | `@`   | `2606:50c0:8000::153`   |
| AAAA   | `@`   | `2606:50c0:8001::153`   |
| AAAA   | `@`   | `2606:50c0:8002::153`   |
| AAAA   | `@`   | `2606:50c0:8003::153`   |
| CNAME  | `www` | `markorland.github.io.` |

The `www` record is optional but worth adding — GitHub then redirects `www.lionseyeindustries.com`
to the apex automatically, so the address works either way.

Once DNS resolves, tick **Enforce HTTPS** in Settings → Pages. The certificate can take a few
minutes to issue, and the tick box stays greyed out until it has.

## Editing

Copy lives directly in `index.html` — sector cards are a repeated `<article class="card">`
block, group figures are the `<dl class="stats">` list. Colours and type are set once in
`:root` at the top of `site.css`.

The group bulletin numeral in the status strip is likewise computed: bulletin **I** was
issued in March 1947 and one has been issued every quarter since, in the final month of the
quarter it covers, so the numeral advances by one per quarter and never resets (the hundredth,
**C**, was December 1971; **CCCXIX** is the third quarter of 2026). The numeral in the markup
is a static fallback for the no-JavaScript case — it will drift, so refresh it if you ever
care. Hovering the numeral shows the arabic number and the quarter.

## Replying to mail

The three addresses on the page — `enquiries@`, `disclosure@`, `engagements@` — each answer in a
different register: the Office of the Secretary is courteous and useless, Group Disclosure is cold
and confirms nothing, and the Engagements Desk wants the business but demands credentials first.

`.claude/skills/lei-correspondence/SKILL.md` holds the house style, the three voices, worked
examples, and the reference-number format. Paste an inbound message into Claude Code, say which
address it arrived at, and it will draft the reply. It drafts only — nothing is sent.

It also carries a list of cases where it breaks character and answers plainly instead: anyone
acting on a belief that the company is real in a way that could cost them something, legal or
official process, apparent minors or distress, and anyone who asks outright whether the company
exists.

### Signatures

`assets/signatures.html` renders a signature for each mailbox, each signed by its desk rather
than by a person. Open it, select a signature inside its dashed box, and paste the rendered block
into the mailbox settings — Gmail's signature editor has no HTML view, so pasting source would
show the markup as text. The page is unlinked and `noindex`.

The logo in them loads from `lionseyeindustries.com/assets/img/logo-email.png`, so images appear
only once the domain resolves. It is a PNG rather than the site's SVG because almost no mail
client renders SVG; `tools/make-logo.py` redraws it if the size or colour ever needs to change.

The three signatures differ only in the desk name and their two fine-print lines, so edit
`tools/make-signatures.py` and re-run it rather than changing the generated HTML three times.
Neither signature carries its own email address — it is already in the From header.
