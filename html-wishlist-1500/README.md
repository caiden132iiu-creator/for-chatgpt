# Quality HTML wishlist — 1,500 pages

Every requested line is represented: **89 descriptions, 1,500 complete HTML documents, and 1,500 paired description files**. Counts follow the individual `description | Xcount` lines. Those lines sum to exactly 1,500; the interactive category has 235 pages, correcting the summary's 230.

## Files

- `pages/<category>/<id>.html`: a complete document with the exact requested Tailwind 2.2.19 CDN link.
- `pages/<category>/<id>.txt`: its description, brand, location, palette, and layout direction.
- `all_1500_pages.txt`: every description and HTML document in one UTF-8 text file, separated by category headings and long `=` / `-` dividers. It is a text compilation, not one executable HTML document.
- `manifest.jsonl`: one record per page, including the original requested description, expanded description, paths, palette, layout, topic, and HTML SHA-256.
- `manifest.csv`: a spreadsheet-friendly inventory.
- `wishlist_catalog.json`: the 89 base descriptions and exact requested counts.
- `BROWSE.md`: one example link for each requested topic.
- `assets/photos/`: the 23 small, bundled photographic assets. Keep this directory next to `pages` when extracting.
- `preview.jpg`: twelve rendered examples spanning all eight shell layouts.
- `qa_*.json`: the actual validation reports.
- `builder/`: deterministic generator and validation scripts.

## Open and use

Extract the whole ZIP before opening an HTML file. The documents use the requested Tailwind CDN stylesheet; images load from the bundled local assets. An exact copy of the pinned stylesheet is included under `assets/` for renderers that intercept CDN requests or otherwise supply CSS locally. There are no external JavaScript libraries in the generated pages.

For training, pair the `.txt` and `.html` files by basename, or read the paths and descriptions from `manifest.jsonl`. Avoid feeding the long category and file separators from the combined text file as part of the target HTML.

## Coverage

| Category | Pages |
| --- | ---: |
| Pricing | 200 |
| Tables | 150 |
| Forms | 170 |
| Grids | 240 |
| Dashboards | 145 |
| Interactive | 235 |
| Unusual | 150 |
| Colours | 90 |
| Multisection | 120 |
| **Total** | **1,500** |

All organizations, people assigned to portraits, testimonials, products, property listings, mission programs, and dashboard records are illustrative. The pages contain substantive domain content, not placeholder paragraphs. Weather and volcano observations are explicitly simulated. Photographs are representational, not portraits of the named fictional staff.

## Variation

Eight structural shells combine with component arrangements, sixteen base palettes, forced palettes for the color requests, varied brands, copy, data, prices, and illustrations. There are 1,040 distinct DOM-and-class signatures and no identical HTML or visible-text hashes. Related examples intentionally share some components and conventions; these are generated variations, not 1,500 independently hand-designed websites.

The median page contains 127 elements. The collection contains 425 actual semantic tables, 1,000 forms, and 1,200 pages with short inline JavaScript. The longest script is 4,395 characters, including inline message/track data.

Keep variants from the same base description together when creating training/evaluation splits; `split_group` is provided for that purpose. Overlap at the component level is also present. Repetition weights and tokenization are decisions for your training pipeline; JavaScript and inline SVG tokens need to be supported before using those targets.

## Working interactions

All 16 requested interactive types are implemented, covering all 235 interactive pages. Extra working examples include bakery quantity/total controls, project-stage moves, inbox filtering, profile follow state, and a browser-synthesized music player.

Forms use browser validation and show a local review summary. They do not submit to a server, authenticate an account, make a reservation, subscribe an address, or charge a payment. Passwords and payment credentials are excluded from those summaries. Use sample details in checkout examples. Timers use explicit future UTC dates, clamp at zero, and show a launch state after expiry. Games include reset/retry behavior; modal and tab examples include keyboard behavior.

## Validation performed

- All 1,500 documents: exact topic counts, HTML boundaries, required Tailwind link, unique IDs, internal anchor targets, local image files, labels, table structure, feature requirements, and substantive text.
- All 1,200 inline scripts: syntax checked with Node.js.
- All 1,500 pages: rendered in Chromium at 1440 × 1000 and 390 × 844; no document-level horizontal overflow, broken photographs, or JavaScript runtime errors found.
- 315 pages: real browser actions tested, including **every interactive page**, all bakery order pages, and the interactive app dashboards.
- 55 representative forms: filled and submitted through browser controls, including file upload, invalid date ordering, and credential redaction checks.
- 89 pages: one varied example of every requested topic checked with axe-core 4.10.3 using WCAG 2/2.1 A/AA rule tags; no automated violations reported. This is not a full manual accessibility audit; any checks requiring review remain listed in the report.
- Regeneration: a clean rebuild reproduced all 1,500 HTML hashes, the manifest, the catalog, and the complete combined text byte for byte.

Browser tests used the exact cached Tailwind stylesheet to avoid CDN availability affecting results. They did not contact external services or test real backend behavior. These checks demonstrate the stated behavior, not a guarantee of training performance.

## Regenerate

From the extracted collection directory, with Python 3.12 or later:

```sh
python3 builder/build.py
```

The generator uses the bundled wishlist and photographs. No network request or third-party Python package is needed to regenerate the HTML. The optional `fetch_photos.py` can refresh the photographic thumbnails and requires Pillow and network access.

Validation scripts additionally need Node.js, lxml, Playwright, Pillow, and Chromium at `/usr/bin/chromium` (adjust the script path for another installation). To repeat the checks:

```sh
python3 builder/validate_static.py
node builder/check_js.cjs
python3 builder/validate_browser.py --mobile-all
python3 builder/validate_accessibility.py
```

## Asset sources

Original text, layouts, scripts, and inline SVG illustrations were generated for this request. Bundled photographs are resized copies from the public Start Bootstrap source repositories. Exact per-file origins are recorded in `assets/photo_sources.json`; the source project's README and license links are retained in `assets/photo_source_README.md`. That README licenses source code; it is not a separate certification of rights to each photograph. Consult the original asset terms for your intended training or redistribution use.

Tailwind CSS 2.2.19 is MIT licensed; its notice is in `assets/TAILWIND_LICENSE.txt`. The optional accessibility checker in `builder/axe.min.js` retains its Deque copyright and Mozilla Public License 2.0 notice. None of that checker code is included in the generated HTML.
