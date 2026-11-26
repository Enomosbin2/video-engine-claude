"""Offline narration with Kokoro, one sentence-group (cue) at a time, so animation can be timed to it."""
import os, re, json, hashlib
import numpy as np, soundfile as sf
from .geo import DATA

SR = 24000
LEAD, GAP, TAIL = 0.8, 0.4, 1.0
_k = None

ONES = "zero one two three four five six seven eight nine".split()
TEENS = "ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def _two(n):
    if n < 10: return "oh " + ONES[n]
    if n < 20: return TEENS[n - 10]
    return TENS[n // 10] + ("" if n % 10 == 0 else "-" + ONES[n % 10])


def _under100(n):
    if n < 10: return ONES[n]
    if n < 20: return TEENS[n - 10]
    return TENS[n // 10] + ("" if n % 10 == 0 else "-" + ONES[n % 10])


def _year(y):
    if 2000 <= y < 2010: return "two thousand" + ("" if y == 2000 else " and " + ONES[y - 2000])
    if y >= 2010: return "twenty " + _two(y - 2000)
    return _two(y // 100) + " " + (_two(y % 100) if y % 100 else "hundred")


def _decade(m):
    w = _year(int(m.group(1)))
    return w[:-1] + 'ies' if w.endswith('y') else w + 's'


def _bc(m):
    n = int(m.group(1)); era = 'BC' if m.group(2).upper() in ('BC', 'BCE') else 'AD'
    if n < 100: w = _under100(n)
    elif n % 100 == 0: w = ONES[n // 100] + " hundred" if n < 1000 else _year(n)
    elif n < 1000: w = ONES[n // 100] + " " + _two(n % 100)
    else: w = _year(n)
    return f"{w} {'B.C.' if era == 'BC' else 'A.D.'}"


def spoken(s, say=None):
    """What the narrator reads. Screen text keeps figures; the voice gets natural English."""
    for a, b in (say or {}).items(): s = s.replace(a, b)
    s = re.sub(r"\b(\d{1,4}) ?(BCE|BC|AD|CE)\b", _bc, s)
    s = re.sub(r"\b(1[1-9]\d0|20\d0)s\b", _decade, s)
    s = re.sub(r"(?<![\d,.])\b(1[1-9]\d\d|20\d\d)\b(?![,.]\d)", lambda m: _year(int(m.group(1))), s)
    s = re.sub(r"(\d),(\d{3})\b", r"\1\2", s)            # 8,000 -> 8000 (Kokoro reads plain numbers well)
    s = s.replace('%', ' per cent').replace('&', ' and ').replace('"', '').replace('“', '').replace('”', '')
    return s


def kokoro():
    global _k
    if _k is None:
        from kokoro_onnx import Kokoro
        _k = Kokoro(os.path.join(DATA, 'kokoro-v1.0.onnx'), os.path.join(DATA, 'voices-v1.0.bin'))
    return _k


def narrate(scene_cues, out_wav, voice='bm_george', speed=0.95, lang='en-gb', say=None):
    """scene_cues: list of (text, pause_seconds). Empty text = a silent beat of pause_seconds.
    Returns (duration, [{text,start,end}]). Re-uses the audio if nothing changed."""
    key = hashlib.md5(json.dumps([scene_cues, voice, speed, say or {}]).encode()).hexdigest()[:12]
    meta = out_wav[:-4] + '.json'
    if os.path.exists(meta) and os.path.exists(out_wav):
        m = json.load(open(meta))
        if m.get('key') == key: return m['dur'], m['cues']
    k = kokoro(); parts = [np.zeros(int(LEAD * SR), np.float32)]; t = LEAD; cues = []
    for s, pause in scene_cues:
        if not s.strip():
            p = pause or 2.0
            cues.append({'text': '', 'start': round(t, 3), 'end': round(t + p, 3)}); parts.append(np.zeros(int((p + GAP) * SR), np.float32)); t += p + GAP
            continue
        a, _ = k.create(spoken(s, say), voice=voice, speed=speed, lang=lang); a = a.astype(np.float32); d = len(a) / SR
        cues.append({'text': s, 'start': round(t, 3), 'end': round(t + d, 3)})
        parts += [a, np.zeros(int(GAP * SR), np.float32)]; t += d + GAP
    parts.append(np.zeros(int(TAIL * SR), np.float32)); audio = np.concatenate(parts)
    pk = float(np.max(np.abs(audio))) or 1.0; audio = audio * (0.9 / pk)
    sf.write(out_wav, audio, SR); dur = round(len(audio) / SR, 3)
    json.dump({'key': key, 'dur': dur, 'cues': cues}, open(meta, 'w'))
    return dur, cues
