"""Services: five flat, animated interface scenes, one story per service.

A  Shopify Development   a storefront: a shopper adds a product, it drops into the cart, the cart
                         drawer opens and checkout completes.
B  Shopify Optimization  a speed score climbs and the vitals pass, the store's search result rises
                         to the top and the conversions line climbs.
C  WordPress Development a block editor: blocks are dragged in to build a page, then it is published.
D  Custom Development    code is written and run; a request travels through a custom API to the
                         database and back, and the app's chart fills with the data.
E  UI/UX Design          a mobile wireframe is laid on a grid, turned into the finished design, then
                         wired to the next screen as a prototype.

Every scene is one inline SVG (viewBox 640 x 360) animated only with transform, opacity and
stroke-dashoffset. The base styles are the finished frame, so reduced motion and no-script visitors
see a complete picture. Loops only run while the scene is on screen (script adds .is-live)."""
import pathlib, re
from products import photo

ROOT = pathlib.Path(__file__).resolve().parent.parent


def T(x, y, s, size, cls='xt', anchor=None, weight=None, extra=''):
    a = f' text-anchor="{anchor}"' if anchor else ''
    w = f' font-weight="{weight}"' if weight else ''
    return f'<text x="{x}" y="{y}" font-size="{size}" class="{cls}"{a}{w}{extra}>{s}</text>'


def R(x, y, w, h, rx=0, cls='', extra=''):
    c = f' class="{cls}"' if cls else ''
    r = f' rx="{rx}"' if rx else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}"{r}{c}{extra}/>'


def P(d, cls='', extra=''):
    c = f' class="{cls}"' if cls else ''
    return f'<path d="{d}"{c}{extra}/>'


def C(cx, cy, r, cls='', extra=''):
    c = f' class="{cls}"' if cls else ''
    return f'<circle cx="{cx}" cy="{cy}" r="{r}"{c}{extra}/>'


def G(inner, cls='', extra=''):
    c = f' class="{cls}"' if cls else ''
    return f'<g{c}{extra}>{inner}</g>'


CURSOR = P('M0 0L0 17L4.6 13.1L7.6 20.2L10.7 18.9L7.8 12.1L13.4 12.1Z', 'xcur')
CHECK = 'M-3.6 0.2L-1.1 2.7L3.8-2.4'


def check(x, y, cls='xchk'):
    return P(CHECK, cls, f' transform="translate({x} {y})"')


def window(id_, x=16, y=8, w=608, h=344, cls='xw'):
    return (f'<defs><clipPath id="{id_}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14"/></clipPath></defs>'
            + R(x, y, w, h, 14, cls))


# ================================================================== A. Shopify Development








def scene_a():
    o = window('sxa-win')
    o += '<g clip-path="url(#sxa-win)">'
    # browser chrome
    o += ''.join(C(36 + 14 * k, 23, 4, 'xdot') for k in range(3))
    o += R(232, 15, 176, 16, 8, 'xpill') + T(320, 26.5, 'northandco.com', 9, 'xm', 'middle')
    o += P('M16 38H624', 'xl')
    # store header
    o += T(36, 62, 'NORTH&amp;CO', 17, 'xt xdisp', weight=500)
    o += T(246, 60, 'Shop', 10, 'xt') + T(282, 60, 'New in', 10, 'xm') + T(328, 60, 'Journal', 10, 'xm')
    o += C(552, 55, 5.5, 'xico') + P('M556 59l4 4', 'xico')
    o += P('M575 50h18l-1.6 15h-14.8Z', 'xico') + P('M579 50v-2.5a5 5 0 0 1 10 0V50', 'xico')
    o += G(C(595, 47, 7.5, 'xo') + T(595, 50.2, '1', 9, 'xwt', 'middle', 700), 'aA-badge')
    o += P('M16 74H624', 'xl')
    o += T(36, 100, 'New arrivals', 11.5, 'xt', weight=700) + T(604, 100, 'View all', 9, 'xm', 'end')
    cards = [(36, 'burgundy-tote', 'Bordeaux Tote', '$240'), (238, 'noir-bag', 'Noir Top Handle', '$215'), (440, 'ivory-bag', 'Ivory Top Handle', '$195')]
    for k, (x, slug, name, price) in enumerate(cards):
        o += photo(slug, x, 110, 164, 146, 10, f'sxa-p{k}', fill=.9)
        o += T(x, 274, name, 10.5, 'xt', weight=600) + T(x + 164, 274, price, 10, 'xm', 'end')
        if k != 1:
            o += R(x, 286, 164, 28, 14, 'xbtn') + T(x + 82, 303.5, 'Add to cart', 9.5, 'xt', 'middle', 700)
        else:
            o += R(x, 286, 164, 28, 14, 'xbtn') + R(x, 286, 164, 28, 14, 'xo aA-bfill')
            o += T(x + 82, 303.5, 'Add to cart', 9.5, 'xt aA-l1', 'middle', 700)
            o += G(T(x + 88, 303.5, 'Added', 9.5, 'xwt', 'middle', 700) + check(x + 62, 300, 'xchk-w'), 'aA-l2')
    # the product thrown into the bag: X eases in, Y eases out, so it arcs up and over
    o += G(G(G(photo('noir-bag', 306, 286, 28, 28, 7, 'sxa-pf', fill=.94) + R(306, 286, 28, 28, 7, 'xthumb'), 'aA-fo'), 'aA-fy'), 'aA-fx')
    # cart drawer
    o += R(16, 38, 608, 314, 0, 'aA-dim')
    d = R(404, 38, 220, 314, 0, 'xdrawer') + P('M404.5 38V352', 'xl')
    d += T(420, 63, 'Your cart', 11.5, 'xt', weight=700) + T(474, 63, '(1)', 10, 'xm')
    d += P('M600 54l8 8M608 54l-8 8', 'xico')
    d += P('M404 76H624', 'xl')
    d += photo('noir-bag', 420, 88, 48, 48, 8, 'sxa-pd', fill=.94)
    d += T(478, 104, 'Noir Top Handle', 10.5, 'xt', weight=600) + T(608, 104, '$215', 10.5, 'xt', 'end', 600)
    d += T(478, 119, 'Qty 1', 9, 'xm')
    d += P('M420 150H608', 'xl')
    d += T(420, 172, 'You may also like', 9, 'xm', weight=600)
    d += photo('burgundy-tote', 420, 182, 90, 62, 8, 'sxa-pa1', fill=.9) + photo('ivory-bag', 518, 182, 90, 62, 8, 'sxa-pa2', fill=.9)
    d += T(420, 268, 'Subtotal', 10, 'xm') + T(608, 268, '$215.00', 11, 'xt', 'end', 700)
    d += T(420, 283, 'Shipping calculated at checkout', 8, 'xf')
    d += G(R(420, 296, 188, 36, 18, 'xo'), 'aA-cbtn')
    d += G(P('M482 311v-3a4 4 0 0 1 8 0v3', 'xlock') + R(480, 311, 12, 9, 2, 'xwf') + T(528, 318, 'Checkout', 11, 'xwt', 'middle', 700), 'aA-co')
    d += G(check(474, 314, 'xchk-w') + T(522, 318, 'Order placed', 11, 'xwt', 'middle', 700), 'aA-ok')
    o += G(d, 'aA-drawer')
    o += G(G(CURSOR, 'aA-press'), 'aA-cur')
    o += '</g>'
    return o


CSS_A = '''
.svx .xthumb{fill:none;stroke:var(--orange);stroke-width:1.5}
.aA-dim{fill:rgba(8,7,9,.62)}
.svx .xdrawer{fill:#222026}
.xlock{fill:none;stroke:#fff;stroke-width:1.6}
.aA-l1,.aA-ok,.aA-fo{opacity:0}
.aA-fo,.aA-badge,.aA-cbtn{transform-box:fill-box;transform-origin:50% 50%}
.aA-cur{transform:translate(572px,320px)}
'''
KF_A = '''
.js .aA-cur{animation:aA-cur 10s cubic-bezier(.5,0,.25,1) infinite both}
@keyframes aA-cur{0%,6%{transform:translate(660px,390px)}20%,40%{transform:translate(322px,302px)}52%{transform:translate(322px,302px)}62%,76%{transform:translate(572px,320px)}88%,100%{transform:translate(660px,390px)}}
.js .aA-press{animation:aA-press 10s ease infinite both}
@keyframes aA-press{0%,20%,23%,63%,66%,100%{transform:scale(1)}21.5%,64.5%{transform:scale(.8)}}
.js .aA-bfill,.js .aA-l2{animation:aA-on 10s ease infinite both}
.js .aA-l1{animation:aA-off 10s ease infinite both}
@keyframes aA-on{0%,21.5%{opacity:0}22.5%,86%{opacity:1}90%,100%{opacity:0}}
@keyframes aA-off{0%,21.5%{opacity:1}22.5%,86%{opacity:0}90%,100%{opacity:1}}
.js .aA-fx{animation:aA-fx 10s cubic-bezier(.55,0,.9,.55) infinite both}
.js .aA-fy{animation:aA-fy 10s cubic-bezier(.1,.6,.35,1) infinite both}
.js .aA-fo{animation:aA-fo 10s ease infinite both}
@keyframes aA-fx{0%,22.5%{transform:none}38%,100%{transform:translateX(264px)}}
@keyframes aA-fy{0%,22.5%{transform:none}38%,100%{transform:translateY(-236px)}}
@keyframes aA-fo{0%,22%{opacity:0;transform:scale(.6)}24.5%{opacity:1;transform:scale(1)}34%{opacity:1;transform:scale(.8)}38%,100%{opacity:0;transform:scale(.35)}}
.js .aA-badge{animation:aA-badge 10s var(--ease-out) infinite both}
@keyframes aA-badge{0%,37.5%{transform:scale(0)}40%{transform:scale(1.35)}43%,92%{transform:scale(1)}95%,100%{transform:scale(0)}}
.js .aA-dim{animation:aA-dim 10s ease infinite both}
@keyframes aA-dim{0%,42%{opacity:0}49%,86%{opacity:1}92%,100%{opacity:0}}
.js .aA-drawer{animation:aA-drawer 10s cubic-bezier(.32,.72,0,1) infinite both}
@keyframes aA-drawer{0%,42%{transform:translateX(232px)}51%,86%{transform:none}93%,100%{transform:translateX(232px)}}
.js .aA-cbtn{animation:aA-cbtn 10s ease infinite both}
@keyframes aA-cbtn{0%,64%,66.5%,100%{transform:scale(1)}65%{transform:scale(.95)}}
.js .aA-co{animation:aA-off2 10s ease infinite both}
.js .aA-ok{animation:aA-on2 10s ease infinite both}
@keyframes aA-on2{0%,65.5%{opacity:0}67%,88%{opacity:1}91%,100%{opacity:0}}
@keyframes aA-off2{0%,65.5%{opacity:1}67%,88%{opacity:0}91%,100%{opacity:1}}
'''


# ================================================================== B. Shopify Optimization
def scene_b():
    o = window('sxb-w1', 16, 16, 376, 328)
    o += '<g clip-path="url(#sxb-w1)">'
    o += R(32, 32, 344, 30, 15, 'xin') + C(50, 46, 6, 'xico') + P('M54.4 50.4L58 54', 'xico')
    o += T(66, 50.5, 'linen shirts', 11, 'xt')
    o += T(34, 84, 'All', 9.5, 'xt', weight=700) + T(58, 84, 'Shopping', 9.5, 'xm') + T(110, 84, 'Images', 9.5, 'xm') + T(152, 84, 'News', 9.5, 'xm')
    o += R(32, 88, 16, 2, 1, 'xo') + P('M16 96H392', 'xl')
    rows = ''
    for r in range(4):
        rows += T(36, 108 + r * 58 + 22, str(r + 1), 10.5, 'xm', 'middle', 700)
    o += rows

    # the other results for the same query: real sites, titles and snippets (the store starts below them)
    others = [('C', 'coastlinesupply.com &#8250; mens &#8250; shirts', 'Men&#8217;s Linen Shirts - Coastline Supply', 'Classic and camp collar linen shirts, with new styles added every week.'),
              ('T', 'thelinenedit.com &#8250; guides', 'How to Wear a Linen Shirt This Summer', 'A style guide to fabrics, fits and colours, and how to keep linen crisp.'),
              ('H', 'harbourandhale.com &#8250; clothing', 'Linen Shirts - Harbour &amp; Hale', 'Lightweight shirts in European linen, sizes XS to XXL, delivered in 3 to 5 days.')]

    def row(y0, ini, url, title, snip):
        return (C(64, y0 + 16, 7, 'xfav') + T(64, y0 + 18.6, ini, 7, 'xfavt', 'middle', 800) + T(78, y0 + 18.4, url, 8, 'xm') +
                T(56, y0 + 33.5, title, 11, 'xrt', weight=700) + T(56, y0 + 47, snip, 7.5, 'xrs'))
    res = ''
    for k, o_ in enumerate(others):
        res += G(row(108 + (k + 1) * 58, *o_), f'bB-o bB-o{k + 1}')
    us = R(26, 112, 356, 52, 10, 'xrowbg') + R(26, 112, 356, 52, 10, 'bB-glow')
    us += C(64, 124, 7, 'xo') + T(64, 126.6, 'N', 7, 'xfavt', 'middle', 800) + T(78, 127.4, 'northandco.com &#8250; linen', 8.5, 'xacc')
    us += T(56, 142.5, 'Linen Shirts for Summer &#183; North&amp;Co', 11.5, 'xacc2', weight=700)
    us += T(56, 156, 'Breathable linen shirts in 14 colours. Free delivery over $100 and free returns.', 7.5, 'xrs')
    us += R(314, 117, 56, 16, 8, 'xchip') + P('M327 119.5l-4 6.2h3.4l-1.2 5 4.8-6.6h-3.4z', 'xbolt') + T(353, 128.2, 'Fast', 8.5, 'xacc', 'middle', 700)
    res += G(us, 'bB-us')
    o += G(res, 'bB-res') + '</g>'
    # speed card
    o += R(408, 16, 216, 180, 14, 'xw') + T(424, 38, 'Performance', 10, 'xt', weight=700) + T(608, 38, 'Mobile', 8.5, 'xm', 'end')
    o += C(516, 102, 42, 'xtrack')
    o += f'<circle cx="516" cy="102" r="42" pathLength="100" class="xarc bB-arc" transform="rotate(-90 516 102)"/>'
    o += P('M519 84l-13 20h10l-3.5 15 15-21.5h-10z', 'xbolt2')
    for k, (lbl, x) in enumerate([('LCP', 424), ('CLS', 490), ('INP', 556)]):
        o += R(x, 160, 54, 20, 10, 'xvoff') + T(x + 27, 173.4, lbl, 8.5, 'xm', 'middle', 700)
        o += G(R(x, 160, 54, 20, 10, 'xvon') + T(x + 23, 173.4, lbl, 8.5, 'xwt', 'middle', 700) + check(x + 42, 170, 'xchk-o'), f'bB-v bB-v{k + 1}')
    # conversions card
    o += R(408, 208, 216, 136, 14, 'xw') + T(424, 230, 'Conversions', 10, 'xt', weight=700)
    o += R(572, 218, 38, 18, 9, 'xchip') + P('M585 231l10-8M589 223h6v6', 'xarr')
    o += ''.join(P(f'M424 {y}H608', 'xgrid') for y in (262, 290, 318))
    pts = [(424, 324), (450, 318), (476, 321), (502, 306), (528, 300), (554, 284), (580, 271), (604, 252)]
    d = f'M{pts[0][0]} {pts[0][1]}'
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]; x1, y1 = pts[i]; cx = (x0 + x1) / 2
        d += f'C{cx} {y0} {cx} {y1} {x1} {y1}'
    o += G(P(d + 'V334H424Z', 'xarea bB-area') + P(d, 'xline bB-line', ' pathLength="1"') +
           G(C(604, 252, 4.5, 'xo') + C(604, 252, 1.8, 'xwf'), 'bB-dot'), 'bB-chart')
    return o


CSS_B = '''
.svx .xfav{fill:rgba(255,255,255,.22)}.svx .xfavt{fill:#19181D}.svx .xrt{fill:rgba(255,255,255,.8)}.svx .xrs{fill:rgba(255,255,255,.5);font-weight:500}.svx .xbar1{fill:rgba(255,255,255,.55)}.svx .xbar2{fill:rgba(255,255,255,.2)}.svx .xbar3{fill:rgba(255,255,255,.12)}
.svx .xacc{fill:var(--orange-soft)}.svx .xacc2{fill:#FF8A71}
.svx .xrowbg{fill:#1C1B20}.bB-glow{fill:rgba(231,81,57,.09);stroke:rgba(231,81,57,.4);stroke-width:1}
.svx .xchip{fill:rgba(231,81,57,.16)}.svx .xbolt{fill:var(--orange)}.svx .xbolt2{fill:var(--orange)}
.svx .xtrack{fill:none;stroke:rgba(255,255,255,.08);stroke-width:9}
.svx .xarc{fill:none;stroke:var(--orange);stroke-width:9;stroke-linecap:round;stroke-dasharray:100;stroke-dashoffset:4}
.svx .xvoff{fill:none;stroke:rgba(255,255,255,.18)}.svx .xvon{fill:#3A221D;stroke:rgba(231,81,57,.75)}
.svx .xchk-o{fill:none;stroke:var(--orange-soft);stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.svx .xarr{fill:none;stroke:var(--orange);stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.svx .xgrid{stroke:rgba(255,255,255,.07);stroke-dasharray:3 4}
.svx .xarea{fill:rgba(231,81,57,.14)}
.svx .xline{fill:none;stroke:var(--orange);stroke-width:2.5;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:0}
.bB-dot{transform-box:fill-box;transform-origin:50% 50%}
'''
KF_B = '''
.js .bB-arc{animation:bB-arc 9s var(--ease-out) infinite both}
@keyframes bB-arc{0%,8%{stroke-dashoffset:70}34%,90%{stroke-dashoffset:4}97%,100%{stroke-dashoffset:70}}
.js .bB-v{animation:bB-v1 9s ease infinite both}.js .bB-v2{animation-name:bB-v2}.js .bB-v3{animation-name:bB-v3}
@keyframes bB-v1{0%,15%{opacity:0}18%,90%{opacity:1}94%,100%{opacity:0}}
@keyframes bB-v2{0%,21%{opacity:0}24%,90%{opacity:1}94%,100%{opacity:0}}
@keyframes bB-v3{0%,27%{opacity:0}30%,90%{opacity:1}94%,100%{opacity:0}}
.js .bB-res{animation:bB-res 9s ease infinite both}
@keyframes bB-res{0%,90%{opacity:1}93%,96%{opacity:0}100%{opacity:1}}
.js .bB-us{animation:bB-us 9s var(--ease-io) infinite both}
@keyframes bB-us{0%,36%{transform:translateY(174px)}54%,93.5%{transform:none}94%,100%{transform:translateY(174px)}}
.js .bB-o{animation:bB-o 9s var(--ease-io) infinite both}
@keyframes bB-o{0%,38%{transform:translateY(-58px)}55%,93.5%{transform:none}94%,100%{transform:translateY(-58px)}}
.js .bB-glow{animation:bB-glow 9s ease infinite both}
@keyframes bB-glow{0%,36%{opacity:0}46%,90%{opacity:1}93%,100%{opacity:0}}
.js .bB-chart{animation:bB-res 9s ease infinite both}
.js .bB-line{animation:bB-line 9s cubic-bezier(.45,0,.2,1) infinite both}
@keyframes bB-line{0%,55%{stroke-dashoffset:1}75%,93%{stroke-dashoffset:0}95%,100%{stroke-dashoffset:1}}
.js .bB-area{animation:bB-area 9s ease infinite both}
@keyframes bB-area{0%,62%{opacity:0}78%,90%{opacity:1}93%,100%{opacity:0}}
.js .bB-dot{animation:bB-dot 9s var(--ease-out) infinite both}
@keyframes bB-dot{0%,73%{transform:scale(0)}77%{transform:scale(1.4)}80%,90%{transform:scale(1)}93%,100%{transform:scale(0)}}
'''


# ================================================================== C. WordPress Development
TILES = [(30, 102, 'Heading'), (90, 102, 'Paragraph'), (30, 158, 'Image'), (90, 158, 'Columns'), (30, 214, 'Button'), (90, 214, 'Gallery')]


def tile_icon(k, cx, cy):
    if k == 0: return T(cx, cy + 6.5, 'H', 19, 'xt xdisp', 'middle', 500)
    if k == 1: return T(cx, cy + 6, '&#182;', 17, 'xt', 'middle', 600)
    if k == 2: return R(cx - 11, cy - 8, 22, 16, 3, 'xicon-o') + P(f'M{cx - 9} {cy + 6}l6-7 4 4 3-3 6 6', 'xicon-l') + C(cx + 5, cy - 3, 2, 'xicon-f')
    if k == 3: return R(cx - 11, cy - 8, 10, 16, 2, 'xicon-o') + R(cx + 1, cy - 8, 10, 16, 2, 'xicon-o')
    if k == 4: return R(cx - 11, cy - 5, 22, 10, 5, 'xicon-o') + R(cx - 6, cy - 1, 12, 2, 1, 'xicon-f')
    return ''.join(R(cx - 10 + 11 * (i % 2), cy - 9 + 10 * (i // 2), 9, 8, 2, 'xicon-o') for i in range(4))


def scene_c():
    o = window('sxc-win')
    o += '<g clip-path="url(#sxc-win)">'
    # top bar
    o += R(30, 17, 22, 22, 6, 'xo') + P('M41 23v10M36 28h10', 'xplus')
    o += P('M68 31a6 6 0 1 1 6 4M68 31v-4.5M68 31h4.5', 'xico') + P('M98 31a6 6 0 1 0-6 4M98 31v-4.5M98 31h-4.5', 'xico')
    o += T(320, 31.5, 'Home page', 10, 'xm', 'middle', 600)
    o += R(472, 17, 58, 22, 11, 'xbtn') + T(501, 31.5, 'Preview', 9, 'xt', 'middle', 600)
    o += G(R(538, 17, 74, 22, 11, 'xo'), 'cC-pb')
    o += T(575, 31.5, 'Publish', 9.5, 'xwt cC-p1', 'middle', 700)
    o += G(check(550, 28, 'xchk-w') + T(581, 31.5, 'Published', 9, 'xwt', 'middle', 700), 'cC-p2')
    o += P('M16 46H624', 'xl') + P('M156.5 46V352', 'xl') + P('M484.5 46V352', 'xl')
    # inserter
    o += T(30, 66, 'Blocks', 10, 'xt', weight=700) + R(30, 74, 112, 18, 9, 'xin') + C(42, 83, 3.6, 'xico') + T(51, 86.2, 'Search', 8, 'xf')
    for k, (x, y, lbl) in enumerate(TILES):
        o += R(x, y, 52, 48, 8, 'xtile') + tile_icon(k, x + 26, y + 19) + T(x + 26, y + 41, lbl, 7.5, 'xm', 'middle')
    # settings panel
    o += T(500, 66, 'Page', 9.5, 'xm') + T(540, 66, 'Block', 9.5, 'xt', weight=700) + R(539, 71, 28, 2, 1, 'xo') + P('M484 80H624', 'xl')
    o += T(500, 100, 'Color', 8.5, 'xm', weight=600)
    sw = ['var(--orange)', 'var(--coral)', '#F5F4F1', '#19181D', '#77777D']
    o += ''.join(C(508 + 22 * i, 117, 7.5, 'xsw', f' style="fill:{c}"') for i, c in enumerate(sw))
    o += G(C(508, 117, 10.5, 'xring'), 'cC-ring')
    o += T(500, 150, 'Typography', 8.5, 'xm', weight=600) + R(500, 162, 108, 4, 2, 'xtrk') + R(500, 162, 60, 4, 2, 'xo') + C(560, 164, 5.5, 'xknob')
    o += T(500, 194, 'Spacing', 8.5, 'xm', weight=600)
    o += R(500, 202, 50, 20, 6, 'xin') + T(510, 215.5, '24', 8.5, 'xt') + R(558, 202, 50, 20, 6, 'xin') + T(568, 215.5, '16', 8.5, 'xt')
    o += T(500, 248, 'Open in new tab', 8.5, 'xm', weight=600) + R(586, 239, 22, 12, 6, 'xo') + C(602, 245, 4, 'xwf')
    # canvas
    o += R(172, 58, 298, 284, 10, 'xpage')
    o += G(T(188, 92, 'Type / to choose a block', 10, 'xf') + R(187, 82, 1.2, 13, 0, 'xcaret'), 'cC-ph')
    blocks = [
        T(188, 101, 'The Bag Collection', 27, 'xt xdisp', weight=500),
        # the supplied banner, whole and at its own proportions (2.13:1): the image area is 94 high,
        # so it is 200 wide, left-aligned with the heading and the button
        photo('wp-banner', 188, 114, 200, 94, 8, 'sxc-p1', box=(0, 0, 760, 357)),
        ''.join(R(x, 218, 129, 64, 8, 'xcol') + photo(slug, x + 8, 226, 26, 26, 5, f'sxc-c{k}', fill=.92) +
                T(x + 42, 236, name, 8, 'xt', weight=700) + T(x + 42, 247.5, price, 7.5, 'xacc') +
                T(x + 8, 266.5, l1, 6.5, 'xrs') + T(x + 8, 275.5, l2, 6.5, 'xrs')
                for k, (x, slug, name, price, l1, l2) in enumerate(((188, 'burgundy-tote', 'Bordeaux Tote', '$240', 'Saffiano leather with a gold', 'padlock charm and suede lining.'),
                                                                     (325, 'noir-bag', 'Noir Top Handle', '$215', 'Pebbled black leather, gold', 'turn-lock and a detachable strap.')))),
        R(188, 294, 108, 28, 14, 'xo') + T(242, 311.5, 'Shop the edit', 9.5, 'xwt', 'middle', 700),
    ]
    boxes = [(184, 74, 274, 34), (184, 110, 274, 102), (184, 214, 274, 72), (184, 290, 116, 36)]
    for k, blk in enumerate(blocks):
        bx, by, bw, bh = boxes[k]
        o += R(188, by - 2, 266, 2, 1, f'xo cC-ins cC-ins{k}')
        o += G(blk, f'cC-b cC-b{k}')
        o += R(bx, by, bw, bh, 8, f'xsel cC-sel cC-sel{k}')
    # dragged tiles
    targets = [(230, 88), (320, 160), (320, 250), (242, 308)]
    for k, ti in enumerate([0, 5, 3, 4]):
        x, y, _ = TILES[ti]
        dx, dy = targets[k][0] - (x + 26), targets[k][1] - (y + 24)
        o += G(R(x, y, 52, 48, 8, 'xtile xghost') + tile_icon(ti, x + 26, y + 19), f'cC-g cC-g{k}', f' style="--dx:{dx}px;--dy:{dy}px"')
    # toast
    o += G(R(26, 304, 140, 32, 10, 'xtoast') + C(46, 320, 7, 'xo') + check(46, 320, 'xchk-w') + T(60, 323.4, 'Page published', 9.5, 'xt', weight=600), 'cC-toast')
    o += G(G(CURSOR, 'cC-press'), 'cC-cur')
    o += '</g>'
    return o


CSS_C = '''
.svx .xplus{stroke:#fff;stroke-width:2;stroke-linecap:round}
.svx .xtile{fill:rgba(255,255,255,.045);stroke:rgba(255,255,255,.1)}
.svx .xghost{fill:#2C2A31;stroke:var(--orange);stroke-width:1.2}
.svx .xicon-o{fill:none;stroke:rgba(255,255,255,.78);stroke-width:1.5}.svx .xicon-l{fill:none;stroke:rgba(255,255,255,.78);stroke-width:1.5;stroke-linejoin:round}.svx .xicon-f{fill:rgba(255,255,255,.78)}
.svx .xsw{stroke:rgba(255,255,255,.2)}.svx .xring{fill:none;stroke:#fff;stroke-width:1.5}
.svx .xtrk{fill:rgba(255,255,255,.12)}.svx .xknob{fill:#fff}
.svx .xpage{fill:#24222A}
.svx .xcaret{fill:var(--orange)}
.svx .xcol{fill:rgba(255,255,255,.045);stroke:rgba(255,255,255,.1)}
.svx .xsel{fill:none;stroke:var(--orange);stroke-width:1.5}
.svx .xtoast{fill:#322F37;stroke:rgba(255,255,255,.14)}
.cC-p1,.cC-ph,.cC-g,.cC-ins,.cC-sel{opacity:0}
.cC-pb{transform-box:fill-box;transform-origin:50% 50%}
.cC-cur{transform:translate(580px,30px)}
'''


def kf_c():
    s = [6, 20, 34, 48]
    out = '''
.js .cC-cur{animation:cC-cur 11s cubic-bezier(.5,0,.25,1) infinite both}
@keyframes cC-cur{0%{transform:translate(320px,390px)}4%,6%{transform:translate(56px,128px)}12%{transform:translate(230px,92px)}18%,20%{transform:translate(116px,240px)}26%{transform:translate(320px,164px)}32%,34%{transform:translate(116px,184px)}40%{transform:translate(320px,254px)}46%,48%{transform:translate(56px,240px)}54%{transform:translate(242px,312px)}62%,72%{transform:translate(580px,30px)}82%,100%{transform:translate(660px,390px)}}
.js .cC-press{animation:cC-press 11s ease infinite both}
@keyframes cC-press{0%,4.5%,6.5%,18.5%,20.5%,32.5%,34.5%,46.5%,48.5%,63%,65.5%,100%{transform:scale(1)}5.5%,19.5%,33.5%,47.5%,64.2%{transform:scale(.8)}}
.js .cC-ph{animation:cC-ph 11s ease infinite both}
@keyframes cC-ph{0%,9%{opacity:1}11%,95%{opacity:0}98%,100%{opacity:1}}
.js .cC-p1{animation:cC-p1 11s ease infinite both}
.js .cC-p2{animation:cC-p2 11s ease infinite both}
@keyframes cC-p1{0%,64.5%{opacity:1}65.5%,95%{opacity:0}97%,100%{opacity:1}}
@keyframes cC-p2{0%,64.5%{opacity:0}65.5%,95%{opacity:1}97%,100%{opacity:0}}
.js .cC-pb{animation:cC-pb 11s ease infinite both}
@keyframes cC-pb{0%,63.8%,65.5%,100%{transform:scale(1)}64.6%{transform:scale(.94)}}
.js .cC-toast{animation:cC-toast 11s var(--ease-out) infinite both}
@keyframes cC-toast{0%,66%{opacity:0;transform:translateY(46px)}70%,88%{opacity:1;transform:none}92%,100%{opacity:0;transform:translateY(46px)}}
.js .cC-ring{animation:cC-ring 11s var(--ease-io) infinite both}
@keyframes cC-ring{0%,55%{transform:translateX(22px)}59%,100%{transform:none}}
.js .cC-b,.js .cC-g,.js .cC-ins,.js .cC-sel{animation-duration:11s;animation-iteration-count:infinite;animation-fill-mode:both}
'''
    for k, t in enumerate(s):
        out += (f'.js .cC-g{k}{{animation-name:cC-g{k};animation-timing-function:cubic-bezier(.5,0,.25,1)}}\n'
                f'@keyframes cC-g{k}{{0%,{t - 1}%{{opacity:0;transform:none}}{t}%{{opacity:1;transform:none}}{t + 6}%{{opacity:1;transform:translate(var(--dx),var(--dy))}}{t + 7}%,100%{{opacity:0;transform:translate(var(--dx),var(--dy))}}}}\n'
                f'.js .cC-ins{k}{{animation-name:cC-ins{k};animation-timing-function:ease}}\n'
                f'@keyframes cC-ins{k}{{0%,{t + 3}%{{opacity:0}}{t + 4}%,{t + 6}%{{opacity:1}}{t + 7}%,100%{{opacity:0}}}}\n'
                f'.js .cC-b{k}{{animation-name:cC-b{k};animation-timing-function:var(--ease-out)}}\n'
                f'@keyframes cC-b{k}{{0%,{t + 6}%{{opacity:0;transform:translateY(8px)}}{t + 9}%,92%{{opacity:1;transform:none}}95%,100%{{opacity:0;transform:none}}}}\n'
                f'.js .cC-sel{k}{{animation-name:cC-sel{k};animation-timing-function:ease}}\n'
                f'@keyframes cC-sel{k}{{0%,{t + 6}%{{opacity:0}}{t + 7}%,{t + 12}%{{opacity:1}}{t + 13}%,100%{{opacity:0}}}}\n')
    return out


# ================================================================== D. Custom Development
LINE_WINDOWS = [(0, 5), None, (6, 12), (12, 21), (21, 28), (28, 34), (34, 35.5)]
CODE = [
    [('import', 'ck'), (' { Chart } ', 'ci'), ('from', 'ck'), (" './chart'", 'cs')],
    [],
    [('export async function', 'ck'), (' Orders', 'cw'), ('() {', 'cp')],
    [('  const', 'ck'), (' res = ', 'ci'), ('await', 'ck'), (' fetch(', 'ci'), ("'/api/orders'", 'cs'), (')', 'cp')],
    [('  const', 'ck'), (' data = ', 'ci'), ('await', 'ck'), (' res.json()', 'ci')],
    [('  return', 'ck'), (' &lt;Chart', 'cj'), (' data={data}', 'ci'), (' /&gt;', 'cj')],
    [('}', 'cp')],
]


def scene_d():
    o = window('sxd-ed', 16, 16, 320, 328, 'xed')
    o += '<g clip-path="url(#sxd-ed)">'
    o += R(28, 22, 94, 22, 6, 'xtab') + C(40, 33, 3, 'xo') + T(48, 36.5, 'orders.tsx', 9, 'xt xmono') + T(134, 36.5, 'chart.tsx', 9, 'xm xmono')
    o += G(C(314, 31, 9, 'xo') + P('M311 26.5v9l7.5-4.5z', 'xwf'), 'dD-run')
    o += P('M16 44H336', 'xl')
    for n, segs in enumerate(CODE):
        y = 70 + 22 * n
        o += T(40, y, str(n + 1), 9, 'xf xmono', 'end')
        if segs:
            o += '<text x="52" y="%s" font-size="10" class="xmono" xml:space="preserve">' % y + ''.join(f'<tspan class="{c}">{t}</tspan>' for t, c in segs) + '</text>'
            o += R(50, y - 12, 286, 17, 0, f'xedbg dD-cv dD-cv{n}')
    o += R(58, 197, 1.6, 12, 0, 'xcaret dD-caret')
    o += P('M16 228H336', 'xl') + T(32, 247, 'TERMINAL', 8, 'xm', weight=700)
    o += T(32, 268, '$ npm run dev', 9, 'xm xmono') + T(32, 288, 'GET /api/orders', 9, 'xt xmono dD-t1') + T(32, 308, '200 OK', 9, 'xacc xmono dD-t2')
    o += '</g>'
    # app card
    o += R(352, 16, 272, 134, 14, 'xw') + T(368, 40, 'Orders', 11, 'xt', weight=700) + T(368, 54, 'This week', 8.5, 'xm')
    o += G(R(552, 26, 58, 18, 9, 'xchip') + T(581, 38.4, '200 OK', 8.5, 'xacc xmono', 'middle', 700), 'dD-chip')
    o += ''.join(P(f'M368 {y}H608', 'xgrid') for y in (80, 108))
    hs = [30, 44, 36, 54, 46, 64, 58, 74]
    o += ''.join(R(370 + 30 * i, 138 - h, 18, h, 3, 'xbarc' + (' xo' if i == 7 else ''), f' style="--i:{i}"') for i, h in enumerate(hs))
    # links
    o += P('M488 150V182', 'xlink') + P('M488 230V262', 'xlink') + P('M408 206H438', 'xlink') + P('M538 206H568', 'xlink')
    o += C(488, 150, 4.5, 'xo dD-req') + C(488, 262, 4.5, 'xwf dD-res') + C(408, 206, 3.5, 'xo dD-auth')
    # nodes
    o += R(434, 178, 108, 56, 14, 'xglow dD-glow')
    o += R(438, 182, 100, 48, 12, 'xnode') + T(488, 206, 'API', 17, 'xt xdisp', 'middle', 500) + T(488, 221, '/api/orders', 7.5, 'xm xmono', 'middle')
    o += C(392, 206, 16, 'xnode2') + C(388, 203, 4.5, 'xico') + P('M391.5 206.5l7 7M396 211l2-2', 'xico') + T(392, 236, 'Auth', 8, 'xm', 'middle', 600)
    o += C(584, 206, 16, 'xnode2') + R(576, 200, 16, 12, 2, 'xico') + P('M576 201.5l8 5.5 8-5.5', 'xico') + T(584, 236, 'Email', 8, 'xm', 'middle', 600)
    o += P('M458 270v40a30 8 0 0 0 60 0v-40', 'xdb') + '<ellipse cx="488" cy="270" rx="30" ry="8" class="xdbt"/>' + P('M458 290a30 8 0 0 0 60 0', 'xdbl')
    o += T(488, 336, 'Database', 8.5, 'xm', 'middle', 600)
    return o


CSS_D = '''
.svx .xed{fill:#141317;stroke:rgba(255,255,255,.1)}.svx .xedbg{fill:#141317}
.svx .xtab{fill:#232127}
.svx .xmono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-weight:500}
.svx .ck{fill:#FF8A71}.svx .ci{fill:rgba(255,255,255,.72)}.svx .cs{fill:#F2E3D5}.svx .cp{fill:rgba(255,255,255,.45)}.svx .cw{fill:#fff}.svx .cj{fill:var(--coral)}
.svx .xbarc{fill:rgba(255,255,255,.2);transform-box:fill-box;transform-origin:50% 100%}.svx .xbarc.xo{fill:var(--orange)}
.svx .xlink{stroke:rgba(255,255,255,.2);stroke-dasharray:3 3}
.svx .xnode{fill:#232127;stroke:rgba(231,81,57,.6)}.svx .xnode2{fill:#232127;stroke:rgba(255,255,255,.14)}
.svx .xglow{fill:rgba(231,81,57,.16)}
.svx .xdb{fill:#232127;stroke:rgba(255,255,255,.22)}.svx .xdbt{fill:#2C2A31;stroke:rgba(255,255,255,.22)}.svx .xdbl{fill:none;stroke:rgba(255,255,255,.16)}
.dD-cv{transform:translateX(290px)}
.dD-req,.dD-res,.dD-auth,.dD-glow{opacity:0}
.dD-chip,.dD-run{transform-box:fill-box;transform-origin:50% 50%}
'''
KF_D = '''
.js .dD-caret{animation:dD-blink 1s steps(1,end) infinite}
@keyframes dD-blink{50%{opacity:0}}
.js .dD-run{animation:dD-run 9s ease infinite both}
@keyframes dD-run{0%,36%,39%,100%{transform:scale(1)}37.5%{transform:scale(.8)}}
.js .dD-t1{animation:dD-t1 9s ease infinite both}
@keyframes dD-t1{0%,39%{opacity:0}41%,90%{opacity:1}93%,100%{opacity:0}}
.js .dD-t2{animation:dD-t2 9s ease infinite both}
@keyframes dD-t2{0%,70%{opacity:0}72%,90%{opacity:1}93%,100%{opacity:0}}
.js .dD-req{animation:dD-req 9s cubic-bezier(.45,0,.55,1) infinite both}
@keyframes dD-req{0%,40%{opacity:0;transform:none}41%{opacity:1;transform:none}56%{opacity:1;transform:translateY(112px)}57%,100%{opacity:0;transform:translateY(112px)}}
.js .dD-auth{animation:dD-auth 9s ease-in-out infinite both}
@keyframes dD-auth{0%,43%{opacity:0;transform:none}44%{opacity:1;transform:none}49%{opacity:1;transform:translateX(30px)}50%,100%{opacity:0;transform:translateX(30px)}}
.js .dD-res{animation:dD-res 9s cubic-bezier(.45,0,.55,1) infinite both}
@keyframes dD-res{0%,57%{opacity:0;transform:none}58%{opacity:1;transform:none}71%{opacity:1;transform:translateY(-112px)}72%,100%{opacity:0;transform:translateY(-112px)}}
.js .dD-glow{animation:dD-glow 9s ease infinite both}
@keyframes dD-glow{0%,44%{opacity:0}47%{opacity:1}52%,60%{opacity:0}63%{opacity:1}68%,100%{opacity:0}}
.js .dD-chip{animation:dD-chip 9s var(--ease-out) infinite both}
@keyframes dD-chip{0%,71%{transform:scale(0)}74%{transform:scale(1.2)}77%,91%{transform:scale(1)}94%,100%{transform:scale(0)}}
.js .svx .xbarc{animation:dD-bar 9s var(--ease-out) infinite both;animation-delay:calc(var(--i) * .08s)}
@keyframes dD-bar{0%,72%{transform:scaleY(.06)}84%,91%{transform:none}96%,100%{transform:scaleY(.06)}}
'''


def kf_d():
    """Each line of code is uncovered in typing steps inside its own slice of the loop."""
    out = KF_D
    for n, w in enumerate(LINE_WINDOWS):
        if not w:
            continue
        a, b = w
        chars = sum(len(re.sub('&[a-z]+;', 'x', t)) for t, _ in CODE[n])
        out += (f'.js .dD-cv{n}{{animation:dD-l{n} 9s steps({chars},end) infinite both}}\n'
                f'@keyframes dD-l{n}{{0%,{a}%{{transform:none}}{b}%,91%{{transform:translateX({chars * 6.05 + 4:.0f}px)}}94%,100%{{transform:none}}}}\n')
    return out


# ================================================================== E. UI/UX & Digital Design


def phone(x, wire, hi):
    return (R(x, 18, 164, 324, 26, 'xph') + R(x + 8, 26, 148, 308, 19, 'xscr') + wire + hi + R(x + 62, 32, 40, 8, 4, 'xnotch'))


def scene_e():
    o = ('<defs><pattern id="sxe-dots" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".9" class="xdotp"/></pattern></defs>'
         + R(16, 8, 608, 344, 14, 'xcanvas') + R(16, 8, 608, 344, 14, '', ' fill="url(#sxe-dots)"'))
    # styles column
    o += T(34, 34, 'Styles', 9.5, 'xt', weight=700)
    o += C(44, 58, 10, 'xo') + C(70, 58, 10, 'xsw2', ' style="fill:var(--coral)"') + C(44, 84, 10, 'xsw2', ' style="fill:#F5F4F1"') + C(70, 84, 10, 'xsw2', ' style="fill:#19181D"')
    o += T(32, 140, 'Aa', 34, 'xt xdisp', weight=500) + T(34, 156, 'Display', 8, 'xm')
    o += T(33, 188, 'Aa', 18, 'xt', weight=700) + T(34, 202, 'Text', 8, 'xm')
    o += R(34, 222, 72, 22, 11, 'xo') + T(70, 236.5, 'Button', 8.5, 'xwt', 'middle', 700)
    o += R(34, 252, 72, 22, 11, 'xbtn') + T(70, 266.5, 'Button', 8.5, 'xt', 'middle', 700)
    o += R(34, 284, 26, 14, 7, 'xo') + C(53, 291, 5, 'xwf') + R(66, 284, 26, 14, 7, 'xtrk') + C(73, 291, 5, 'xknob')
    # Both phones share one layout: content sits 12 units inside the screen on each side (the screen
    # is x+8..x+156, so content is x+20..x+144, 124 wide), the header icons and the centred brand sit
    # on one line under the notch, and the call to action keeps its line (y 288..318) so the cursor,
    # the tap ripple and the prototype link land where they always did.
    BRAND = 'LUM&#201;RA'
    HY = 58                                     # header line (centre)
    BTN_Y, BTN_H = 288, 30

    def brand(cx):                              # letter-spacing is added after every glyph, so nudge right by half of it
        return T(cx + 1.1, HY + 3.6, BRAND, 10, 'xt', 'middle', 700, ' style="letter-spacing:2.2px"')

    def bag(r):                                 # shopping bag icon whose right edge (with stroke) is r
        return P(f'M{r - 11.2} {HY - 2.5}h10.4l-.9 8.7h-8.6ZM{r - 8.5} {HY - 2.5}v-1.4a2.5 2.5 0 0 1 5 0v1.4', 'xnavl')

    def cta(l, label):
        return R(l, BTN_Y, 124, BTN_H, 15, 'xo') + T(l + 62, BTN_Y + 18.5, label, 9.5, 'xwt', 'middle', 700)

    # phone 1: collection / home
    x = 160
    L, RE, CX = x + 20, x + 144, x + 82
    HERO_Y, HERO_H = 72, 116
    TB = HERO_Y + HERO_H + 18                   # collection title baseline (13.5: 119 of the 124 units)
    SB = TB + 12                                # subtitle baseline
    TY, TS = SB + 10, 38                        # thumbnails: three 38-unit squares, 5 apart
    thumbs = [L + (TS + 5) * i for i in range(3)]
    w1 = [P(f'M{L + .8} {HY - 2.5}h11M{L + .8} {HY + 2.5}h11', 'xwl') + R(CX - 20, HY - 4.5, 40, 9, 3, 'xwf1') + R(RE - 11, HY - 5, 11, 10, 3, 'xwf1'),
          R(L, HERO_Y, 124, HERO_H, 12, 'xwbox') + P(f'M{L} {HERO_Y}L{RE} {HERO_Y + HERO_H}M{RE} {HERO_Y}L{L} {HERO_Y + HERO_H}', 'xwl'),
          R(L, TB - 11, 100, 12, 3, 'xwf1') + R(L, SB - 5, 92, 5, 2.5, 'xwf2'),
          ''.join(R(tx, TY, TS, TS, 8, 'xwbox') for tx in thumbs),
          R(L, BTN_Y, 124, BTN_H, 15, 'xwbox') + R(CX - 24, BTN_Y + 13, 48, 4, 2, 'xwf1')]
    h1 = [
        P(f'M{L + .8} {HY - 2.5}h11M{L + .8} {HY + 2.5}h11', 'xnavl') + brand(CX) + bag(RE),
        photo('serum-hydrating', L, HERO_Y, 124, HERO_H, 12, 'sxe-hero', box=(0, 12, 640, round(640 * HERO_H / 124, 1))) +
        R(L + 8, HERO_Y + 8, 30, 14, 7, 'xtag') + T(L + 23, HERO_Y + 18, 'New', 8, 'xwt', 'middle', 700),
        T(L, TB, 'Skincare Essentials', 13.5, 'xt xdisp', weight=500) + T(L, SB, 'Serums for every skin type', 7.5, 'xm'),
        ''.join(photo(slug, tx, TY, TS, TS, 8, f'sxe-t{i}', box=(0, 0, 640, 640))
                for i, (tx, slug) in enumerate(zip(thumbs, ('serum-brightening', 'serum-retinol-night', 'serum-retinol')))),
        cta(L, 'Shop now'),
    ]
    p1 = ''.join(G(w1[k], f'eE-w eE-w{k}') + G(h1[k], f'eE-h eE-h{k}') for k in range(5))
    grid = G(''.join(R(L + 33 * i, 26, 25, 308, 0, 'xgridc') for i in range(4)), 'eE-grid')
    sel = G(R(L - 1, HERO_Y - 1, 126, HERO_H + 2, 0, 'xsel') +
            ''.join(R(px - 2.5, py - 2.5, 5, 5, 0, 'xhandle') for px in (L - 1, RE + 1) for py in (HERO_Y - 1, HERO_Y + HERO_H + 1)) +
            R(CX - 22, HERO_Y + HERO_H - 17, 44, 13, 3, 'xo') + T(CX, HERO_Y + HERO_H - 7.6, f'124 &#215; {HERO_H}', 7, 'xwt xmono', 'middle'), 'eE-sel')
    o += phone(x, '', p1 + grid + sel)
    # phone 2: product page for the featured serum
    x2 = 392
    L2, RE2, CX2 = x2 + 20, x2 + 144, x2 + 82
    IMG_Y = 72                                  # 124-unit square, the whole photo
    PT = IMG_Y + 124 + 18                       # product title, two lines as on the bottle; price on line one
    PT2 = PT + 17
    PR = PT2 + 13                               # subtitle
    SY = PR + 8                                 # size pills
    pill = (124 - 12) / 3
    w2 = (R(L2, HY - 5, 9, 10, 3, 'xwf1') + R(CX2 - 20, HY - 4.5, 40, 9, 3, 'xwf1') + R(RE2 - 11, HY - 5, 11, 10, 3, 'xwf1') +
          R(L2, IMG_Y, 124, 124, 12, 'xwbox') + P(f'M{L2} {IMG_Y}L{RE2} {IMG_Y + 124}M{RE2} {IMG_Y}L{L2} {IMG_Y + 124}', 'xwl') +
          R(L2, PT - 11, 64, 12, 3, 'xwf1') + R(RE2 - 20, PT - 9, 20, 9, 3, 'xwf1') + R(L2, PT2 - 11, 76, 12, 3, 'xwf1') + R(L2, PR - 5, 72, 5, 2.5, 'xwf2') +
          ''.join(R(round(L2 + (pill + 6) * i, 2), SY, round(pill, 2), 18, 9, 'xwbox') for i in range(3)) + R(L2, BTN_Y, 124, BTN_H, 15, 'xwbox'))
    h2 = (P(f'M{L2 + 6} {HY - 5}l-5 5 5 5', 'xnavl') + brand(CX2) + bag(RE2) +
          photo('serum-hydrating', L2, IMG_Y, 124, 124, 12, 'sxe-pdp', box=(0, 0, 640, 640)) +
          T(L2, PT, 'Hydrating', 15, 'xt xdisp', weight=500) + T(RE2, PT, '$42', 11, 'xt', 'end', 700) +
          T(L2, PT2, 'Face Serum', 15, 'xt xdisp', weight=500) + T(L2, PR, 'Hyaluronic Acid + B5', 7.5, 'xm') +
          ''.join(R(round(L2 + (pill + 6) * i, 2), SY, round(pill, 2), 18, 9, 'xsize' + (' xsize-on' if i == 0 else '')) +
                  T(round(L2 + (pill + 6) * i + pill / 2, 2), SY + 12, sz, 7.5, 'xt' if i == 0 else 'xm', 'middle', 700) for i, sz in enumerate(('30 ml', '50 ml', '100 ml'))) +
          cta(L2, 'Add to bag'))
    o += phone(x2, '', G(w2, 'eE-p2w') + G(h2, 'eE-p2h'))
    # prototype link: from the end of the Shop now button to the product screen
    o += G(P(f'M{RE} 303C{RE + 52} 303 340 120 392 120', 'xnoodle eE-noodle', ' pathLength="1"') + C(RE, 303, 4, 'xo') + G(P('M384 115l8 5-8 5', 'xarrow'), 'eE-head'), 'eE-proto')
    o += C(242, 303, 7, 'xrip eE-rip')
    o += G(G(CURSOR, 'eE-press'), 'eE-cur')
    return o


CSS_E = '''
.svx .xcanvas{fill:#17161B;stroke:rgba(255,255,255,.1)}.svx .xdotp{fill:rgba(255,255,255,.08)}
.svx .xsw2{stroke:rgba(255,255,255,.2)}
.svx .xph{fill:#0E0D11;stroke:rgba(255,255,255,.2);stroke-width:1.5}.svx .xscr{fill:#1F1E23}.svx .xnotch{fill:#0E0D11}
.svx .xwf1{fill:rgba(255,255,255,.16)}.svx .xwf2{fill:rgba(255,255,255,.1)}.svx .xwl{stroke:rgba(255,255,255,.16);fill:none}
.svx .xwbox{fill:none;stroke:rgba(255,255,255,.28);stroke-dasharray:4 3}
.svx .xtag{fill:#19181D}
.svx .xnavl{fill:none;stroke:rgba(255,255,255,.8);stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.svx .xsize{fill:none;stroke:rgba(255,255,255,.2)}.svx .xsize-on{stroke:var(--orange);fill:rgba(231,81,57,.14)}
.svx .xgridc{fill:rgba(231,81,57,.1)}
.svx .xhandle{fill:#fff;stroke:var(--orange);stroke-width:1.2}
.svx .xnoodle{fill:none;stroke:var(--orange);stroke-width:2;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:0}
.svx .xarrow{fill:none;stroke:var(--orange);stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.svx .xrip{fill:none;stroke:#fff;stroke-width:1.5;opacity:0;transform-box:fill-box;transform-origin:50% 50%}
.eE-w,.eE-p2w,.eE-grid,.eE-sel{opacity:0}
.eE-cur{transform:translate(284px,310px)}
'''
KF_E = '''
.js .eE-cur{animation:eE-cur 10s cubic-bezier(.5,0,.25,1) infinite both}
@keyframes eE-cur{0%,4%{transform:translate(660px,390px)}14%,40%{transform:translate(236px,124px)}56%,68%{transform:translate(284px,310px)}80%,100%{transform:translate(660px,390px)}}
.js .eE-press{animation:eE-press 10s ease infinite both}
@keyframes eE-press{0%,15%,17.5%,61%,64%,100%{transform:scale(1)}16.3%,62.5%{transform:scale(.8)}}
.js .eE-grid{animation:eE-grid 10s ease infinite both}
@keyframes eE-grid{0%,6%{opacity:0}12%,44%{opacity:1}50%,100%{opacity:0}}
.js .eE-sel{animation:eE-sel 10s ease infinite both}
@keyframes eE-sel{0%,16.5%{opacity:0}18%,40%{opacity:1}44%,100%{opacity:0}}
.js .eE-w,.js .eE-h{animation-duration:10s;animation-iteration-count:infinite;animation-fill-mode:both;animation-timing-function:ease}
.js .eE-rip{animation:eE-rip 10s var(--ease-out) infinite both}
@keyframes eE-rip{0%,62%{opacity:0;transform:scale(.5)}63%{opacity:.9;transform:scale(.8)}69%,100%{opacity:0;transform:scale(3.2)}}
.js .eE-noodle{animation:eE-noodle 10s cubic-bezier(.45,0,.2,1) infinite both}
@keyframes eE-noodle{0%,48%{stroke-dashoffset:1}58%,90%{stroke-dashoffset:0}94%,100%{stroke-dashoffset:1}}
.js .eE-proto>circle,.js .eE-head{animation:eE-head 10s ease infinite both}
.js .eE-proto>circle{animation-name:eE-dot}
@keyframes eE-head{0%,57%{opacity:0}59%,90%{opacity:1}94%,100%{opacity:0}}
@keyframes eE-dot{0%,47%{opacity:0}48%,90%{opacity:1}94%,100%{opacity:0}}
.js .eE-p2w{animation:eE-p2w 10s ease infinite both}
@keyframes eE-p2w{0%,66%{opacity:1}70%,93%{opacity:0}97%,100%{opacity:1}}
.js .eE-p2h{animation:eE-p2h 10s var(--ease-out) infinite both}
@keyframes eE-p2h{0%,66%{opacity:0;transform:translateX(22px)}74%,90%{opacity:1;transform:none}94%,100%{opacity:0;transform:none}}
'''


def kf_e():
    out = KF_E
    for k in range(5):
        t = 20 + 5 * k if k else 34
        out += (f'.js .eE-w{k}{{animation-name:eE-w{k}}}@keyframes eE-w{k}{{0%,{t}%{{opacity:1}}{t + 4}%,90%{{opacity:0}}94%,100%{{opacity:1}}}}\n'
                f'.js .eE-h{k}{{animation-name:eE-h{k}}}@keyframes eE-h{k}{{0%,{t}%{{opacity:0}}{t + 4}%,90%{{opacity:1}}94%,100%{{opacity:0}}}}\n')
    return out


SCENES = [
    ('a', scene_a(), '62% 26%', 'Illustration: a Shopify storefront of leather bags where a shopper adds the black top handle bag to the cart, the cart opens and the order is placed'),
    ('b', scene_b(), '70% 30%', 'Illustration: the North&amp;Co store\'s speed score rising, its Linen Shirts page climbing from fourth to first in search results for linen shirts, and conversions growing'),
    ('c', scene_c(), '58% 24%', 'Illustration: a WordPress block editor where a heading, a Luxury Bags banner, two product columns for the Bordeaux Tote and Noir Top Handle bags and a button are dragged in to build a page that is then published'),
    ('d', scene_d(), '66% 22%', 'Illustration: code calling a custom API that reads the database and returns data to an app chart'),
    ('e', scene_e(), '60% 28%', 'Illustration: a mobile wireframe for a skincare store turned into the finished design, with the Hydrating Face Serum as the featured product and three more serums below, then linked to its product page as a prototype'),
]


def scene_html(key, body, light, label):
    return (f'<div class="svc__media media svx svx--{key}" style="--light:{light}" role="img" aria-label="{label}">'
            f'<div class="svx__scene" aria-hidden="true"><svg viewBox="0 0 640 360" focusable="false">{body}</svg></div></div>')


CSS = '''
/* Services: one flat interface scene per service, each telling what the service does (storefront
   and cart, speed and ranking, block editor, code to API to data, wireframe to prototype). The
   base styles are the finished frame; loops only run while the scene can be seen (.is-live). */
.svc__media.svx{container-type:size;background:var(--black);box-shadow:inset 0 0 0 1px rgba(255,255,255,.1)}
.svx__scene{position:absolute;left:5%;right:5%;top:22%;bottom:5%;pointer-events:none}
.svx__scene>svg{display:block;width:100%;height:100%;overflow:visible}
@media (min-width:1024px){.svx__scene{left:3%;right:0;top:15%;bottom:31%}}
.svx-managed .svx:not(.is-on) .svx__scene{display:none}
.svx text{font-family:var(--body);font-weight:600;letter-spacing:0}
.svx .xdisp{font-family:var(--display)}
.svx .xt{fill:rgba(255,255,255,.9)}.svx .xm{fill:rgba(255,255,255,.52)}.svx .xf{fill:rgba(255,255,255,.3)}.svx .xwt{fill:#fff}
.svx .xw{fill:#1C1B20;stroke:rgba(255,255,255,.12)}
.svx .xl{stroke:rgba(255,255,255,.09);fill:none}
.svx .xdot{fill:rgba(255,255,255,.16)}.svx .xpill{fill:rgba(255,255,255,.06)}
.svx .xin{fill:rgba(255,255,255,.05);stroke:rgba(255,255,255,.12)}
.svx .xo{fill:var(--orange)}.svx .xwf{fill:#fff}
.svx .xico{fill:none;stroke:rgba(255,255,255,.72);stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.svx .xbtn{fill:none;stroke:rgba(255,255,255,.24)}
.svx .xchk,.svx .xchk-w{fill:none;stroke:#fff;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.svx .xcur{fill:#fff;stroke:#19181D;stroke-width:1.2;stroke-linejoin:round}
.svx .xcaret{fill:var(--orange)}
''' + CSS_A + CSS_B + CSS_C + CSS_D + CSS_E + '''
@media (prefers-reduced-motion:no-preference){
  .js .svc .svx:not(.is-live) *{animation-play-state:paused}
''' + KF_A + KF_B + kf_c() + kf_d() + kf_e() + '''
}
'''


if __name__ == '__main__':
    body = (ROOT / 'src/02-body.html').read_text()
    olds = re.findall(r'<div class="svc__media media svx[^"]*"[^>]*><div class="svx__scene" aria-hidden="true">(?:<div class="svx__tilt">.*?</div></div></div></div>|<svg.*?</svg></div></div>)', body)
    assert len(olds) == 5, len(olds)
    for old, (key, html, light, label) in zip(olds, SCENES):
        body = body.replace(old, scene_html(key, html, light, label), 1)
    (ROOT / 'src/02-body.html').write_text(body)
    head = (ROOT / 'src/01-head.html').read_text()
    start, end = '/* SVX:START */', '/* SVX:END */'
    block = start + '\n' + CSS.strip() + '\n' + end
    assert start in head
    head = re.sub(re.escape(start) + r'.*?' + re.escape(end), lambda m: block, head, flags=re.S)
    (ROOT / 'src/01-head.html').write_text(head)
    print('services scenes written;', len(block) // 1024, 'KB css;', sum(len(s[1]) for s in SCENES) // 1024, 'KB svg')
