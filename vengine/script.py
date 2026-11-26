"""Reads a video script (see GUIDE.md) into a plain data structure."""
import re
from . import geo

TAG = re.compile(r"\[([a-zA-Z_]+)\s*(?::\s*(.*?))?\]\s*")
HEADER_KEYS = ('TITLE', 'VOICE', 'SPEED', 'LANG', 'PLACE', 'SAY', 'TEMPLATE', 'THEME', 'LENGTH', 'MARKING', 'FOOTER')


def parse_tag(name, body):
    args = [a.strip() for a in (body or '').split('|')] if body else []
    return {'name': name.lower(), 'args': [a for a in args if a != '']}


def parse(text):
    meta = {'TITLE': '', 'VOICE': 'bm_george', 'SPEED': '0.95', 'LANG': 'en-gb', 'MARKING': '', 'FOOTER': ''}
    say = {}; scenes = []; pending = []
    cur = None

    def scene(kicker, title):
        s = {'kicker': kicker, 'title': title, 'cues': []}; scenes.append(s); return s

    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith('//'): continue
        m = re.match(r"^([A-Z]+):\s*(.*)$", line)
        if m and m.group(1) in HEADER_KEYS and cur is None or (m and m.group(1) in ('PLACE', 'SAY')):
            k, v = m.group(1), m.group(2).strip()
            if k == 'PLACE':
                n, xy = v.split('=', 1); lon, lat = [float(x) for x in xy.split(',')]; geo.USER_PLACES[n.strip()] = (lon, lat)
            elif k == 'SAY':
                a, b = v.split('=', 1); say[a.strip()] = b.strip()
            else: meta[k] = v
            continue
        if line.startswith('##') or line.upper().startswith('SCENE:'):
            h = re.sub(r"^(##+|SCENE:)\s*", '', line, flags=re.I)
            parts = [p.strip() for p in h.split('|')]
            cur = scene(parts[0] if len(parts) > 1 else '', parts[-1])
            continue
        if cur is None: cur = scene('', '')
        tags = []
        while True:
            m = TAG.match(line)
            if not m: break
            tags.append(parse_tag(m.group(1), m.group(2))); line = line[m.end():].strip()
        if tags and not line:
            pending += tags; continue
        tags = pending + tags; pending = []
        silent = any(t['name'] == 'pause' for t in tags)
        cur['cues'].append({'text': '' if silent else line, 'tags': tags,
                            'pause': float(next((t['args'][0] for t in tags if t['name'] == 'pause' and t['args']), 2)) if silent else 0})
        if silent and line: cur['cues'].append({'text': line, 'tags': [], 'pause': 0})
    if pending and cur is not None:
        cur['cues'].append({'text': '', 'tags': pending, 'pause': 2.0})
    scenes = [s for s in scenes if s['cues']]
    return meta, say, scenes


def check_places(scenes):
    """Names the gazetteer cannot find (so they can be added with PLACE: lines)."""
    from .scenes import place_args
    missing = set()
    for s in scenes:
        for c in s['cues']:
            for t in c['tags']:
                for n in place_args(t):
                    if geo.where(n) is None: missing.add(n)
    return sorted(missing)
