# INFA ELITE website

Source for **infaelite.com**: the INFA ELITE home page plus service pages for Shopify development, Shopify store design and redesign, WordPress and WooCommerce development, a privacy policy and a 404 page.

The site is static HTML, CSS and JavaScript. `build.py` assembles it from `src/` into `dist/`, and a GitHub Actions workflow publishes `dist/` to GitHub Pages on every push to `main`.

## Project layout

| Path | What it holds |
| --- | --- |
| `src/00-meta.html` | Home page `<head>`: title, description, Open Graph, structured data |
| `src/01-head.html` | The stylesheet (published as `assets/site.css`) |
| `src/02-body.html` | Home page markup, including the shared header, menu and footer |
| `src/03-script.html` | Animation libraries (jsDelivr) and the site script (published as `assets/site.js`) |
| `src/pages/*.html` | Other pages. The comment at the top of each file sets its address, title, description and breadcrumb |
| `src/pages/pages.css` | Styles for the service, policy and 404 pages and the project review slot |
| `assets/` | Images and the display font |
| `brand/` | Official INFA ELITE logo and logo mark, used unmodified |
| `static/` | `og-image.jpg` and the logo file referenced by structured data |
| `viz/` | Generators for the animated illustrations (they rewrite marked blocks in `src/`) |
| `build.py` | The build. Business details (email, phone, registration, Fiverr figures) live in `BIZ` at the top |

## Build locally

```bash
python3 -m pip install -r requirements.txt
npm ci
python3 build.py dist            # production site in dist/
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000. `python3 build.py out/index.html` builds a single self-contained home page for quick previews.

## Deploy with GitHub Pages

1. Push this repository to GitHub (branch `main`).
2. In the repository: **Settings > Pages > Build and deployment > Source: GitHub Actions**.
3. The **Deploy site to GitHub Pages** workflow runs on every push to `main` (or from the Actions tab with *Run workflow*). When it finishes, the site is live at the address shown in the workflow run.

Until the custom domain is set, the site lives at `https://<account>.github.io/<repository>/`. Every page uses relative links, so it works there too; only the 404 page expects to sit at the domain root.

## Custom domain: infaelite.com

Add the domain in GitHub first, then at the DNS provider. GitHub recommends verifying the domain for the account first (**Settings > Pages > Add a domain**) to prevent takeovers.

1. **Settings > Pages > Custom domain**: enter `infaelite.com` and save. (With Actions deployments no `CNAME` file is needed.)
2. At the DNS provider for infaelite.com, remove any existing A, AAAA or CNAME records for `@` and `www` that point elsewhere, then add:

| Type | Host | Value |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| AAAA | @ | 2606:50c0:8000::153 |
| AAAA | @ | 2606:50c0:8001::153 |
| AAAA | @ | 2606:50c0:8002::153 |
| AAAA | @ | 2606:50c0:8003::153 |
| CNAME | www | `<account>.github.io` |

3. Wait for the DNS check in **Settings > Pages** to pass (DNS changes can take up to 24 hours), then tick **Enforce HTTPS** once GitHub has issued the certificate.
4. Check: `dig infaelite.com +noall +answer` lists the four A records, and `https://infaelite.com` and `https://www.infaelite.com` both load the site over HTTPS.

The canonical URLs, sitemap and structured data already use `https://infaelite.com/` (`SITE` in `build.py`).

## Content notes

- The contact form serves two intents, a free consultation and a project brief. Links choose one with `data-intent` on the home page, or `?intent=consultation|project&service=...#contact` from other pages; `?project=<name>#work` opens a project popup.
- The form has no server behind it. It opens the visitor's email app with a pre-filled message addressed to the email in `BIZ`, and says so on the page; no consultation is booked until you confirm one by reply. Connecting a form service or a booking calendar is a separate decision.
- Each project popup ends with the client's review, quoted word for word as supplied, above the project call to action.
- The privacy policy describes the site as built (no cookies, no analytics, third-party fonts, scripts and photos). Update it if analytics, a form service or other tracking is added.
