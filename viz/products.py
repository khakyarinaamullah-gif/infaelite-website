"""Product photography for the animated scenes.

The supplied product photos are embedded once, as <image> elements in a hidden sprite at the top of
the page (src/02-body.html, between <!-- PRODUCTS:START/END -->). Every scene that shows a product
places a copy with photo(): a rounded clip, an optional backdrop colour, and a nested <svg> whose
viewBox is the crop of the source photo, so one embedded file serves every size and aspect ratio
(object-fit: cover, focused on the product) without being repeated in the page.

Sources: assets/product-*.webp, resized from the supplied PNGs (880 px on the long side; the serums 640 px)."""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent

# slug -> (width, height, product bounds in the image as x0, y0, x1, y1, backdrop colour)
PRODUCTS = {
    'burgundy-tote': (880, 587, (183, 23, 705, 552), '#DDD0CA'),
    'smartwatch':    (880, 587, (229, 23, 647, 552), '#D0CED0'),
    'ivory-bag':     (880, 587, (218, 40, 676, 540), '#D6C7BC'),
    'noir-bag':      (880, 587, (115, 46, 771, 546), '#D6C8BE'),
    # Services E (UI/UX & Design): the four supplied serum photos, 640 px square.
    'serum-hydrating':     (640, 640, (226, 26, 412, 561), '#B69E94'),
    'serum-brightening':   (640, 640, (227, 26, 412, 600), '#E1D1CB'),
    'serum-retinol-night': (640, 640, (226, 26, 416, 571), '#ECDFD9'),
    'serum-retinol':       (640, 640, (227, 32, 412, 560), '#CDBEB6'),
}

# Stage 03 (Creative Design): the three supplied design directions, A, B and C, shown whole.
# A was supplied inside a black frame, so it is cropped to its card; B and C are used as supplied.
DESIGNS = {
    'dir-a': (460, 804, (0, 0, 460, 804), '#E9E8EA'),
    'dir-b': (460, 763, (0, 0, 460, 763), '#000000'),
    'dir-c': (460, 762, (0, 0, 460, 762), '#4A2420'),
    # Stage 04 (Development & Engineering) staging preview: hero banner and the two product tiles.
    # The watch photo was supplied inside a black rounded frame, so it is cropped to the photo.
    'p4-banner': (640, 301, (0, 0, 640, 301), '#6B4A33'),
    'p4-watch': (360, 243, (0, 0, 360, 243), '#2E3238'),
    'p4-sunglasses': (360, 255, (0, 0, 360, 255), '#D8C9B8'),
    # Stage 05 (Testing & Optimization) device screens: the supplied mobile, tablet, desktop and
    # checkout views, shown whole; the backdrop is each page's own background. The tablet view was
    # supplied inside a black rounded frame and the desktop view with a 1 px dark border; both are
    # cropped to the page.
    'p5-mobile': (300, 533, (0, 0, 300, 533), '#FDFCFB'),
    'p5-tablet': (560, 746, (0, 0, 560, 746), '#FBFBFB'),
    'p5-desktop': (860, 483, (0, 0, 860, 483), '#FEFEFE'),
    'p5-checkout': (860, 440, (0, 0, 860, 440), '#FEFEFE'),
    # Services C (WordPress Development): the supplied Luxury Bags banner, shown whole.
    'wp-banner': (760, 357, (0, 0, 760, 357), '#6E4A31'),
}
ALL = {**PRODUCTS, **DESIGNS}

NAMES = {
    'burgundy-tote': 'burgundy leather tote with a gold padlock',
    'smartwatch': 'white smartwatch',
    'ivory-bag': 'ivory top handle bag',
    'noir-bag': 'black top handle bag',
    'serum-hydrating': 'Hydrating Face Serum in a purple dropper bottle',
    'serum-brightening': 'Brightening Face Serum in a pink dropper bottle',
    'serum-retinol-night': 'Retinol Night Serum in a purple dropper bottle',
    'serum-retinol': 'Retinol Serum in a purple dropper bottle',
}


def sprite():
    imgs = ''.join(f'<image id="pi-{k}" width="{w}" height="{h}" href="{{{{asset:{"" if k in DESIGNS else "product-"}{k}.webp}}}}"/>'
                   for k, (w, h, _, _) in ALL.items())
    return ('<!-- PRODUCTS:START -->\n<svg class="sprite" width="0" height="0" aria-hidden="true" focusable="false" '
            'style="position:absolute;width:0;height:0;overflow:hidden"><defs>' + imgs + '</defs></svg>\n<!-- PRODUCTS:END -->')


def crop(slug, aspect, fill=.86, fx=None, fy=None):
    """A crop box of the given aspect that covers the product: the product's limiting side takes up
    `fill` of the frame (1 = edge to edge); the crop is centred on the product and kept inside the
    photo where possible."""
    W, H, (x0, y0, x1, y1), _ = ALL[slug]
    pw, ph = x1 - x0, y1 - y0
    cx = (x0 + x1) / 2 if fx is None else fx
    cy = (y0 + y1) / 2 if fy is None else fy
    cw = max(pw / fill, ph / fill * aspect)
    cw = min(cw, W, H * aspect)            # never wider than the photo allows at this aspect
    ch = cw / aspect
    x = min(max(cx - cw / 2, 0), W - cw)
    y = min(max(cy - ch / 2, 0), H - ch)
    return round(x, 1), round(y, 1), round(cw, 1), round(ch, 1)


def photo(slug, x, y, w, h, rx, cid, fill=.86, fx=None, fy=None, box=None, cls='pph'):
    """Place product `slug` in the box (x, y, w, h) with corner radius rx. `box` overrides the crop."""
    vx, vy, vw, vh = box or crop(slug, w / h, fill, fx, fy)
    bg = ALL[slug][3]
    return (f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>'
            f'<g class="{cls}" clip-path="url(#{cid})"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}"/>'
            f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{vx} {vy} {vw} {vh}" preserveAspectRatio="xMidYMid slice" overflow="hidden">'
            f'<use href="#pi-{slug}"/></svg></g>')


def write_sprite():
    body = ROOT / 'src/02-body.html'
    s = body.read_text()
    block = sprite()
    if '<!-- PRODUCTS:START -->' in s:
        s = re.sub(r'<!-- PRODUCTS:START -->.*?<!-- PRODUCTS:END -->', lambda m: block, s, flags=re.S)
    else:
        s = s.replace('<body>\n', '<body>\n' + block + '\n', 1)
    body.write_text(s)


if __name__ == '__main__':
    write_sprite()
    print('sprite written')
