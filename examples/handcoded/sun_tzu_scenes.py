from engine2 import *
import random

def card(c, t, n, title, sub=""):
    section_card(c, n, title, sub, prog(t, 0, 0.5) * (1 - prog(t, 3.2, 0.6)))
    act_tag(c, n + "  ·  " + title.upper(), prog(t, 3.6, 0.6))

KINGS = ['Wu', 'Chu', 'Qi', 'Jin', 'Qin', 'Yue']
def s_open(c, t, q, dur):
    cam = GCam('china', [(0, 113, 32, 26), (q[1], 117, 31.5, 16), (dur, 117, 31.5, 16)])
    mp = 1 - prog(t, q[2], 0.8) + prog(t, q[5], 0.8) * 0
    f = gbase(c, cam, t, 1.0)
    if mp > 0:
        for i, k in enumerate(KINGS):
            col = RED if k == 'Wu' else INK
            dot(f, k, mp * prog(t, 0.5 + i * 0.3, 0.4), col, 7); label(f, k, mp * prog(t, 0.5 + i * 0.3, 0.4), col, size=24)
        rnd = random.Random(2)
        for i in range(6):
            a, b = rnd.sample(KINGS, 2); (x0, y0), (x1, y1) = f.P(a), f.P(b)
            ph = ((t * 0.4) + i / 6) % 1
            explosion(c, lerp(x0, x1, 0.5), lerp(y0, y1, 0.5), ph, mp * 0.8, 26)
        text(c, "WARRING KINGDOMS OF CHINA", SW / 2, 120, 40, INK, mp * prog(t, 0.6, 0.6), face=TITLE, bold=True, align='c', halo=(0.96, 0.93, 0.85))
        if t > q[1]:
            x, y = f.P('Wu'); person(c, x - 90, y + 40, RED, mp * prog(t, q[1] + 1, 0.5), 1.0); person(c, x + 80, y + 40, GOLD, mp * prog(t, q[1] + 1.5, 0.5), 1.2)
            text(c, "Sun Tzu", x - 90, y + 105, 22, RED, mp * prog(t, q[1] + 1, 0.5), bold=True, align='c', halo=(0.96, 0.93, 0.85))
            text(c, "King Helü", x + 80, y + 105, 22, GOLD, mp * prog(t, q[1] + 1.5, 0.5), bold=True, align='c', halo=(0.96, 0.93, 0.85))
    # courtyard drill
    ca = prog(t, q[2], 0.8) * (1 - prog(t, q[5], 0.8))
    if ca > 0:
        c.set_source_rgba(0.55, 0.42, 0.28, ca); c.paint()
        c.set_source_rgba(0.62, 0.50, 0.34, ca); c.rectangle(0, 380, SW, 340); c.fill()
        order = prog(t, q[4] + 3.0, 2.0); rnd = random.Random(5)
        for comp in range(2):
            for i in range(12):
                r, col_ = i // 4, i % 4
                gx, gy = 330 + comp * 420 + col_ * 70, 330 + r * 90
                jx = rnd.uniform(-22, 22) * (1 - order); jy = rnd.uniform(-15, 15) * (1 - order)
                lean = math.sin(t * 6 + i) * 4 * (1 - order) * (t > q[3] and t < q[4] + 3)
                person(c, gx + jx + lean, gy + jy, (0.55, 0.20, 0.45), ca, 0.8)
            cx, cy = 330 + comp * 420 + 105, 250
            capa = ca * (1 - prog(t, q[4] + 1.5, 0.6))
            person(c, cx, cy, GOLD, capa, 0.95)
            if t > q[4] + 2.2: person(c, cx, cy, (0.45, 0.12, 0.35), ca * prog(t, q[4] + 2.2, 0.5), 0.95)
            text(c, "captain", cx, cy - 60, 20, (1, 1, 1), ca, italic=True, align='c')
            if q[3] < t < q[4] + 1.5:
                for k in range(3):
                    text(c, "ha", cx - 60 + k * 50 + 5 * math.sin(t * 8 + k), cy - 90 - 10 * abs(math.sin(t * 5 + k)), 26, (1, 0.95, 0.8), ca * 0.9, italic=True)
        person(c, 140, 470, RED, ca, 1.4); text(c, "SUN TZU", 140, 560, 24, (1, 1, 1), ca, face=TITLE, bold=True, align='c')
        if t > q[4] + 3.5: stamp(c, "ORDERS OBEYED", 1060, 200, ca, (1, 0.95, 0.85), 34, p=prog(t, q[4] + 3.5, 0.4))
    # book
    ba = prog(t, q[5], 0.8)
    if ba > 0:
        parch = (0.90, 0.80, 0.58)
        c.set_source_rgba(0.12, 0.09, 0.05, ba); c.paint()
        for i in range(13):
            p = prog(t, q[5] + 0.2 + i * 0.15, 0.3); x = 250 + i * 60
            c.new_path(); c.set_source_rgba(*parch, ba * p); c.rectangle(x, 220, 46, 300); c.fill()
            c.set_source_rgba(0.3, 0.2, 0.1, ba * p); c.set_line_width(1.5); c.move_to(x, 260); c.line_to(x + 46, 260); c.move_to(x, 480); c.line_to(x + 46, 480); c.stroke()
            text(c, str(i + 1), x + 23, 380, 20, (0.3, 0.2, 0.1), ba * p, bold=True, align='c')
        text(c, "THE ART OF WAR", SW / 2, 150, 54, (0.97, 0.88, 0.62), ba, face=TITLE, bold=True, align='c')
        text(c, "13 chapters  ·  studied for 2,500 years", SW / 2, 590, 28, (0.92, 0.84, 0.68), ba, italic=True, align='c')

def ladder(c, t, t0, a):
    rungs = ["1. Balk the enemy's plans", "2. Break up his alliances", "3. Attack his army", "4. Besiege his cities (worst)"]
    panel(c, 300, 130, 680, 380, a); text(c, "SUN TZU'S ORDER OF STRATEGY", SW / 2, 180, 30, INK, a, face=TITLE, bold=True, align='c')
    for i, r in enumerate(rungs):
        p = prog(t, t0 + 0.8 * i, 0.4) * a; y = 240 + i * 66
        col = (0.2, 0.5, 0.25) if i == 0 else (RED if i == 3 else INK)
        c.new_path(); c.set_source_rgba(*col, 0.15 * p); c.rectangle(340, y - 30, 600, 50); c.fill()
        text(c, r, 360, y + 5, 30, col, p, bold=(i == 0))
    text(c, "← best", 910, 245, 24, (0.2, 0.5, 0.25), a * prog(t, t0 + 3.4, 0.4), italic=True, bold=True, align='r')

def s_p1(c, t, q, dur):
    cam = GCam('carib', [(0, -80, 25, 22), (q[4], -80.5, 24.5, 18), (dur, -80.5, 24.5, 18)])
    mapa = prog(t, q[3], 0.6) * (1 - prog(t, q[5], 0.6))
    parch_bg(c)
    if mapa > 0:
        c.push_group(); f = gbase(c, cam, t)
        dot(f, 'Havana', 1, RED, 7); label(f, 'Havana', 1, RED, size=22); dot(f, 'Miami', 1, BLUE, 6); label(f, 'Miami', 1, BLUE, size=22)
        x, y = f.P('SanCristobal'); g = prog(t, q[3] + 1, 2.0)
        for k in range(3):
            c.new_path(); c.move_to(x - 16 + k * 16, y + 6); c.line_to(x - 10 + k * 16, y - 14); c.line_to(x - 4 + k * 16, y + 6); c.close_path(); c.set_source_rgba(*RED, g); c.fill()
        c.new_path(); c.arc(x, y, 700 * g, 0, 7); c.set_source_rgba(*RED, 0.08 * g); c.fill()
        text(c, "Soviet missiles, Oct 1962", x + 20, y + 40, 22, RED, g, bold=True, halo=(0.96, 0.93, 0.85))
        qa = prog(t, q[4], 0.6)
        if qa > 0:
            pts = path_pts(f, [(-80.5, 26.8), (-77.5, 25.2), (-74.5, 23.0), (-73.0, 20.5)])
            partial_line(c, pts, qa, BLUE, 1, 4, dash=[10, 7])
            for k in range(6):
                xx, yy, ang = along(pts, k / 5); ship(c, xx, yy, ang + 1.57, BLUE, qa * prog(t, q[4] + 0.3 * k, 0.4), 1.4)
            text(c, "US naval quarantine", *f.S(-77.0, 27.2), 24, BLUE, qa, bold=True, halo=(0.96, 0.93, 0.85))
            sp = prog(t, q[4] + 1, 5.0); turn = prog(t, q[4] + 4, 1.0)
            sx, sy = f.S(lerp(-66, -71.5, sp) + turn * 3, lerp(22, 22.8, sp))
            ship(c, sx, sy, math.pi if turn < 0.5 else 0, RED, qa, 1.4)
            if t > q[4] + 6: stamp(c, "MISSILES REMOVED", 900, 470, qa, (0.2, 0.5, 0.25), 36, p=prog(t, q[4] + 6, 0.4))
        c.pop_group_to_source(); c.paint_with_alpha(mapa)
    cr = prog(t, q[5], 0.6)
    if cr > 0:
        cam2 = GCam('europe', [(q[5], 34, 46.8, 15), (dur, 34.2, 45.8, 10)])
        c.push_group(); f = gbase(c, cam2, t)
        dot(f, 'Kyiv', 1, BLUE, 7); label(f, 'Kyiv', 1, BLUE, size=22)
        x, y = f.P('Crimea'); g = prog(t, q[5] + 1, 2)
        c.new_path(); c.arc(x, y, 70, 0, 7); c.set_source_rgba(*RED, 0.25 * g); c.fill()
        for k in range(6): soldier(c, x - 60 + k * 24, y + 20, (0.35, 0.40, 0.30), g, 0.8)
        text(c, "Crimea, Feb–Mar 2014", x, y - 95, 26, RED, g, bold=True, align='c', halo=(0.96, 0.93, 0.85))
        text(c, "unmarked troops · information war · staged vote", x, y - 125, 20, INK, prog(t, q[5] + 2.5, 0.5), italic=True, align='c', halo=(0.96, 0.93, 0.85))
        c.pop_group_to_source(); c.paint_with_alpha(cr)
        if t > q[6]: stamp(c, "CREDIBLE FORCE BEHIND THE THREAT", SW / 2, 200, prog(t, q[6], 0.4), RED, 34, p=prog(t, q[6], 0.4))
    quote_box(c, "To fight and conquer in all your battles is not supreme excellence; supreme excellence consists in breaking the enemy's resistance without fighting.",
              "Sun Tzu, III", prog(t, q[1] - 0.3, 0.5) * (1 - prog(t, q[2], 0.4)), size=34)
    la = prog(t, q[2], 0.5) * (1 - prog(t, q[3], 0.5))
    if la > 0: ladder(c, t, q[2] + 0.3, la)
    card(c, t, "PRINCIPLE 1", "Win Without Fighting")

def s_p2(c, t, q, dur):
    parch_bg(c)
    ea = prog(t, q[2], 0.6) * (1 - prog(t, q[4], 0.6))
    if ea > 0:
        cam = GCam('europe', [(q[2], 0.4, 50.4, 11.5), (dur, 0.4, 50.3, 11)])
        c.push_group(); f = gbase(c, cam, t)
        for n, col in (('Calais', RED), ('Dover', BLUE), ('London', BLUE)): dot(f, n, 1, col, 6); label(f, n, 1, col, size=22)
        x, y = f.S(0.6, 51.25); inf = prog(t, q[2] + 0.5, 1.5)
        for k in range(5): tank(c, x - 60 + k * 30, y + (k % 2) * 16, (0.45, 0.50, 0.35), 1, 0.9, max(0.15, inf))
        radio(c, x + 90, y - 20, t, inf)
        text(c, "FAKE ARMY (FUSAG)", x - 30, y + 50, 22, BLUE, inf, bold=True, align='c', halo=(0.96, 0.93, 0.85))
        partial_line(c, path_pts(f, [(1.2, 51.1), 'Calais']), prog(t, q[2] + 2, 1.5), BLUE, 0.8, 5, dash=[10, 6], arrow=True)
        xc, yc = f.P('Calais')
        for k in range(6): soldier(c, xc + 20 + k * 18, yc + 30, (0.35, 0.35, 0.35), 1, 0.7)
        text(c, "German 15th Army waits", xc + 70, yc + 75, 22, INK, prog(t, q[3] + 2, 0.5), bold=True, align='c', halo=(0.96, 0.93, 0.85))
        rl = prog(t, q[3], 0.5)
        if rl > 0:
            route = path_pts(f, [(-1.0, 50.6), (-0.6, 50.0), 'Normandy'])
            for k in range(8):
                xx, yy, ang = along(route, max(0, prog(t, q[3], 3) - k * 0.04)); ship(c, xx - k * 4, yy, ang, BLUE, rl, 1.2)
            text(c, "6 Jun 1944: Normandy", *f.S(-4.8, 49.9), 26, BLUE, rl, bold=True, halo=(0.96, 0.93, 0.85))
            if t > q[3] + 3: text(c, "?", xc + 70, yc - 10, 46, INK, prog(t, q[3] + 3, 0.4), bold=True, align='c')
        c.pop_group_to_source(); c.paint_with_alpha(ea)
    ua = prog(t, q[4], 0.6) * (1 - prog(t, q[6], 0.6))
    if ua > 0:
        cam = GCam('europe', [(q[4], 34.3, 48.5, 15), (dur, 34.3, 48.5, 14.5)])
        c.push_group(); f = gbase(c, cam, t)
        for n in ('Kyiv', 'Kharkiv', 'Kherson'): dot(f, n, 1, BLUE, 6); label(f, n, 1, INK, size=22)
        partial_line(c, path_pts(f, [(32.0, 47.6), (32.5, 47.0)]), prog(t, q[4] + 0.5, 1.5), BLUE, 0.9, 6, dash=[10, 6], arrow=True)
        text(c, "announced offensive", *f.S(30.6, 47.9), 22, BLUE, prog(t, q[4] + 1, 0.5), italic=True, bold=True, halo=(0.96, 0.93, 0.85))
        mv = prog(t, q[5], 3)
        for k in range(5):
            xx, yy = f.S(lerp(36.5, 33.4, mv) + k * 0.25, lerp(49.6, 47.2, mv) + (k % 2) * 0.2); tank(c, xx, yy, RED, 1, 0.7)
        br = prog(t, q[5] + 3, 2)
        if br > 0:
            partial_line(c, path_pts(f, [(35.4, 49.3), (36.6, 49.6), (37.6, 49.2)]), br, BLUE, 1, 8, arrow=True)
            for k in range(3): explosion(c, *f.S(36.0 + k * 0.5, 49.45), ((t - q[5] - 3) * 0.8 + k * 0.3) % 1, 1, 30)
            text(c, "Sep 2022: Kharkiv breakthrough", *f.S(35.0, 50.4), 26, BLUE, br, bold=True, halo=(0.96, 0.93, 0.85))
        c.pop_group_to_source(); c.paint_with_alpha(ua)
    ma = prog(t, q[6], 0.6)
    if ma > 0:
        parch_bg(c, dark=True)
        panel(c, 120, 170, 480, 300, ma, fill=(0.1, 0.12, 0.12), border=(0.5, 0.9, 0.5))
        text(c, "STATUS:  NORMAL", 360, 230, 34, (0.4, 1, 0.4), ma, face="DejaVu Sans Mono", bold=True, align='c')
        cx, cy = 360, 370; ang = t * 30
        for k in range(6):
            c.new_path(); c.arc(cx + 70 * math.cos(ang + k), cy + 50 * math.sin(ang + k), 12, 0, 7); c.set_source_rgba(1, 0.3, 0.2, ma); c.fill()
        text(c, "malware fakes the readings", 360, 500, 22, (0.95, 0.9, 0.8), ma, italic=True, align='c')
        panel(c, 680, 170, 480, 300, ma, fill=(0.15, 0.15, 0.2), border=(0.7, 0.7, 0.9))
        gl = 4 * math.sin(t * 20)
        person(c, 920 + gl, 360, (0.8, 0.75, 0.7), ma, 2.0); person(c, 925 - gl, 360, (0.4, 0.6, 1.0), ma * 0.35, 2.0)
        text(c, "deepfake video of a leader", 920, 500, 22, (0.95, 0.9, 0.8), ma, italic=True, align='c')
        sa = prog(t, q[7], 0.5)
        if sa > 0:
            c.set_source_rgba(0.05, 0.04, 0.03, 0.85 * sa); c.paint()
            ex, ey = SW / 2, 330; c.new_path(); c.arc(ex, ey, 120, 0, 7); c.set_source_rgba(0.9, 0.95, 1, sa); c.set_line_width(5); c.stroke()
            c.new_path(); c.arc(ex, ey, 45, 0, 7); c.set_source_rgba(0.3, 0.6, 0.9, sa); c.fill()
            for k in range(4):
                a2 = t * 0.8 + k * 1.57; sx, sy = ex + 220 * math.cos(a2), ey + 110 * math.sin(a2)
                c.new_path(); c.rectangle(sx - 14, sy - 6, 28, 12); c.set_source_rgba(0.9, 0.9, 0.9, sa); c.fill()
            text(c, "satellites and open-source analysts see everything", SW / 2, 520, 28, (1, 0.95, 0.85), sa, italic=True, align='c')
    quote_box(c, "All warfare is based on deception.", "Sun Tzu, I", prog(t, q[0] - 0.3, 0.5) * (1 - prog(t, q[1] - 0.2, 0.4)), size=44)
    quote_box(c, "When able to attack, we must seem unable; when we are near, we must make the enemy believe we are far away.",
              "Sun Tzu, I", prog(t, q[1] - 0.2, 0.4) * (1 - prog(t, q[2], 0.4)), size=34)
    card(c, t, "PRINCIPLE 2", "All Warfare Is Based on Deception")

def s_p3(c, t, q, dur):
    parch_bg(c)
    sp = prog(t, q[2], 0.5) * (1 - prog(t, q[3], 0.5))
    if sp > 0:
        parch_bg(c, dark=True); person(c, 640, 420, (0.1, 0.08, 0.06), sp, 2.4)
        c.new_path(); c.set_source_rgba(0.1, 0.08, 0.06, sp); c.rectangle(580, 300, 120, 16); c.fill(); c.rectangle(605, 262, 70, 40); c.fill()
        text(c, "Knowledge “can only be obtained from other men”", 640, 600, 32, (0.97, 0.88, 0.62), sp, italic=True, align='c')
        text(c, "spies and agents, not spirits or guesswork", 640, 640, 24, (0.9, 0.82, 0.66), sp, align='c')
    ma = prog(t, q[3], 0.5) * (1 - prog(t, q[4], 0.5))
    if ma > 0:
        c.set_source_rgba(0.16, 0.30, 0.42, ma); c.paint()
        for i in range(30):
            x = (i * 97 + t * 20) % SW; c.new_path(); c.move_to(x, 100 + (i * 53) % 500); c.line_to(x + 30, 100 + (i * 53) % 500); c.set_source_rgba(1, 1, 1, 0.15 * ma); c.set_line_width(2); c.stroke()
        panel(c, 50, 120, 530, 170, ma, fill=(0.95, 0.93, 0.85))
        text(c, "Intercepted:  “AF is short of water”", 315, 180, 21, INK, ma, face="DejaVu Sans Mono", align='c')
        dc = prog(t, q[3] + 2, 1.0)
        text(c, "AF = MIDWAY", 315, 245, 40, RED, ma * dc, face=TITLE, bold=True, align='c')
        radio(c, 560, 200, t, ma, (1, 1, 1))
        for k in range(4):
            x = 700 + k * 130; sk = prog(t, q[3] + 3.5 + k * 0.6, 1.2)
            c.new_path(); c.save(); c.translate(x, 470 + sk * 40); c.rotate(sk * 0.5)
            c.set_source_rgba(0.55, 0.15, 0.12, ma * (1 - sk)); c.rectangle(-50, -10, 100, 20); c.fill(); c.rectangle(10, -26, 18, 16); c.fill(); c.restore()
            explosion(c, x, 470, sk, ma, 40)
        text(c, "Jun 1942: 4 Japanese carriers sunk", 900, 620 - 60, 28, (1, 0.97, 0.9), ma * prog(t, q[3] + 4, 0.5), bold=True, align='c')
    ua = prog(t, q[4], 0.5)
    if ua > 0:
        cam = GCam('europe', [(q[4], 31.5, 51.4, 14), (dur, 31.0, 51.2, 11)])
        c.push_group(); f = gbase(c, cam, t)
        dot(f, 'Kyiv', 1, BLUE, 9, 1, t); label(f, 'Kyiv', 1, BLUE, size=26)
        p = prog(t, q[4] + 0.5, 3) * 0.85
        for src in ((30.3, 52.4), (31.3, 52.2), (32.6, 51.9)):
            partial_line(c, path_pts(f, [src, 'Kyiv']), p, RED, 1, 6, arrow=True)
        text(c, "Plan: Kyiv falls in days", *f.S(27.8, 52.4), 28, RED, prog(t, q[4] + 1, 0.5), bold=True, halo=(0.96, 0.93, 0.85))
        if t > q[5]: stamp(c, "STALLED", *f.S(30.8, 51.4), prog(t, q[5], 0.4), RED, 40, p=prog(t, q[5], 0.4))
        c.pop_group_to_source(); c.paint_with_alpha(ua)
        ka = prog(t, q[5] + 1.5, 0.5)
        if ka > 0:
            panel(c, 820, 140, 420, 140, ka)
            for i, s in enumerate(("Know the enemy", "Know yourself")):
                text(c, s, 850, 195 + i * 50, 30, INK, ka, bold=True); text(c, "✗", 1190, 195 + i * 50, 38, RED, ka * prog(t, q[5] + 2 + i * 0.6, 0.3), bold=True, face="DejaVu Sans", align='c')
        if t > q[6]: stamp(c, "KNOW YOURSELF", SW / 2, 470, prog(t, q[6], 0.4), RED, 50, p=prog(t, q[6], 0.4))
    quote_box(c, "If you know the enemy and know yourself, you need not fear the result of a hundred battles.", "Sun Tzu, III",
              prog(t, q[0] - 0.3, 0.5) * (1 - prog(t, q[1] - 0.2, 0.4)), size=36)
    quote_box(c, "If you know neither the enemy nor yourself, you will succumb in every battle.", "Sun Tzu, III",
              prog(t, q[1] - 0.2, 0.4) * (1 - prog(t, q[2], 0.4)), size=36)
    card(c, t, "PRINCIPLE 3", "Know the Enemy and Know Yourself")

def water(c, t, a):
    c.set_source_rgba(*PARCH, a); c.paint()
    for k in range(9):
        y0 = 360 + k * 18
        c.new_path(); c.move_to(100, y0)
        for x in range(100, 1181, 10):
            d = abs(x - 640); bump = -max(0, 140 - d) * 1.1 if y0 < 470 else 0
            y = y0 + 6 * math.sin(x * 0.03 - t * 4 + k) + (bump if d < 140 else 0)
            c.line_to(x, y if d >= 90 or y0 >= 470 else max(y, 520))
        c.set_source_rgba(0.25, 0.45, 0.70, a * 0.6); c.set_line_width(3); c.stroke()
    c.new_path(); c.set_source_rgba(0.45, 0.40, 0.35, a); c.move_to(540, 540); c.line_to(640, 300); c.line_to(740, 540); c.close_path(); c.fill()
    text(c, "STRENGTH", 640, 290, 26, INK, a, face=TITLE, bold=True, align='c')

def s_p4(c, t, q, dur):
    parch_bg(c)
    wa = prog(t, 3.6, 0.5) * (1 - prog(t, q[2], 0.5))
    if wa > 0: water(c, t, wa)
    ra = prog(t, q[2], 0.6) * (1 - prog(t, q[4], 0.6))
    if ra > 0:
        cam = GCam('mideast', [(q[2], 41.5, 17.5, 16), (dur, 41.0, 16.5, 13)])
        c.push_group(); f = gbase(c, cam, t)
        dot(f, 'Sanaa', 1, RED, 7); label(f, 'Sanaa', 1, RED, size=22, txt='Houthis (Yemen)')
        rnd = random.Random(4)
        for k in range(5):
            sx, sy = f.S(39.0 + k * 0.6, 17.5 + k * 1.2 - 2)
            ship(c, sx, sy, 2.0, (0.35, 0.35, 0.35), 1, 1.3)
            ph = ((t - q[2]) * 0.25 + k * 0.2) % 1; hx, hy = f.P('Hodeidah')
            drone(c, lerp(hx, sx, ph), lerp(hy, sy, ph), math.atan2(sy - hy, sx - hx), RED, 1, 1.2)
            if ph > 0.92: explosion(c, sx, sy, (ph - 0.92) / 0.08, 1, 30)
        wx, wy = f.S(38.6, 19.6); ship(c, wx, wy, 0.4, BLUE, prog(t, q[3], 0.5), 2.2)
        if t > q[3]:
            for k in range(3):
                ph = ((t - q[3]) * 0.5 + k / 3) % 1; c.new_path(); c.arc(lerp(wx, wx + 100, ph), lerp(wy, wy + 80, ph), 4, 0, 7); c.set_source_rgba(*BLUE, 1); c.fill()
            panel(c, 760, 130, 460, 120, prog(t, q[3] + 0.5, 0.5))
            text(c, "Drone:  ~ thousands of $", 790, 175, 28, RED, prog(t, q[3] + 0.5, 0.5), bold=True)
            text(c, "Interceptor:  ~ millions of $", 790, 220, 28, BLUE, prog(t, q[3] + 1.2, 0.5), bold=True)
        partial_line(c, path_pts(f, [(37.5, 22.0), (34.0, 16.0), (33.5, 11.5)]), prog(t, q[3] + 2, 2), (0.35, 0.35, 0.35), 0.8, 5, dash=[8, 6], arrow=True)
        text(c, "shipping diverts around Africa", *f.S(34.6, 20.5), 20, INK, prog(t, q[3] + 3, 0.5), italic=True, halo=(0.96, 0.93, 0.85))
        c.pop_group_to_source(); c.paint_with_alpha(ra)
    ba = prog(t, q[4], 0.6) * (1 - prog(t, q[6], 0.6))
    if ba > 0:
        cam = GCam('europe', [(q[4], 33.2, 45.6, 14), (dur, 33.4, 45.4, 13)])
        c.push_group(); f = gbase(c, cam, t)
        dot(f, 'Odesa', 1, BLUE, 7); label(f, 'Odesa', 1, BLUE, size=22); dot(f, 'Sevastopol', 1, RED, 7); label(f, 'Sevastopol', 1, RED, size=22)
        mx, my = f.S(30.9, 45.2); sk = prog(t, q[4] + 3, 2.0)
        ship(c, mx, my + sk * 20, 0.2, RED, 1 - sk, 2.4, tilt=sk)
        if 0 < sk < 1: fire(c, mx, my, t, 1, seed=3)
        x0, y0 = f.S(31.0, 46.7); mp = prog(t, q[4] + 1, 2.0)
        if mp < 1: drone(c, lerp(x0, mx, mp), lerp(y0, my, mp), math.atan2(my - y0, mx - x0), BLUE, 1, 1.4)
        explosion(c, mx, my, prog(t, q[4] + 3, 0.8), 1, 50)
        text(c, "Apr 2022: cruiser Moskva sunk", mx, my - 50, 26, RED, prog(t, q[4] + 3, 0.5), bold=True, align='c', halo=(0.96, 0.93, 0.85))
        fl = prog(t, q[5], 5)
        if fl > 0:
            for k in range(4):
                fx, fy = f.S(lerp(32.5, 37.5, fl) + k * 0.4, 44.3 + (k % 2) * 0.3); ship(c, fx, fy, 0, RED, 1, 1.4)
                dx, dy = f.S(lerp(31.8, 36.8, fl) + k * 0.3, 44.4 + (k % 2) * 0.3 + 0.1 * math.sin(t * 6 + k)); drone(c, dx, dy, 0, BLUE, 1, 1.1)
            text(c, "sea drones push the fleet east", *f.S(33.0, 43.6), 24, BLUE, prog(t, q[5], 0.5), bold=True, halo=(0.96, 0.93, 0.85))
        c.pop_group_to_source(); c.paint_with_alpha(ba)
    if t > q[6]:
        a = prog(t, q[6], 0.5); c.set_source_rgba(0, 0, 0, 0.3 * a); c.paint()
        stamp(c, "REFUSE STRENGTH  ·  STRIKE WEAKNESS", SW / 2, SH / 2 - 20, a, RED, 40, p=prog(t, q[6], 0.4))
    quote_box(c, "Military tactics are like unto water; for water in its natural course runs away from high places and hastens downwards.", "Sun Tzu, VI",
              prog(t, q[0] - 0.3, 0.5) * (1 - prog(t, q[1] - 0.2, 0.4)), y=60, size=30)
    quote_box(c, "So in war, the way is to avoid what is strong and to strike at what is weak.", "Sun Tzu, VI",
              prog(t, q[1] - 0.2, 0.4) * (1 - prog(t, q[2], 0.4)), y=60, size=34)
    card(c, t, "PRINCIPLE 4", "Avoid Strength, Strike Weakness")

def s_p5(c, t, q, dur):
    parch_bg(c, dark=True)
    sa = prog(t, q[1], 0.5) * (1 - prog(t, q[3], 0.5))
    if sa > 0:
        c.set_source_rgba(0.62, 0.58, 0.50, sa); c.rectangle(0, 470, SW, 250); c.fill()
        for k in range(4):
            x = 120 + k * 150; op = prog(t, q[1] + 2 + k * 0.4, 0.6)
            c.new_path(); c.set_source_rgba(0.30, 0.30, 0.28, sa); c.rectangle(x, 400, 110, 60); c.fill(); c.rectangle(x + 110, 418, 30, 42); c.fill()
            c.set_source_rgba(0.5, 0.5, 0.48, sa); c.save(); c.translate(x, 400); c.rotate(-op * 1.2); c.rectangle(0, -6, 110, 6); c.fill(); c.restore()
            c.new_path(); c.set_source_rgba(0.1, 0.1, 0.1, sa); [c.arc(x + 20 + i * 70, 465, 10, 0, 7) or c.fill() for i in range(2)]
            for d in range(3):
                ph = clamp((t - q[1] - 3 - k * 0.4 - d * 0.2) / 3)
                if ph > 0: drone(c, lerp(x + 55, 820 + d * 90, ph), lerp(400, 240 + k * 30, ph) - 120 * math.sin(ph * 3.14), -0.3, (0.3, 0.55, 0.9), sa, 1.2)
        for k in range(3):
            bx = 860 + k * 130; hit = prog(t, q[1] + 6 + k * 0.4, 0.8)
            c.new_path(); c.save(); c.translate(bx, 300); c.set_source_rgba(0.25, 0.25, 0.25, sa * (1 - 0.5 * hit))
            c.move_to(-50, 0); c.line_to(50, 0); c.line_to(55, 6); c.line_to(-50, 6); c.close_path(); c.fill()
            c.move_to(-10, 3); c.line_to(25, -35); c.line_to(35, -35); c.line_to(15, 3); c.close_path(); c.fill(); c.restore()
            explosion(c, bx, 300, hit, sa, 50); fire(c, bx, 300, t, sa * (hit >= 1), seed=k)
        text(c, "OPERATION SPIDERWEB  ·  1 Jun 2025", SW / 2, 120, 38, (0.97, 0.88, 0.62), sa, face=TITLE, bold=True, align='c')
        if t > q[2]:
            for i, s in enumerate(("unexpected routes", "unguarded spots", "complete surprise")):
                text(c, s, 260 + i * 380, 610, 28, (1, 0.95, 0.85), sa * prog(t, q[2] + i * 0.6, 0.4), italic=True, bold=True, align='c')
    la = prog(t, q[4], 0.5)
    if la > 0:
        parch_bg(c)
        yrs = ["2022", "2023", "2024", "2025", "2026"]; k = min(4, int((t - q[4]) / 1.2))
        panel(c, 120, 200, 260, 280, la); text(c, yrs[k], 250, 370, 76, RED, la, face=TITLE, bold=True, align='c')
        text(c, "year of war", 250, 430, 24, INK, la, italic=True, align='c')
        h = prog(t, q[4], 6)
        for i in range(int(40 * h)):
            x = 470 + (i % 10) * 34; y = 520 - (i // 10) * 40
            c.new_path(); c.rectangle(x, y - 30, 22, 30); c.set_source_rgba(0.55, 0.48, 0.25, la); c.fill(); c.move_to(x, y - 30); c.line_to(x + 11, y - 42); c.line_to(x + 22, y - 30); c.close_path(); c.fill()
        for i in range(3):
            fx = 900 + i * 100; c.new_path(); c.set_source_rgba(0.4, 0.4, 0.42, la); c.rectangle(fx, 400, 80, 120); c.fill(); c.rectangle(fx + 50, 340, 16, 60); c.fill()
            c.new_path(); c.arc(fx + 58 + 6 * math.sin(t + i), 320 - ((t * 20 + i * 15) % 40), 12, 0, 7); c.set_source_rgba(0.5, 0.5, 0.5, la * 0.5); c.fill()
        text(c, "shells · drones · factories: a war of attrition", SW / 2, 620, 30, INK, la, italic=True, align='c')
    quote_box(c, "Rapidity is the essence of war: take advantage of the enemy's unreadiness, make your way by unexpected routes, and attack unguarded spots.",
              "Sun Tzu, XI", prog(t, q[0] - 0.3, 0.5) * (1 - prog(t, q[1], 0.4)), size=32)
    quote_box(c, "There is no instance of a country having benefited from prolonged warfare.", "Sun Tzu, II",
              prog(t, q[3] - 0.3, 0.5) * (1 - prog(t, q[4], 0.4)), size=38)
    card(c, t, "PRINCIPLE 5", "Speed, and the Danger of Long Wars")

def s_p6(c, t, q, dur):
    parch_bg(c)
    va = prog(t, q[0], 0.5) * (1 - prog(t, q[1], 0.5))
    if va > 0:
        person(c, SW / 2, 420, RED, va, 1.8)
        for i, v in enumerate(("Wisdom", "Sincerity", "Benevolence", "Courage", "Strictness")):
            ang = -math.pi / 2 + i * 2 * math.pi / 5; x, y = SW / 2 + 300 * math.cos(ang), 395 + 185 * math.sin(ang)
            p = prog(t, q[0] + 3 + i * 0.6, 0.4) * va
            c.new_path(); c.arc(x, y, 62, 0, 7); c.set_source_rgba(*GOLD, 0.2 * p); c.fill(); c.set_source_rgba(*GOLD, p); c.set_line_width(3); c.arc(x, y, 62, 0, 7); c.stroke()
            text(c, v, x, y + 9, 24, INK, p, bold=True, align='c')
        text(c, "THE FIVE VIRTUES OF THE COMMANDER", SW / 2, 110, 34, INK, va, face=TITLE, bold=True, align='c')
    ia = prog(t, q[2], 0.6) * (1 - prog(t, q[3] + 0.5, 0.6))
    if ia > 0:
        cam = GCam('sasia2', [(q[2], 73.5, 31.0, 20), (dur, 73.5, 31.0, 19)])
        c.push_group(); f = gbase(c, cam, t)
        dot(f, 'Delhi', 1, (0.85, 0.45, 0.1), 8); label(f, 'Delhi', 1, (0.85, 0.45, 0.1), size=24, txt='INDIA')
        dot(f, 'Islamabad', 1, (0.1, 0.45, 0.25), 8); label(f, 'Islamabad', 1, (0.1, 0.45, 0.25), size=24, txt='PAKISTAN')
        d = min(4, 1 + int((t - q[2]) / 2.2))
        for k in range(6):
            ph = ((t - q[2]) * 0.6 + k / 6) % 1; a_, b_ = ('Delhi', 'Lahore') if k % 2 == 0 else ('Islamabad', 'Srinagar')
            (x0, y0), (x1, y1) = f.P(a_), f.P(b_)
            if t < q[2] + 8: drone(c, lerp(x0, x1, ph), lerp(y0, y1, ph) - 40 * math.sin(ph * 3.14), math.atan2(y1 - y0, x1 - x0), RED, 1, 1.2)
        panel(c, 900, 130, 300, 100, 1); text(c, f"Day {d} of 4", 1050, 195, 40, INK, 1, face=TITLE, bold=True, align='c')
        if t > q[2] + 8: stamp(c, "CEASEFIRE  ·  10 May 2025", SW / 2, 430, prog(t, q[2] + 8, 0.4), (0.2, 0.5, 0.25), 40, p=prog(t, q[2] + 8, 0.4))
        c.pop_group_to_source(); c.paint_with_alpha(ia)
    if t > q[3]: stamp(c, "RESTRAINT IS STRATEGY", SW / 2, 250, prog(t, q[3], 0.4), RED, 44, p=prog(t, q[3], 0.4))
    quote_box(c, "Move not unless you see an advantage; use not your troops unless there is something to be gained; fight not unless the position is critical.",
              "Sun Tzu, XII", prog(t, q[1] - 0.3, 0.5) * (1 - prog(t, q[2], 0.4)), size=32)
    card(c, t, "PRINCIPLE 6", "The Commander and Restraint")

def s_close(c, t, q, dur):
    parch_bg(c)
    la = prog(t, q[0], 0.5) * (1 - prog(t, q[6], 0.5))
    if la > 0:
        text(c, "SUN TZU'S LESSONS", SW / 2, 110, 46, INK, la, face=TITLE, bold=True, align='c')
        bullet_list(c, ["Win without fighting where you can", "Deceive, and expect to be deceived", "Know the enemy, and above all yourself",
                        "Avoid strength, strike weakness", "Move fast, and avoid long wars"], t, q[1:6], y0=200, dy=78, size=34, a=la)
    ma = prog(t, q[6], 0.5) * (1 - prog(t, q[7], 0.5))
    if ma > 0:
        for i, (s, sym) in enumerate((("Nuclear weapons", "☢"), ("Laws of war", "⚖"), ("Artificial intelligence", "AI"))):
            x = 280 + i * 360; p = prog(t, q[6] + 0.8 * i, 0.4) * ma
            text(c, sym, x, 330, 90, INK, p, face="DejaVu Sans", bold=True, align='c'); text(c, s, x, 420, 30, INK, p, bold=True, align='c')
        text(c, "beyond his world — but his principles still hold", SW / 2, 530, 32, RED, ma * prog(t, q[6] + 3, 0.5), italic=True, align='c')
    e = prog(t, q[7], 0.6)
    if e > 0:
        parch_bg(c, dark=True); c.set_source_rgba(0, 0, 0, 1 - e); c.paint()
        text(c, "“The art of war is of vital importance to the State.”", SW / 2, 330, 44, (0.97, 0.88, 0.62), e, italic=True, align='c')
        text(c, "— Sun Tzu", SW / 2, 400, 28, (0.9, 0.8, 0.6), e * prog(t, q[7] + 2, 0.6), align='c')

SCENE_FN = {'open': s_open, 'p1': s_p1, 'p2': s_p2, 'p3': s_p3, 'p4': s_p4, 'p5': s_p5, 'p6': s_p6, 'close': s_close}
