#!/usr/bin/env python3
"""Script in, narrated MP4 out.

  python3 make_video.py myscript.txt            full video -> myscript.mp4
  python3 make_video.py myscript.txt --check    narration + plan + contact sheets of test frames (no video)
  python3 make_video.py myscript.txt --scene 3  re-render one scene (1-based), then rejoin
"""
import argparse, json, os, subprocess, sys, time
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cairo
from vengine import script as S, scenes as SC, speech, geo
from vengine.core import SW, SH, FPS

FF = ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p']


def load(path):
    meta, say, scenes = S.parse(open(path, encoding='utf-8').read())
    SC.SCRIPT_DIR = os.path.dirname(os.path.abspath(path))
    return meta, say, scenes


def timing(work, i, scene, meta, say):
    return speech.narrate([(c['text'], c['pause']) for c in scene['cues']], os.path.join(work, f'aud_{i:02d}.wav'),
                          voice=meta['VOICE'], speed=float(meta['SPEED']), lang=meta['LANG'], say=say)


def frame(scene, boards, cues, t, dur, meta, surf=None):
    surf = surf or cairo.ImageSurface(cairo.FORMAT_RGB24, SW, SH); c = cairo.Context(surf)
    SC.draw(c, scene, boards, cues, t, dur, meta); return surf


def render_scene(job):
    path, work, i = job
    meta, say, scenes = load(path); sc = scenes[i]; dur, cues = timing(work, i, sc, meta, say)
    boards = SC.plan(sc, dur, cues, i, meta); n = int(round(dur * FPS))
    tmp, out = os.path.join(work, f'v_{i:02d}.tmp.mp4'), os.path.join(work, f'v_{i:02d}.mp4')
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{SW}x{SH}', '-r', str(FPS),
                          '-i', '-', *FF, tmp], stdin=subprocess.PIPE)
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, SW, SH)
    for k in range(n):
        frame(sc, boards, cues, k / FPS, dur, meta, surf); surf.flush(); p.stdin.write(bytes(surf.get_data()))
    p.stdin.close()
    if p.wait() != 0: return f'scene {i + 1}: ffmpeg failed'
    os.replace(tmp, out); return f'scene {i + 1} done ({dur:.1f}s)'


def check(path, work, meta, say, scenes):
    from PIL import Image
    shots = []
    for i, sc in enumerate(scenes):
        dur, cues = timing(work, i, sc, meta, say); boards = SC.plan(sc, dur, cues, i, meta)
        print(f"\nScene {i + 1}: {sc['kicker'] + ' | ' if sc['kicker'] else ''}{sc['title'] or '(untitled)'}  {dur:.1f}s")
        for b in boards:
            print(f"   {b['t0']:6.1f}s  {b['kind']:<9} {' | '.join(b['args'])[:60]}   +{len(b['ov'])} overlays")
            starts = sorted(set(o['t0'] for o in b['ov']))[-3:]
            ts = [min(b['t1'] - 0.7, b['t0'] + 4.2)] + [min(b['t1'] - 0.7, s0 + 2.5) for s0 in starts]
            for t in sorted(set(round(x, 1) for x in ts)):
                fn = os.path.join(work, f'still_{i + 1:02d}_{t:06.1f}.png'); frame(sc, boards, cues, t, dur, meta).write_to_png(fn); shots.append((fn, f'{i + 1}@{t:.1f}s'))
    from PIL import ImageDraw
    per = 12; sheets = []
    for k in range(0, len(shots), per):
        grp = shots[k:k + per]; rows = (len(grp) + 2) // 3; sheet = Image.new('RGB', (3 * 480, rows * 270), 'white'); d = ImageDraw.Draw(sheet)
        for j, (fn, lab) in enumerate(grp):
            x, y = (j % 3) * 480, (j // 3) * 270; sheet.paste(Image.open(fn).resize((480, 270)), (x, y)); d.rectangle([x, y, x + 90, y + 18], fill='black'); d.text((x + 4, y + 3), lab, fill='white')
        out = os.path.join(work, f'sheet_{k // per + 1}.jpg'); sheet.save(out, quality=78); sheets.append(out)
    print('\nContact sheets:', *sheets, sep='\n  ')


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('script'); ap.add_argument('--check', action='store_true')
    ap.add_argument('--scene', type=int, action='append'); ap.add_argument('--out'); ap.add_argument('--jobs', type=int, default=os.cpu_count())
    ap.add_argument('--force', action='store_true', help='render even if some places are unknown')
    a = ap.parse_args(); path = os.path.abspath(a.script)
    base = os.path.splitext(path)[0]; work = base + '_work'; os.makedirs(work, exist_ok=True); out = a.out or base + '.mp4'
    meta, say, scenes = load(path)
    miss = S.check_places(scenes)
    if miss:
        print('Unknown places (add a line  PLACE: Name = lon, lat ):', ', '.join(miss))
        if not a.force: sys.exit(2)
    t0 = time.time()
    print(f'{len(scenes)} scenes. Narrating...', flush=True)
    durs = [timing(work, i, sc, meta, say)[0] for i, sc in enumerate(scenes)]
    words = sum(len(c['text'].split()) for sc in scenes for c in sc['cues'])
    print(f'Narration {sum(durs) / 60:.1f} min, {words} words')
    if a.check: check(path, work, meta, say, scenes); return
    todo = [i - 1 for i in a.scene] if a.scene else list(range(len(scenes)))
    with Pool(max(1, min(a.jobs, len(todo)))) as pool:
        for msg in pool.imap_unordered(render_scene, [(path, work, i) for i in todo]): print(msg, flush=True)
    lst = os.path.join(work, 'list.txt'); alst = os.path.join(work, 'alist.txt')
    open(lst, 'w').write(''.join(f"file 'v_{i:02d}.mp4'\n" for i in range(len(scenes))))
    open(alst, 'w').write(''.join(f"file 'aud_{i:02d}.wav'\n" for i in range(len(scenes))))
    run = lambda *x: subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *x], check=True)
    run('-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', os.path.join(work, 'video.mp4'))
    run('-f', 'concat', '-safe', '0', '-i', alst, '-c', 'copy', os.path.join(work, 'audio.wav'))
    run('-i', os.path.join(work, 'video.mp4'), '-i', os.path.join(work, 'audio.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-shortest', out)
    vol = subprocess.run(['ffmpeg', '-i', out, '-af', 'volumedetect', '-f', 'null', '-'], capture_output=True, text=True).stderr
    mx = next((l.split(':')[-1].strip() for l in vol.splitlines() if 'max_volume' in l), '?')
    print(f'\nDone: {out}  ({sum(durs) / 60:.1f} min, audio peak {mx}, {time.time() - t0:.0f}s)')
    st = 0
    for i, (sc, d) in enumerate(zip(scenes, durs)):
        print(f'  {int(st // 60)}:{int(st % 60):02d}  scene {i + 1}  {sc["title"]}'); st += d


if __name__ == '__main__':
    main()
