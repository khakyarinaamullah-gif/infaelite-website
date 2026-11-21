"""Technology grid: official logos in place of the two-letter abbreviations.

Paths come from assets/tech-logos (Simple Icons, see SOURCES.md). Each logo's viewBox is cropped to
its own bounds and its height is set so every mark covers about the same area, so a wide wordmark
(WooCommerce) and a tall shield (HTML5) read as the same size. Run after editing; it rewrites the
<span class="el__logo"> (or legacy el__sym) of each tile in src/02-body.html."""
import math, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGOS = ROOT / 'assets/tech-logos'

# name in the grid -> (source, bbox x, y, w, h on the 24 grid, weight fudge)
FILLED = {
    'Shopify': ('shopify', 1.45, 0, 21.1, 24, 1.0),
    'WooCommerce': ('woocommerce', 0, 9.58, 24, 4.84, 1.0),
    'WordPress': ('wordpress', 0, 0, 24, 24, .94),
    'PHP': ('php', 0, 5.69, 24, 12.63, 1.0),
    'HTML5': ('html5', 1.5, 0, 21, 24, 1.0),
    'CSS3': ('css3', 1.5, 0, 21, 24, 1.0),
    'JavaScript': ('javascript', 0, 0, 24, 24, .84),
    'React': ('react', 0, 1.31, 24, 21.38, 1.06),
    'GraphQL': ('graphql', 1.32, 0, 21.36, 24, 1.04),
}
AREA, MAX_W, MAX_H = .8, 1.9, 1.0      # em^2 of a typical mark, and the box it must fit


def size(w, h, k):
    a = w / h
    hh = math.sqrt(AREA * k / a)
    hh = min(hh, MAX_H, MAX_W / a)
    return round(hh, 3)


def svg(viewbox, inner, h, stroke=False):
    paint = 'fill="none" stroke="currentColor"' if stroke else 'fill="currentColor"'
    return (f'<svg class="el__svg" viewBox="{viewbox}" style="height:{h}em" {paint} '
            f'aria-hidden="true" focusable="false">{inner}</svg>')


def path_of(slug):
    t = (LOGOS / f'{slug}.svg').read_text()
    return re.search(r'<path d="([^"]+)"', t).group(1)


MARKS = {}
for name, (slug, x, y, w, h, k) in FILLED.items():
    MARKS[name] = svg(f'{x} {y} {w} {h}', f'<path d="{path_of(slug)}"/>', size(w, h, k))

# Shopify Liquid: the water drop from Shopify's Liquid documentation, traced on its 128 grid.
LIQUID = ('<path d="M64 4.5L29.88 66.1A39 39 0 1 0 98.12 66.1Z" stroke-width="6.5" stroke-linejoin="round"/>'
          '<path d="M60.5 31L41.1 74.9A25 25 0 0 0 64 110" stroke-width="6.5" stroke-linecap="round"/>')
MARKS['Shopify Liquid'] = svg('21.5 1.5 85 126', LIQUID, size(85, 126, 1.0), stroke=True)
# REST APIs: no official logo exists for an architectural style, so a neutral pair of braces.
BRACES = ('<path d="M8.2 3.5H7.4C5.9 3.5 5.2 4.3 5.2 5.8V9.4C5.2 10.7 4.5 11.5 3.2 12C4.5 12.5 5.2 13.3 5.2 14.6V18.2'
          'C5.2 19.7 5.9 20.5 7.4 20.5H8.2M15.8 3.5H16.6C18.1 3.5 18.8 4.3 18.8 5.8V9.4C18.8 10.7 19.5 11.5 20.8 12'
          'C19.5 12.5 18.8 13.3 18.8 14.6V18.2C18.8 19.7 18.1 20.5 16.6 20.5H15.8" stroke-width="1.9" '
          'stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="12" r="1.35" fill="currentColor" stroke="none"/>')
MARKS['REST APIs'] = svg('2.2 2.5 19.6 19', BRACES, size(19.6, 19, .92), stroke=True)


def run():
    body = ROOT / 'src/02-body.html'
    s = body.read_text()
    n = 0
    for name, mark in MARKS.items():
        pat = re.compile(r'<span class="el__(?:sym|logo)" aria-hidden="true">(?:[^<]|<(?!/span>))*</span>(<span class="el__name">'
                         + re.escape(name) + r'</span>)')
        s, k = pat.subn(lambda m: f'<span class="el__logo" aria-hidden="true">{mark}</span>' + m.group(1), s)
        n += k
    body.write_text(s)
    print('logos placed:', n)


if __name__ == '__main__':
    run()
