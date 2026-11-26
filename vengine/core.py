"""Drawing primitives for the video engine (1280x720, 30 fps)."""
import cairo, math, random, textwrap
SW, SH, FPS = 1280, 720, 30
BLUE = (0.16, 0.36, 0.66); RED = (0.70, 0.18, 0.15); INK = (0.17, 0.13, 0.09)
GOLD = (0.72, 0.53, 0.04); PURPLE = (0.42, 0.25, 0.60); GREY = (0.45, 0.45, 0.45)
PARCH = (0.94, 0.89, 0.80)
SERIF = "Liberation Serif"; TITLE = "DejaVu Serif"

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def prog(t, a, d=1.0): return ease((t - a) / d) if d > 0 else (1.0 if t >= a else 0.0)
def lerp(a, b, p): return a + (b - a) * p

PLACES = {}

def vignette(c):
    g = cairo.RadialGradient(SW / 2, SH / 2, SH * 0.35, SW / 2, SH / 2, SW * 0.75)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.15, 0.1, 0.05, 0.45)
    c.set_source(g); c.paint()

def text(c, s, x, y, size, rgb=INK, a=1.0, face=SERIF, bold=False, italic=False, align='l', halo=None):
    c.select_font_face(face, cairo.FONT_SLANT_ITALIC if italic else cairo.FONT_SLANT_NORMAL,
                       cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size); e = c.text_extents(s)
    if align == 'c': x -= e.x_advance / 2
    elif align == 'r': x -= e.x_advance
    if halo is not None and a > 0:
        c.move_to(x, y); c.text_path(s); c.set_source_rgba(*halo, a * 0.85); c.set_line_width(size * 0.22); c.set_line_join(1); c.stroke()
    c.move_to(x, y); c.set_source_rgba(*rgb, a); c.show_text(s); c.new_path()
    return e.x_advance

def label(f, name, a, rgb=INK, dx=10, dy=-8, size=20, bold=True, txt=None, align='l'):
    if a <= 0: return
    x, y = f.P(name) if isinstance(name, str) else f.S(*name)
    text(f.c, txt or name, x + dx, y + dy, size, rgb, a, bold=bold, halo=(0.96, 0.93, 0.85), align=align)

def dot(f, name, a, rgb=INK, r=6, pulse=0.0, t=0):
    if a <= 0: return
    f.c.new_path()
    x, y = f.P(name) if isinstance(name, str) else f.S(*name); c = f.c
    if pulse:
        rr = r + 10 + 8 * math.sin(t * 4); c.arc(x, y, rr, 0, 7); c.set_source_rgba(*rgb, 0.18 * a * pulse); c.fill()
    c.arc(x, y, r, 0, 7); c.set_source_rgba(*rgb, a); c.fill_preserve(); c.set_source_rgba(1, 1, 1, a); c.set_line_width(1.6); c.stroke()

def halo(f, name, a, rgb, r=34):
    if a <= 0: return
    f.c.new_path()
    x, y = f.P(name) if isinstance(name, str) else f.S(*name)
    g = cairo.RadialGradient(x, y, 0, x, y, r); g.add_color_stop_rgba(0, *rgb, 0.45 * a); g.add_color_stop_rgba(1, *rgb, 0)
    f.c.set_source(g); f.c.arc(x, y, r, 0, 7); f.c.fill()

def path_pts(f, pts):
    return [f.P(p) if isinstance(p, str) else f.S(*p) for p in pts]

def along(pts, p):
    """point & angle at fraction p along polyline (screen pts)"""
    segs = [math.dist(a, b) for a, b in zip(pts, pts[1:])]; L = sum(segs) or 1; d = clamp(p) * L
    for (a, b), s in zip(zip(pts, pts[1:]), segs):
        if d <= s or s == segs[-1]:
            q = d / s if s else 0; q = clamp(q)
            return (lerp(a[0], b[0], q), lerp(a[1], b[1], q), math.atan2(b[1] - a[1], b[0] - a[0]))
        d -= s
    return (*pts[-1], 0)

def partial_line(c, pts, p, rgb, a=1.0, wdt=4, dash=None, arrow=False):
    if p <= 0 or a <= 0: return
    segs = [math.dist(x, y) for x, y in zip(pts, pts[1:])]; L = sum(segs); d = p * L
    c.save(); c.set_source_rgba(*rgb, a); c.set_line_width(wdt); c.set_line_cap(1); c.set_line_join(1)
    if dash: c.set_dash(dash)
    c.move_to(*pts[0]); last = pts[0]; ang = 0
    for (x0, x1), s in zip(zip(pts, pts[1:]), segs):
        if d >= s: c.line_to(*x1); last = x1; ang = math.atan2(x1[1] - x0[1], x1[0] - x0[0]); d -= s
        else:
            q = d / s if s else 0; last = (lerp(x0[0], x1[0], q), lerp(x0[1], x1[1], q)); ang = math.atan2(x1[1] - x0[1], x1[0] - x0[0]); c.line_to(*last); break
    c.stroke(); c.set_dash([])
    if arrow:
        hx, hy = last; sz = wdt * 3.2
        c.move_to(hx + math.cos(ang) * sz, hy + math.sin(ang) * sz)
        c.line_to(hx + math.cos(ang + 2.5) * sz, hy + math.sin(ang + 2.5) * sz)
        c.line_to(hx + math.cos(ang - 2.5) * sz, hy + math.sin(ang - 2.5) * sz); c.close_path(); c.fill()
    c.restore()

def ship(c, x, y, ang, rgb, a=1.0, sc=1.0, tilt=0.0):
    if a <= 0: return
    c.new_path(); c.save(); c.translate(x, y); c.rotate(ang + tilt); c.scale(sc, sc)
    # hull
    c.move_to(-14, -3); c.line_to(12, -3); c.line_to(18, 0); c.line_to(12, 4); c.line_to(-12, 4); c.close_path()
    c.set_source_rgba(*rgb, a); c.fill()
    # oars
    c.set_source_rgba(*rgb, a * 0.8); c.set_line_width(1)
    for i in range(-10, 11, 5):
        c.move_to(i, -3); c.line_to(i - 3, -8); c.move_to(i, 4); c.line_to(i - 3, 9)
    c.stroke()
    # sail
    c.move_to(-2, 0); c.line_to(-2, -12); c.line_to(6, -6); c.close_path(); c.set_source_rgba(1, 1, 1, a * 0.85); c.fill()
    c.restore()

def soldier(c, x, y, rgb, a=1.0, sc=1.0, shield=True, down=0.0):
    if a <= 0: return
    c.new_path(); c.save(); c.translate(x, y); c.scale(sc, sc)
    c.set_source_rgba(*rgb, a)
    c.arc(0, -22, 5, 0, 7); c.fill()                       # head
    c.move_to(-4, -27); c.line_to(0, -33); c.line_to(4, -27); c.fill()  # crest
    c.move_to(-6, -16); c.line_to(6, -16); c.line_to(5, 2); c.line_to(-5, 2); c.close_path(); c.fill()
    c.set_line_width(2.5); c.move_to(-3, 2); c.line_to(-4, 14); c.move_to(3, 2); c.line_to(4, 14); c.stroke()
    c.set_line_width(1.5); c.move_to(9, -30); c.line_to(9, 12); c.stroke()     # spear
    if shield:
        sx, sy = -6 + down * -4, -6 + down * 20
        c.arc(sx, sy, 8, 0, 7); c.set_source_rgba(*GOLD, a); c.fill_preserve(); c.set_source_rgba(*rgb, a); c.set_line_width(1.5); c.stroke()
    c.restore()

def person(c, x, y, rgb, a=1.0, sc=1.0):
    if a <= 0: return
    c.new_path(); c.save(); c.translate(x, y); c.scale(sc, sc); c.set_source_rgba(*rgb, a)
    c.arc(0, -40, 10, 0, 7); c.fill()
    c.move_to(-14, -27); c.curve_to(-20, 0, -18, 30, -16, 40); c.line_to(16, 40); c.curve_to(18, 30, 20, 0, 14, -27); c.close_path(); c.fill()
    c.restore()

def fire(c, x, y, t, a=1.0, n=7, seed=0, sc=1.0):
    if a <= 0: return
    c.new_path(); rnd = random.Random(seed)
    for i in range(n):
        ox = rnd.uniform(-8, 8) * sc; ph = rnd.uniform(0, 6)
        h = (14 + 6 * math.sin(t * 9 + ph)) * sc
        c.move_to(x + ox - 4 * sc, y); c.curve_to(x + ox - 5 * sc, y - h * 0.6, x + ox, y - h * 0.8, x + ox, y - h)
        c.curve_to(x + ox, y - h * 0.8, x + ox + 5 * sc, y - h * 0.6, x + ox + 4 * sc, y); c.close_path()
        c.set_source_rgba(0.95, 0.45 + 0.2 * math.sin(t * 7 + ph), 0.1, 0.75 * a); c.fill()
    c.arc(x, y - 22 * sc, 10 * sc, 0, 7); c.set_source_rgba(0.3, 0.3, 0.3, 0.15 * a); c.fill()

def panel(c, x, y, wd, ht, a=1.0, fill=PARCH, border=INK, r=10):
    if a <= 0: return
    c.new_path(); c.save()
    c.arc(x + wd - r, y + r, r, -math.pi / 2, 0); c.arc(x + wd - r, y + ht - r, r, 0, math.pi / 2)
    c.arc(x + r, y + ht - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2); c.close_path()
    c.set_source_rgba(0, 0, 0, 0.25 * a); c.save(); c.translate(4, 5); c.fill_preserve(); c.restore(); c.new_path()
    c.arc(x + wd - r, y + r, r, -math.pi / 2, 0); c.arc(x + wd - r, y + ht - r, r, 0, math.pi / 2)
    c.arc(x + r, y + ht - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2); c.close_path()
    c.set_source_rgba(*fill, a); c.fill_preserve(); c.set_source_rgba(*border, a); c.set_line_width(2.5); c.stroke(); c.restore()

def wrap_lines(c, s, size, maxw, face=SERIF, italic=False, bold=False):
    c.select_font_face(face, cairo.FONT_SLANT_ITALIC if italic else 0, cairo.FONT_WEIGHT_BOLD if bold else 0); c.set_font_size(size)
    words = s.split(); lines = []; cur = ''
    for wd in words:
        tryl = (cur + ' ' + wd).strip()
        if c.text_extents(tryl).x_advance > maxw and cur: lines.append(cur); cur = wd
        else: cur = tryl
    if cur: lines.append(cur)
    return lines

def quote_box(c, q, src, a, y=None, size=36, wd=980):
    if a <= 0: return
    lines = wrap_lines(c, q, size, wd - 90, italic=True)
    lh = size * 1.3; ht = len(lines) * lh + 90
    x = (SW - wd) / 2; y = y if y is not None else (SH - ht) / 2 - 40
    c.set_source_rgba(0, 0, 0, 0.35 * a); c.paint()
    panel(c, x, y, wd, ht, a)
    text(c, '“', x + 22, y + 70, 80, GOLD, a, face=TITLE)
    for i, l in enumerate(lines):
        text(c, l, SW / 2, y + 55 + i * lh, size, INK, a, italic=True, align='c')
    text(c, '— ' + src, x + wd - 40, y + ht - 22, 22, GOLD, a, bold=True, align='r')

def caption(c, s, a):
    if a <= 0 or not s: return
    lines = wrap_lines(c, s, 27, 1120)[:3]
    lh = 34; ht = len(lines) * lh + 22; y0 = SH - ht - 18
    c.set_source_rgba(0.08, 0.06, 0.04, 0.72 * a); c.rectangle(0, y0, SW, ht + 18); c.fill()
    for i, l in enumerate(lines):
        text(c, l, SW / 2, y0 + 33 + i * lh, 27, (0.98, 0.96, 0.90), a, align='c')

def act_card(c, num, title, sub, a):
    if a <= 0: return
    c.set_source_rgba(0.10, 0.07, 0.04, 0.55 * a); c.paint()
    text(c, num, SW / 2, SH / 2 - 60, 26, GOLD, a, face=TITLE, bold=True, align='c')
    text(c, title, SW / 2, SH / 2 + 5, 52, (0.98, 0.95, 0.88), a, face=TITLE, bold=True, align='c')
    c.set_source_rgba(*GOLD, a); c.set_line_width(2); c.move_to(SW / 2 - 200, SH / 2 + 30); c.line_to(SW / 2 + 200, SH / 2 + 30); c.stroke()
    text(c, sub, SW / 2, SH / 2 + 70, 28, (0.95, 0.90, 0.80), a, italic=True, align='c')

def year_badge(c, s, a):
    if a <= 0: return
    panel(c, SW - 210, 18, 190, 64, a, fill=(0.17, 0.13, 0.09), border=GOLD, r=8)
    text(c, s, SW - 115, 63, 36, (0.98, 0.93, 0.80), a, face=TITLE, bold=True, align='c')

def act_tag(c, s, a):
    if a <= 0: return
    text(c, s, 24, 44, 22, INK, a * 0.85, face=TITLE, bold=True, halo=(0.96, 0.93, 0.85))

def stamp(c, s, x, y, a, rgb=RED, size=60, rot=-0.12, p=1.0):
    if a <= 0: return
    sc = 1 + 1.5 * (1 - p)
    c.new_path(); c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc, sc)
    c.select_font_face(TITLE, 0, 1); c.set_font_size(size); e = c.text_extents(s)
    c.rectangle(-e.x_advance / 2 - 16, -size * 0.95, e.x_advance + 32, size * 1.25)
    c.set_source_rgba(*rgb, a * p); c.set_line_width(5); c.stroke()
    c.move_to(-e.x_advance / 2, 0); c.show_text(s); c.restore()

def counter_text(c, s, x, y, a, size=40, rgb=INK):
    text(c, s, x, y, size, rgb, a, face=TITLE, bold=True, align='c', halo=(0.96, 0.93, 0.85))

def parch_bg(c, dark=False):
    if dark:
        c.set_source_rgb(0.07, 0.05, 0.03); c.paint()
        g = cairo.RadialGradient(640, 330, 20, 640, 330, 650); g.add_color_stop_rgba(0, 0.45, 0.32, 0.16, 0.9); g.add_color_stop_rgba(1, 0.05, 0.03, 0.02, 0)
        c.set_source(g); c.paint()
    else:
        c.set_source_rgb(*PARCH); c.paint()
def radio(c, x, y, t, a, rgb=INK):
    if a <= 0: return
    for k in range(3):
        r = ((t * 30 + k * 20) % 60) + 8
        c.new_path(); c.arc(x, y, r, -0.9, 0.9); c.set_source_rgba(*rgb, a * (1 - r / 70)); c.set_line_width(3); c.stroke()
def tank(c, x, y, rgb, a=1.0, sc=1.0, inflate=1.0):
    if a <= 0: return
    c.new_path(); c.save(); c.translate(x, y); c.scale(sc, sc * inflate)
    c.set_source_rgba(*rgb, a); c.rectangle(-22, -8, 44, 14); c.fill(); c.rectangle(-10, -16, 20, 9); c.fill()
    c.set_line_width(3); c.move_to(8, -12); c.line_to(28, -14); c.stroke()
    c.set_source_rgba(0.2, 0.2, 0.2, a); [c.arc(-16 + i * 8, 7, 3.5, 0, 7) or c.fill() for i in range(5)]; c.restore()
def drone(c, x, y, ang, rgb, a=1.0, sc=1.0):
    if a <= 0: return
    c.new_path(); c.save(); c.translate(x, y); c.rotate(ang); c.scale(sc, sc); c.set_source_rgba(*rgb, a)
    c.move_to(12, 0); c.line_to(-8, -9); c.line_to(-4, 0); c.line_to(-8, 9); c.close_path(); c.fill(); c.restore()
def explosion(c, x, y, p, a=1.0, r=30):
    if a <= 0 or p <= 0 or p >= 1: return
    c.new_path(); c.arc(x, y, r * p, 0, 7); c.set_source_rgba(0.98, 0.6, 0.1, a * (1 - p)); c.fill()
    c.new_path(); c.arc(x, y, r * p * 0.55, 0, 7); c.set_source_rgba(1, 0.9, 0.5, a * (1 - p)); c.fill()
def bullet_list(c, items, t, starts, x=170, y0=170, dy=70, size=32, a=1.0, col=RED):
    for i, s in enumerate(items):
        p = prog(t, starts[i], 0.5) * a; y = y0 + i * dy
        c.new_path(); c.arc(x, y - 9, 16, 0, 7); c.set_source_rgba(*col, p); c.fill()
        text(c, str(i + 1), x, y, 22, (1, 1, 1), p, bold=True, align='c'); text(c, s, x + 35, y, size, INK, p)

def fade_io(c, t, dur, fi=0.5, fo=0.5):
    a = 1 - min(clamp(t / fi), clamp((dur - t) / fo))
    if a > 0: c.set_source_rgba(0, 0, 0, a); c.paint()

H = (0.96, 0.93, 0.85)   # text halo colour on maps
GREEN = (0.20, 0.50, 0.25)
COLORS = {'red': RED, 'blue': BLUE, 'gold': GOLD, 'ink': INK, 'black': INK, 'purple': PURPLE, 'grey': GREY, 'gray': GREY,
          'green': GREEN, 'brown': (0.45, 0.30, 0.15), 'orange': (0.85, 0.45, 0.10), 'olive': (0.40, 0.45, 0.30), 'white': (1, 1, 1)}
