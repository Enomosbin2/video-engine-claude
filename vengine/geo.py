"""World maps on demand: any region, any place name, cached as PNG."""
import json, math, os, hashlib, cairo
from .core import SW, SH, PARCH, ease, lerp

DATA = os.environ.get('VENGINE_DATA', os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data'))
CACHE = os.path.join(DATA, 'cache')
_land = _borders = _gaz = None
USER_PLACES = {}          # filled from PLACE: lines in the script


def _load(name):
    return json.load(open(os.path.join(DATA, name)))


def gazetteer():
    """name.lower() -> (lon, lat). Countries first, then cities (bigger city wins)."""
    global _gaz
    if _gaz is None:
        _gaz = {}; pop = {}
        for f in _load('cities.geojson')['features']:
            p = f['properties']; lon, lat = f['geometry']['coordinates'][:2]; n = p.get('pop_max') or p.get('POP_MAX') or 0
            for key in ('name', 'nameascii', 'NAME', 'NAMEASCII'):
                k = (p.get(key) or '').lower()
                if k and n >= pop.get(k, -1): _gaz[k] = (lon, lat); pop[k] = n
        for f in _load('countries.geojson')['features']:
            p = f['properties']; x, y = p.get('LABEL_X'), p.get('LABEL_Y')
            if x is None: continue
            for key in ('NAME', 'NAME_LONG', 'ADMIN', 'NAME_EN', 'ABBREV'):
                k = (p.get(key) or '').lower().strip('.')
                if k: _gaz[k] = (x, y)
    return _gaz


def where(name):
    """Place name, 'lon,lat' or a PLACE: definition -> (lon, lat) or None."""
    if isinstance(name, tuple): return name
    s = name.strip()
    if s in USER_PLACES: return USER_PLACES[s]
    if s.lower() in {k.lower(): 1 for k in USER_PLACES}:
        return next(v for k, v in USER_PLACES.items() if k.lower() == s.lower())
    try:
        a, b = [float(v) for v in s.split(',')]; return (a, b)
    except ValueError:
        pass
    return gazetteer().get(s.lower())


class GeoMap:
    """A parchment map of one lon/lat box, drawn once and cached."""
    def __init__(self, l0, l1, a0, a1):
        self.l0, self.l1, self.a0, self.a1 = l0, l1, a0, a1
        self.C = math.cos(math.radians((a0 + a1) / 2))
        self.K = min(260.0, 4600.0 / max((l1 - l0) * self.C, (a1 - a0)))      # px per degree of latitude
        self.W = int((l1 - l0) * self.C * self.K); self.H = int((a1 - a0) * self.K)
        os.makedirs(CACHE, exist_ok=True)
        key = hashlib.md5(f'{l0:.2f},{l1:.2f},{a0:.2f},{a1:.2f}'.encode()).hexdigest()[:10]
        fn = os.path.join(CACHE, f'map_{key}.png')
        if not os.path.exists(fn): self.build(fn)
        self.surf = cairo.ImageSurface.create_from_png(fn)

    def w(self, lon, lat): return ((lon - self.l0) * self.C * self.K, (self.a1 - lat) * self.K)

    def build(self, fn):
        global _land, _borders
        if _land is None: _land = _load('land.geojson'); _borders = _load('borders.geojson')
        s = cairo.ImageSurface(cairo.FORMAT_RGB24, self.W, self.H); c = cairo.Context(s)
        g = cairo.LinearGradient(0, 0, 0, self.H); g.add_color_stop_rgb(0, 0.80, 0.85, 0.83); g.add_color_stop_rgb(1, 0.74, 0.81, 0.80)
        c.set_source(g); c.paint()
        lw = max(1.2, self.K / 110)
        for f in _land['features']:
            geo = f['geometry']; PP = geo['coordinates'] if geo['type'] == 'MultiPolygon' else [geo['coordinates']]
            for poly in PP:
                ring = poly[0]; xs = [p[0] for p in ring]; ys = [p[1] for p in ring]
                if max(xs) < self.l0 - 1 or min(xs) > self.l1 + 1 or max(ys) < self.a0 - 1 or min(ys) > self.a1 + 1: continue
                for i, (lo, la) in enumerate(ring):
                    x, y = self.w(lo, la); (c.move_to if i == 0 else c.line_to)(x, y)
                c.close_path()
        c.set_source_rgba(0.62, 0.72, 0.72, 0.55); c.set_line_width(lw * 6); c.set_line_join(1); c.stroke_preserve()
        c.set_source_rgb(0.91, 0.86, 0.73); c.fill_preserve(); c.set_source_rgb(0.45, 0.38, 0.27); c.set_line_width(lw); c.stroke()
        c.set_source_rgba(0.45, 0.38, 0.27, 0.55); c.set_line_width(lw * 0.8); c.set_dash([lw * 3, lw * 2])
        for f in _borders['features']:
            geo = f['geometry']; LL = geo['coordinates'] if geo['type'] == 'MultiLineString' else [geo['coordinates']]
            for line in LL:
                xs = [p[0] for p in line]; ys = [p[1] for p in line]
                if max(xs) < self.l0 or min(xs) > self.l1 or max(ys) < self.a0 or min(ys) > self.a1: continue
                for i, (lo, la) in enumerate(line):
                    x, y = self.w(lo, la); (c.move_to if i == 0 else c.line_to)(x, y)
                c.stroke()
        s.write_to_png(fn)


def fit(points, pad=0.35, min_span=3.0):
    """Camera (lon, lat, span_lon) that shows every point with room for labels and the caption bar."""
    lons = [p[0] for p in points]; lats = [p[1] for p in points]
    lo0, lo1, la0, la1 = min(lons), max(lons), min(lats), max(lats)
    C = math.cos(math.radians((la0 + la1) / 2))
    w = max(lo1 - lo0, 0.01); h = max(la1 - la0, 0.01)
    usable_h = (SH - 200) / SW            # keep clear of the top tag and bottom caption
    span = max(w * (1 + 2 * pad), h * (1 + 2 * pad) / (usable_h * C), min_span)
    # shift centre a little down-screen so places sit above the caption bar
    return ((lo0 + lo1) / 2, (la0 + la1) / 2 - 18 * span * C / SW, span)


def map_for(cams):
    """One GeoMap covering every camera position in a board (with margin)."""
    l0 = a0 = 1e9; l1 = a1 = -1e9
    for lon, lat, span in cams:
        C = math.cos(math.radians(lat)); hw = span * 0.75; hh = span * C * (SH / SW) * 0.75 + 0.5
        l0, l1, a0, a1 = min(l0, lon - hw), max(l1, lon + hw), min(a0, lat - hh), max(a1, lat + hh)
    return GeoMap(max(-180, l0), min(180, l1), max(-85, a0), min(85, a1))


class GeoCam:
    """keys: list of (time, lon, lat, span)."""
    def __init__(self, gm, keys): self.g = gm; self.keys = keys

    def at(self, t):
        k = self.keys; c = k[0]
        if t >= k[-1][0]: c = k[-1]
        else:
            for a, b in zip(k, k[1:]):
                if a[0] <= t <= b[0]:
                    p = ease((t - a[0]) / max(1e-6, b[0] - a[0]))
                    c = (t, lerp(a[1], b[1], p), lerp(a[2], b[2], p), math.exp(lerp(math.log(a[3]), math.log(b[3]), p))); break
        _, lon, lat, span = c; cx, cy = self.g.w(lon, lat)
        return cx, cy, SW / (span * self.g.C * self.g.K)


class GeoFrame:
    def __init__(self, ctx, gm, cam):
        self.c = ctx; self.g = gm; self.cx, self.cy, self.s = cam

    def S(self, lon, lat):
        x, y = self.g.w(lon, lat); return ((x - self.cx) * self.s + SW / 2, (y - self.cy) * self.s + SH / 2)

    def P(self, name):
        p = where(name)
        return self.S(*p) if p else (-999, -999)

    def draw(self, alpha=1.0):
        c = self.c; c.save(); c.set_source_rgb(*PARCH); c.paint()
        c.translate(SW / 2, SH / 2); c.scale(self.s, self.s); c.translate(-self.cx, -self.cy)
        c.set_source_surface(self.g.surf, 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(alpha); c.restore()
