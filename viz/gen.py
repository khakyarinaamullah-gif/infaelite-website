"""Six stages: animated stage visuals.

Builds the six SVG scenes (markup) and their CSS (base = finished frame, keyframes = the loop),
then writes them into the page sources. Every scene is drawn on a 300 x 200 grid that the page
scales to the panel (1 unit = 0.1em of the scene)."""
import math, pathlib, re
from products import photo, ALL

ROOT = pathlib.Path(__file__).resolve().parent.parent
EO = 'cubic-bezier(.23,1,.32,1)'      # strong ease-out (site --ease-out)
IO = 'cubic-bezier(.77,0,.175,1)'     # ease-in-out (site --ease-io)
BK = 'cubic-bezier(.34,1.45,.64,1)'   # gentle overshoot (site --ease-back)
SOFT = 'cubic-bezier(.4,0,.2,1)'


def pct(t, T):
    v = max(0.0, min(100.0, t / T * 100))
    s = f'{v:.2f}'.rstrip('0').rstrip('.')
    return s + '%'


KF = []      # keyframes
RULES = []   # animation rules (motion only)


def cyc(sel, name, T, t_in, dur, init, final, t_out, out=.45, ease=EO, oease=SOFT):
    """Element enters at t_in, holds, leaves at t_out; loops every T seconds."""
    a, b, c, d = pct(t_in, T), pct(t_in + dur, T), pct(t_out, T), pct(min(t_out + out, T), T)
    KF.append(f'@keyframes {name}{{0%,{a}{{{init};animation-timing-function:{ease}}}'
              f'{b},{c}{{{final};animation-timing-function:{oease}}}{d},100%{{{init}}}}}')
    RULES.append(f'.js {sel}{{animation:{name} {T}s linear infinite both}}')


def raw(sel, name, T, frames, extra='linear infinite both'):
    KF.append(f'@keyframes {name}{{{frames}}}')
    RULES.append(f'.js {sel}{{animation:{name} {T}s {extra}}}')


FADE_UP = ('opacity:0;transform:translateY(6px)', 'opacity:1;transform:none')
POP = ('opacity:0;transform:scale(.55)', 'opacity:1;transform:none')
FADE = ('opacity:0', 'opacity:1')
DRAW = ('stroke-dashoffset:1', 'stroke-dashoffset:0')
GROW = ('transform:scaleX(0)', 'transform:none')
REVEAL = ('opacity:0;transform:translateX(-4px)', 'opacity:1;transform:none')

CHECK = 'stroke:#fff;stroke-width:1.7;fill:none;stroke-linecap:round;stroke-linejoin:round'

# ------------------------------------------------------------------ 01 Discovery & Strategy (ink)
C1 = (96, 102)
def polar(c, r, deg):
    a = math.radians(deg)
    return round(c[0] + r * math.cos(a), 2), round(c[1] + r * math.sin(a), 2)

blips = [(52, -40), (78, 40), (52, 200)]
T_SWEEP = 4.8
blip_svg = ''
for k, (r, deg) in enumerate(blips):
    x, y = polar(C1, r, deg)
    hit = ((deg + 90) % 360) / 360 * T_SWEEP
    blip_svg += (f'<g class="vz1-blip" style="--t:{hit:.3f}s"><circle class="vz1-ping" cx="{x}" cy="{y}" r="3.4"/>'
                 f'<circle class="vz1-dot" cx="{x}" cy="{y}" r="3.2"/></g>')
ax, ay = polar(C1, 52, -40)
bx, by = polar(C1, 78, 40)
end_x, end_y = polar(C1, 78, -150)

rows1 = [('Goals', 'More online orders'), ('Audience', 'Women 25 to 45'), ('Scope', 'Shopify, 12 pages')]
rows1_svg = ''
for k, (label, value) in enumerate(rows1):
    y = 84 + 28 * k
    rows1_svg += (f'<g class="vz1-row vz1-row{k}"><g class="vz-chk vz1-chk{k}"><circle cx="206" cy="{y}" r="6"/>'
                  f'<path d="M203.3 {y + .2}l1.9 1.9 3.6-3.8"/></g>'
                  f'<text x="218" y="{y + 3}">{label}</text>'
                  f'<text class="vz-val vz1-sk{k}" x="218" y="{y + 12.5}">{value}</text></g>')

S1 = f'''<svg class="vz vz1" viewBox="0 0 300 200" aria-hidden="true" focusable="false">
<g class="vz1-grid"><circle cx="{C1[0]}" cy="{C1[1]}" r="26"/><circle cx="{C1[0]}" cy="{C1[1]}" r="52"/><circle cx="{C1[0]}" cy="{C1[1]}" r="78"/><line x1="18" y1="{C1[1]}" x2="174" y2="{C1[1]}"/><line x1="{C1[0]}" y1="24" x2="{C1[0]}" y2="180"/></g>
<g class="vz1-sweep"><path d="M{C1[0]} {C1[1]}L{C1[0]} 24A78 78 0 0 0 {end_x} {end_y}Z" fill="#E75139" fill-opacity=".22"/><line x1="{C1[0]}" y1="{C1[1]}" x2="{C1[0]}" y2="24"/></g>
<path class="vz1-link" d="M{ax + 3} {ay - 1}C158 52 178 68 199 81"/>
<path class="vz1-link" d="M{bx + 3} {by}C174 150 184 142 199 140"/>
{blip_svg}
<circle class="vz1-core" cx="{C1[0]}" cy="{C1[1]}" r="4"/>
<rect class="vz-glass" x="188" y="34" width="100" height="134" rx="12"/>
<text class="vz-h" x="200" y="55">Project brief</text>
<line class="vz-rule" x1="200" y1="65" x2="276" y2="65"/>
{rows1_svg}
</svg>'''

T1 = 7.2
RULES.append('.js .vz1-sweep{animation:vz-spin 4.8s linear infinite}')
RULES.append('.js .vz1-link{animation:vz-flow 1.4s linear infinite}')
raw('.vz1-ping', 'vz1-ping', T_SWEEP, '0%{opacity:.95;transform:scale(1)}32%,100%{opacity:0;transform:scale(4.6)}',
    f'{EO} var(--t) infinite both')
raw('.vz1-dot', 'vz1-dot', T_SWEEP, '0%{fill:#FF9A85;transform:scale(1.55)}24%,100%{fill:#fff;transform:none}',
    f'ease var(--t) infinite both')
for k in range(3):
    t = .5 + .45 * k
    cyc(f'.vz1-row{k}', f'vz1-row{k}', T1, t, .6, 'opacity:0;transform:translateX(-6px)', 'opacity:1;transform:none', 6.6, .4)
    cyc(f'.vz1-chk{k}', f'vz1-chk{k}', T1, t + .3, .5, *POP, 6.6, .4, ease=BK)
    cyc(f'.vz1-sk{k}', f'vz1-sk{k}', T1, t + .25, .8, *REVEAL, 6.6, .4)

# ------------------------------------------------------------------ 02 Research & Planning (ember)
T2 = 9
leaves = [(38, 136), (70, 136), (138, 136), (222, 136)]
S2 = '''<svg class="vz vz2" viewBox="0 0 300 200" aria-hidden="true" focusable="false">
<g class="vz2-seg"><rect class="vz2-segbg" x="48" y="10" width="204" height="28" rx="14"/><rect class="vz2-thumb" x="51" y="13" width="66" height="22" rx="11"/>
<text x="84" y="27.6">Shopify</text><text x="150" y="27.6">WordPress</text><text x="216" y="27.6">Custom</text></g>
<path class="vz2-wire vz2-w0" d="M150 76V88H66V100" pathLength="1"/>
<path class="vz2-wire vz2-w1" d="M150 76V100" pathLength="1"/>
<path class="vz2-wire vz2-w2" d="M150 88H234V100" pathLength="1"/>
<path class="vz2-wire vz2-w3" d="M66 120V128H50V136M66 128H82V136" pathLength="1"/>
<path class="vz2-wire vz2-w4" d="M150 120V136" pathLength="1"/>
<path class="vz2-wire vz2-w5" d="M234 120V136" pathLength="1"/>
<g class="vz2-node vz2-n0"><rect x="120" y="56" width="60" height="20" rx="6"/><text x="150" y="69.6">Home</text></g>
<g class="vz2-node vz2-n1"><rect x="40" y="100" width="52" height="20" rx="6"/><text x="66" y="113.6">Shop</text></g>
<g class="vz2-node vz2-n2"><rect x="124" y="100" width="52" height="20" rx="6"/><text x="150" y="113.6">About</text></g>
<g class="vz2-node vz2-n3"><rect x="208" y="100" width="52" height="20" rx="6"/><text x="234" y="113.6">Contact</text></g>
''' + ''.join(f'<g class="vz2-leaf vz2-l{k}"><rect x="{x}" y="{y}" width="24" height="14" rx="4"/><text x="{x + 12}" y="{y + 9.4}">{n}</text></g>' for k, ((x, y), n) in enumerate(zip(leaves, ('Bags', 'Sale', 'Story', 'FAQ')))) + '''
<line class="vz2-track" x1="40" y1="174" x2="260" y2="174"/>
<line class="vz2-prog" x1="40" y1="174" x2="260" y2="174"/>
''' + ''.join(f'<circle class="vz2-ms vz2-m{k}" cx="{40 + 220 * k / 3:.1f}" cy="174" r="5"/>' for k in range(4)) + '''
<text class="vz2-tl" x="35" y="193">Kick-off</text><text class="vz2-tl" x="265" y="193" text-anchor="end">Launch</text>
</svg>'''

raw('.vz2-thumb', 'vz2-thumb', T2,
    f'0%,22%{{transform:none;animation-timing-function:{IO}}}28%,50%{{transform:translateX(66px);animation-timing-function:{IO}}}'
    f'56%,78%{{transform:translateX(132px);animation-timing-function:{IO}}}84%,100%{{transform:none}}')
cyc('.vz2-n0', 'vz2-n0', T2, .2, .5, *POP, 8.4, .45, ease=BK)
for k in range(3):
    cyc(f'.vz2-w{k}', f'vz2-w{k}', T2, .55, .6, *DRAW, 8.4)
    cyc(f'.vz2-n{k + 1}', f'vz2-n{k + 1}', T2, .95 + .12 * k, .5, *POP, 8.4, ease=BK)
for k in range(3, 6):
    cyc(f'.vz2-w{k}', f'vz2-w{k}', T2, 1.4, .5, *DRAW, 8.4)
for k in range(4):
    cyc(f'.vz2-l{k}', f'vz2-l{k}', T2, 1.75 + .1 * k, .45, *POP, 8.4, ease=BK)
cyc('.vz2-prog', 'vz2-prog', T2, 2.2, 4.2, *GROW, 8.4, ease='linear')
for k in range(4):
    t = 2.2 + 1.4 * k
    cyc(f'.vz2-m{k}', f'vz2-m{k}', T2, t, .25, 'fill:#fff;transform:none', 'fill:var(--vz-ink,#19181D);transform:none', 8.4)

# ------------------------------------------------------------------ 03 Creative Design (ink)
# Direction first: three visual directions are laid out, one is picked and approved, and the
# design system (type, colour, spacing) is drawn out of the chosen direction.
T3 = 10
tiles3 = [(30, 'A', 'vz3-ta'), (86, 'B', 'vz3-tb'), (142, 'C', 'vz3-tc')]
tiles_svg = ''
for k, (x, lbl, cls) in enumerate(tiles3):
    # each card shows its supplied design (A light, B dark with orange, C warm brown), cropped to the
    # card and clipped to its corners; B keeps its hairline edge on top of the image
    edge = f'<rect class="vz3-tbe" x="{x}" y="48" width="46" height="74" rx="7"/>' if cls == 'vz3-tb' else ''
    tiles_svg += (f'<g class="vz3-t vz3-t{k}"><g class="vz3-cd vz3-cd{k}"><rect class="{cls}" x="{x}" y="48" width="46" height="74" rx="7"/>'
                  + photo(('dir-a', 'dir-b', 'dir-c')[k], x, 48, 46, 74, 7, f'vz3-im{k}', fill=1) + edge + '</g>'
                  f'<text class="vz3-tl" x="{x + 23}" y="136">{lbl}</text></g>')
S3 = f'''<svg class="vz vz3" viewBox="0 0 300 200" aria-hidden="true" focusable="false">
<rect class="vz-glass" x="18" y="16" width="176" height="168" rx="12"/>
<text class="vz-h" x="30" y="36">Directions</text>
{tiles_svg}
<rect class="vz3-ring" x="82.5" y="44.5" width="53" height="81" rx="9.5"/>
<g class="vz3-ok"><rect x="80" y="146" width="58" height="17" rx="8.5"/><path d="M86.5 154.7l2.2 2.2 4.2-4.4"/><text x="115" y="157.8">Approved</text></g>
<rect class="vz-glass" x="204" y="16" width="84" height="168" rx="12"/>
<text class="vz-h" x="216" y="36">System</text>
<text class="vz3-aa" x="215" y="66">Aa</text>
<text class="vz-val vz3-s0" x="216" y="78.5">Display 48</text><text class="vz-val vz3-s1" x="216" y="87">Body 16</text>
<circle class="vz3-sw vz3-sw0" cx="228" cy="106" r="9" fill="#E75139"/><circle class="vz3-sw vz3-sw1" cx="256" cy="106" r="9" fill="#D75A44"/>
<circle class="vz3-sw vz3-sw2" cx="228" cy="130" r="9" fill="#F5F4F1"/><circle class="vz3-sw vz3-sw3" cx="256" cy="130" r="9" fill="#19181D"/>
<g class="vz3-sp0"><rect class="vz3-tok" x="216" y="152" width="12" height="4" rx="2"/><text class="vz-val" x="232" y="156">8</text></g><g class="vz3-sp1"><rect class="vz3-tok" x="216" y="160" width="26" height="4" rx="2"/><text class="vz-val" x="246" y="164">16</text></g><g class="vz3-sp2"><rect class="vz3-tok" x="216" y="168" width="44" height="4" rx="2"/><text class="vz-val" x="264" y="172">32</text></g>
<circle class="vz3-ripple" cx="109" cy="86" r="10"/>
<g class="vz3-cur"><path class="vz-cursor vz3-arrow" d="M0 0L0 17L4.6 12.8L8 20L11 18.6L7.8 11.6L13.5 11.4Z"/></g>
</svg>'''
for k in range(3):
    cyc(f'.vz3-t{k}', f'vz3-t{k}', T3, .2 + .15 * k, .6, *FADE_UP, 9.3)
for k in (0, 2):  # the two directions that are not chosen step back
    raw(f'.vz3-cd{k}', f'vz3-dim{k}', T3,
        f'0%,{pct(3.0, T3)}{{opacity:1;animation-timing-function:{SOFT}}}{pct(3.5, T3)},100%{{opacity:.35}}')
raw('.vz3-cur', 'vz3-cur', T3,
    f'0%,{pct(1.4, T3)}{{opacity:0;transform:translate(262px,186px);animation-timing-function:{EO}}}'
    f'{pct(2.4, T3)},{pct(2.75, T3)}{{opacity:1;transform:translate(112px,88px);animation-timing-function:{IO}}}'
    f'{pct(3.6, T3)}{{opacity:1;transform:translate(176px,176px);animation-timing-function:{SOFT}}}'
    f'{pct(4.0, T3)},100%{{opacity:0;transform:translate(182px,182px)}}')
raw('.vz3-arrow', 'vz3-press', T3,
    f'0%,{pct(2.45, T3)}{{transform:none;animation-timing-function:{EO}}}{pct(2.6, T3)}{{transform:scale(.86);animation-timing-function:{EO}}}{pct(2.8, T3)},100%{{transform:none}}')
raw('.vz3-ripple', 'vz3-ripple', T3,
    f'0%,{pct(2.6, T3)}{{opacity:0;transform:scale(.4);animation-timing-function:{EO}}}{pct(2.65, T3)}{{opacity:.9;transform:scale(.4);animation-timing-function:{EO}}}'
    f'{pct(3.4, T3)},100%{{opacity:0;transform:scale(2.6)}}')
cyc('.vz3-ring', 'vz3-ring', T3, 2.65, .5, *POP, 9.3, ease=BK)
cyc('.vz3-ok', 'vz3-ok', T3, 2.85, .5, 'opacity:0;transform:translateY(5px)', 'opacity:1;transform:none', 9.3)
cyc('.vz3-aa', 'vz3-aa', T3, 3.4, .6, *FADE_UP, 9.3)
for k in range(2):
    cyc(f'.vz3-s{k}', f'vz3-s{k}', T3, 3.55 + .1 * k, .6, *REVEAL, 9.3)
for k in range(4):
    cyc(f'.vz3-sw{k}', f'vz3-sw{k}', T3, 3.8 + .1 * k, .5, *POP, 9.3, ease=BK)
for k in range(3):
    cyc(f'.vz3-sp{k}', f'vz3-sp{k}', T3, 4.4 + .1 * k, .6, *REVEAL, 9.3)

# ------------------------------------------------------------------ 04 Development & Engineering (ember)
# Versioned build: each commit lands on the branch and the private staging preview grows with it,
# until staging is ready to click through.
T4 = 9
commits = [('Theme setup', 'e41b7c2'), ('Header and menu', '9fa03d1'), ('Product page', 'c72e5a8'),
           ('Cart drawer', '1d8b4f0'), ('Mobile polish', 'b36e9a2')]
T_COMMIT = [.5 + .65 * k for k in range(5)]
rows4 = ''
for k, (msg, sha) in enumerate(commits):
    y = 60 + 24 * k
    rows4 += (f'<g class="vz4-cm vz4-cm{k}"><circle class="vz4-node" cx="32" cy="{y}" r="4"/>'
              f'<text class="vz4-msg" x="44" y="{y + 1}">{msg}</text><text class="vz4-sha" x="44" y="{y + 10}">{sha}</text></g>')
S4 = f'''<svg class="vz vz4" viewBox="0 0 300 200" aria-hidden="true" focusable="false">
<rect class="vz-drop" x="24" y="26" width="176" height="164" rx="12"/>
<rect class="vz4-ed" x="18" y="16" width="176" height="164" rx="12"/>
<circle cx="30" cy="28.5" r="2.4" fill="#E75139"/><circle class="vz4-dim" cx="38" cy="28.5" r="2.4"/><circle class="vz4-dim" cx="46" cy="28.5" r="2.4"/>
<rect class="vz4-tab" x="58" y="21" width="34" height="16" rx="5"/><text class="vz4-tabt" x="64.5" y="32">main</text><text class="vz4-tabt vz4-tabt--dim" x="100" y="32">5 commits</text>
<line class="vz4-sep" x1="18" y1="40" x2="194" y2="40"/>
<line class="vz4-branch" x1="32" y1="60" x2="32" y2="156"/>
{rows4}
<g class="vz4-pv"><rect class="vz-drop" x="174" y="64" width="112" height="122" rx="12"/>
<rect class="vz4-prev" x="168" y="58" width="112" height="122" rx="12"/></g>
<g class="vz4-p vz4-p0"><text class="vz4-logo" x="178" y="73">Atelier</text><circle class="vz4-ash" cx="258" cy="70.5" r="2"/><circle class="vz4-ash" cx="266" cy="70.5" r="2"/></g>
<g class="vz4-p vz4-p1">{photo("p4-banner", 178, 80, 92, 40, 7, "vz4-ph0", fill=1)}</g>
<g class="vz4-p vz4-p2"><rect class="vz4-tile" x="178" y="127" width="44" height="44" rx="6"/>{photo("p4-watch", 181, 130, 38, 26, 4, "vz4-ph1", fill=1)}<text class="vz4-name" x="183" y="165.6">Classic Watch</text></g>
<g class="vz4-p vz4-p3"><rect class="vz4-tile" x="226" y="127" width="44" height="44" rx="6"/>{photo("p4-sunglasses", 229, 130, 38, 26, 4, "vz4-ph2", fill=1)}<text class="vz4-name" x="231" y="165.6">Sunglasses</text></g>
<g class="vz4-chip"><rect x="200" y="18" width="88" height="26" rx="13"/>
<circle class="vz4-spin" cx="214" cy="31" r="5"/>
<g class="vz4-ok"><circle cx="214" cy="31" r="6.5"/><path d="M211 31.2l2 2 4-4.2"/></g>
<text class="vz4-st vz4-st0" x="225" y="34">Building</text><text class="vz4-st vz4-st1" x="225" y="34">Staging ready</text></g>
</svg>'''
raw('.vz4-branch', 'vz4-branch', T4,
    f'0%,{pct(.4, T4)}{{transform:scaleY(0);animation-timing-function:{SOFT}}}{pct(T_COMMIT[-1] + .2, T4)},{pct(8.3, T4)}{{transform:none}}{pct(8.75, T4)},100%{{transform:scaleY(0)}}')
for k, t in enumerate(T_COMMIT):
    cyc(f'.vz4-cm{k}', f'vz4-cm{k}', T4, t, .5, 'opacity:0;transform:translateX(-6px)', 'opacity:1;transform:none', 8.3)
cyc('.vz4-pv', 'vz4-pv', T4, .55, .7, 'opacity:0;transform:translateY(10px) scale(.96)', 'opacity:1;transform:none', 8.4)
for k, t in enumerate([T_COMMIT[1] + .3, T_COMMIT[2] + .3, T_COMMIT[3] + .3, T_COMMIT[4] + .3]):
    cyc(f'.vz4-p{k}', f'vz4-p{k}', T4, t, .6, *FADE_UP, 8.3)
KF.append(f'@keyframes vz4-st0{{0%,{pct(3.9, T4)}{{opacity:1}}{pct(4.2, T4)},{pct(8.5, T4)}{{opacity:0}}{pct(8.8, T4)},100%{{opacity:1}}}}')
RULES.append(f'.js .vz4-st0{{animation:vz4-st0 {T4}s linear infinite both}}')
KF.append(f'@keyframes vz4-spinvis{{0%,{pct(3.9, T4)}{{opacity:1}}{pct(4.1, T4)},{pct(8.5, T4)}{{opacity:0}}{pct(8.8, T4)},100%{{opacity:1}}}}')
cyc('.vz4-ok', 'vz4-ok', T4, 4.0, .5, *POP, 8.4, ease=BK)
cyc('.vz4-st1', 'vz4-st1', T4, 4.1, .5, 'opacity:0;transform:translateY(4px)', 'opacity:1;transform:none', 8.4)

# ------------------------------------------------------------------ 05 Testing & Optimization (ink)
# Every breakpoint is tried for real: the device under test changes to match the QA row being
# checked (phone, tablet, desktop), and the last pass runs through checkout.
T5 = 9
T_ROW = [.7 + 1.2 * k for k in range(4)]
icons = [
    lambda y: f'<rect x="172" y="{y + 4}" width="8" height="14" rx="2"/><line x1="175" y1="{y + 15.5}" x2="177" y2="{y + 15.5}"/>',
    lambda y: f'<rect x="170" y="{y + 4}" width="12" height="14" rx="2"/><line x1="175" y1="{y + 15.5}" x2="177" y2="{y + 15.5}"/>',
    lambda y: f'<rect x="168.5" y="{y + 5}" width="15" height="9.5" rx="1.5"/><line x1="173" y1="{y + 17.5}" x2="179" y2="{y + 17.5}"/>',
    lambda y: f'<path d="M168.5 {y + 6}h2.4l1.9 8.2h8.4l1.7-5.8h-10.9"/><circle cx="174.2" cy="{y + 17.4}" r="1.1"/><circle cx="180.4" cy="{y + 17.4}" r="1.1"/>',
]
labels5 = ['Mobile', 'Tablet', 'Desktop', 'Checkout']
rows5 = ''
for k in range(4):
    y = 60 + 28 * k
    rows5 += (f'<g class="vz5-row vz5-r{k}"><rect class="vz5-rbg" x="164" y="{y}" width="116" height="22" rx="7"/>'
              f'<g class="vz5-ic">{icons[k](y)}</g><text x="190" y="{y + 14.5}">{labels5[k]}</text></g>'
              f'<rect class="vz5-scan vz5-sc{k}" x="164" y="{y}" width="40" height="22" rx="7" fill="#fff" fill-opacity=".1"/>'
              f'<circle class="vz5-wait vz5-wt{k}" cx="268" cy="{y + 11}" r="4.5"/>'
              f'<g class="vz-chk vz5-ck{k}"><circle cx="268" cy="{y + 11}" r="6"/><path d="M265.2 {y + 11.2}l1.9 1.9 3.6-3.8"/></g>')
def screen(slug, x, y, w, h, rx, cid):
    """A supplied page view on a device screen, shown whole (object-fit: contain): a view wider than
    the screen fills its width from the top of the page, a taller one fills its height, centred; any
    space left over is the page's own background."""
    W, H = ALL[slug][:2]
    if W / H >= w / h:
        box = (0, 0, W, round(W * h / w, 1))
    else:
        bw = round(H * w / h, 1)
        box = (round((W - bw) / 2, 1), 0, bw, H)
    return photo(slug, x, y, w, h, rx, cid, box=box)


DEV = f'''<g class="vz5-dev vz5-ph"><rect class="vz5-frame" x="61" y="44" width="46" height="92" rx="8"/><rect class="vz5-notch" x="77" y="48" width="14" height="3" rx="1.5"/>
{screen("p5-mobile", 64, 54, 40, 78, 4, "vz5-p1")}</g>
<g class="vz5-dev vz5-tb"><rect class="vz5-frame" x="43" y="40" width="82" height="104" rx="8"/>
{screen("p5-tablet", 47, 44, 74, 96, 4.5, "vz5-p2")}</g>
<g class="vz5-dev vz5-dt"><rect class="vz5-frame" x="20" y="46" width="128" height="82" rx="6"/><rect class="vz5-stand" x="76" y="128" width="16" height="8"/><rect class="vz5-stand" x="64" y="136" width="40" height="3" rx="1.5"/>
<rect x="24" y="50" width="120" height="74" rx="2.5" fill="#FDFDFD"/>
<g class="vz5-main">{screen("p5-desktop", 24, 50, 120, 74, 2.5, "vz5-p3")}</g>
<g class="vz5-co">{screen("p5-checkout", 24, 50, 120, 74, 2.5, "vz5-p4")}</g></g>'''
S5 = f'''<svg class="vz vz5" viewBox="0 0 300 200" aria-hidden="true" focusable="false">
{DEV}
<g class="vz5-w vz5-w0"><text class="vz5-lbl" x="84" y="172">390 px</text></g><g class="vz5-w vz5-w1"><text class="vz5-lbl" x="84" y="172">768 px</text></g><g class="vz5-w vz5-w2"><text class="vz5-lbl" x="84" y="172">1440 px</text></g>
<rect class="vz-glass" x="156" y="20" width="132" height="160" rx="12"/>
<text class="vz-h" x="168" y="41">QA report</text>
<line class="vz-rule" x1="168" y1="50" x2="276" y2="50"/>
{rows5}
</svg>'''
DEV_IN = 'opacity:0;transform:scale(.94)'
spans = [('.vz5-ph', .3, T_ROW[1] - .15), ('.vz5-tb', T_ROW[1] - .15, T_ROW[2] - .15)]
for sel, a, b in spans:
    raw(sel, 'vz5' + sel.replace('.vz5', ''), T5,
        f'0%,{pct(a, T5)}{{{DEV_IN};animation-timing-function:{EO}}}{pct(a + .4, T5)},{pct(b, T5)}{{opacity:1;transform:none;animation-timing-function:{SOFT}}}{pct(b + .25, T5)},100%{{{DEV_IN}}}')
raw('.vz5-dt', 'vz5-dt', T5,
    f'0%,{pct(T_ROW[2] - .15, T5)}{{{DEV_IN};animation-timing-function:{EO}}}{pct(T_ROW[2] + .25, T5)},{pct(8.3, T5)}{{opacity:1;transform:none;animation-timing-function:{SOFT}}}{pct(8.7, T5)},100%{{{DEV_IN}}}')
raw('.vz5-main', 'vz5-main', T5, f'0%,{pct(T_ROW[3] - .1, T5)}{{opacity:1}}{pct(T_ROW[3] + .2, T5)},{pct(8.7, T5)}{{opacity:0}}100%{{opacity:1}}')
raw('.vz5-co', 'vz5-co', T5, f'0%,{pct(T_ROW[3], T5)}{{opacity:0}}{pct(T_ROW[3] + .3, T5)},{pct(8.3, T5)}{{opacity:1}}{pct(8.7, T5)},100%{{opacity:0}}')
for k, (a, b) in enumerate([(.3, T_ROW[1] - .15), (T_ROW[1] - .15, T_ROW[2] - .15)]):
    raw(f'.vz5-w{k}', f'vz5-w{k}', T5, f'0%,{pct(a, T5)}{{opacity:0}}{pct(a + .3, T5)},{pct(b, T5)}{{opacity:1}}{pct(b + .2, T5)},100%{{opacity:0}}')
raw('.vz5-w2', 'vz5-w2', T5, f'0%,{pct(T_ROW[2] - .15, T5)}{{opacity:0}}{pct(T_ROW[2] + .15, T5)},{pct(8.3, T5)}{{opacity:1}}{pct(8.7, T5)},100%{{opacity:0}}')
for k in range(4):
    cyc(f'.vz5-r{k}', f'vz5-r{k}', T5, .3 + .15 * k, .5, 'opacity:0;transform:translateX(6px)', 'opacity:1;transform:none', 8.3)
    t = T_ROW[k]
    raw(f'.vz5-sc{k}', f'vz5-sc{k}', T5,
        f'0%,{pct(t, T5)}{{opacity:0;transform:none;animation-timing-function:{SOFT}}}{pct(t + .15, T5)}{{opacity:1;transform:translateX(10px);animation-timing-function:{SOFT}}}'
        f'{pct(t + .6, T5)}{{opacity:1;transform:translateX(66px);animation-timing-function:{SOFT}}}{pct(t + .75, T5)},100%{{opacity:0;transform:translateX(76px)}}')
    raw(f'.vz5-wt{k}', f'vz5-wt{k}', T5,
        f'0%,{pct(t - .05, T5)}{{opacity:0}}{pct(t + .05, T5)},{pct(t + .6, T5)}{{opacity:1}}{pct(t + .7, T5)},100%{{opacity:0}}')
    cyc(f'.vz5-ck{k}', f'vz5-ck{k}', T5, t + .65, .45, *POP, 8.3, ease=BK)

# ------------------------------------------------------------------ 06 Launch & Support (ember)
# Go-live: build, deploy, live; the old addresses are redirected to the new ones so nothing is lost,
# and support picks up after launch.
T6 = 9
nodes6 = [(60, 'Build'), (150, 'Deploy'), (240, 'Live')]
nodes_svg = ''
for k, (x, lbl) in enumerate(nodes6):
    nodes_svg += (f'<circle class="vz6-ring" cx="{x}" cy="36" r="13"/>'
                  f'<g class="vz6-done vz6-d{k}"><circle cx="{x}" cy="36" r="13"/><path d="M{x - 5.5} 36.5l3.8 3.8 7-7.4"/></g>'
                  f'<text class="vz6-lbl" x="{x}" y="64">{lbl}</text>')
redirects = [('/shop', '/collections'), ('/about-us', '/about'), ('/p/1042', '/products/tote')]
T_RD = [3.6, 4.0, 4.4]
rd_svg = ''
for k, (old, new) in enumerate(redirects):
    y = 151 + 13 * k
    rd_svg += (f'<text class="vz6-old" x="40" y="{y}">{old}</text>'
               f'<path class="vz6-arr vz6-a{k}" d="M80 {y - 2.6}H96M93 {y - 5.2}l3 2.6-3 2.6" pathLength="1"/>'
               f'<g class="vz6-new vz6-n{k}"><text x="102" y="{y}">{new}</text></g>'
               f'<g class="vz6-ok vz6-o{k}"><circle cx="170" cy="{y - 2.6}" r="4"/><path d="M168.2 {y - 2.5}l1.2 1.2 2.4-2.5"/></g>')
S6 = f'''<svg class="vz vz6" viewBox="0 0 300 200" aria-hidden="true" focusable="false">
<line class="vz6-track" x1="73" y1="36" x2="137" y2="36"/><line class="vz6-track" x1="163" y1="36" x2="227" y2="36"/>
<line class="vz6-prog vz6-p0" x1="73" y1="36" x2="137" y2="36"/><line class="vz6-prog vz6-p1" x1="163" y1="36" x2="227" y2="36"/>
<g class="vz6-pulse"><circle cx="240" cy="36" r="13"/></g>
{nodes_svg}
<rect class="vz-drop vz-drop--soft" x="33" y="82" width="240" height="30" rx="15"/>
<rect class="vz6-bar" x="30" y="78" width="240" height="30" rx="15"/>
<rect class="vz6-lock" x="44" y="92" width="9" height="7.5" rx="1.8"/><path class="vz6-shackle" d="M46.2 92v-2.2a2.3 2.3 0 0 1 4.6 0V92"/>
<text class="vz6-url" x="60" y="96.8">atelierstore.com</text>
<g class="vz6-live"><rect x="216" y="85" width="46" height="16" rx="8"/><circle class="vz6-ldot" cx="227" cy="93" r="2.6"/><text x="233" y="96.3">Live</text></g>
<g class="vz6-rd"><rect class="vz-drop vz-drop--soft" x="33" y="125" width="150" height="66" rx="10"/><rect class="vz6-panel" x="30" y="122" width="150" height="66" rx="10"/>
<text class="vz6-ph" x="40" y="136">Redirects</text><text class="vz6-ph2" x="170" y="136">301</text>
{rd_svg}</g>
<g class="vz6-chat"><rect x="192" y="124" width="78" height="30" rx="10"/><path d="M200 153l-1 8 8-7.5Z"/><circle class="vz6-av" cx="206" cy="139" r="6.5"/>
<text class="vz6-msg" x="218" y="137.4">Can we add a</text><text class="vz6-msg" x="218" y="145">sale banner?</text></g>
<text class="vz6-sup" x="231" y="178">Support</text>
</svg>'''
for k, t in enumerate([.3, 1.45, 2.6]):
    cyc(f'.vz6-d{k}', f'vz6-d{k}', T6, t, .5, *POP, 8.4, ease=BK)
cyc('.vz6-p0', 'vz6-p0', T6, .5, .95, *GROW, 8.4, ease=SOFT)
cyc('.vz6-p1', 'vz6-p1', T6, 1.65, .95, *GROW, 8.4, ease=SOFT)
cyc('.vz6-pulse', 'vz6-pulse', T6, 2.8, .3, *FADE, 8.4)
RULES.append('.js .vz6-pulse circle{animation:vz6-ping 1.8s cubic-bezier(.23,1,.32,1) infinite}')
KF.append('@keyframes vz6-ping{0%{opacity:.7;transform:none}70%,100%{opacity:0;transform:scale(1.9)}}')
cyc('.vz6-live', 'vz6-live', T6, 2.85, .55, *POP, 8.4, ease=BK)
RULES.append('.js .vz6-ldot{animation:vz6-blink 1.4s ease-in-out infinite}')
KF.append('@keyframes vz6-blink{50%{opacity:.25}}')
cyc('.vz6-rd', 'vz6-rd', T6, 3.2, .55, *FADE_UP, 8.4)
for k, t in enumerate(T_RD):
    cyc(f'.vz6-a{k}', f'vz6-a{k}', T6, t, .35, *DRAW, 8.4, ease=SOFT)
    cyc(f'.vz6-n{k}', f'vz6-n{k}', T6, t + .25, .35, 'opacity:0;transform:translateX(-4px)', 'opacity:1;transform:none', 8.4)
    cyc(f'.vz6-o{k}', f'vz6-o{k}', T6, t + .4, .4, *POP, 8.4, ease=BK)
cyc('.vz6-chat', 'vz6-chat', T6, 5.3, .55, 'opacity:0;transform:translateY(6px) scale(.94)', 'opacity:1;transform:none', 8.4, ease=BK)
cyc('.vz6-sup', 'vz6-sup', T6, 5.5, .4, *FADE, 8.4)

# ------------------------------------------------------------------ shared CSS
BASE = r'''
/* Six stages: animated stage visuals. Each stage image is replaced by an illustration drawn on a
   300 x 200 grid; the scene scales with its panel (1 unit = 0.1em). Base styles are the finished
   frame (reduced motion and no-script show this); the motion rules below play the loop, and only
   for the visual that can be seen (script adds .is-playing). */
.rf-viz{container-type:size;display:grid;place-items:center;--viz-reserve:3rem}
.rf-step__media.rf-viz{aspect-ratio:5/4}
.rf-step__media.rf-viz::after{content:none}
.rf-step__media.rf-viz--ink{background:var(--black);box-shadow:inset 0 0 0 1px rgba(255,255,255,.08)}
.rf-step__media.rf-viz--ember{background:var(--orange)}
.rf-viz__scene{width:30em;height:20em;margin-bottom:var(--viz-reserve);font-size:min(calc((100cqw - 2.5rem) / 30),calc((100cqh - var(--viz-reserve) - 1.75rem) / 20))}
.rf-viz__scene>svg{display:block;width:100%;height:100%;overflow:visible}
.rf-process.is-stepper .rf-viz{--viz-reserve:0px}
.rf-process.is-stepper .rf-step__media.rf-viz--ink,.rf-process.is-stepper .rf-step__media.rf-viz--ember{background:none;box-shadow:none}
/* With no orange panel behind them, the stage 2, 4 and 6 visuals sit on the dark section: lines and
   labels drawn in charcoal for the panel turn light, and progress takes the orange accent. */
.rf-process.is-stepper .rf-viz--ember{--vz-ink:var(--orange)}
.rf-process.is-stepper .vz2-segbg{fill:rgba(255,255,255,.5);stroke:rgba(255,255,255,.65)}
.rf-process.is-stepper .vz2-wire{stroke:rgba(255,255,255,.5)}
.rf-process.is-stepper .vz2-track,.rf-process.is-stepper .vz6-track{stroke:rgba(255,255,255,.22)}
.rf-process.is-stepper .vz2-prog,.rf-process.is-stepper .vz6-prog{stroke:var(--orange)}
.rf-process.is-stepper .vz2-tl,.rf-process.is-stepper .vz6-lbl{fill:rgba(255,255,255,.72)}
.rf-process.is-stepper .vz4-ed{stroke:rgba(255,255,255,.14);stroke-width:1}
.rf-process.is-stepper .vz4-chip rect{fill:rgba(255,255,255,.08);stroke:rgba(255,255,255,.24)}
.rf-process.is-stepper .vz4-st{fill:var(--white)}
.rf-process.is-stepper .vz4-spin{stroke:var(--white)}
.rf-process.is-stepper .vz4-ok circle{fill:var(--orange)}
.rf-process.is-stepper .vz6-pulse circle{stroke:var(--orange)}
.rf-process.is-stepper .vz6-ring{fill:rgba(255,255,255,.12);stroke:rgba(255,255,255,.4)}
.rf-process.is-stepper .vz6-sup{fill:rgba(255,255,255,.72)}
.rf-process.is-stepper .rf-viz__scene{transform:scale(1.06);transition:transform 1.4s var(--ease-out)}
.rf-process.is-stepper .rf-step.is-active .rf-viz__scene{transform:none}
.vz text{font-family:var(--body);font-weight:600}
.vz-glass{fill:rgba(255,255,255,.06);stroke:rgba(255,255,255,.16);stroke-width:1}
.vz .vz-h{font-family:var(--body);font-size:10px;fill:var(--white);letter-spacing:-.01em}
.vz-rule{stroke:rgba(255,255,255,.12)}
.vz .vz-val{font-size:5.6px;font-weight:500;fill:rgba(255,255,255,.66)}
.vz3-tok{fill:var(--orange)}
.vz-dot{fill:rgba(255,255,255,.28)}
.vz-chk circle{fill:var(--orange)}
.vz-chk path{''' + CHECK + r'''}
.vz-drop{fill:rgba(25,24,29,.2)}
.vz-drop--soft{fill:rgba(25,24,29,.12)}
.vz-cursor{fill:var(--white);stroke:var(--charcoal);stroke-width:1.5;stroke-linejoin:round}
.vz [class*="vz"]{transform-box:fill-box}
.vz-chk,.vz2-node,.vz2-leaf,.vz3-sw,.vz3-ring,.vz3-ripple,.vz4-ok,.vz4-node,.vz5-wait,.vz6-done,.vz6-live,.vz6-ok,.vz6-pulse circle,.vz1-ping,.vz1-dot{transform-origin:center}
.vz-sk,.vz1-row .vz-sk,.vz2-prog,.vz6-prog,.vz3-sp0,.vz3-sp1,.vz3-sp2{transform-origin:left center}
.vz6-chat{transform-origin:left bottom}
.vz4-pv{transform-origin:center}
/* 01 */
.vz1-grid circle,.vz1-grid line{fill:none;stroke:rgba(255,255,255,.12);stroke-width:1}
.vz1-grid line{stroke:rgba(255,255,255,.06)}
.vz .vz1-sweep{transform-box:view-box;transform-origin:96px 102px;transform:rotate(130deg)}
.vz1-sweep line{stroke:var(--orange);stroke-width:1.4;stroke-linecap:round}
.vz1-link{fill:none;stroke:var(--orange-soft);stroke-width:1.2;stroke-dasharray:2 3;stroke-linecap:round;opacity:.75}
.vz1-dot{fill:var(--white)}
.vz1-ping{fill:none;stroke:var(--orange);stroke-width:1.2;opacity:0}
.vz1-core{fill:var(--orange)}
.vz1-row text{font-size:8.6px;fill:rgba(255,255,255,.9)}
/* 02 */
.vz2-segbg{fill:rgba(255,255,255,.3);stroke:rgba(255,255,255,.45)}
.vz2-thumb{fill:var(--white)}
.vz2-seg text,.vz2-node text{font-size:9px;fill:var(--charcoal);text-anchor:middle}
.vz2-node rect{fill:var(--white)}
.vz2-leaf rect{fill:rgba(255,255,255,.5)}.vz .vz2-leaf text{font-size:5.5px;fill:var(--charcoal);text-anchor:middle}
.vz2-wire{fill:none;stroke:rgba(25,24,29,.5);stroke-width:1.4;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1 2}
.vz2-track{stroke:rgba(255,255,255,.45);stroke-width:3;stroke-linecap:round}
.vz2-prog{stroke:var(--charcoal);stroke-width:3;stroke-linecap:round}
.vz2-ms{fill:var(--vz-ink,var(--charcoal));stroke:var(--white);stroke-width:2}
.vz2-tl{font-size:8.6px;fill:rgba(25,24,29,.72)}
/* 03 */
.vz3-ta{fill:#F5F4F1}
.vz3-tb{fill:var(--charcoal);stroke:rgba(255,255,255,.22)}.vz3-tbe{fill:none;stroke:rgba(255,255,255,.22)}
.vz3-tc{fill:var(--coral)}
.vz3-cd0,.vz3-cd2{opacity:.35}
.vz .vz3-tl{font-size:8px;fill:rgba(255,255,255,.6);text-anchor:middle}
.vz3-ring{fill:none;stroke:var(--white);stroke-width:1.4}
.vz3-ok rect{fill:var(--orange)}
.vz3-ok path{fill:none;stroke:var(--charcoal);stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.vz .vz3-ok text{font-size:7.8px;fill:var(--charcoal);text-anchor:middle}
.vz .vz3-aa{font-family:var(--display);font-size:26px;fill:var(--white);letter-spacing:0}
.vz3-sw3{stroke:rgba(255,255,255,.3)}
.vz3-ripple{fill:none;stroke:var(--white);stroke-width:1.6;opacity:0}
.vz3-cur{opacity:0}
.vz3-arrow{transform-origin:left top}
/* 04 */
.vz4-ed{fill:var(--charcoal)}
.vz4-dim{fill:rgba(255,255,255,.22)}
.vz4-tab{fill:var(--charcoal-3)}
.vz .vz4-tabt{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:7.6px;font-weight:500;fill:rgba(255,255,255,.88)}
.vz .vz4-tabt--dim{fill:rgba(255,255,255,.38)}
.vz4-sep{stroke:rgba(255,255,255,.08)}
.vz4-branch{stroke:rgba(255,255,255,.18);stroke-width:1.6;transform-origin:center top}
.vz4-node{fill:var(--orange);stroke:var(--charcoal);stroke-width:2}
.vz .vz4-msg{font-size:8.2px;fill:rgba(255,255,255,.9)}
.vz .vz4-sha{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:6.4px;font-weight:500;fill:rgba(255,255,255,.4)}
.vz4-prev{fill:var(--white)}
.vz .vz4-logo{font-size:6.5px;font-weight:800;letter-spacing:.04em;fill:var(--charcoal)}.vz .vz4-name{font-size:5px;fill:rgba(25,24,29,.72)}
.vz4-ash{fill:rgba(25,24,29,.2)}
.vz4-wb{fill:var(--white)}
.vz4-tile{fill:#F2F0EC}
.vz4-chip rect{fill:rgba(255,255,255,.3);stroke:rgba(255,255,255,.5)}
.vz4-spin{fill:none;stroke:var(--charcoal);stroke-width:1.6;stroke-linecap:round;stroke-dasharray:20 12;transform-origin:center;opacity:0}
.vz4-ok circle{fill:var(--charcoal)}
.vz4-ok path{''' + CHECK + r'''}
.vz4-st{font-size:8.4px;fill:var(--charcoal)}
.vz4-st0{opacity:0}
/* 05 */
.vz5-frame{fill:#141417;stroke:rgba(255,255,255,.3);stroke-width:1.2}
.vz5-notch,.vz5-stand{fill:rgba(255,255,255,.3)}
.vz5-k1{fill:rgba(255,255,255,.55)}.vz5-k2{fill:rgba(255,255,255,.22)}
.vz5-img{fill:rgba(255,255,255,.1)}.vz5-tile{fill:rgba(255,255,255,.07)}.vz5-btn{fill:var(--orange)}
.vz5-field{fill:none;stroke:rgba(255,255,255,.25)}.vz5-sum{fill:rgba(255,255,255,.06)}
.vz5-ph,.vz5-tb,.vz5-co,.vz5-w0,.vz5-w1{opacity:0}
.vz5-dev{transform-origin:center}
.vz5-lbl{font-size:9px;fill:var(--text-muted-on-dark);text-anchor:middle}
.vz5-rbg{fill:rgba(255,255,255,.04)}
.vz5-ic{fill:none;stroke:rgba(255,255,255,.75);stroke-width:1.2;stroke-linecap:round;stroke-linejoin:round}
.vz5-row text{font-size:8.6px;fill:rgba(255,255,255,.9)}
.vz5-scan,.vz5-wait{opacity:0}
.vz5-wait{fill:none;stroke:rgba(255,255,255,.55);stroke-width:1.4;stroke-dasharray:18 10}
/* 06 */
.vz6-track{stroke:rgba(255,255,255,.45);stroke-width:3;stroke-linecap:round}
.vz6-prog{stroke:var(--charcoal);stroke-width:3;stroke-linecap:round}
.vz6-ring{fill:rgba(255,255,255,.28);stroke:rgba(255,255,255,.55);stroke-width:1.5}
.vz6-done circle{fill:var(--white)}
.vz6-done path{stroke:var(--charcoal);stroke-width:1.9;fill:none;stroke-linecap:round;stroke-linejoin:round}
.vz6-pulse circle{fill:none;stroke:var(--charcoal);stroke-width:1.5;opacity:0;transform-box:fill-box}
.vz6-lbl{font-size:9.4px;fill:var(--charcoal);text-anchor:middle}
.vz6-bar,.vz6-panel{fill:rgba(255,255,255,.95)}
.vz6-lock{fill:var(--charcoal)}
.vz6-shackle{fill:none;stroke:var(--charcoal);stroke-width:1.5}
.vz6-url{font-size:10px;fill:var(--charcoal)}
.vz6-live rect{fill:var(--charcoal)}
.vz6-live text{font-size:8px;fill:var(--white)}
.vz6-ldot{fill:var(--white)}
.vz .vz6-ph{font-size:8.4px;fill:var(--charcoal)}
.vz .vz6-ph2{font-size:7.4px;fill:rgba(25,24,29,.5);text-anchor:end}
.vz .vz6-old{font-size:7.4px;fill:rgba(25,24,29,.5)}
.vz .vz6-new text{font-size:7.4px;fill:var(--charcoal)}
.vz6-arr{fill:none;stroke:var(--orange);stroke-width:1.3;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:0}
.vz6-ok circle{fill:var(--orange)}
.vz6-ok path{fill:none;stroke:#fff;stroke-width:1.3;stroke-linecap:round;stroke-linejoin:round}
.vz6-chat rect:first-child,.vz6-chat path{fill:var(--white)}
.vz6-av{fill:var(--orange)}
.vz .vz6-msg{font-size:5.2px;fill:var(--charcoal)}
.vz .vz6-sup{font-size:8.4px;fill:var(--charcoal);text-anchor:middle}
'''

MOTION_HEAD = '''@media (prefers-reduced-motion:no-preference){
  /* Visuals that cannot be seen hold their frame; .is-playing lets them run. */
  .js .rf-process .rf-viz:not(.is-playing) *{animation-play-state:paused}
  @keyframes vz-spin{to{transform:rotate(360deg)}}
  @keyframes vz-flow{to{stroke-dashoffset:-10}}
  .js .vz4-spin{animation:vz-spin .9s linear infinite,vz4-spinvis 9s linear infinite both}
'''


def build_css():
    rules = [r for r in RULES if not r.startswith(('.js .vz4-spin{', '.js .vz4-endcar{'))]
    body = '\n'.join('  ' + r for r in rules) + '\n' + '\n'.join('  ' + k for k in KF)
    return BASE.strip() + '\n' + MOTION_HEAD + body + '\n}\n'


SCENES = [
    ('ink', S1, 'Illustration: a radar scan turning findings into a project brief with goals, audience and scope'),
    ('ember', S2, 'Illustration: a platform comparison, a sitemap tree and a timeline from kick-off to launch'),
    ('ink', S3, 'Illustration: three visual directions for a wireless headphones product page side by side; B, the dark design with orange accents, is approved and its type, colours and spacing become the design system'),
    ('ember', S4, 'Illustration: commits landing on the main branch while the private staging preview builds up with a Luxury Bags banner and product tiles for a watch and sunglasses, then staging is ready'),
    ('ink', S5, 'Illustration: the same menswear store page, with its Classic Jacket, tested on a phone, a tablet and a desktop and through checkout, each ticked off in a QA report'),
    ('ember', S6, 'Illustration: build, deploy and live steps, the live address, old pages redirected to their new addresses and a support message'),
]


def media_html(kind, svg, label):
    svg = re.sub(r'\n', '', svg)
    return (f'<div class="rf-step__media rf-media rf-viz rf-viz--{kind}" data-viz role="img" aria-label="{label}">'
            f'<div class="rf-viz__scene">{svg}</div></div>')


if __name__ == '__main__':
    body = (ROOT / 'src/02-body.html').read_text()
    olds = re.findall(r'<div class="rf-step__media rf-media[^"]*"[^>]*>.*?</div></div>|<div class="rf-step__media rf-media"><img [^>]*></div>', body)
    assert len(olds) == 6, len(olds)
    for old, (kind, svg, label) in zip(olds, SCENES):
        body = body.replace(old, media_html(kind, svg, label), 1)
    (ROOT / 'src/02-body.html').write_text(body)

    head = (ROOT / 'src/01-head.html').read_text()
    start, end = '/* VIZ:START */', '/* VIZ:END */'
    block = start + '\n' + build_css() + end
    if start in head:
        head = re.sub(re.escape(start) + r'.*?' + re.escape(end), lambda m: block, head, flags=re.S)
    else:
        anchor = '@media (hover:hover) and (pointer:fine){.rf-process.is-stepper .rf-step:not(.is-active) .rf-step__body:hover h3{color:var(--white)}}\n'
        assert anchor in head
        head = head.replace(anchor, anchor + block + '\n', 1)
    (ROOT / 'src/01-head.html').write_text(head)
    print('scenes written; css', len(block) // 1024, 'KB;', len(KF), 'keyframes')
