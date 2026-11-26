"""Turns parsed cues + narration timing into drawable 'boards' with overlays, and draws any frame."""
import math, os, random, cairo
from .core import *
from . import geo, customs

BOARDS = {'map', 'quote', 'bullets', 'title', 'timeline', 'compare', 'image', 'custom', 'text', 'blank', 'dark'}
MAP_OVERLAYS = {'arrow', 'move', 'boom', 'area', 'label', 'pulse', 'zoom', 'place'}
XFADE = 0.6
SCRIPT_DIR = '.'


# ---------- small parsing helpers ----------
def opts(args):
    """Split args into (plain values, colour, flags, key=value dict)."""
    plain, col, flags, kv = [], None, set(), {}
    for a in args:
        low = a.lower()
        if low in COLORS: col = COLORS[low]
        elif '=' in a and a.split('=')[0].strip().isalpha() and len(a.split('=')[0].strip()) < 8 and not a.strip().startswith('#'):
            k, v = a.split('=', 1); kv[k.strip().lower()] = v.strip()
        elif low in ('dashed', 'thick', 'thin', 'step', 'arrow', 'left', 'right', 'top', 'bottom', 'middle', 'big', 'loop', 'dark', 'fade'): flags.add(low)
        else: plain.append(a)
    return plain, col, flags, kv


def route(s): return [p.strip() for p in s.split('>') if p.strip()]


def place_args(tag):
    n, a = tag['name'], tag['args']
    plain = opts(a)[0]
    if n in ('map', 'zoom', 'place', 'pulse'): return _map_list(tag)
    if n == 'arrow' and plain: return route(plain[0])
    if n == 'move' and len(plain) > 1: return route(plain[1])
    if n in ('boom', 'area') and plain: return [p.strip() for p in plain[0].split(',')]
    if n == 'label' and plain and '@' in plain[0]: return [plain[0].split('@', 1)[1].strip()]
    return []


def _isnum(s):
    try: float(s); return True
    except ValueError: return False


def _map_list(tag):
    plain = opts(tag['args'])[0]
    out = []
    for x in plain:
        if ',' in x and all(_isnum(v) for v in x.split(',')): out.append(x)
        else: out += [p.strip() for p in x.split(',') if p.strip()]
    return out


# ---------- plan ----------
def plan(scene, dur, cues, index, meta):
    """Group cues into boards. Each board: kind, args, t0, t1, overlays, cam."""
    boards = []; cur = None
    for i, (cue, tm) in enumerate(zip(scene['cues'], cues)):
        t0 = 0.0 if i == 0 else tm['start'] - 0.2
        for tag in cue['tags']:
            if tag['name'] in BOARDS:
                if cur is not None and abs(cur['t0'] - t0) < 0.01 and not cur['ov']:
                    boards.pop()
                cur = {'kind': tag['name'], 'args': tag['args'], 't0': t0, 'ov': [], 'cues': []}; boards.append(cur)
        if cur is None:
            first = index == 0 and meta.get('TITLE')
            cur = {'kind': 'title' if first else 'blank', 'args': ['', meta['TITLE'], ''] if first else [], 't0': 0.0, 'ov': [], 'cues': []}
            boards.append(cur)
        cur['cues'].append((tm['start'], tm['end']))
        for tag in cue['tags']:
            if tag['name'] not in BOARDS and tag['name'] != 'pause':
                cur['ov'].append({**tag, 't0': tm['start'], 't1': max(tm['end'], tm['start'] + 2.0)})
    for b, nb in zip(boards, boards[1:] + [None]):
        b['t1'] = nb['t0'] + XFADE if nb else dur
        if b['kind'] == 'map': _plan_map(b)
    return boards


def _plan_map(b):
    tag = {'name': 'map', 'args': b['args']}; plain, col, flags, kv = opts(b['args'])
    names = _map_list(tag)
    pts = [geo.where(n) for n in names]; pts = [p for p in pts if p]
    if not pts:
        for o in b['ov']: pts += [geo.where(n) for n in place_args(o) if o['name'] != 'zoom' and geo.where(n)]
    if not pts: pts = [(0, 20)]; kv.setdefault('span', '120')
    lon, lat, span = geo.fit(pts, pad=float(kv.get('pad', 0.35)), min_span=float(kv.get('min', 3)))
    if 'center' in kv: lon, lat = [float(v) for v in kv['center'].split(',')]
    if 'span' in kv: span = float(kv['span'])
    keys = [(b['t0'], lon, lat, span * 1.06), (b['t0'] + 4.0, lon, lat, span)]
    for o in b['ov']:
        if o['name'] != 'zoom': continue
        zp, _, _, zkv = opts(o['args'])
        zpts = [geo.where(n) for n in place_args(o)]; zpts = [p for p in zpts if p]
        if not zpts: continue
        zl, za, zs = geo.fit(zpts, pad=float(zkv.get('pad', 0.4)), min_span=float(zkv.get('min', 2.5)))
        if 'span' in zkv: zs = float(zkv['span'])
        keys += [(o['t0'], *keys[-1][1:]), (o['t0'] + float(zkv.get('time', 2.5)), zl, za, zs)]
    keys.sort(key=lambda k: k[0])
    b['places'] = [n for n in names if geo.where(n)]
    b['gm'] = geo.map_for([k[1:] for k in keys]); b['cam'] = geo.GeoCam(b['gm'], keys)


# ---------- drawing ----------
def _a(t, o, d=0.5):
    return prog(t, o['t0'], d)


def draw_board(c, b, t, ctx):
    k = b['kind']; f = None
    if k == 'map':
        f = geo.GeoFrame(c, b['gm'], b['cam'].at(t)); f.draw()
        for i, n in enumerate(b['places']):
            a = prog(t, b['t0'] + 0.4 + 0.25 * i, 0.4); dot(f, n, a, INK, 6); label(f, n, a, INK, size=22)
    elif k == 'dark': parch_bg(c, dark=True)
    else: parch_bg(c)
    BOARD_FN.get(k, lambda *x: None)(c, b, t, ctx)
    for o in b['ov']:
        if t < o['t0'] - 0.05: continue
        fn = OVERLAY_FN.get(o['name'])
        if fn is None: continue
        if o['name'] in MAP_OVERLAYS and f is None: continue
        fn(c, f, o, t, b)


def b_title(c, b, t, ctx):
    p = b['args'] + ['', '', '']; a = prog(t, b['t0'] + 0.2, 0.6)
    parch_bg(c, dark=True); c.set_source_rgba(0, 0, 0, 0)
    if p[0]: text(c, p[0].upper(), SW / 2, SH / 2 - 70, 26, GOLD, a, face=TITLE, bold=True, align='c')
    for i, l in enumerate(wrap_lines(c, p[1], 56, 1100, face=TITLE, bold=True)[:2]):
        text(c, l, SW / 2, SH / 2 + i * 66, 56, (0.97, 0.88, 0.62), a, face=TITLE, bold=True, align='c')
    c.set_source_rgba(*GOLD, a); c.set_line_width(2); c.move_to(SW / 2 - 220, SH / 2 + 40); c.line_to(SW / 2 + 220, SH / 2 + 40); c.stroke()
    if p[2]: text(c, p[2], SW / 2, SH / 2 + 95, 30, (0.92, 0.84, 0.68), prog(t, b['t0'] + 1.0, 0.6), italic=True, align='c')


def b_quote(c, b, t, ctx):
    q = b['args'][0] if b['args'] else ''; src = b['args'][1] if len(b['args']) > 1 else ''
    n = len(q); size = 46 if n < 60 else 40 if n < 110 else 34 if n < 170 else 30
    quote_box(c, q, src, prog(t, b['t0'] + 0.1, 0.5), size=size)


def _reveal_times(b, n):
    plain, col, flags, kv = opts(b['args'])
    if 'step' in flags:
        cs = b['cues']; off = max(0, len(cs) - n); return [cs[min(i + off, len(cs) - 1)][0] for i in range(n)]
    s0, e0 = b['cues'][0] if b['cues'] else (b['t0'], b['t0'] + 3)
    gap = max(0.6, (e0 - s0) / max(1, n)); return [s0 + 0.2 + i * gap for i in range(n)]


def b_bullets(c, b, t, ctx):
    plain, col, flags, kv = opts(b['args'])
    head = plain[0][1:].strip() if plain and plain[0].startswith('#') else ''
    items = plain[1:] if head else plain
    y0 = 200 if head else 150; dy = min(78, 430 / max(1, len(items))); size = 34 if dy >= 70 else 28
    if head: text(c, head.upper(), SW / 2, 115, 44, INK, prog(t, b['t0'], 0.5), face=TITLE, bold=True, align='c')
    ts = _reveal_times(b, len(items))
    for i, s in enumerate(items):
        p = prog(t, ts[i], 0.5); y = y0 + i * dy
        c.new_path(); c.arc(150, y - 10, 17, 0, 7); c.set_source_rgba(*(col or RED), p); c.fill()
        text(c, str(i + 1), 150, y - 1, 21, (1, 1, 1), p, bold=True, align='c')
        for j, l in enumerate(wrap_lines(c, s, size, 1000)[:2]):
            text(c, l, 190 + (1 - p) * 30, y + j * size * 1.1, size, INK, p)


def b_timeline(c, b, t, ctx):
    plain, col, flags, kv = opts(b['args'])
    items = [(x.split('=', 1) + [''])[:2] for x in plain]; n = len(items); ts = _reveal_times(b, n)
    x0, x1, y = 120, SW - 120, 330
    c.new_path(); c.set_source_rgba(*INK, prog(t, b['t0'], 0.6)); c.set_line_width(4); c.move_to(x0, y); c.line_to(lerp(x0, x1, prog(t, b['t0'], 1.5)), y); c.stroke()
    for i, (d, s) in enumerate(items):
        x = x0 + (x1 - x0) * (i + 0.5) / n; p = prog(t, ts[i], 0.5); up = i % 2 == 0
        c.new_path(); c.arc(x, y, 12, 0, 7); c.set_source_rgba(*(col or RED), p); c.fill()
        text(c, d.strip(), x, y + (-30 if up else 55), 32, col or RED, p, face=TITLE, bold=True, align='c')
        for j, l in enumerate(wrap_lines(c, s.strip(), 22, 1000 / n + 60)[:3]):
            text(c, l, x, y + (-70 - 26 * (2 - j) if up else 95 + 26 * j), 22, INK, p, align='c')


def b_compare(c, b, t, ctx):
    plain, col, flags, kv = opts(b['args']); sides = plain[:2] + [''] * (2 - len(plain[:2]))
    cols = [BLUE, RED]
    for i, s in enumerate(sides):
        parts = [x.strip() for x in s.split(';')]; x = 120 + i * 560; a = prog(t, b['t0'] + 0.3 + i * 0.8, 0.5)
        panel(c, x, 140, 480, 400, a, fill=(0.98, 0.95, 0.88), border=cols[i])
        text(c, parts[0].upper(), x + 240, 205, 40, cols[i], a, face=TITLE, bold=True, align='c')
        yy = 270
        for line in parts[1:]:
            for l in wrap_lines(c, line, 26, 420)[:3]: text(c, l, x + 240, yy, 26, INK, a, align='c'); yy += 34
            yy += 14
    if 'arrow' in flags: partial_line(c, [(610, 340), (670, 340)], prog(t, b['t0'] + 1.5, 0.5), INK, 1, 6, arrow=True)


_img = {}
def b_image(c, b, t, ctx):
    fn = os.path.join(SCRIPT_DIR, b['args'][0]) if b['args'] else ''
    if fn not in _img:
        try: _img[fn] = cairo.ImageSurface.create_from_png(fn) if fn.lower().endswith('.png') else _load_any(fn)
        except Exception: _img[fn] = None
    im = _img[fn]
    if im is None: text(c, f"[missing image: {fn}]", SW / 2, SH / 2, 30, RED, 1, align='c'); return
    w, h = im.get_width(), im.get_height(); p = clamp((t - b['t0']) / max(1, b['t1'] - b['t0']))
    s = max(SW / w, SH / h) * (1.0 + 0.08 * p)
    c.save(); c.translate(SW / 2, SH / 2); c.scale(s, s); c.translate(-w / 2, -h / 2 - 10 * p / s)
    c.set_source_surface(im, 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint(); c.restore()


def _load_any(fn):
    from PIL import Image; import io
    im = Image.open(fn).convert('RGB'); buf = io.BytesIO(); im.save(buf, 'PNG'); buf.seek(0)
    return cairo.ImageSurface.create_from_png(buf)


def b_text(c, b, t, ctx):
    plain, col, flags, kv = opts(b['args']); a = prog(t, b['t0'] + 0.2, 0.5)
    big = plain[0] if plain else ''
    lines = wrap_lines(c, big, 52, 1100, face=TITLE, bold=True)[:3]
    y0 = SH / 2 - 40 - (len(lines) - 1) * 32
    for i, l in enumerate(lines): text(c, l, SW / 2, y0 + i * 64, 52, col or INK, a, face=TITLE, bold=True, align='c')
    for i, s in enumerate(plain[1:3]):
        text(c, s, SW / 2, y0 + len(lines) * 64 + 20 + i * 44, 30, INK, prog(t, b['t0'] + 1 + i * 0.6, 0.5), italic=True, align='c')


def b_custom(c, b, t, ctx):
    name = b['args'][0].lower() if b['args'] else ''
    fn = customs.REGISTRY.get(name)
    if fn is None: text(c, f"[unknown custom: {name}]", SW / 2, SH / 2, 30, RED, 1, align='c'); return
    fn(c, t - b['t0'], b['t1'] - b['t0'], b['args'][1:], b)


BOARD_FN = {'title': b_title, 'quote': b_quote, 'bullets': b_bullets, 'timeline': b_timeline, 'compare': b_compare,
            'image': b_image, 'text': b_text, 'custom': b_custom}


# ---------- overlays ----------
def o_place(c, f, o, t, b):
    for i, n in enumerate(place_args(o)):
        a = prog(t, o['t0'] + 0.3 * i, 0.4); col = opts(o['args'])[1] or INK
        dot(f, n, a, col, 7); label(f, n, a, col, size=22)


def o_pulse(c, f, o, t, b):
    col = opts(o['args'])[1] or RED
    for n in place_args(o):
        a = _a(t, o); dot(f, n, a, col, 9, 1.0, t); label(f, n, a, col, size=24)


def o_arrow(c, f, o, t, b):
    plain, col, flags, kv = opts(o['args'])
    if not plain: return
    pts = [f.P(n) for n in route(plain[0])]
    if any(p[0] < -900 for p in pts): return
    dur = float(kv.get('time', min(3.0, o['t1'] - o['t0'])))
    w = 9 if 'thick' in flags else 3 if 'thin' in flags else 6
    partial_line(c, pts, prog(t, o['t0'] + 0.2, dur), col or BLUE, 1, w, dash=[12, 8] if 'dashed' in flags else None, arrow=True)
    if 'text' in kv:
        x, y, _ = along(pts, 0.5); text(c, kv['text'], x, y - 18, 22, col or BLUE, prog(t, o['t0'] + 1, 0.5), bold=True, align='c', halo=H)


UNIT = {'tank': tank, 'tanks': tank, 'ship': None, 'ships': None, 'soldier': soldier, 'soldiers': soldier, 'troops': soldier,
        'drone': drone, 'drones': drone, 'missile': drone, 'missiles': drone, 'plane': drone, 'planes': drone}


def o_move(c, f, o, t, b):
    plain, col, flags, kv = opts(o['args'])
    if len(plain) < 2: return
    kind = plain[0].lower(); pts = [f.P(n) for n in route(plain[1])]
    if any(p[0] < -900 for p in pts): return
    n = int(kv.get('n', 5 if kind.endswith('s') else 1)); col = col or RED
    dur = float(kv.get('time', max(2.0, o['t1'] - o['t0'])))
    p = prog(t, o['t0'] + 0.2, dur)
    if 'loop' in flags: p = ((t - o['t0']) / dur) % 1
    if 'trail' in kv or 'dashed' in flags: partial_line(c, pts, p, col, 0.7, 3, dash=[8, 6])
    for i in range(n):
        q = clamp(p - i * 0.035) if p < 1 else 1 - i * 0.035
        x, y, ang = along(pts, max(0, q))
        off = (i % 2) * 10 - 5
        if kind.startswith('ship'): ship(c, x + off, y + off, ang, col, 1, 1.4)
        elif kind.startswith(('tank',)): tank(c, x - i * 6 * (p >= 1), y + off, col, 1, 0.7)
        elif kind.startswith(('soldier', 'troop')): soldier(c, x - i * 8 * (p >= 1), y + off, col, 1, 0.8)
        else: drone(c, x, y + off, ang, col, 1, 1.2)


def o_boom(c, f, o, t, b):
    plain, col, flags, kv = opts(o['args']); n = int(kv.get('n', 3)); rnd = random.Random(len(o['args']) + int(o['t0']))
    for name in place_args(o):
        x, y = f.P(name)
        for k in range(n):
            ph = ((t - o['t0']) * 0.8 + k / n) % 1
            if t - o['t0'] < float(kv.get('time', 1e9)): explosion(c, x + rnd.uniform(-40, 40), y + rnd.uniform(-30, 30), ph, 1, 30)


def o_area(c, f, o, t, b):
    plain, col, flags, kv = opts(o['args']); col = col or RED; r = float(kv.get('r', 70)); a = _a(t, o, 0.8)
    for name in place_args(o):
        x, y = f.P(name); c.new_path(); c.arc(x, y, r, 0, 7); c.set_source_rgba(*col, 0.22 * a); c.fill_preserve()
        c.set_source_rgba(*col, 0.6 * a); c.set_line_width(2); c.set_dash([6, 5]); c.stroke(); c.set_dash([])
    if 'text' in kv:
        x, y = f.P(place_args(o)[0]); text(c, kv['text'], x, y - r - 12, 24, col, a, bold=True, align='c', halo=H)


def o_label(c, f, o, t, b):
    plain, col, flags, kv = opts(o['args'])
    if not plain: return
    s, _, at = plain[0].partition('@'); a = _a(t, o)
    if at.strip(): x, y = f.P(at.strip()); y += float(kv.get('dy', 40)); x += float(kv.get('dx', 0))
    else: x, y = SW / 2, 140
    text(c, s.strip(), x, y, int(kv.get('size', 24)), col or INK, a, bold=True, italic='italic' in kv, align='c', halo=H)


def o_stamp(c, f, o, t, b):
    plain, col, flags, kv = opts(o['args'])
    if not plain: return
    y = 330 if 'middle' in flags else 520 if 'bottom' in flags else 190
    x = 380 if 'left' in flags else 900 if 'right' in flags else SW / 2
    s = plain[0].upper(); size = 46 if len(s) < 18 else 36 if len(s) < 28 else 28
    p = prog(t, o['t0'] + float(kv.get('delay', 0.6)), 0.35); stamp(c, s, x, y, p, col or RED, size, p=p)


def o_year(c, f, o, t, b):
    later = [x for x in b['ov'] if x['name'] == 'year' and o['t0'] < x['t0'] <= t]
    if later or not o['args']: return
    year_badge(c, o['args'][0], _a(t, o, 0.4))


def o_counter(c, f, o, t, b):
    plain, col, flags, kv = opts(o['args'])
    if not plain: return
    rng = plain[0].replace('→', '-').replace('->', '-'); lab = plain[1] if len(plain) > 1 else ''
    try:
        a0, a1 = [float(x.replace(',', '')) for x in rng.split('-', 1)]
    except ValueError:
        return
    p = prog(t, o['t0'] + 0.3, float(kv.get('time', max(1.5, o['t1'] - o['t0'] - 0.5))))
    v = lerp(a0, a1, p); s = f"{int(round(v)):,}"; a = _a(t, o, 0.4)
    y = 110 if not any(x['name'] == 'year' for x in b['ov']) else 110 + 80
    panel(c, SW - 330, y - 20, 300, 110, a, fill=(0.98, 0.95, 0.88))
    text(c, s, SW - 180, y + 45, 48, col or INK, a, face=TITLE, bold=True, align='c')
    text(c, lab, SW - 180, y + 78, 20, INK, a, italic=True, align='c')


def o_note(c, f, o, t, b):
    plain, col, flags, kv = opts(o['args']); a = _a(t, o)
    lines = [l for p in plain for l in wrap_lines(c, p, 24, 400)][:5]
    if not lines: return
    x = 60 if 'left' in flags else SW - 500; y = 90
    panel(c, x, y, 440, 30 + 34 * len(lines), a, fill=(0.98, 0.95, 0.88))
    for i, l in enumerate(lines): text(c, l, x + 220, y + 40 + 34 * i, 24, col or INK, a, bold=i == 0, align='c')


OVERLAY_FN = {'place': o_place, 'pulse': o_pulse, 'arrow': o_arrow, 'move': o_move, 'boom': o_boom, 'area': o_area,
              'label': o_label, 'stamp': o_stamp, 'year': o_year, 'counter': o_counter, 'note': o_note, 'zoom': lambda *a: None}


def draw(c, scene, boards, cues, t, dur, meta):
    prev = None
    active = [b for b in boards if b['t0'] <= t < b['t1']] or boards[-1:]
    if len(active) > 1:
        draw_board(c, active[0], t, None)
        c.push_group(); draw_board(c, active[-1], t, None); c.pop_group_to_source()
        c.paint_with_alpha(prog(t, active[-1]['t0'], XFADE))
    else: draw_board(c, active[0], t, None)
    if scene['title'] and active[-1]['kind'] != 'title':
        tag = (scene['kicker'] + '  ·  ' if scene['kicker'] else '') + scene['title'].upper()
        dark = any(b['kind'] in ('dark', 'title') for b in active)
        text(c, tag, 24, 44, 22, (0.95, 0.9, 0.8) if dark else INK, 0.85 * prog(t, 3.6 if scene['kicker'] else 0.3, 0.6), face=TITLE, bold=True,
             halo=None if dark else H)
    if scene['kicker']:
        act_card(c, scene['kicker'], scene['title'], '', prog(t, 0, 0.5) * (1 - prog(t, 3.0, 0.6)))
    vignette(c)
    cur = None
    for cu in cues:
        if cu['text'] and cu['start'] - 0.1 <= t <= cu['end'] + 0.35: cur = cu
    if cur: caption(c, cur['text'], min(prog(t, cur['start'] - 0.1, 0.2), 1 - prog(t, cur['end'] + 0.15, 0.2)))
    m = meta.get('MARKING', '').strip()
    if m and m.upper() != 'NONE':
        for y in (22, SH - 6):
            text(c, m.upper(), SW / 2, y if y > 30 else 22, 18, RED, 0.9, face=TITLE, bold=True, align='c', halo=H)
    fade_io(c, t, dur, 0.5, 0.5)
