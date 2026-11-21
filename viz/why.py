"""Why: four promises, each told by its own animated scene.

1  One team, from design to code   the design file and the live site sit under one wipe: the divider
                                   sweeps across and every edge lines up; on the live side the button
                                   really responds to the pointer.
2  Fast by default                 a network waterfall: a slow page loads, then four optimisations are
                                   applied one by one and the "page ready" line moves from 3.6s to 0.9s.
3  Built to be found, and chosen   the page's own markup (title, meta, alt, schema) builds its search
                                   result piece by piece; the searcher picks it and an enquiry arrives.
4  Finished properly, delivered    a delivery board: each task passes its QA checks before it moves to
   as planned                      Done, the milestone fills and closes on its due date.

Every scene is drawn on a 480 x 300 grid. Base styles are the finished frame (reduced motion and no
script see a complete picture); the loops run only while the card is on screen (.is-live) and only
animate transform, opacity, stroke-dashoffset and, for the wipe, clip-path.
Writes the markup between <!-- WHY:START/END --> in src/02-body.html and the CSS between
/* WHY:START/END */ in src/01-head.html."""
import pathlib, re
from products import photo

ROOT = pathlib.Path(__file__).resolve().parent.parent
EO = 'cubic-bezier(.23,1,.32,1)'
IO = 'cubic-bezier(.77,0,.175,1)'
SOFT = 'cubic-bezier(.4,0,.2,1)'
WIPE = 'cubic-bezier(.65,0,.35,1)'


def T(x, y, s, size, cls='wt', anchor=None, extra=''):
    a = f' text-anchor="{anchor}"' if anchor else ''
    return f'<text x="{x}" y="{y}" font-size="{size}" class="{cls}"{a}{extra}>{s}</text>'


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


def svg(inner, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<svg{c} viewBox="0 0 480 300" aria-hidden="true" focusable="false">{inner}</svg>'


def pc(t, T):
    v = max(0.0, min(100.0, t / T * 100))
    return f'{v:.2f}'.rstrip('0').rstrip('.') + '%'


CURSOR = 'M0 0L0 17L4.6 13.1L7.6 20.2L10.7 18.9L7.8 12.1L13.4 12.1Z'
CHECK = 'M-3.6 .2L-1.1 2.7L3.8-2.4'


def check(x, y, cls='wchk', s=1):
    sc = f' scale({s})' if s != 1 else ''
    return P(CHECK, cls, f' transform="translate({x} {y}){sc}"')


def star(cx, cy, r, cls):
    import math
    pts = []
    for k in range(10):
        rr = r if k % 2 == 0 else r * .45
        a = math.radians(-90 + k * 36)
        pts.append(f'{cx + rr * math.cos(a):.2f} {cy + rr * math.sin(a):.2f}')
    return P('M' + 'L'.join(pts) + 'Z', cls)


KF = []   # keyframes
AN = []   # animation rules
ENTER = []  # one-shot entrances: play once when the card first comes on screen (paused until then)


def anim(sel, name, T, frames, ease='linear'):
    KF.append(f'@keyframes {name}{{{frames}}}')
    AN.append(f'.js .wv {sel}{{animation:{name} {T}s {ease} infinite both}}')


# =================================================================== 1. design -> code
T1 = 10.0
WIN = (24, 30, 432, 252)


BRAND = 'arcwell'
NAV = [('Watches', 302), ('Bands', 347.5), ('Support', 383)]   # 12 units apart, ending at 414


def page_common(dark):
    """The store page, drawn identically in the design file (dark canvas) and on the live site:
    same copy, same geometry, so every edge lines up under the wipe."""
    ink, mute = ('wt', 'wm') if dark else ('wink', 'winkm')
    o = T(44, 74, BRAND, 11.5, f'{ink} w1-logo')
    o += ''.join(T(x, 73.5, lbl, 8, mute) for lbl, x in NAV)
    o += P('M422.6 67h10.8l-1 9.4h-8.8ZM425.5 67v-1.6a2.5 2.5 0 0 1 5 0V67', 'w1-cartd' if dark else 'w1-cart')
    o += G(T(44, 98, 'Arc Watch S2', 8, 'wo w1-eyet'), 'w1-in w1-in0')
    o += G(T(44, 132, 'Health on', 34, f'w1-h {ink}') + T(44, 166, 'your wrist', 34, f'w1-h {ink}'), 'w1-in w1-in1')
    o += G(T(44, 184, 'Heart rate, sleep and GPS tracking', 8, mute) + T(44, 195, 'with a 14-day battery.', 8, mute), 'w1-in w1-in2')
    o += G(T(162, 221, '$299', 13, f'{ink} w1-price') + T(162, 233, 'Free shipping &amp; returns', 7, mute), 'w1-in w1-in4')
    return o


def scene1():
    x, y, w, h = WIN
    clipL = f'<defs><clipPath id="w1-cl"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/></clipPath></defs>'
    # ---- live site
    live = R(x, y, w, h, 0, 'w1-page') + R(x, y, w, 22, 0, 'w1-bar')
    live += ''.join(C(cx, 41, 3, 'w1-dot') for cx in (38, 48, 58))
    live += R(176, 35, 128, 12, 6, 'w1-url') + T(240, 44, 'arcwell.com', 7.5, 'winkm', 'middle')
    live += page_common(False)
    live += G(photo('smartwatch', 252, 86, 184, 176, 10, 'w1-ph', fill=.86), 'w1-in w1-in5')
    btn = R(44, 206, 104, 32, 16, 'w1-btnbg') + R(44, 206, 104, 32, 16, 'w1-btnh') + T(96, 226, 'Shop now', 11, 'w1-btnt', 'middle')
    live += G(G(btn, 'w1-btn'), 'w1-in w1-in3') + C(100, 222, 14, 'w1-rip')
    live_svg = svg(clipL + G(live, '', ' clip-path="url(#w1-cl)"'))

    # ---- design file
    clipD = (f'<defs><clipPath id="w1-cd"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/></clipPath>'
             '<pattern id="w1-dots" width="12" height="12" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".9" class="w1-gdot"/></pattern></defs>')
    des = R(x, y, w, h, 0, 'w1-canvas') + R(x, y, w, h, 0, '', ' fill="url(#w1-dots)"') + R(x, y, w, 22, 0, 'w1-dbar')
    des += T(36, 44, 'Home', 8.5, 'wt') + T(64, 44, 'Desktop 1440', 8.5, 'wm') + T(444, 44, '100%', 8.5, 'wm', 'end')
    colw = (392 - 5 * 12) / 6
    des += ''.join(R(round(44 + k * (colw + 12), 2), 52, round(colw, 2), 230, 0, 'w1-col') for k in range(6))
    des += page_common(True)
    des += R(40, 100, 156, 74, 0, 'w1-bbox') + R(200, 101, 50, 14, 7, 'w1-tag') + T(225, 111, 'H1 34', 8, 'w1-tagt', 'middle')
    des += P('M158 195.5V205.5M155 195.5H161M155 205.5H161', 'w1-red') + T(165, 203.5, '12', 8, 'w1-redt')
    des += P('M24.5 222H43.5M24.5 219V225M43.5 219V225', 'w1-red') + T(34, 216, '20', 8, 'w1-redt', 'middle')
    des += G(R(44, 206, 104, 32, 16, 'w1-btnbg') + T(96, 226, 'Shop now', 11, 'w1-btnt', 'middle'), 'w1-in w1-in3')
    des += R(41.5, 203.5, 109, 37, 0, 'w1-sel')
    des += ''.join(R(hx - 2.75, hy - 2.75, 5.5, 5.5, 0, 'w1-hdl') for hx, hy in ((41.5, 203.5), (150.5, 203.5), (41.5, 240.5), (150.5, 240.5)))
    des += R(66, 246, 60, 14, 7, 'w1-dim') + T(96, 256, '104 x 32', 8, 'w1-dimt', 'middle')
    des += G(photo('smartwatch', 252, 86, 184, 176, 10, 'w1-phd', fill=.86), 'w1-in w1-in5')
    des += R(251.5, 85.5, 185, 177, 10.5, 'w1-frm') + T(252, 82, 'Product image', 7, 'wm')
    des_svg = svg(clipD + G(des, '', ' clip-path="url(#w1-cd)"'))

    # ---- overlay: frame, labels, pointer
    top = R(x, y, w, h, 12, 'w1-frame')
    top += R(24, 4, 60, 18, 9, 'w1-chip') + T(54, 16.5, 'Design', 9, 'wt', 'middle')
    top += R(392, 4, 64, 18, 9, 'w1-chip') + T(424, 16.5, 'Live site', 9, 'wt', 'middle')
    top += G(R(186, 4, 108, 18, 9, 'w1-ok') + check(200, 13, 'wchk-o') + T(246, 16.5, 'Pixel-matched', 9, 'w1-okt', 'middle'), 'w1-match')
    top += G(P(CURSOR, 'wcur'), 'w1-cur')
    top_svg = svg(top)

    html = (f'<div class="wv wv--sync">{live_svg}<div class="w1-design">{des_svg}</div>'
            f'<div class="w1-wipe"><i class="w1-knob"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
            f'<path d="M9.5 7.5L5 12l4.5 4.5M14.5 7.5L19 12l-4.5 4.5"/></svg></i></div>{top_svg}</div>')

    # wipe position p (% from the left; the design file shows left of it)
    stops = [(0, 50), (.6, 50), (2.0, 84), (3.0, 84), (4.6, 12), (7.4, 12), (8.6, 50), (10, 50)]
    wipe, clip = [], []
    for k, (t, p) in enumerate(stops):
        e = f';animation-timing-function:{WIPE}' if k + 1 < len(stops) and stops[k + 1][1] != p else ''
        wipe.append(f'{pc(t, T1)}{{transform:translateX({p}%){e}}}')
        clip.append(f'{pc(t, T1)}{{clip-path:inset(0 {100 - p}% 0 0){e}}}')
    anim('.w1-wipe', 'w1-wipe', T1, ''.join(wipe))
    anim('.w1-design', 'w1-clip', T1, ''.join(clip))
    # pointer on the live side: in, hover, press, out
    cur = (f'0%,{pc(4.7, T1)}{{opacity:0;transform:translate(476px,300px)}}'
           f'{pc(4.9, T1)}{{opacity:1;transform:translate(476px,300px);animation-timing-function:{EO}}}'
           f'{pc(5.7, T1)}{{opacity:1;transform:translate(104px,224px)}}'
           f'{pc(6.2, T1)}{{opacity:1;transform:translate(104px,224px) scale(.82)}}'
           f'{pc(6.35, T1)}{{opacity:1;transform:translate(104px,224px);animation-timing-function:{SOFT}}}'
           f'{pc(6.9, T1)}{{opacity:1;transform:translate(104px,224px);animation-timing-function:{IO}}}'
           f'{pc(7.4, T1)}{{opacity:0;transform:translate(150px,300px)}}100%{{opacity:0;transform:translate(476px,300px)}}')
    anim('.w1-cur', 'w1-cur', T1, cur)
    anim('.w1-btnh', 'w1-hov', T1, f'0%,{pc(5.6, T1)}{{opacity:0}}{pc(5.8, T1)},{pc(6.9, T1)}{{opacity:1}}{pc(7.1, T1)},100%{{opacity:0}}')
    anim('.w1-btn', 'w1-press', T1, f'0%,{pc(6.15, T1)}{{transform:none}}{pc(6.25, T1)}{{transform:scale(.95)}}{pc(6.45, T1)},100%{{transform:none}}')
    anim('.w1-rip', 'w1-rip', T1, f'0%,{pc(6.2, T1)}{{opacity:0;transform:scale(.4)}}{pc(6.25, T1)}{{opacity:.9;transform:scale(.4);animation-timing-function:{EO}}}{pc(6.9, T1)},100%{{opacity:0;transform:scale(2.6)}}')
    anim('.w1-match', 'w1-match', T1, f'0%,{pc(8.65, T1)}{{opacity:0;transform:translateY(4px) scale(.96);animation-timing-function:{EO}}}{pc(9.05, T1)},{pc(9.7, T1)}{{opacity:1;transform:none}}{pc(9.95, T1)},100%{{opacity:0;transform:none}}')
    ENTER.append('.js .wv .w1-in{animation:w1-in .7s ' + EO + ' both}' + ''.join(
        f'.js .wv .w1-in{k}{{animation-delay:{.12 + .08 * k:.2f}s}}' for k in range(6)))
    KF.append('@keyframes w1-in{from{opacity:0;transform:translateY(6px)}}')
    return html


CSS1 = '''
.wv--sync>svg,.w1-design,.w1-design>svg{position:absolute;inset:0;width:100%;height:100%}
.w1-design{clip-path:inset(0 50% 0 0)}
.w1-wipe{position:absolute;left:0;top:10%;bottom:6%;width:100%;transform:translateX(50%);pointer-events:none}
.w1-wipe::before{content:"";position:absolute;left:-1px;top:0;bottom:0;width:2px;background:var(--white);box-shadow:0 0 0 1px rgba(0,0,0,.18)}
.w1-knob{position:absolute;left:0;top:50%;width:6%;aspect-ratio:1;transform:translate(-50%,-50%);display:grid;place-items:center;border-radius:50%;background:var(--white);box-shadow:0 2px 8px rgba(0,0,0,.35)}
.w1-knob svg{width:62%;height:62%;fill:none;stroke:var(--charcoal);stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.wv .w1-page{fill:#F5F4F1}.wv .w1-bar{fill:#E6E4DF}.wv .w1-dot{fill:rgba(25,24,29,.22)}.wv .w1-url{fill:#fff}
.wv .w1-logo{font-weight:800;letter-spacing:-.02em}
.wv .w1-cart{fill:none;stroke:#19181D;stroke-width:1.4;stroke-linejoin:round}.wv .w1-cartd{fill:none;stroke:rgba(255,255,255,.85);stroke-width:1.4;stroke-linejoin:round}
.wv .w1-eyet{font-weight:700}.wv .w1-price{font-weight:800}
.wv .w1-h{font-family:var(--display);font-weight:600}
.wv .w1-btnbg{fill:var(--orange)}.wv .w1-btnh{fill:#19181D;opacity:0}.wv .w1-btnt{fill:#fff;font-weight:700}
.wv .w1-btn{transform-origin:96px 222px;transform-box:view-box}
.wv .w1-rip{fill:none;stroke:#fff;stroke-width:2;opacity:0;transform-origin:100px 222px;transform-box:view-box}
.wv .w1-canvas{fill:#0E0E11}.wv .w1-gdot{fill:rgba(255,255,255,.09)}.wv .w1-dbar{fill:#17171B}
.wv .w1-col{fill:rgba(231,81,57,.07)}
.wv .w1-bbox{fill:none;stroke:rgba(255,255,255,.4);stroke-width:1;stroke-dasharray:3 3}
.wv .w1-tag{fill:rgba(255,255,255,.1)}.wv .w1-tagt{fill:rgba(255,255,255,.75)}
.wv .w1-red{fill:none;stroke:var(--orange);stroke-width:1.2}.wv .w1-redt{fill:var(--orange);font-weight:700}
.wv .w1-sel{fill:none;stroke:var(--orange);stroke-width:1.5}
.wv .w1-hdl{fill:#fff;stroke:var(--orange);stroke-width:1.2}
.wv .w1-dim{fill:var(--orange)}.wv .w1-dimt{fill:#fff;font-weight:700}
.wv .w1-frm{fill:none;stroke:rgba(255,255,255,.4);stroke-width:1;stroke-dasharray:3 3}
.wv .w1-frame{fill:none;stroke:rgba(255,255,255,.16);stroke-width:1}
.wv .w1-chip{fill:rgba(255,255,255,.08);stroke:rgba(255,255,255,.16)}
.wv .w1-ok{fill:rgba(231,81,57,.16);stroke:rgba(231,81,57,.6)}.wv .w1-okt{fill:var(--orange-soft)}
.wv .w1-cur{opacity:0}
'''

# =================================================================== 2. fast by default
T2 = 11.0
X0, PX = 160, 72          # 0s at x=160, 72 units per second


def tx(t):
    return round(X0 + PX * t, 2)


ROWS = [  # name before/after, size before/after, class, (start, end) before, after, step
    ('index.html', None, '14 KB', None, 'w2-doc', (0, .32), (0, .32), None),
    ('styles.css', None, '86 KB', '18 KB', 'w2-css', (.32, .82), (.32, .5), 2),
    ('inter.woff2', None, '48 KB', None, 'w2-font', (.82, 1.45), (.34, .62), 1),
    ('hero.jpg', 'hero.avif', '2.4 MB', '160 KB', 'w2-img', (.86, 3.3), (.36, .84), 0),
    ('app.js', None, '410 KB', '96 KB', 'w2-js', (.82, 2.55), (.5, .88), 2),
    ('chat-widget.js', None, '320 KB', None, 'w2-3p', (1.4, 3.62), (1.2, 1.62), 3),
]
STEPS = ['AVIF images', 'Font preload', 'Lean CSS/JS', 'Lazy embeds']
T_STEP = [2.0, 3.35, 4.7, 6.05]
MORPH = .9
READY = (3.62, .92)


def scene2():
    o = R(16, 14, 448, 272, 14, 'wpanel')
    o += T(32, 38, 'Network', 12, 'wt w2-title') + T(92, 38, '6 requests', 9, 'wm')
    for k in range(5):
        xx = tx(k)
        o += P(f'M{xx} 66V222', 'w2-grid') + T(xx, 59, f'{k}s', 8.5, 'wm', 'start' if k == 0 else ('end' if k == 4 else 'middle'))
    for i, (n0, n1, s0, s1, cls, b, a, st) in enumerate(ROWS):
        y = 82 + i * 26
        if n1:
            o += G(T(32, y + 3.5, n0, 10.5, 'wt'), f'w2-n0 w2-r{i}n0') + G(T(32, y + 3.5, n1, 10.5, 'wt'), f'w2-n1 w2-r{i}n1')
        else:
            o += T(32, y + 3.5, n0, 10.5, 'wt')
        if s1:
            o += G(T(148, y + 3.5, s0, 9, 'wm', 'end'), f'w2-s0 w2-r{i}s0') + G(T(148, y + 3.5, s1, 9, 'w2-good', 'end'), f'w2-s1 w2-r{i}s1')
        else:
            o += T(148, y + 3.5, s0, 9, 'wm', 'end')
        xa, wa = tx(a[0]), round(PX * (a[1] - a[0]), 2)
        o += R(xa, y - 4.5, wa, 9, 0, f'w2-bar {cls} w2-b{i}')
        if cls == 'w2-3p':
            o += G(T(xa + wa + 6, y + 3.2, 'on demand', 8, 'w2-lazy'), 'w2-lz')
        xb, wb = tx(b[0]), PX * (b[1] - b[0])
        dx, k = round(xb - xa, 2), round(wb / wa, 4)
        t_in = .25 + .12 * i
        frames = (f'0%,{pc(t_in, T2)}{{opacity:1;transform:translateX({dx}px) scaleX(0);animation-timing-function:{EO}}}'
                  f'{pc(t_in + .55, T2)}{{opacity:1;transform:translateX({dx}px) scaleX({k})}}')
        if st is not None:
            ts = T_STEP[st]
            frames += (f'{pc(ts, T2)}{{opacity:1;transform:translateX({dx}px) scaleX({k});animation-timing-function:{IO}}}'
                       f'{pc(ts + MORPH, T2)}{{opacity:1;transform:none}}')
        frames += f'{pc(10.2, T2)}{{opacity:1;transform:{"none" if st is not None else f"translateX({dx}px) scaleX({k})"}}}{pc(10.6, T2)},100%{{opacity:0;transform:translateX({dx}px) scaleX(0)}}'
        anim(f'.w2-b{i}', f'w2-b{i}', T2, frames)
        if st is not None:
            ts = T_STEP[st]
            if n1:
                anim(f'.w2-r{i}n0', f'w2-r{i}n0', T2, f'0%,{pc(ts + .2, T2)}{{opacity:1}}{pc(ts + .5, T2)},{pc(10.6, T2)}{{opacity:0}}100%{{opacity:1}}')
                anim(f'.w2-r{i}n1', f'w2-r{i}n1', T2, f'0%,{pc(ts + .3, T2)}{{opacity:0}}{pc(ts + .6, T2)},{pc(10.2, T2)}{{opacity:1}}{pc(10.6, T2)},100%{{opacity:0}}')
            if s1:
                anim(f'.w2-r{i}s0', f'w2-r{i}s0', T2, f'0%,{pc(ts + .2, T2)}{{opacity:1}}{pc(ts + .5, T2)},{pc(10.6, T2)}{{opacity:0}}100%{{opacity:1}}')
                anim(f'.w2-r{i}s1', f'w2-r{i}s1', T2, f'0%,{pc(ts + .3, T2)}{{opacity:0}}{pc(ts + .6, T2)},{pc(10.2, T2)}{{opacity:1}}{pc(10.6, T2)},100%{{opacity:0}}')
    tl = T_STEP[3]
    anim('.w2-lz', 'w2-lz', T2, f'0%,{pc(tl + .6, T2)}{{opacity:0}}{pc(tl + .9, T2)},{pc(10.2, T2)}{{opacity:1}}{pc(10.6, T2)},100%{{opacity:0}}')
    # page-ready line
    xr = tx(READY[1])
    dxr = round(tx(READY[0]) - xr, 2)
    o += G(P(f'M{xr} 66V228', 'w2-ready') + R(xr - 26, 228, 52, 16, 8, 'w2-rchip') + T(xr, 239.5, 'Ready', 8.5, 'w2-rchipt', 'middle'), 'w2-mark')
    anim('.w2-mark', 'w2-mark', T2,
         f'0%,{pc(1.1, T2)}{{opacity:0;transform:translateX({dxr}px)}}{pc(1.4, T2)}{{opacity:1;transform:translateX({dxr}px)}}'
         f'{pc(7.1, T2)}{{opacity:1;transform:translateX({dxr}px);animation-timing-function:{IO}}}{pc(8.2, T2)},{pc(10.2, T2)}{{opacity:1;transform:none}}'
         f'{pc(10.6, T2)},100%{{opacity:0;transform:translateX({dxr}px)}}')
    # optimisation chips
    for k, lbl in enumerate(STEPS):
        cx = 32 + k * 105
        o += R(cx, 254, 96, 20, 10, 'w2-off') + T(cx + 48, 267.5, lbl, 8.5, 'wm', 'middle')
        o += G(R(cx, 254, 96, 20, 10, 'w2-on') + check(cx + 13, 264, 'wchk-o', .9) + T(cx + 53, 267.5, lbl, 8.5, 'wt', 'middle'), f'w2-c w2-c{k}')
        ts = T_STEP[k]
        anim(f'.w2-c{k}', f'w2-c{k}', T2, f'0%,{pc(ts - .05, T2)}{{opacity:0}}{pc(ts + .25, T2)},{pc(10.2, T2)}{{opacity:1}}{pc(10.6, T2)},100%{{opacity:0}}')
    return f'<div class="wv wv--speed">{svg(o)}</div>'


CSS2 = '''
.wv .w2-title{font-weight:700}
.wv .w2-grid{stroke:rgba(255,255,255,.07);stroke-width:1}
.wv .w2-bar{transform-box:fill-box;transform-origin:left center}
.wv .w2-doc{fill:rgba(255,255,255,.82)}.wv .w2-css{fill:var(--coral)}.wv .w2-font{fill:#A5A4AA}
.wv .w2-img{fill:var(--orange)}.wv .w2-js{fill:#F5F4F1;fill-opacity:.55}
.wv .w2-3p{fill:#55555B}
.wv .w2-lazy{fill:rgba(255,255,255,.5);font-style:italic}
.wv .w2-good{fill:var(--orange-soft)}
.wv .w2-n0,.wv .w2-s0{opacity:0}
.wv .w2-ready{stroke:var(--orange);stroke-width:1.5}
.wv .w2-rchip{fill:var(--orange)}.wv .w2-rchipt{fill:#19181D;font-weight:700}
.wv .w2-off{fill:none;stroke:rgba(255,255,255,.16)}
.wv .w2-on{fill:#331B1A;stroke:rgba(231,81,57,.7)}
'''

# =================================================================== 3. found and chosen
T3 = 11.0
TAGS = [  # label, y of chip, connector path, target class
    ('&lt;title&gt;', 17, 'M212 24C230 24 224 94 240 94', 't'),
    ('&lt;meta&gt;', 98, 'M212 105C228 105 224 112 240 112', 'd'),
    ('alt', 178, 'M212 185C228 185 222 157 244 157H408C420 157 425 146 425 128', 'i'),   # runs in the gap under the result, clear of the next listing
    ('schema', 207, 'M212 214C230 214 224 133 240 133', 's'),
]
T_TAG = [1.6, 2.6, 3.6, 4.6]


MONO = ' style="font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"'
# each tag lights the field it comes from on the page, then draws its line to the piece of the result it builds
SRC = {
    't': [(23, 47, 126, 48, 6)],                       # the product title
    'd': [(23, 95, 141, 22, 5)],                       # the description that becomes the meta description
    'i': [(25, 119, 126, 86, 9)],                      # the photo and its alt text
    's': [(26, 205, 126, 16, 5), (152, 129, 40, 30, 5)],   # rating and reviews, price and availability
}
ENDS = {'t': (240, 94), 'd': (240, 112), 'i': (425, 128), 's': (240, 133)}


def scene3():
    clip = '<defs><clipPath id="w3-pc"><rect x="16" y="14" width="188" height="272" rx="12"/></clipPath><clipPath id="w3-q"><rect x="258" y="30" width="160" height="16"/></clipPath></defs>'
    pg = R(16, 14, 188, 272, 0, 'w3-page') + R(16, 14, 188, 20, 0, 'w3-bar') + T(28, 27.5, 'halden.co/bags/ivory-top-handle', 7.5, 'winkm')
    pg += T(28, 66, 'Ivory Top', 21, 'w1-h wink') + T(28, 88, 'Handle Bag', 21, 'w1-h wink')
    pg += T(28, 104, 'Structured saffiano leather with', 7, 'winkm') + T(28, 113, 'gold hardware and a detachable strap.', 7, 'winkm')
    pg += photo('ivory-bag', 28, 122, 120, 80, 8, 'w3-ph1', fill=.9) + T(156, 141, '$195', 11, 'wink w3-price') + T(156, 154, 'In stock', 7.5, 'winkm')
    pg += G(R(32, 187, 112, 11, 5.5, 'w3-alt') + T(37, 194.4, 'alt="Ivory top handle bag"', 6, 'w3-altt', extra=MONO), 'w3-altg')
    pg += ''.join(star(33 + k * 10, 213, 4.4, 'w3-star') for k in range(5)) + T(84, 216, '4.8 (126 reviews)', 7.5, 'winkm')
    cta = R(28, 236, 84, 28, 14, 'w1-btnbg') + T(70, 254, 'Add to bag', 9.5, 'w1-btnt', 'middle')
    pg += G(cta, 'w3-cta') + R(28, 236, 84, 28, 14, 'w3-ring')
    pg += G(R(120, 236, 72, 28, 14, 'w3-toast') + C(136, 250, 6.5, 'w3-tok') + check(136, 250, 'wchk-w', .8) + T(166, 253.5, 'Added', 9, 'wt', 'middle'), 'w3-toastg')
    pg += ''.join(G(''.join(R(*r, cls='w3-src') for r in rects), f'w3-src{k}') for k, rects in SRC.items())
    o = clip + G(pg, '', ' clip-path="url(#w3-pc)"') + R(16, 14, 188, 272, 12, 'w3-pframe')
    # search results
    o += R(222, 14, 242, 272, 14, 'wpanel')
    o += R(234, 26, 218, 24, 12, 'w3-search') + C(248, 37, 4.5, 'w3-mag') + P('M251.3 40.3L254.5 43.5', 'w3-mag')
    o += G(T(260, 41.5, 'ivory top handle bag', 9.5, 'wt') + R(258, 30, 160, 16, 0, 'w3-cover'), '', ' clip-path="url(#w3-q)"')
    o += R(232, 60, 222, 90, 10, 'w3-card') + R(232, 60, 222, 90, 10, 'w3-hl')
    o += C(246, 75, 5, 'wo') + T(246, 77.2, 'H', 6, 'w3-fav', 'middle') + T(256, 73.4, 'Halden', 7.5, 'wt') + T(256, 81.6, 'halden.co &#8250; bags &#8250; top-handle', 6.5, 'wm')
    o += G(T(242, 98, 'Ivory Top Handle Bag', 11.5, 'w3-title'), 'w3-pt')
    o += G(T(242, 109, 'Structured saffiano leather top handle', 7, 'w3-snip') + T(242, 118, 'bag with gold hardware. Free returns.', 7, 'w3-snip'), 'w3-pd')
    o += G(photo('ivory-bag', 404, 84, 42, 42, 6, 'w3-ph2', fill=.92), 'w3-pi')
    o += G(''.join(star(246 + k * 9, 133, 3.8, 'w3-stard') for k in range(5)) + T(292, 136, '4.8 (126) &#183; $195.00 &#183; In stock', 7.5, 'wm'), 'w3-ps')
    comps = [('M', 'Marlow &amp; Finch', 'marlowandfinch.com &#8250; handbags', 'New In: Women&#8217;s Top Handle Bags', 'Leather top handle bags in black, tan and ivory.'),
             ('C', 'The Carry Edit', 'thecarryedit.com &#8250; guides', 'Best Top Handle Bags to Buy Now', 'Twelve structured bags compared by size and price.')]
    for k, (yy, (ini, site, url, title, snip)) in enumerate(zip((164, 216), comps)):
        o += G(C(246, yy + 6, 4.5, 'w3-cfav') + T(246, yy + 8, ini, 5.5, 'w3-fav', 'middle') + T(255, yy + 4.6, site, 7, 'wt') + T(255, yy + 12.4, url, 6, 'wm') +
               T(242, yy + 27, title, 9.5, 'w3-ctitle') + T(242, yy + 38, snip, 7, 'w3-snip'), 'w3-comp')
    # annotations: tags on the page edge, the field they read, the line they draw, the piece they build
    for k, (lbl, yy, d, tgt) in enumerate(TAGS):
        o += P(d, f'w3-link w3-l{k}', ' pathLength="1"')
        ex, ey = ENDS[tgt]
        o += C(ex, ey, 2.2, f'w3-end w3-e{k}')
        o += G(R(164, yy, 48, 15, 7.5, 'w3-tagoff') + T(188, yy + 10.6, lbl, 7.5, 'w3-tagt', 'middle'), f'w3-tg')
        o += G(R(164, yy, 48, 15, 7.5, 'w3-tagon') + T(188, yy + 10.6, lbl, 7.5, 'w3-tagto', 'middle'), f'w3-tgon w3-tg{k}')
        t = T_TAG[k]
        anim(f'.w3-tg{k}', f'w3-tg{k}', T3, f'0%,{pc(t, T3)}{{opacity:0;transform:scale(.92)}}{pc(t + .25, T3)},{pc(10.1, T3)}{{opacity:1;transform:none;animation-timing-function:{EO}}}{pc(10.6, T3)},100%{{opacity:0;transform:none}}')
        anim(f'.w3-src{tgt}', f'w3-src{tgt}', T3, f'0%,{pc(t, T3)}{{opacity:0}}{pc(t + .2, T3)},{pc(t + .9, T3)}{{opacity:1;animation-timing-function:{SOFT}}}{pc(t + 1.25, T3)},100%{{opacity:0}}')
        anim(f'.w3-l{k}', f'w3-l{k}', T3, f'0%,{pc(t + .1, T3)}{{stroke-dashoffset:1;opacity:1;animation-timing-function:{SOFT}}}{pc(t + .65, T3)},{pc(10.1, T3)}{{stroke-dashoffset:0;opacity:1}}{pc(10.6, T3)},100%{{stroke-dashoffset:0;opacity:0}}')
        anim(f'.w3-e{k}', f'w3-e{k}', T3, f'0%,{pc(t + .6, T3)}{{opacity:0;transform:scale(.3)}}{pc(t + .8, T3)},{pc(10.1, T3)}{{opacity:1;transform:none;animation-timing-function:{EO}}}{pc(10.6, T3)},100%{{opacity:0;transform:none}}')
        anim(f'.w3-p{tgt}', f'w3-p{tgt}', T3, f'0%,{pc(t + .55, T3)}{{opacity:0;transform:translateY(4px);animation-timing-function:{EO}}}{pc(t + 1.0, T3)},{pc(10.1, T3)}{{opacity:1;transform:none}}{pc(10.6, T3)},100%{{opacity:0;transform:none}}')
    t_alt = T_TAG[2]
    anim('.w3-altg', 'w3-alt', T3, f'0%,{pc(t_alt + .05, T3)}{{opacity:0;transform:translateY(3px);animation-timing-function:{EO}}}{pc(t_alt + .4, T3)},{pc(10.1, T3)}{{opacity:1;transform:none}}{pc(10.6, T3)},100%{{opacity:0;transform:none}}')
    o += C(300, 94, 12, 'w3-rip') + G(P(CURSOR, 'wcur'), 'w3-cur')
    anim('.w3-cover', 'w3-type', T3, f'0%,{pc(.2, T3)}{{transform:none}}' + ''.join(
        f'{pc(.2 + 1.2 * k / 21, T3)}{{transform:translateX({k * 114 / 21:.1f}px)}}' for k in range(1, 22)) +
        f'{pc(10.1, T3)}{{transform:translateX(114px);opacity:1}}{pc(10.6, T3)}{{transform:translateX(114px);opacity:1}}100%{{transform:none}}')
    anim('.w3-hl', 'w3-hl', T3, f'0%,{pc(5.6, T3)}{{opacity:0}}{pc(6.0, T3)},{pc(7.1, T3)}{{opacity:.45}}{pc(7.25, T3)},{pc(10.1, T3)}{{opacity:1}}{pc(10.6, T3)},100%{{opacity:0}}')
    anim('.w3-comp', 'w3-comp', T3, f'0%,{pc(5.6, T3)}{{opacity:1}}{pc(6.0, T3)},{pc(10.1, T3)}{{opacity:.45}}{pc(10.6, T3)},100%{{opacity:1}}')
    anim('.w3-cur', 'w3-cur', T3,
         f'0%,{pc(5.95, T3)}{{opacity:0;transform:translate(476px,300px)}}{pc(6.05, T3)}{{opacity:1;transform:translate(476px,300px);animation-timing-function:{EO}}}'
         f'{pc(6.9, T3)}{{opacity:1;transform:translate(298px,92px)}}{pc(7.05, T3)}{{opacity:1;transform:translate(298px,92px) scale(.82)}}'
         f'{pc(7.2, T3)}{{opacity:1;transform:translate(298px,92px);animation-timing-function:{IO}}}{pc(7.9, T3)}{{opacity:1;transform:translate(330px,150px)}}'
         f'{pc(8.3, T3)},100%{{opacity:0;transform:translate(330px,150px)}}')
    anim('.w3-rip', 'w3-rip', T3, f'0%,{pc(7.05, T3)}{{opacity:0;transform:scale(.4)}}{pc(7.1, T3)}{{opacity:.9;transform:scale(.4);animation-timing-function:{EO}}}{pc(7.7, T3)},100%{{opacity:0;transform:scale(2.4)}}')
    anim('.w3-cta', 'w3-cta', T3, f'0%,{pc(7.6, T3)}{{transform:none}}{pc(7.72, T3)}{{transform:scale(.94)}}{pc(7.95, T3)},100%{{transform:none}}')
    anim('.w3-ring', 'w3-ring', T3, f'0%,{pc(7.7, T3)}{{opacity:0;transform:scale(1)}}{pc(7.75, T3)}{{opacity:.9;transform:scale(1);animation-timing-function:{EO}}}{pc(8.5, T3)},100%{{opacity:0;transform:scale(1.35)}}')
    anim('.w3-toastg', 'w3-toast', T3, f'0%,{pc(7.85, T3)}{{opacity:0;transform:translateX(-8px)}}{pc(8.25, T3)},{pc(10.1, T3)}{{opacity:1;transform:none;animation-timing-function:{EO}}}{pc(10.6, T3)},100%{{opacity:0;transform:none}}')
    return f'<div class="wv wv--search">{svg(o)}</div>'


CSS3 = '''
.wv .w3-page{fill:#F5F4F1}.wv .w3-bar{fill:#E6E4DF}.wv .w3-pframe{fill:none;stroke:rgba(255,255,255,.14)}
.wv .w3-price{font-weight:800}.wv .w3-star{fill:var(--orange)}.wv .w3-stard{fill:var(--orange)}
.wv .w3-cta,.wv .w3-ring{transform-box:fill-box;transform-origin:center}
.wv .w3-ring{fill:none;stroke:var(--orange);stroke-width:2;opacity:0}
.wv .w3-toast{fill:#19181D}.wv .w3-tok{fill:var(--orange)}
.wv .w3-search{fill:rgba(255,255,255,.07);stroke:rgba(255,255,255,.12)}
.wv .w3-mag{fill:none;stroke:rgba(255,255,255,.7);stroke-width:1.5;stroke-linecap:round}
.wv .w3-cover{fill:#222224;transform:translateX(114px)}
.wv .w3-card{fill:rgba(255,255,255,.03);stroke:rgba(255,255,255,.1)}
.wv .w3-hl{fill:rgba(231,81,57,.07);stroke:var(--orange);stroke-width:1.5}
.wv .w3-title{fill:var(--orange-soft);font-weight:700}
.wv .w3-snip{fill:rgba(255,255,255,.62);font-weight:500}.wv .w3-ctitle{fill:rgba(255,255,255,.9);font-weight:700}
.wv .w3-fav{fill:#19181D;font-weight:800}.wv .w3-cfav{fill:rgba(255,255,255,.55)}
.wv .w3-alt{fill:rgba(25,24,29,.82)}.wv .w3-altt{fill:#fff;font-weight:500}
.wv .w3-src{fill:rgba(231,81,57,.07);stroke:var(--orange);stroke-width:1.2}.wv .w3-srct,.wv .w3-srcd,.wv .w3-srci,.wv .w3-srcs{opacity:0}
.wv .w3-end{fill:var(--orange);transform-box:fill-box;transform-origin:center}
.wv .w3-comp{opacity:.45}
.wv .w3-link{fill:none;stroke:var(--orange);stroke-width:1.2;stroke-dasharray:1;stroke-dashoffset:0;opacity:.85}
.wv .w3-tagoff{fill:#19181D;stroke:rgba(255,255,255,.22)}.wv .w3-tagt{fill:rgba(255,255,255,.75);font-weight:700}
.wv .w3-tagon{fill:var(--orange)}.wv .w3-tagto{fill:#19181D;font-weight:700}
.wv .w3-rip{fill:none;stroke:#fff;stroke-width:2;opacity:0;transform-box:fill-box;transform-origin:center}
.wv .w3-cur{opacity:0}
'''

# =================================================================== 4. delivered as planned
T4 = 12.0
COLX = [32, 176, 320]
CW, CH = 116, 38


def slot(k):
    return 98 + k * 44


CARDS = [  # title, final Done slot, waypoints [(t_start, t_end, col, slot)], qa dot times, done time
    ('Homepage', 0, [], [], None),
    ('Product page', 1, [(0, 0, 1, 0), (2.0, 2.6, 2, 1)], [.9, 1.2, 1.5], 2.6),
    ('Checkout', 2, [(0, 0, 0, 0), (2.9, 3.5, 1, 0), (5.0, 5.6, 2, 2)], [3.9, 4.2, 4.5], 5.6),
    ('Mobile menu', 3, [(0, 0, 0, 1), (3.1, 3.6, 0, 0), (5.9, 6.5, 1, 0), (8.0, 8.6, 2, 3)], [6.9, 7.2, 7.5], 8.6),
]
PROG = [(2.6, .5), (5.6, .75), (8.6, 1)]
SUBS = {'Homepage': 'Hero and sections', 'Product page': 'Gallery and reviews', 'Checkout': 'Shipping and tax', 'Mobile menu': 'Drawer and search'}


def scene4():
    o = R(16, 14, 448, 272, 14, 'wpanel')
    o += T(32, 38, 'Launch milestone', 12, 'wt w2-title')
    o += R(32, 50, 248, 6, 3, 'w4-track') + R(32, 50, 248, 6, 3, 'w4-fill')
    for k, (lbl, v) in enumerate([('25%', None), ('50%', 2.6), ('75%', 5.6), ('100%', 8.6)]):
        o += G(T(290, 56, lbl, 9, 'wm'), f'w4-pct w4-p{k}')
    o += G(R(368, 28, 80, 20, 10, 'w4-due') + T(408, 41.5, 'Due Friday', 9, 'wm', 'middle'), 'w4-dueg')
    o += G(R(330, 28, 118, 20, 10, 'w4-done') + check(344, 38, 'wchk-k', .9) + T(395, 41.5, 'Delivered on time', 9, 'w4-donet', 'middle'), 'w4-doneg')
    for c, lbl in zip(COLX, ['In progress', 'QA', 'Done']):
        o += T(c + 6, 82, lbl, 9, 'wm') + R(c, 90, 128, 188, 10, 'w4-col')
    qa = [('Browsers', 0), ('Mobile', 1), ('Forms and links', 2)]
    o += R(182, 146, 116, 84, 8, 'w4-qa') + T(192, 162, 'QA checks', 8.5, 'wm')
    for lbl, j in qa:
        yy = 182 + j * 18
        o += T(192, yy + 3, lbl, 9, 'wt') + C(286, yy, 5.5, 'w4-qoff')
        o += G(C(286, yy, 5.5, 'w4-qon') + check(286, yy, 'wchk-w', .7), f'w4-q w4-q{j}')
        fr, last = ['0%{opacity:0;transform:scale(.4)}'], 0
        for (_, _, way, dots, _) in CARDS[1:]:
            t_on, t_off = dots[j], way[-1][0]
            fr.append(f'{pc(t_on, T4)}{{opacity:0;transform:scale(.4)}}{pc(t_on + .18, T4)}{{opacity:1;transform:scale(1.2)}}{pc(t_on + .3, T4)},{pc(t_off - .05, T4)}{{opacity:1;transform:none}}{pc(t_off + .2, T4)}{{opacity:0;transform:none}}')
        fr.append('100%{opacity:0;transform:none}')
        anim(f'.w4-q{j}', f'w4-q{j}', T4, ''.join(fr))
    for i, (title, fin, way, dots, tdone) in enumerate(CARDS):
        x, y = COLX[2] + 6, slot(fin)
        card = R(x, y, CW, CH, 8, 'w4-card') + T(x + 10, y + 16, title, 10, 'wt') + T(x + 10, y + 29.5, SUBS[title], 7, 'w4-subt')
        dg = ''.join(C(x + 80 + j * 8, y + 26, 2.6, 'w4-dot') for j in range(3))
        dg += ''.join(G(C(x + 80 + j * 8, y + 26, 2.6, 'w4-don'), f'w4-d w4-d{i}{j}') for j in range(3))
        card += G(dg, f'w4-dots w4-ds{i}')
        card += G(C(x + 101, y + 19, 7, 'w4-badge') + check(x + 101, y + 19, 'wchk-w', .85), f'w4-chk w4-ck{i}')
        o += G(card, f'w4-c w4-c{i}')
        fx, fy = COLX[2], slot(fin)
        if way:
            fr = []
            pos = [(COLX[w[2]] - fx, slot(w[3]) - fy) for w in way]
            fr.append(f'0%{{opacity:0;transform:translate({pos[0][0]}px,{pos[0][1]}px)}}')
            fr.append(f'{pc(.35, T4)}{{opacity:1;transform:translate({pos[0][0]}px,{pos[0][1]}px)}}')
            for k in range(1, len(way)):
                t0, t1 = way[k][0], way[k][1]
                fr.append(f'{pc(t0, T4)}{{opacity:1;transform:translate({pos[k - 1][0]}px,{pos[k - 1][1]}px);animation-timing-function:{IO}}}')
                fr.append(f'{pc(t1, T4)}{{opacity:1;transform:translate({pos[k][0]}px,{pos[k][1]}px)}}')
            fr.append(f'{pc(10.9, T4)}{{opacity:1;transform:none}}{pc(11.4, T4)},100%{{opacity:0;transform:none}}')
            anim(f'.w4-c{i}', f'w4-c{i}', T4, ''.join(fr))
            ta = way[-1][0]
            anim(f'.w4-ds{i}', f'w4-ds{i}', T4, f'0%,{pc(ta, T4)}{{opacity:1}}{pc(ta + .2, T4)},100%{{opacity:0}}')
            for j, td in enumerate(dots):
                anim(f'.w4-d{i}{j}', f'w4-d{i}{j}', T4, f'0%,{pc(td, T4)}{{opacity:0;transform:scale(.3)}}{pc(td + .18, T4)}{{opacity:1;transform:scale(1.25)}}{pc(td + .3, T4)},100%{{opacity:1;transform:none}}')
            anim(f'.w4-ck{i}', f'w4-ck{i}', T4, f'0%,{pc(tdone, T4)}{{opacity:0;transform:scale(.4)}}{pc(tdone + .2, T4)}{{opacity:1;transform:scale(1.15)}}{pc(tdone + .35, T4)},100%{{opacity:1;transform:none}}')
        else:
            anim(f'.w4-c{i}', f'w4-c{i}', T4, f'0%{{opacity:0}}{pc(.35, T4)},{pc(10.9, T4)}{{opacity:1}}{pc(11.4, T4)},100%{{opacity:0}}')
    fill = f'0%{{transform:scaleX(.25)}}'
    prev = .25
    for t, v in PROG:
        fill += f'{pc(t - .3, T4)}{{transform:scaleX({prev});animation-timing-function:{EO}}}{pc(t + .3, T4)}{{transform:scaleX({v})}}'
        prev = v
    fill += f'{pc(10.9, T4)}{{transform:scaleX(1);opacity:1}}{pc(11.4, T4)}{{transform:scaleX(1);opacity:0}}100%{{transform:scaleX(.25);opacity:0}}'
    anim('.w4-fill', 'w4-fill', T4, fill)
    ts = [0, 2.6, 5.6, 8.6, 11.4]
    for k in range(4):
        a, b = ts[k], ts[k + 1]
        if k == 0:
            fr = f'0%,{pc(b - .05, T4)}{{opacity:1}}{pc(b + .1, T4)},100%{{opacity:0}}'
        elif k == 3:
            fr = f'0%,{pc(a, T4)}{{opacity:0}}{pc(a + .15, T4)},{pc(10.9, T4)}{{opacity:1}}{pc(11.4, T4)},100%{{opacity:0}}'
        else:
            fr = f'0%,{pc(a, T4)}{{opacity:0}}{pc(a + .15, T4)},{pc(b - .05, T4)}{{opacity:1}}{pc(b + .1, T4)},100%{{opacity:0}}'
        anim(f'.w4-p{k}', f'w4-p{k}', T4, fr)
    anim('.w4-dueg', 'w4-due', T4, f'0%,{pc(8.85, T4)}{{opacity:1}}{pc(9.05, T4)},{pc(11.4, T4)}{{opacity:0}}100%{{opacity:1}}')
    anim('.w4-doneg', 'w4-donec', T4, f'0%,{pc(8.9, T4)}{{opacity:0;transform:scale(.9)}}{pc(9.25, T4)},{pc(10.9, T4)}{{opacity:1;transform:none;animation-timing-function:{EO}}}{pc(11.4, T4)},100%{{opacity:0;transform:none}}')
    return f'<div class="wv wv--board">{svg(o)}</div>'


CSS4 = '''
.wv .w4-track{fill:rgba(255,255,255,.1)}.wv .w4-fill{fill:var(--orange);transform-box:fill-box;transform-origin:left center}
.wv .w4-pct{opacity:0}.wv .w4-p3{opacity:1}
.wv .w4-due{fill:none;stroke:rgba(255,255,255,.2)}.wv .w4-dueg{opacity:0}
.wv .w4-done{fill:var(--orange)}.wv .w4-donet{fill:#19181D;font-weight:700}
.wv .w4-doneg{transform-box:fill-box;transform-origin:center}
.wv .w4-col{fill:rgba(255,255,255,.035)}
.wv .w4-card{fill:#1B1B1F;stroke:rgba(255,255,255,.1)}
.wv .w4-subt{fill:rgba(255,255,255,.5);font-weight:500}
.wv .w4-dot{fill:rgba(255,255,255,.18)}.wv .w4-don{fill:var(--orange)}
.wv .w4-dots{opacity:0}
.wv .w4-d,.wv .w4-chk{transform-box:fill-box;transform-origin:center}
.wv .w4-badge{fill:var(--orange)}
.wv .w4-qa{fill:#151518;stroke:rgba(255,255,255,.08)}.wv .w4-qoff{fill:none;stroke:rgba(255,255,255,.22);stroke-width:1.2}.wv .w4-qon{fill:var(--orange)}
.wv .w4-q{transform-box:fill-box;transform-origin:center}
'''

CSS_SHARED = '''
/* WHY:START */
/* 14. Why: four promises, one card system. Every card is the same black panel with the same radius,
   inset and caption; each scene tells its own story (see viz/why.py). Base styles are the finished
   frame; the loops run only while a card is on screen (.is-live) and never under reduced motion. */
.benefits{display:grid;gap:1rem}
.benefit{position:relative;display:flex;flex-direction:column;overflow:hidden;isolation:isolate;border-radius:var(--r-panel);background:var(--black);color:var(--white)}
.benefit__stage{position:relative;aspect-ratio:480/300;margin:clamp(.75rem,1.6vw,1.25rem) clamp(.75rem,1.6vw,1.25rem) 0}
.benefit__text{display:grid;gap:.875rem;margin-top:auto;padding:clamp(1rem,2vw,1.5rem) clamp(1.25rem,2.4vw,1.75rem) clamp(1.25rem,2.4vw,1.75rem)}
.benefit h3{font-size:clamp(1.375rem,.9vw + 1.05rem,1.875rem);letter-spacing:0}
.benefit .tags li{background:rgba(255,255,255,.08);box-shadow:inset 0 0 0 1px rgba(255,255,255,.16)}
.benefit .tags svg{color:var(--orange)}
@media (min-width:900px){.benefits{grid-template-columns:repeat(2,minmax(0,1fr));gap:1.25rem}}
.wv{position:absolute;inset:0}
.wv>svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.wv text{font-family:var(--body);font-weight:600}
.wv .wt{fill:#fff}.wv .wm{fill:rgba(255,255,255,.55)}.wv .wo{fill:var(--orange)}
.wv .wink{fill:#19181D}.wv .winkm{fill:rgba(25,24,29,.55)}.wv .winkf{fill:rgba(25,24,29,.16)}
.wv .wpanel{fill:#111114;stroke:rgba(255,255,255,.12);stroke-width:1}
.wv .wchk-o{fill:none;stroke:var(--orange-soft);stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.wv .wchk-w{fill:none;stroke:#fff;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.wv .wchk-k{fill:none;stroke:#19181D;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.wv .wcur{fill:#fff;stroke:#19181D;stroke-width:1.4;stroke-linejoin:round}
.wv g,.wv rect,.wv path,.wv circle,.wv text{transform-box:fill-box}
.wv .w1-cur,.wv .w3-cur{transform-box:view-box;transform-origin:0 0}
'''


def build():
    KF.clear(); AN.clear(); ENTER.clear()
    s1, s2, s3, s4 = scene1(), scene2(), scene3(), scene4()
    motion = ('@media (prefers-reduced-motion:no-preference){\n' + '\n'.join(AN) + '\n' + '\n'.join(ENTER) + '\n' + '\n'.join(KF) +
              '\n.js .wv:not(.is-live) *,.js .wv:not(.is-live){animation-play-state:paused}\n}\n')
    css = CSS_SHARED + CSS1 + CSS2 + CSS3 + CSS4 + motion + '/* WHY:END */'
    cards = [
        (s1, 'One team, from design to code', ['Design-led development', 'Custom-built solutions'],
         'A design file and the live Arcwell store compared under a sliding divider: the Arc Watch S2 page, with its headline, copy, price and product photo, lines up edge for edge, and the live Shop now button responds to the pointer.'),
        (s2, 'Fast by default', ['Performance-focused engineering', 'Responsive-first execution'],
         'A network waterfall: compressed images, a preloaded font, leaner code and lazy embeds move the page-ready line from 3.6 to 0.9 seconds.'),
        (s3, 'Built to be found, and chosen', ['SEO-conscious architecture', 'Conversion-focused strategy'],
         "A Halden product page for the Ivory Top Handle Bag, $195 and in stock: its title, meta description, image alt text and review schema each build part of its Google result, with the thumbnail, a 4.8 rating from 126 reviews, the price and availability; the shopper picks it and adds it to their bag."),
        (s4, 'Finished properly, delivered as planned', ['Attention to detail', 'Reliable project delivery'],
         'A delivery board: the homepage, product page, checkout and mobile menu each pass browser, mobile and link checks before they move to Done, and the launch milestone closes on its due date.'),
    ]
    html = '<!-- WHY:START -->\n    <div class="benefits">\n'
    for scene, title, tags, alt in cards:
        lis = ''.join(f'<li>{{{{ic:check}}}}{t}</li>' for t in tags)
        html += (f'      <article class="benefit">\n        <div class="benefit__stage" role="img" aria-label="{alt}">{scene}</div>\n'
                 f'        <div class="benefit__text">\n          <h3>{title}</h3>\n          <ul class="tags">{lis}</ul>\n        </div>\n      </article>\n')
    html += '    </div>\n    <!-- WHY:END -->'
    return css, html


def run():
    css, html = build()
    head = ROOT / 'src/01-head.html'
    h = head.read_text()
    if '/* WHY:START */' in h:
        h = re.sub(r'/\* WHY:START \*/.*?/\* WHY:END \*/', lambda m: css.lstrip('\n'), h, flags=re.S)
    else:
        a = h.index('/* 14. Why: four promises, told visually')
        b = h.index('\n', h.index('.js [data-art]:not(.is-in) .serp__cursor')) + 1
        h = h[:a] + css + '\n' + h[b:]
    head.write_text(h)
    body = ROOT / 'src/02-body.html'
    b = body.read_text()
    if '<!-- WHY:START -->' in b:
        b = re.sub(r'<!-- WHY:START -->.*?<!-- WHY:END -->', lambda m: html, b, flags=re.S)
    else:
        a = b.index('<div class="promises">')
        e = b.index('<!-- ================================ STACK')
        e = b.rindex('  </div>\n</section>', a, e)
        b = b[:a] + html.lstrip() + '\n' + b[e:]
    body.write_text(b)
    print('why: css', len(css), 'html', len(html), 'keyframes', len(KF))


if __name__ == '__main__':
    run()
