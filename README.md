# Sentora 2027 website

The site at https://sentorareloaded2027.github.io, served by GitHub Pages from the `main` branch.
The panel itself lives in [RusTus/sentora-core-2027](https://github.com/RusTus/sentora-core-2027)
and its installers in [RusTus/sentora-installers-2027](https://github.com/RusTus/sentora-installers-2027).

- `index.html`: the main page (no build step).
- Topic pages, one for each thing people search for: `/install/`, `/docker/`, `/windows/`,
  `/migrate/`, `/cpanel-alternative/`. They are made by `tools/build-pages.py` (their text is in
  it) with the main page's own style, menu and footer; change the text there and run
  `python3 tools/build-pages.py` from the top folder, then commit the pages it wrote.
- `sitemap.xml` lists every page for search engines; add a new page there too.
- Only tested facts go on the site.
- `google580fbb6ffa1f5907.html`: Google Search Console's ownership file (verified 2026-11-11, sitemap
  submitted). Keep it: Google checks it now and then, and removing it drops the verification.
