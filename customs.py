"""Custom animations, called with [custom: name | args...].
Each function: fn(c, t, dur, args, board) where t is seconds since the board appeared.
Add new ones at the bottom and register them in REGISTRY."""
import math, random
from .core import *


def gears(c, t, dur, args, b):
    """[custom: gears | TITLE | word | word ...]  Gears that slow down as grit builds up (friction)."""
    title = args[0] if args else 'FRICTION'; words = args[1:]
    sl = clamp((t - 2) / max(3, dur - 3)); ang = t * 1.4 * (1 - 0.45 * sl)
    _gear(c, 500, 330, 110, ang, INK, 1, 12); _gear(c, 690, 330, 80, -ang * 1.37 + 0.2, (0.4, 0.3, 0.2), 1, 9)
    rnd = random.Random(3)
    for i in range(int(160 * sl)):
        c.new_path(); c.arc(rnd.uniform(400, 780), rnd.uniform(230, 440), 2.5, 0, 7); c.set_source_rgba(0.75, 0.6, 0.35, 1); c.fill()
    text(c, title.upper(), 600, 520, 44, RED, prog(t, 0.3, 0.5), face=TITLE, bold=True, align='c')
    for i, s in enumerate(words[:6]):
        text(c, s, 1040, 200 + i * 50, 28, INK, prog(t, 1 + i * (dur - 2) / max(1, len(words)), 0.4), italic=True, bold=True, align='c')


def _gear(c, x, y, r, ang, rgb, a, n=10):
    c.new_path(); c.save(); c.translate(x, y); c.rotate(ang)
    for i in range(n * 2):
        rr = r if i % 2 == 0 else r * 0.8; a0 = i * math.pi / n
        c.line_to(rr * math.cos(a0), rr * math.sin(a0)); c.line_to(rr * math.cos(a0 + math.pi / n), rr * math.sin(a0 + math.pi / n))
    c.close_path(); c.set_source_rgba(*rgb, a); c.fill(); c.arc(0, 0, r * 0.25, 0, 7); c.set_source_rgba(*PARCH, a); c.fill(); c.restore()


def magnets(c, t, dur, args, b):
    """[custom: magnets | A ; sub | B ; sub | C ; sub | pull=1 | object=WAR]  Three forces pulling one object.
    pull=1/2/3 makes that magnet win in the second half of the board."""
    labs = [(x.split(';') + [''])[:2] for x in args if not x.startswith(('pull=', 'object='))] or [['PASSION', 'the people'], ['CHANCE', 'army'], ['REASON', 'government']]
    labs = (labs + [['', '']] * 3)[:3]
    pull = next((int(x[5:]) for x in args if x.startswith('pull=')), 0)
    pts = [(640, 130), (330, 470), (950, 470)]; cols = (RED, GOLD, BLUE)
    for (x, y), (n, s), col in zip(pts, labs, cols):
        a = prog(t, 0.2 + pts.index((x, y)) * 0.6, 0.5)
        c.new_path(); c.set_source_rgba(*col, a); c.set_line_width(26); c.arc(x, y, 40, math.pi, 2 * math.pi); c.stroke()
        yy = y + 50 if y < 300 else y + 85
        text(c, n.strip().upper(), x, yy, 30, col, a, face=TITLE, bold=True, align='c'); text(c, s.strip(), x, yy + 32, 22, INK, a, italic=True, align='c')
    sw = 0.35 * math.sin(t * 1.3); w = [1 + sw, 1 - sw * 0.5, 1 + math.cos(t * 1.7) * 0.35]
    if pull:
        pp = prog(t, dur * 0.45, 3); w = [wi * (1 - 0.9 * pp) for wi in w]; w[pull - 1] = 1 + 3 * pp
    tot = sum(w); ox = sum(p[0] * k for p, k in zip(pts, w)) / tot; oy = sum(p[1] * k for p, k in zip(pts, w)) / tot + 40
    for (x, y), col in zip(pts, cols):
        c.new_path(); c.set_source_rgba(*col, 0.5); c.set_line_width(2); c.set_dash([6, 6]); c.move_to(x, y); c.line_to(ox, oy); c.stroke(); c.set_dash([])
    c.new_path(); c.arc(ox, oy, 26, 0, 7); c.set_source_rgba(*INK, 1); c.fill(); obj = next((x[7:] for x in args if x.startswith('object=')), 'WAR')
    text(c, obj, ox, oy + 6, 16, (1, 1, 1), 1, bold=True, align='c')


def hub(c, t, dur, args, b):
    """[custom: hub | CENTRE | spoke | spoke ... | collapse]  Hub-and-spoke wheel; 'collapse' knocks out the hub halfway."""
    centre = args[0] if args else 'CoG'; spokes = [a for a in args[1:] if a != 'collapse'] or ['army', 'capital', 'alliance', 'leader', 'opinion', 'economy']
    hit = prog(t, dur * 0.5, 1.5) if 'collapse' in args else 0
    cx, cy = 640, 370; n = len(spokes)
    for i, s in enumerate(spokes):
        ang = i * 2 * math.pi / n - math.pi / 2; fall = hit * (1 + i * 0.1); a = prog(t, 0.5 + i * 0.3, 0.4)
        x, y = cx + 230 * math.cos(ang), cy + 190 * math.sin(ang) + 220 * fall ** 2
        c.new_path(); c.set_source_rgba(*INK, a * (1 - hit)); c.set_line_width(4); c.move_to(cx, cy); c.line_to(x, y); c.stroke()
        panel(c, x - 85, y - 25, 170, 50, a * (1 - 0.6 * hit)); text(c, s, x, y + 8, 22, INK, a * (1 - 0.6 * hit), bold=True, align='c')
    c.new_path(); c.arc(cx, cy, 72, 0, 7); c.set_source_rgba(*RED, 1 - hit); c.fill()
    text(c, centre, cx, cy + 10, 28 if len(centre) < 6 else 20, (1, 1, 1), 1 - hit, face=TITLE, bold=True, align='c')
    explosion(c, cx, cy, hit * 1.2, 1, 110)


def water(c, t, dur, args, b):
    """[custom: water | STRENGTH]  Water flowing around an obstacle."""
    lab = args[0] if args else 'STRENGTH'
    for k in range(9):
        y0 = 360 + k * 18; c.new_path(); c.move_to(100, y0)
        for x in range(100, 1181, 10):
            d = abs(x - 640); bump = -max(0, 140 - d) * 1.1 if y0 < 470 else 0
            y = y0 + 6 * math.sin(x * 0.03 - t * 4 + k) + (bump if d < 140 else 0)
            c.line_to(x, y if d >= 90 or y0 >= 470 else max(y, 520))
        c.set_source_rgba(0.25, 0.45, 0.70, 0.6); c.set_line_width(3); c.stroke()
    c.new_path(); c.set_source_rgba(0.45, 0.40, 0.35, 1); c.move_to(540, 540); c.line_to(640, 300); c.line_to(740, 540); c.close_path(); c.fill()
    text(c, lab.upper(), 640, 290, 26, INK, 1, face=TITLE, bold=True, align='c')


def curve(c, t, dur, args, b):
    """[custom: curve | POINT LABEL | attacker | defender]  Strength falling with distance until it crosses a line."""
    lab = args[0] if args else 'CULMINATING POINT'; la = args[1] if len(args) > 1 else 'attacker'; lb = args[2] if len(args) > 2 else 'defender'
    c.new_path(); c.set_source_rgba(*INK, 1); c.set_line_width(3); c.move_to(150, 560); c.line_to(1130, 560); c.move_to(150, 560); c.line_to(150, 180); c.stroke()
    text(c, "distance →", 1120, 600, 22, INK, 1, italic=True, align='r'); text(c, "strength", 140, 170, 22, INK, 1, italic=True)
    p = prog(t, 0.5, max(2, dur * 0.5)); c.new_path(); c.move_to(150, 220)
    for i in range(int(100 * p) + 1): x = 150 + 9.8 * i; c.line_to(x, 220 + 0.00036 * (9.8 * i) ** 2)
    c.set_source_rgba(*RED, 1); c.set_line_width(6); c.stroke()
    c.new_path(); c.set_dash([10, 8]); c.move_to(150, 400); c.line_to(1130, 400); c.set_source_rgba(*BLUE, 1); c.set_line_width(3); c.stroke(); c.set_dash([])
    text(c, lb, 1120, 390, 22, BLUE, 1, bold=True, align='r'); text(c, la, 300, 210, 22, RED, 1, bold=True)
    cx = 150 + math.sqrt(180 / 0.00036); a = prog(t, 0.5 + max(2, dur * 0.5) * 0.75, 0.6)
    c.new_path(); c.arc(cx, 400, 14, 0, 7); c.set_source_rgba(*GOLD, a); c.fill(); text(c, lab.upper(), cx, 470, 28, GOLD, a, face=TITLE, bold=True, align='c')


def ladder(c, t, dur, args, b):
    """[custom: ladder | TITLE | best option | ... | worst option]  Ranked options, best on top."""
    title = args[0] if args else ''; rungs = args[1:]; n = max(1, len(rungs))
    panel(c, 260, 110, 760, 90 + 66 * n, 1); text(c, title.upper(), SW / 2, 160, 30, INK, 1, face=TITLE, bold=True, align='c')
    for i, r in enumerate(rungs):
        a = prog(t, 0.6 + i * max(0.6, (dur - 2) / n), 0.4); y = 220 + i * 66
        col = GREEN if i == 0 else RED if i == n - 1 else INK
        c.new_path(); c.set_source_rgba(*col, 0.15 * a); c.rectangle(300, y - 30, 680, 50); c.fill()
        text(c, f"{i + 1}. {r}", 320, y + 5, 30, col, a, bold=i == 0)


def scales(c, t, dur, args, b):
    """[custom: scales | LEFT | RIGHT | tip=left]  A balance that tips one way."""
    L = args[0] if args else 'A'; R = args[1] if len(args) > 1 else 'B'
    tip = -1 if any(a == 'tip=left' for a in args) else 1 if any(a == 'tip=right' for a in args) else 0
    ang = tip * 0.25 * prog(t, dur * 0.4, 2) + 0.03 * math.sin(t * 2) * (1 - abs(tip) * prog(t, dur * 0.4, 2))
    cx, cy = 640, 260
    c.new_path(); c.set_source_rgba(*INK, 1); c.set_line_width(8); c.move_to(cx, cy); c.line_to(cx, 560); c.stroke()
    c.move_to(cx - 120, 560); c.line_to(cx + 120, 560); c.stroke()
    dx, dy = 320 * math.cos(ang), 320 * math.sin(ang)
    c.move_to(cx - dx, cy - dy); c.line_to(cx + dx, cy + dy); c.stroke()
    for sgn, s, col in ((-1, L, BLUE), (1, R, RED)):
        x, y = cx + sgn * dx, cy + sgn * dy + 110
        c.set_line_width(2); c.move_to(x, y - 110); c.line_to(x - 70, y); c.move_to(x, y - 110); c.line_to(x + 70, y); c.stroke()
        c.new_path(); c.set_source_rgba(*col, 1); c.arc(x, y, 80, 0, math.pi); c.fill()
        text(c, s, x, y + 120, 30, col, 1, face=TITLE, bold=True, align='c')


# ---------- added Nov 2026: spiral, web, lift, lenses, rings ----------
def _col(name, default):
    return COLORS.get(name.strip().lower(), default) if name else default


def spiral(c, t, dur, args, b):
    """[custom: spiral | STATE A | STATE B | step | step ...]  Security dilemma: two castles take turns building;
    each build raises the OTHER side's fear meter until both are maxed out."""
    A = args[0] if args else 'STATE A'; B = args[1] if len(args) > 1 else 'STATE B'
    steps = args[2:] or ['walls', 'towers', 'missiles', 'warships']; n = len(steps)
    gap = max(1.2, (dur - 3) / n); xs = (380, 900); base = 545
    built = [0.0, 0.0]; fear = [0.08, 0.08]; flash = None
    for i in range(n):
        p = prog(t, 1 + i * gap, 0.8); side = i % 2
        built[side] += p; fear[1 - side] += 0.92 * p / max(1, (n + 1) // 2)
        if 0 < t - (1 + i * gap) < gap: flash = (side, i, t - (1 + i * gap))
    for k, (x, name) in enumerate(zip(xs, (A, B))):
        col = BLUE if k == 0 else RED
        layers = built[k]; h = 60 + 46 * layers
        c.new_path(); c.set_source_rgba(*col, 0.9); c.rectangle(x - 90, base - h, 180, h); c.fill()
        for j in range(5):  # battlements
            c.rectangle(x - 90 + j * 40, base - h - 18, 22, 18)
        c.fill()
        c.set_source_rgba(*PARCH, 0.9); c.rectangle(x - 18, base - 44, 36, 44); c.fill()
        c.set_source_rgba(0, 0, 0, 0.35); c.set_line_width(1.5)
        for j in range(1, int(layers) + 1):
            c.move_to(x - 90, base - 60 - 46 * j + 46); c.line_to(x + 90, base - 60 - 46 * j + 46)
        c.stroke()
        text(c, name.upper(), x, base + 36, 26, col, 1, face=TITLE, bold=True, align='c')
        f = clamp(fear[k]); bx = x - 120
        text(c, 'FEAR', bx, 112, 18, INK, 1, bold=True)
        c.new_path(); c.set_source_rgba(*INK, 0.25); c.rectangle(bx, 122, 240, 22); c.fill()
        fc = (lerp(0.3, 0.75, f), lerp(0.55, 0.15, f), 0.12)
        c.set_source_rgba(*fc, 1); c.rectangle(bx, 122, 240 * f, 22); c.fill()
    for i in range(n):  # step labels stacked in the middle
        a = prog(t, 1 + i * gap, 0.5); side = i % 2
        text(c, ('→ ' if side == 0 else '← ') + steps[i], 640, 230 + i * 40, 24, BLUE if side == 0 else RED, a, italic=True, bold=True, align='c')
    if flash:
        side, i, dt = flash; x0, x1 = (xs[0] + 100, xs[1] - 100) if side == 0 else (xs[1] - 100, xs[0] + 100)
        pp = clamp(dt / 0.9)
        c.new_path(); c.set_source_rgba(*(BLUE if side == 0 else RED), 0.8 * (1 - clamp(dt - 1))); c.set_line_width(5)
        c.set_dash([10, 8]); c.move_to(x0, 200); c.line_to(lerp(x0, x1, pp), 200); c.stroke(); c.set_dash([])
    end = prog(t, 1 + n * gap, 0.8)
    if end > 0: stamp(c, 'BOTH LESS SAFE', 640, 420, end, RED, 44, -0.08, end)


def web(c, t, dur, args, b):
    """[custom: web | A | B | C ... | shock=B | title=...]  States linked like a web; a shock to one shakes every
    other node in turn (regional security complex)."""
    title = next((a[6:] for a in args if a.startswith('title=')), '')
    names = [a for a in args if '=' not in a] or ['A', 'B', 'C', 'D', 'E', 'F']
    shock = next((a[6:] for a in args if a.startswith('shock=')), names[0])
    n = len(names); cx, cy, R = 640, 300, 200
    pts = [(cx + R * math.cos(i * 2 * math.pi / n - math.pi / 2), cy + 0.95 * R * math.sin(i * 2 * math.pi / n - math.pi / 2)) for i in range(n)]
    si = names.index(shock) if shock in names else 0; t0 = dur * 0.35
    def shake(i):
        d = min(abs(i - si), n - abs(i - si)); ts = t0 + d * 0.55
        if t < ts: return 0.0, 0.0
        k = math.exp(-(t - ts) * 0.9); return 9 * k * math.sin((t - ts) * 22), clamp(k * 1.6)
    off = [shake(i) for i in range(n)]
    P = [(x + o[0], y + o[0] * 0.5) for (x, y), o in zip(pts, off)]
    a0 = prog(t, 0.3, 1)
    for i in range(n):
        for j in range(i + 1, n):
            hot = max(off[i][1], off[j][1])
            c.new_path(); c.set_source_rgba(lerp(INK[0], RED[0], hot), lerp(INK[1], RED[1], hot), lerp(INK[2], RED[2], hot), a0 * (0.25 + 0.5 * hot))
            c.set_line_width(1.5 + 2 * hot); c.move_to(*P[i]); c.line_to(*P[j]); c.stroke()
    for i, ((x, y), nm) in enumerate(zip(P, names)):
        a = prog(t, 0.4 + i * 0.25, 0.4); hot = off[i][1]
        c.new_path(); c.arc(x, y, 30 + 8 * hot, 0, 7); c.set_source_rgba(*(RED if i == si and t > t0 else GOLD), a); c.fill()
        c.new_path(); c.arc(x, y, 30 + 8 * hot, 0, 7); c.set_source_rgba(*INK, a); c.set_line_width(2); c.stroke()
        ty = y + 58 if y > cy else y - 42
        text(c, nm, x, ty, 22, INK, a, bold=True, align='c', halo=PARCH)
    if t > t0: explosion(c, *P[si], prog(t, t0, 1.2), 1, 50)
    if title: text(c, title.upper(), 640, 595, 30, RED, prog(t, t0 + 1.5, 0.6), face=TITLE, bold=True, align='c')


def lift(c, t, dur, args, b):
    """[custom: lift | ISSUE | floor 1 | floor 2 | floor 3 | measures=TEXT]  Securitisation lift: the issue rises a
    floor only as the audience bar fills; the top floor brings extraordinary measures."""
    issue = args[0] if args else 'ISSUE'
    floors = [a for a in args[1:] if '=' not in a] or ['Non-politicised', 'Politicised', 'Securitised']
    meas = next((a[9:] for a in args if a.startswith('measures=')), 'EXTRAORDINARY MEASURES')
    x0, x1, top, bot = 200, 660, 95, 575; fh = (bot - top) / 3
    c.new_path(); c.set_source_rgba(*INK, 1); c.set_line_width(4); c.rectangle(x0, top, x1 - x0, bot - top); c.stroke()
    for k in range(1, 3):
        y = top + k * fh; c.move_to(x0, y); c.line_to(x1, y)
    c.stroke()
    cols = (GREY, GOLD, RED)
    for k, fl in enumerate(floors[:3]):
        y = bot - k * fh - fh / 2
        text(c, f"{k + 1}  {fl.upper()}", x0 + 22, y + 8, 22, cols[k], 1, face=TITLE, bold=True)
    # audience: 12 people who turn green as they accept
    aud = clamp((t - dur * 0.15) / (dur * 0.6))
    for i in range(12):
        px = 770 + (i % 4) * 90; py = 270 + (i // 4) * 105
        agree = aud * 12 > i
        person(c, px, py, GREEN if agree else GREY, 1, 1.05)
    text(c, 'AUDIENCE', 905, 140, 26, INK, 1, face=TITLE, bold=True, align='c')
    c.new_path(); c.set_source_rgba(*INK, 0.2); c.rectangle(760, 560, 290, 18); c.fill()
    c.set_source_rgba(*GREEN, 1); c.rectangle(760, 560, 290 * aud, 18); c.fill()
    text(c, 'accepts the claim', 905, 600, 20, INK, 1, italic=True, align='c')
    level = lerp(0, 2, ease(clamp(aud * 1.15)))
    by = bot - level * fh - fh / 2 - 20
    c.new_path(); c.set_source_rgba(*cols[min(2, int(round(level)))], 1); c.rectangle(x1 - 150, by - 30, 130, 60); c.fill()
    text(c, issue.upper(), x1 - 85, by + 7, 18 if len(issue) > 9 else 22, (1, 1, 1), 1, bold=True, align='c')
    end = prog(t, dur * 0.8, 0.7)
    if end > 0: stamp(c, meas, 640, 360, end, RED, 40, -0.1, end)


def lenses(c, t, dur, args, b):
    """[custom: lenses | Lens ; what it sees | Lens ; ... | subject=TEXT]  One subject seen through lenses in turn."""
    subj = next((a[8:] for a in args if a.startswith('subject=')), 'THE CASE')
    L = [(x.split(';') + [''])[:2] for x in args if '=' not in x] or [['Realism', 'power'], ['Idealism', 'institutions'], ['Constructivism', 'ideas']]
    cols = (BLUE, GREEN, PURPLE, GOLD); n = len(L); seg = dur / n
    cx, cy = 640, 290
    c.new_path(); c.arc(cx, cy, 120, 0, 7); c.set_source_rgba(*PARCH, 1); c.fill_preserve(); c.set_source_rgba(*INK, 1); c.set_line_width(3); c.stroke()
    text(c, subj.upper(), cx, cy + 8, 26 if len(subj) < 14 else 20, INK, 1, face=TITLE, bold=True, align='c')
    k = min(n - 1, int(t / seg)); lt = t - k * seg
    slide = 1 - prog(lt, 0, 0.9); out = prog(lt, seg - 0.6, 0.6) if k < n - 1 else 0
    lx = cx - 700 * slide + 700 * out; col = cols[k % 4]
    c.new_path(); c.arc(lx, cy, 140, 0, 7); c.set_source_rgba(*col, 0.28); c.fill()
    c.new_path(); c.arc(lx, cy, 140, 0, 7); c.set_source_rgba(*col, 1); c.set_line_width(14); c.stroke()
    c.new_path(); c.move_to(lx + 99, cy + 99); c.line_to(lx + 190, cy + 190); c.set_line_width(22); c.set_line_cap(1); c.stroke(); c.set_line_cap(0)
    a = prog(lt, 0.7, 0.5) * (1 - out)
    text(c, L[k][0].strip().upper(), cx, 500, 40, col, a, face=TITLE, bold=True, align='c')
    text(c, L[k][1].strip(), cx, 548, 26, INK, a, italic=True, align='c')
    for i in range(n):  # progress dots
        c.new_path(); c.arc(cx - (n - 1) * 20 + i * 40, 590, 8, 0, 7); c.set_source_rgba(*cols[i % 4], 1 if i <= k else 0.25); c.fill()


def rings(c, t, dur, args, b):
    """[custom: rings | Inner ; note | Middle ; note | Outer ; note | focus=1,2]  Nested levels of analysis;
    rings appear inside-out, light up in turn, then 'focus=' keeps chosen rings lit."""
    L = [(x.split(';') + [''])[:2] for x in args if '=' not in x] or [['Individual', ''], ['State', ''], ['System', '']]
    focus = next(([int(v) for v in a[6:].split(',')] for a in args if a.startswith('focus=')), None)
    cols = (RED, GOLD, BLUE); cx, cy = 640, 335; R = (85, 165, 245)
    for k in (2, 1, 0):
        a = prog(t, 0.3 + (2 - k) * 0.5 if False else 0.3 + k * 0.6, 0.5)
        seq = dur / 3; lit = 1 if (seq * k <= t < seq * (k + 1)) else 0
        if focus: lit = (1 if (k + 1) in focus else 0) if t > 2.2 else lit
        c.new_path(); c.arc(cx, cy, R[k], 0, 7); c.set_source_rgba(*cols[k], a * (0.12 + 0.3 * lit)); c.fill()
        c.new_path(); c.arc(cx, cy, R[k], 0, 7); c.set_source_rgba(*cols[k], a); c.set_line_width(3 + 4 * lit); c.stroke()
    for k in range(3):
        a = prog(t, 0.3 + k * 0.6, 0.5); y = cy - R[k] + (26 if k else 0) + (0 if k else 8)
        name, note = L[k] if k < len(L) else ('', '')
        text(c, name.strip().upper(), cx, y + 4 if k else cy - 4, 24 if k else 22, cols[k], a, face=TITLE, bold=True, align='c', halo=PARCH)
        if note.strip(): text(c, note.strip(), cx, (y + 30) if k else cy + 24, 20, INK, a, italic=True, align='c', halo=PARCH)


REGISTRY = {'gears': gears, 'magnets': magnets, 'hub': hub, 'water': water, 'curve': curve, 'ladder': ladder, 'scales': scales,
            'spiral': spiral, 'web': web, 'lift': lift, 'lenses': lenses, 'rings': rings}
