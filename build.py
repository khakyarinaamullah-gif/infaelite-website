#!/usr/bin/env python3
"""Build the INFA ELITE website.

  python3 build.py dist/             production site: one folder per page, shared CSS/JS/images (GitHub Pages ready)
  python3 build.py out/index.html    single self-contained home page with every asset inlined (previews, test suites)

The production build needs `npm ci` first: it takes the Manrope font files, GSAP, ScrollTrigger and Lenis
from node_modules and serves them from the site itself, and it minifies CSS and JS with esbuild.
Set SITE_URL to build for another address (the GitHub Actions workflow passes the Pages address).

Sources: src/00-meta.html, 01-head.html (the stylesheet), 02-body.html, 03-script.html and src/pages/*.html.
Tokens: {{asset:file}} {{img|...}} {{ic:name}} {{logo}} {{mark}} {{favicon}} {{swash}} {{stars}} {{root}} {{site}}
and the business details in BIZ below.
"""
import re, pathlib, sys, json, html, datetime, base64, io, shutil, os, subprocess
from PIL import Image

root = pathlib.Path(__file__).parent
# The live address of the site: canonical URLs, Open Graph, structured data, robots.txt and sitemap.xml use it.
# The deploy workflow passes the address GitHub Pages actually serves (the custom domain once it is connected,
# the github.io project address until then), so every absolute URL points at a page that answers.
SITE = os.environ.get('SITE_URL', '').strip() or 'https://infaelite.com/'
SITE = SITE.rstrip('/') + '/'
# Google Tag Manager container (Tag Manager sends the events on to GA4, measurement ID G-1XS0JDWF5M).
GTM_ID = 'GTM-T8SR49TW'
# Search Console ownership tag for the github.io property. Keep it: removing it un-verifies the property.
GSC_VERIFY = '2ykQ3kCeqvnUFkXIOyi57XElIFzcvBtiZyMC7p91g-Q'
# Date the page content last changed: sitemap lastmod and dateModified in the structured data.
LASTMOD = '2026-11-22'

# Business details exactly as published on the previous INFA ELITE site (a5qux0-6r.myshopify.com).
BIZ = {
    'email': 'inaamullahkhakyar3@gmail.com',
    'phone': '+974 3026 6940',
    'tel': '+97430266940',
    'legal': 'Infa Elite Web for Services',
    'cr': '248448',
    'address-short': 'Building 194, Floor 1, Zone 26, Al Najma, Doha, Qatar',
    'linkedin': 'https://www.linkedin.com/company/145286204/',
    # Fiverr profile linked from the previous site: 4.9 from 1,405 reviews when checked on 21 November 2026.
    'fiverr': 'https://www.fiverr.com/fareedali90',
    'rating': '4.9',
    'reviews': '1,400+',
}
UPDATED = '22 November 2026'

LUCIDE = {'storefront': 'store', 'layout': 'layout-template', 'brackets-curly': 'braces', 'pen-nib': 'pen-tool',
          'chart-line-up': 'trending-up', 'cube': 'box', 'lightning': 'zap', 'magnifying-glass': 'search',
          'devices': 'monitor-smartphone', 'eye': 'scan-eye', 'code': 'code-xml', 'tree-structure': 'workflow'}


def ic(m):
    name = LUCIDE.get(m.group(1), m.group(1))
    raw = (root / 'node_modules/lucide-static/icons' / f'{name}.svg').read_text()
    inner = re.search(r'<svg[^>]*>([\s\S]*)</svg>', raw).group(1)
    inner = re.sub(r'\s+', ' ', inner).strip().replace(' />', '/>')
    inner = re.sub(r'<(path|circle|rect|line|polyline|polygon|ellipse) ', r'<\1 pathLength="1" ', inner)
    return f'<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{inner}</svg>'


def img(m):
    pid, dim, sizes, loading, alt = m.group(1).split('|')
    w, h = map(int, dim.split('x'))
    def u(x): return f'https://images.unsplash.com/photo-{pid}?auto=format&amp;fit=crop&amp;q=72&amp;w={x}&amp;h={round(x*h/w)}'
    ws = [x for x in (480, 800, 1200, 1600, 2000) if x <= w] or [w]
    if w not in ws: ws.append(w)
    srcset = ', '.join(f'{u(x)} {x}w' for x in ws)
    extra = {'eager': 'fetchpriority="high" decoding="async"', 'low': 'fetchpriority="low" decoding="async"'}.get(loading, 'loading="lazy" decoding="async"')
    return f'<img src="{u(min(w, 1200))}" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" alt="{alt}" {extra}>'


def stars(rating=float(BIZ['rating'])):
    """Five stars, filled to the exact rating (4.9 fills nine tenths of the fifth)."""
    pts = [(12, 2.4), (14.9, 8.7), (21.6, 9.4), (16.5, 13.9), (17.9, 20.6), (12, 17.2), (6.1, 20.6), (7.5, 13.9), (2.4, 9.4), (9.1, 8.7)]
    row = ''.join('<polygon points="' + ' '.join(f'{x + i*26.5:g},{y:g}' for x, y in pts) + '"/>' for i in range(5))
    full = int(rating); clip = full * 26.5 + (rating - full) * 24
    return (f'<svg viewBox="0 0 130 24" aria-hidden="true" focusable="false"><defs><clipPath id="stars-fill"><rect width="{clip:.1f}" height="24"/></clipPath></defs>'
            f'<g fill="currentColor" opacity=".32">{row}</g><g fill="currentColor" clip-path="url(#stars-fill)">{row}</g></svg>')


SWASH = '<svg viewBox="0 0 300 20" preserveAspectRatio="none" aria-hidden="true"><path pathLength="1" d="M3 13 C 52 4, 96 17, 150 9 S 250 5, 297 11"/></svg>'
MIME = {'webp': 'image/webp', 'avif': 'image/avif', 'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'woff2': 'font/woff2'}
FONTS = {'roboto-flex-compressed.woff2': 'assets/roboto-flex-compressed.woff2',
         'manrope-latin-wght-normal.woff2': 'node_modules/@fontsource-variable/manrope/files/manrope-latin-wght-normal.woff2',
         'manrope-latin-ext-wght-normal.woff2': 'node_modules/@fontsource-variable/manrope/files/manrope-latin-ext-wght-normal.woff2'}
# Motion libraries, served from the site (same versions the site used from the jsDelivr CDN before).
VENDOR = [('node_modules/gsap/dist/gsap.min.js', ''), ('node_modules/gsap/dist/ScrollTrigger.min.js', ''),
          ('node_modules/lenis/dist/lenis.min.js', '/*! Lenis 1.1.14 | MIT License | https://github.com/darkroomengineering/lenis */\n')]


def variants(name):
    """Smaller copies of a picture made by tools/responsive-images.mjs: [(file, width)], the original last."""
    stem, ext = name.rsplit('.', 1)
    out = []
    for f in (root / 'assets').glob(f'{stem}-*.{ext}'):
        w = f.stem[len(stem) + 1:]
        if w.isdigit(): out.append((f.name, int(w)))
    full = root / 'assets' / name
    if full.exists(): out.append((name, Image.open(full).width))
    return sorted(out, key=lambda x: x[1])


def esbuild(code, loader):
    exe = root / 'node_modules/.bin/esbuild'
    r = subprocess.run([str(exe), f'--loader={loader}', '--minify', '--legal-comments=inline', '--log-level=warning'],
                       input=code, capture_output=True, text=True)
    if r.returncode: raise SystemExit(f'esbuild ({loader}) failed:\n{r.stderr}')
    if r.stderr.strip(): print(r.stderr.strip())
    return r.stdout


def vendor_js():
    parts = []
    for rel, banner in VENDOR:
        code = (root / rel).read_text()
        code = re.sub(r'\n?//# sourceMappingURL=\S+\s*$', '', code)
        parts.append(banner + code.rstrip().rstrip(';') + ';')
    return '\n'.join(parts) + '\n'


def minify_html(s):
    """Comments and indentation out; whitespace that carries meaning (one space between inline elements) stays."""
    keep = []
    def stash(m): keep.append(m.group(0)); return f'\x00{len(keep) - 1}\x00'
    s = re.sub(r'<(script|style|pre|textarea)\b[\s\S]*?</\1>', stash, s)
    s = re.sub(r'<!--(?!\[if)[\s\S]*?-->', '', s)
    s = re.sub(r'[ \t]*\n\s*', '\n', s)
    return re.sub(r'\x00(\d+)\x00', lambda m: keep[int(m.group(1))], s)


def square_mark(size=None, fmt='PNG'):
    m = Image.open(root / 'brand/mark.png'); side = max(m.size)
    sq = Image.new('RGBA', (side, side), (0, 0, 0, 0)); sq.paste(m, ((side - m.width) // 2, (side - m.height) // 2))
    if size: sq = sq.resize((size, size), Image.LANCZOS)
    buf = io.BytesIO()
    if fmt == 'ICO': sq.save(buf, 'ICO', sizes=[(48, 48), (32, 32), (16, 16)])
    else: sq.save(buf, 'PNG', optimize=True)
    return buf.getvalue()


def lossless_webp(path):
    """The logo files as lossless WebP: every pixel identical to the official PNG, fewer bytes."""
    buf = io.BytesIO(); Image.open(path).save(buf, 'WEBP', lossless=True, quality=100, method=6); return buf.getvalue()


def tokens(s, r='', gtm=''):
    """Text tokens shared by every page and both build modes."""
    s = s.replace('{{swash}}', SWASH).replace('{{stars}}', stars()).replace('{{updated}}', UPDATED)
    s = s.replace('{{gtm}}', gtm).replace('{{gsc}}', GSC_VERIFY).replace('{{lastmod}}', LASTMOD)
    for k, v in BIZ.items():
        s = s.replace('{{' + k + '}}', html.escape(v, quote=True) if k not in ('fiverr', 'linkedin') else v)
    s = s.replace('{{email-wrap}}', html.escape(BIZ['email']).replace('@', '@<wbr>'))
    s = s.replace('{{root}}', r)
    s = re.sub(r'\{\{ic:([a-z0-9-]+)\}\}', ic, s)
    s = re.sub(r'\{\{img\|([^}]+)\}\}', img, s)
    return s


def plain(t): return html.unescape(re.sub(r'<[^>]+>', '', t)).strip()


def faq_entities(markup):
    """FAQ structured data is built from the visible FAQ, so the two always match word for word."""
    faq = re.findall(r'<button class="faq__btn"[^>]*>(.*?)<i>.*?</button>.*?<div class="faq__a[^"]*"[^>]*><div><p>(.*?)</p>', markup, re.S)
    return [{'@type': 'Question', 'name': plain(q), 'acceptedAnswer': {'@type': 'Answer', 'text': plain(a)}} for q, a in faq]


def jsonld(obj): return json.dumps(obj, ensure_ascii=False, indent=2).replace('</', '<\\/')


def read(name): return (root / 'src' / name).read_text()


META, HEAD, BODY, SCRIPT = (read(f) for f in ['00-meta.html', '01-head.html', '02-body.html', '03-script.html'])
CSS = re.search(r'<style>([\s\S]*)</style>', HEAD).group(1)
JS = re.search(r'<script>\n(/\* =+[\s\S]*)</script>', SCRIPT).group(1)
LIBS = SCRIPT[:SCRIPT.index('<script>\n/* =')]


def finish(out, label):
    out = re.sub(r'<!-- SHELL:[A-Z:]+ -->\n?', '', out)
    leftover = re.findall(r'\{\{[^}]*\}\}', out)
    assert not leftover, (label, leftover[:5])
    return out


def icons(r):
    """Favicons: 48px and 192px for browsers and Google results, 180px for iOS home screens."""
    return (f'<link rel="icon" type="image/png" sizes="48x48" href="{r}assets/brand/favicon-48.png">\n'
            f'<link rel="icon" type="image/png" sizes="192x192" href="{r}assets/brand/favicon-192.png">\n'
            f'<link rel="apple-touch-icon" href="{r}assets/brand/apple-touch-icon.png">')


def home_meta(r, ents, icon_links):
    m = META.replace('{{faq-entities}}', json.dumps(ents, ensure_ascii=False, indent=8).replace('</', '<\\/'))
    m = m.replace('{{icons}}', icon_links).replace('{{site}}', SITE)
    return tokens(m, r)


# --------------------------------------------------------------------------------------------- single file
def build_single(dest):
    def uri(b, mime='image/png'): return f'data:{mime};base64,' + base64.b64encode(b).decode()
    def asset(m):
        name = m.group(1)
        return uri((root / 'assets' / name).read_bytes(), MIME[name.rsplit('.', 1)[1]])
    def font(m): return uri((root / FONTS[m.group(1)]).read_bytes(), 'font/woff2')
    logo = uri((root / 'brand/logo.png').read_bytes()); mark = uri((root / 'brand/mark.png').read_bytes())
    body = tokens(BODY, '').replace('{{logo}}', logo)
    # the single file keeps one picture per image: no srcset copies, no AVIF source
    body = re.sub(r'<source type="image/avif" srcset="\{\{srcset-avif:[^}]+\}\}"[^>]*>', '', body)
    body = re.sub(r' srcset="\{\{srcset:[^}]+\}\}"', '', body)
    body = re.sub(r'\{\{asset:([\w.-]+)\}\}', asset, body)
    css = re.sub(r'\{\{font:([\w.-]+)\}\}', font, CSS).replace('{{mark}}', mark)
    css += '\n' + (root / 'src/pages/pages.css').read_text()
    icon = uri(square_mark(192))
    icon_links = f'<link rel="icon" type="image/png" href="{icon}">\n<link rel="apple-touch-icon" href="{icon}">'
    out = home_meta('', faq_entities(body), icon_links) + f'<style>{css}</style>\n</head>\n' + body + LIBS + '<script>\n' + tokens(JS) + '</script>\n</body>\n</html>\n'
    out = finish(out, 'single')
    dest.parent.mkdir(parents=True, exist_ok=True); dest.write_text(out)
    vis = re.sub(r'<(script|style)[\s\S]*?</\1>', '', out)
    print(f'{dest}: {len(out)//1024} KB; dashes in markup: {len(re.findall("[—–]", vis))}; h1: {len(re.findall("<h1", out))}')


# --------------------------------------------------------------------------------------------- production site
def shell(r, current=None):
    """Header, menu and footer from the home page, with in-page links pointed back at the home page."""
    head = BODY[BODY.index('<!-- SHELL:HEADER:START -->'):BODY.index('<!-- SHELL:HEADER:END -->')]
    foot = BODY[BODY.index('<!-- SHELL:FOOTER:START -->'):BODY.index('<!-- SHELL:FOOTER:END -->')]
    def relink(s):
        # links that choose the form's intent carry it to the home page in the address
        s = re.sub(r'href="#contact" data-intent="(\w+)"', r'href="{{root}}?intent=\1#contact" data-intent="\1"', s)
        s = s.replace('href="#top"', 'href="{{root}}"')
        s = re.sub(r'href="#([\w-]+)"', r'href="{{root}}#\1"', s)
        s = s.replace('aria-label="INFA ELITE, back to top"', 'aria-label="INFA ELITE home"')
        return s
    head, foot = relink(head), relink(foot)
    foot = foot.replace('<a class="to-top" href="{{root}}">', '<a class="to-top" href="#top">')
    if current:   # the section of the home page this page belongs to
        head = head.replace(f'<li><a href="{{{{root}}}}#{current}">', f'<li><a href="{{{{root}}}}#{current}" aria-current="true">', 1)
    head = head.replace('<div class="curtain" aria-hidden="true"><span class="mark"></span></div>\n', '')
    return head, foot


def page_meta(p, r):
    url = SITE + p['slug']
    crumbs = [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE}]
    for i, (name, path) in enumerate(p['trail'], 2):
        crumbs.append({'@type': 'ListItem', 'position': i, 'name': name, 'item': SITE + path} if path is not None else {'@type': 'ListItem', 'position': i, 'name': name})
    graph = [
        {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': p['title'], 'description': p['description'],
         'isPartOf': {'@id': SITE + '#website'}, 'about': {'@id': SITE + '#organization'}, 'inLanguage': 'en',
         'breadcrumb': {'@id': url + '#breadcrumb'}, 'dateModified': LASTMOD},
        {'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': crumbs},
    ]
    if p.get('service'):
        graph.append({'@type': 'Service', '@id': url + '#service', 'name': p['service'], 'serviceType': p['service'],
                      'description': p['description'], 'url': url, 'provider': {'@id': SITE + '#organization'},
                      'areaServed': 'Worldwide'})
    if not p.get('index', True):
        graph = [graph[0]]
    if p['faq']:
        graph.append({'@type': 'FAQPage', '@id': url + '#faq', 'isPartOf': {'@id': url + '#webpage'}, 'mainEntity': p['faq']})
    t, d = html.escape(p['title']), html.escape(p['description'])
    robots = 'index, follow, max-image-preview:large, max-snippet:-1' if p.get('index', True) else 'noindex, follow'
    canonical = f'<link rel="canonical" href="{url}">\n' if p.get('index', True) else ''
    # The 404 page is served at whatever address was missing, so it sets its base to the site root:
    # "/" on the custom domain, "/<repository>/" on a github.io project address.
    base = ('<script>(function(){var p=location.pathname.split("/"),b=/\\.github\\.io$/.test(location.hostname)&&p[1]?"/"+p[1]+"/":"/";'
            'document.write(\'<base href="\'+b+\'">\')})()</script>\n') if p['slug'] == '404.html' else ''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
{base}<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t}</title>
<meta name="description" content="{d}">
{canonical}<meta name="robots" content="{robots}">
<meta name="author" content="INFA ELITE">
<meta name="theme-color" content="#19181D">
<meta name="color-scheme" content="light">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="INFA ELITE">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="INFA ELITE: Shopify, WordPress and custom web development">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{SITE}og-image.jpg">
<meta name="twitter:image:alt" content="INFA ELITE: Shopify, WordPress and custom web development">
{icons(r)}
<script>
document.documentElement.classList.add('js');
setTimeout(function(){{if(!window.gsap)document.documentElement.classList.add('no-gsap')}},3500);
</script>
<script type="application/ld+json">
{jsonld({'@context': 'https://schema.org', '@graph': graph})}
</script>
'''


def parse_page(path):
    raw = path.read_text()
    front = re.match(r'<!--\n([\s\S]*?)\n-->\n', raw)
    meta = dict(line.split(': ', 1) for line in front.group(1).splitlines() if line.strip())
    body = raw[front.end():]
    trail = []
    for part in meta.get('trail', '').split(' > '):
        if part:
            name, _, href = part.partition(' @ ')
            trail.append((name, href if href else None))
    return {'slug': meta['slug'], 'title': meta['title'], 'description': meta['description'], 'current': meta.get('nav'),
            'service': meta.get('service'), 'trail': trail, 'index': meta.get('index', 'yes') == 'yes',
            'priority': meta.get('priority', '0.8'), 'body': body}


def lazy(markup):
    """Local images below the first screen load when they come near it."""
    def fix(m):
        tag = m.group(0)
        if 'loading=' in tag or 'fetchpriority=' in tag or 'avatar-' in tag: return tag
        return tag.replace('<img ', '<img loading="lazy" ', 1)
    return re.sub(r'<img [^>]*src="[^"]*assets/img/[^"]*"[^>]*>', fix, markup)


def build_site(dist):
    if dist.exists(): shutil.rmtree(dist)
    (dist / 'assets/img').mkdir(parents=True); (dist / 'assets/fonts').mkdir(); (dist / 'assets/brand').mkdir()
    used = set()
    def local(r):
        def f(m):
            used.add(m.group(1)); return f'{r}assets/img/{m.group(1)}'
        return f
    def srcset(r):
        def f(m):
            avif, name = m.group(1), m.group(2)
            files = variants(name + '.avif') if avif else variants(name)
            assert files, ('no picture for srcset', name)
            for fn, _ in files: used.add(fn)
            return ', '.join(f'{r}assets/img/{fn} {w}w' for fn, w in files)
        return f
    # shared files: the home stylesheet, the extra stylesheet for the other pages, the scripts
    css = re.sub(r'\{\{font:([\w.-]+)\}\}', r'fonts/\1', CSS).replace('{{mark}}', 'brand/infa-elite-mark.webp')
    finish(css, 'css'); (dist / 'assets/site.css').write_text(esbuild(css, 'css'))
    pcss = (root / 'src/pages/pages.css').read_text()
    finish(pcss, 'pages.css'); (dist / 'assets/pages.css').write_text(esbuild(pcss, 'css'))
    js = finish(tokens(JS, gtm=GTM_ID), 'js'); (dist / 'assets/site.js').write_text(esbuild(js, 'js'))
    (dist / 'assets/vendor.js').write_text(vendor_js())
    for name, src in FONTS.items(): shutil.copy(root / src, dist / 'assets/fonts' / name)
    shutil.copy(root / 'brand/logo.png', dist / 'assets/brand/infa-elite-logo.png')
    shutil.copy(root / 'brand/mark.png', dist / 'assets/brand/infa-elite-mark.png')
    (dist / 'assets/brand/infa-elite-logo.webp').write_bytes(lossless_webp(root / 'brand/logo.png'))
    (dist / 'assets/brand/infa-elite-mark.webp').write_bytes(lossless_webp(root / 'brand/mark.png'))
    (dist / 'assets/brand/favicon-48.png').write_bytes(square_mark(48))
    (dist / 'assets/brand/favicon-192.png').write_bytes(square_mark(192))
    (dist / 'assets/brand/apple-touch-icon.png').write_bytes(square_mark(180))
    (dist / 'favicon.ico').write_bytes(square_mark(48, 'ICO'))
    shutil.copy(root / 'static/og-image.jpg', dist / 'og-image.jpg')
    shutil.copy(root / 'static/infa-elite-logo.png', dist / 'infa-elite-logo.png')

    def assemble(meta_html, body_html, r, label, extra_css=False):
        head = (f'<link rel="preload" href="{r}assets/fonts/roboto-flex-compressed.woff2" as="font" type="font/woff2" crossorigin>\n'
                f'<link rel="stylesheet" href="{r}assets/site.css">\n')
        if extra_css: head += f'<link rel="stylesheet" href="{r}assets/pages.css">\n'
        body_html = re.sub(r'\{\{srcset(-avif)?:([\w.-]+)\}\}', srcset(r), body_html)
        body_html = re.sub(r'\{\{asset:([\w.-]+)\}\}', local(r), body_html).replace('{{logo}}', f'{r}assets/brand/infa-elite-logo.webp')
        # the product photos inside the drawn interfaces load when their section comes near (site.js)
        body_html = re.sub(r'(<image id="pi-[\w-]+"[^>]*?) href="', r'\1 data-href="', body_html)
        body_html = lazy(body_html)
        libs = f'<script defer src="{r}assets/vendor.js"></script>\n'
        out = meta_html + head + '</head>\n' + body_html + libs + f'<script defer src="{r}assets/site.js"></script>\n</body>\n</html>\n'
        return minify_html(finish(out, label))

    pages = [('', 1.0)]
    # home
    body = tokens(BODY, '')
    (dist / 'index.html').write_text(assemble(home_meta('', faq_entities(body), icons('')), body, '', 'home'))
    # other pages
    for path in sorted((root / 'src/pages').glob('*.html')):
        p = parse_page(path)
        r = '../' * p['slug'].count('/')
        head, foot = shell(r, p['current'])
        main = p['body']
        fixhash = ''
        if p['slug'] == '404.html':   # with a <base>, links to #ids on this page need the page's own path
            fixhash = '<script>document.querySelectorAll(\'a[href^="#"]\').forEach(function(a){a.setAttribute("href",location.pathname+location.search+a.getAttribute("href"))})</script>\n'
        service = f' data-service="{html.escape(p["service"])}"' if p.get('service') else ''
        body = f'<body{service}>\n<a class="skip" href="#main">Skip to content</a>\n<div class="progress" aria-hidden="true"></div>\n' + head + '\n' + main + '\n' + foot + '\n<div class="toast glass" id="toast" role="status" aria-live="polite"></div>\n' + fixhash
        body = tokens(body, r)
        if p['slug'] and p['slug'] != '404.html':   # the footer marks the page you are on
            body = body.replace(f'<li><a href="{r}{p["slug"]}">', f'<li><a href="{r}{p["slug"]}" aria-current="page">')
        p['faq'] = faq_entities(body)
        meta_html = tokens(page_meta(p, r), r)
        target = dist / p['slug'] / 'index.html' if p['slug'] else dist / 'index.html'
        if p['slug'] == '404.html':
            target = dist / '404.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(assemble(meta_html, body, r, p['slug'], extra_css=True))
        if p['index']: pages.append((p['slug'], float(p['priority'])))
    for name in sorted(used):
        shutil.copy(root / 'assets' / name, dist / 'assets/img' / name)
    # crawling, hosting
    (dist / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n')
    urls = ''.join(f'  <url>\n    <loc>{SITE}{slug}</loc>\n    <lastmod>{LASTMOD}</lastmod>\n  </url>\n' for slug, pr in pages)
    (dist / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    (dist / '.nojekyll').write_text('')
    total = sum(f.stat().st_size for f in dist.rglob('*') if f.is_file())
    print(f'{dist}: {SITE} | {len(pages)} indexed pages, {len(used)} images, {total//1024} KB in total')


if __name__ == '__main__':
    dest = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')
    if dest.suffix == '.html': build_single(dest)
    else: build_site(dest)
