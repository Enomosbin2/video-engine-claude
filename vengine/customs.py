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


REGISTRY = {'gears': gears, 'magnets': magnets, 'hub': hub, 'water': water, 'curve': curve, 'ladder': ladder, 'scales': scales}
