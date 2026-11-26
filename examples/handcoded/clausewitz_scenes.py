from engine2 import *
import random
H = (0.96, 0.93, 0.85)

def card(c, t, n, title, sub=""):
    section_card(c, n, title, sub, prog(t, 0, 0.5) * (1 - prog(t, 3.2, 0.6)))
    act_tag(c, n + "  ·  " + title.upper(), prog(t, 3.6, 0.6))

def s_open(c, t, q, dur):
    keys = [(0, 13.4, 52.0, 13), (q[1], 12.0, 51.5, 12), (q[2] - 0.5, 12.0, 51.5, 12), (q[2] + 3, 26, 54, 30), (q[3], 26, 54, 30), (q[3] + 2.5, 9, 51.5, 15), (q[4], 9, 51.5, 15), (q[4] + 2, 13.4, 52.3, 12), (dur, 13.4, 52.3, 12)]
    f = gbase(c, GCam('europe2', keys), t)
    dot(f, 'Berlin', 1, BLUE, 7); label(f, 'Berlin', 1, BLUE, size=22, txt='Berlin (Prussia)')
    yr = "1792"
    if t < q[1]:
        x, y = f.P('Berlin'); person(c, x - 80, y + 70, BLUE, prog(t, 1, 0.5), 0.8); text(c, "age 12", x - 80, y + 130, 22, BLUE, prog(t, 1.5, 0.5), bold=True, align='c', halo=H)
    if t >= q[1]:
        yr = "1806"; a = prog(t, q[1], 0.5) * (1 - prog(t, q[2], 0.6)); dot(f, 'Jena', a, RED, 8); label(f, 'Jena', a, RED, size=24, txt='Jena')
        x, y = f.P('Jena')
        for k in range(5): soldier(c, x - 70 + k * 30, y + 40, BLUE, a, 0.8, down=prog(t, q[1] + 1.5 + k * 0.2, 0.5))
        for k in range(5): soldier(c, x - 70 + k * 30, y - 50, (0.25, 0.25, 0.55), a * prog(t, q[1] + 0.5, 0.5), 0.8)
        text(c, "Napoleon crushes Prussia", x, y + 110, 24, RED, a * prog(t, q[1] + 1, 0.5), bold=True, align='c', halo=H)
        if t > q[1] + 3: stamp(c, "CAPTURED", x + 160, y - 20, a * prog(t, q[1] + 3, 0.4), RED, 34, p=prog(t, q[1] + 3, 0.4))
    if t >= q[2]:
        yr = "1812"; a = prog(t, q[2], 0.5); pts = path_pts(f, ['Niemen', 'Smolensk', 'Borodino', 'Moscow'])
        partial_line(c, pts, prog(t, q[2] + 1, 3), (0.25, 0.25, 0.55), a, 7, arrow=True)
        partial_line(c, pts[::-1], prog(t, q[2] + 4.5, 3), RED, a * 0.9, 3, dash=[8, 6], arrow=True)
        dot(f, 'Moscow', a, INK, 7); label(f, 'Moscow', a, INK, size=22)
        text(c, "serves with the Russians", *f.S(30, 58), 24, BLUE, a, bold=True, align='c', halo=H)
    if t >= q[3]:
        yr = "1815"; a = prog(t, q[3] + 2, 0.5); dot(f, 'Waterloo', a, RED, 8, 1, t); label(f, 'Waterloo', a, RED, size=24)
    if t >= q[4]:
        yr = "1818–31"; x, y = f.P('Berlin'); a = prog(t, q[4] + 1.5, 0.5)
        panel(c, x - 60, y + 30, 120, 90, a, fill=(0.98, 0.95, 0.88))
        c.set_source_rgba(*INK, a); c.set_line_width(2)
        for k in range(5): c.move_to(x - 45, y + 50 + k * 13); c.line_to(x + 45 - (k == 4) * 30 * (1 - prog(t, q[4] + 2, 6)), y + 50 + k * 13)
        c.stroke(); text(c, "war college", x, y + 145, 22, INK, a, italic=True, align='c', halo=H)
    year_badge(c, yr, prog(t, 0.5, 0.5))
    ba = prog(t, q[5] + 2.5, 0.8)
    if ba > 0:
        parch_bg(c, dark=True); c.set_source_rgba(0, 0, 0, 1 - ba); c.paint()
        c.new_path(); c.set_source_rgba(0.45, 0.12, 0.10, ba); c.rectangle(500, 200, 280, 360); c.fill()
        c.set_source_rgba(*GOLD, ba); c.set_line_width(3); c.rectangle(520, 220, 240, 320); c.stroke()
        text(c, "VOM", 640, 330, 34, GOLD, ba, face=TITLE, bold=True, align='c'); text(c, "KRIEGE", 640, 380, 44, GOLD, ba, face=TITLE, bold=True, align='c')
        text(c, "ON WAR  ·  published by Marie von Clausewitz, 1832", 640, 610, 26, (0.95, 0.88, 0.7), ba, italic=True, align='c')

def s_p1(c, t, q, dur):
    parch_bg(c)
    ma = prog(t, q[3], 0.6)
    if ma > 0:
        keys = [(q[3], 46.5, 30.5, 9), (q[4], 46.5, 30.5, 9), (q[4] + 1.5, 44.5, 32.5, 11), (dur, 44.5, 32.5, 11)]
        c.push_group(); f = gbase(c, GCam('mideast', keys), t)
        for n in ('Kuwait', 'Baghdad', 'Basra'): dot(f, n, 1, INK, 7); label(f, n, 1, INK, size=22)
        if t < q[4] + 0.5:
            p = prog(t, q[3] + 0.5, 4.0)
            for k, (a_, b_) in enumerate((((47.6, 28.6), (47.9, 29.6)), ((46.8, 28.9), (46.9, 30.3)), ((45.0, 29.4), (46.2, 30.6)))):
                partial_line(c, path_pts(f, [a_, b_]), p, BLUE, 1, 8, arrow=True)
            hrs = int(100 * p); panel(c, 900, 120, 300, 110, 1); text(c, f"{hrs} hours", 1050, 192, 50, INK, 1, face=TITLE, bold=True, align='c')
            if p >= 1: stamp(c, "STOP: KUWAIT FREED", 560, 190, prog(t, q[3] + 4.6, 0.4), (0.2, 0.5, 0.25), 36, p=prog(t, q[3] + 4.6, 0.4))
            year_badge(c, "1991", 1)
        else:
            p = prog(t, q[4] + 0.5, 3.0); partial_line(c, path_pts(f, ['Kuwait', 'Basra', (45.6, 32.3), 'Baghdad']), p, BLUE, 1, 9, arrow=True)
            if t > q[4] + 4:
                x, y = f.P('Baghdad'); rnd = random.Random(1)
                for k in range(8):
                    ph = ((t - q[4]) * 0.5 + k / 8) % 1
                    explosion(c, x + rnd.uniform(-160, 160), y + rnd.uniform(-120, 160), ph, 0.9, 26)
                text(c, "no plan for after: insurgency", x, y - 70, 28, RED, prog(t, q[4] + 4, 0.5), bold=True, align='c', halo=H)
            year_badge(c, "2003", 1)
        c.pop_group_to_source(); c.paint_with_alpha(ma * (1 - prog(t, q[5], 0.6)))
    pa = prog(t, q[2], 0.5) * (1 - prog(t, q[3], 0.5))
    if pa > 0:
        for i, (s, col) in enumerate((("POLICY", BLUE), ("WAR", RED))):
            x, y = 360 + i * 560, 360
            panel(c, x - 150, y - 80, 300, 140, pa, fill=(0.98, 0.95, 0.88), border=col)
            text(c, s, x, y + 5, 50, col, pa, face=TITLE, bold=True, align='c')
        partial_line(c, [(530, 340), (750, 340)], prog(t, q[2] + 0.5, 0.8), INK, pa, 6, arrow=True)
        text(c, "sets the aim and limits", 640, 300, 24, INK, pa * prog(t, q[2] + 1, 0.5), italic=True, align='c')
    sa = prog(t, q[5], 0.5)
    if sa > 0:
        for i, s in enumerate(("What is the aim?", "What kind of war is this?", "When do we stop?")):
            text(c, s, SW / 2, 260 + i * 90, 42, INK if i else RED, sa * prog(t, q[5] + 0.6 * i, 0.4), face=TITLE, bold=True, align='c')
    quote_box(c, "War is a mere continuation of policy by other means.", "Clausewitz, On War, Book I", prog(t, q[1] - 0.3, 0.5) * (1 - prog(t, q[2], 0.4)), size=46)
    card(c, t, "IDEA 1", "War Serves Policy")

def magnets(c, t, a, pull):
    pts = [(640, 130), (330, 470), (950, 470)]; names = [("PASSION", "the people", RED), ("CHANCE", "army & commander", GOLD), ("REASON", "government", BLUE)]
    for (x, y), (n, s, col) in zip(pts, names):
        c.new_path(); c.set_source_rgba(*col, a); c.set_line_width(26); c.arc(x, y, 40, math.pi, 2 * math.pi); c.stroke()
        text(c, n, x, y + 50 if y < 300 else y + 85, 30, col, a, face=TITLE, bold=True, align='c'); text(c, s, x, (y + 82) if y < 300 else y + 118, 22, INK, a, italic=True, align='c')
    w = [1, 1, 1]
    if pull is None: sw = 0.35 * math.sin(t * 1.3); w = [1 + sw, 1 - sw * 0.5, 1 + math.cos(t * 1.7) * 0.35]
    else: w = pull
    tot = sum(w); ox = sum(p[0] * k for p, k in zip(pts, w)) / tot; oy = sum(p[1] * k for p, k in zip(pts, w)) / tot + 40
    for (x, y), col in zip(pts, (RED, GOLD, BLUE)):
        c.new_path(); c.set_source_rgba(*col, a * 0.5); c.set_line_width(2); c.set_dash([6, 6]); c.move_to(x, y); c.line_to(ox, oy); c.stroke(); c.set_dash([])
    c.new_path(); c.arc(ox, oy, 26, 0, 7); c.set_source_rgba(*INK, a); c.fill(); text(c, "WAR", ox, oy + 6, 16, (1, 1, 1), a, bold=True, align='c')
    return ox, oy

def s_p2(c, t, q, dur):
    parch_bg(c)
    ta = prog(t, q[0] - 0.2, 0.5) * (1 - prog(t, q[5], 0.5))
    if ta > 0:
        pts = [(640, 170), (380, 560), (900, 560)]; names = [("PASSION", "the people", RED), ("CHANCE", "army & commander", GOLD), ("REASON", "government", BLUE)]
        if t < q[4]:
            for i, ((x, y), (n, s, col)) in enumerate(zip(pts, names)):
                a = ta * prog(t, q[i + 1], 0.5)
                c.new_path(); c.arc(x, y, 70, 0, 7); c.set_source_rgba(*col, 0.15 * a); c.fill()
                text(c, n, x, y + 10, 32, col, a, face=TITLE, bold=True, align='c'); text(c, s, x, y + 100, 24, INK, a, italic=True, align='c')
            c.new_path(); c.set_source_rgba(*INK, ta * prog(t, q[3] + 1, 0.6)); c.set_line_width(3)
            c.move_to(*pts[0]); c.line_to(*pts[1]); c.line_to(*pts[2]); c.close_path(); c.stroke()
        else:
            magnets(c, t, ta * prog(t, q[4], 0.5), None)
            text(c, "“an object suspended between three magnets”", SW / 2, 595, 26, INK, ta * prog(t, q[4], 0.5), italic=True, align='c')
    va = prog(t, q[5], 0.5)
    if va > 0:
        if t < q[6]:
            pp = prog(t, q[5] + 2, 3); magnets(c, t, va * (1 - prog(t, q[6] - 0.5, 0.5)), [1 - 0.9 * pp, 1, 1 + 0.2 * pp])
            text(c, "VIETNAM  ·  Tet 1968", 1040, 230, 36, RED, va, face=TITLE, bold=True, align='c')
            text(c, "won the battles, lost the people", 1040, 270, 26, INK, va * prog(t, q[5] + 2, 0.5), italic=True, align='c')
        else:
            cam = GCam('europe2', [(q[6], 40, 51.4, 35), (dur, 40, 51.4, 34)])
            c.push_group(); f = gbase(c, cam, t)
            dot(f, 'Rostov', 1, INK, 7); label(f, 'Rostov', 1, INK, size=22); dot(f, 'Moscow', 1, RED, 8, 1, t); label(f, 'Moscow', 1, RED, size=24)
            p = prog(t, q[6] + 0.5, 4) * 0.8; pts = path_pts(f, ['Rostov', (39.2, 51.6), (38.5, 54.0), 'Moscow'])
            partial_line(c, pts, p, (0.45, 0.3, 0.15), 1, 8, arrow=True)
            x, y, _ = along(pts, p); tank(c, x, y, (0.45, 0.3, 0.15), 1, 0.9)
            text(c, "Wagner mutiny, Jun 2023", *f.S(41.0, 50.0), 28, (0.45, 0.3, 0.15), 1, bold=True, halo=H)
            c.pop_group_to_source(); c.paint_with_alpha(prog(t, q[6], 0.5))
            if t > q[6] + 5: stamp(c, "ARMY vs GOVERNMENT", 920, 300, prog(t, q[6] + 5, 0.4), RED, 34, p=prog(t, q[6] + 5, 0.4))
    text(c, "“a wonderful trinity”", SW / 2, 380, 46, INK, prog(t, q[0] - 0.2, 0.4) * (1 - prog(t, q[1], 0.4)), face=TITLE, italic=True, align='c')
    card(c, t, "IDEA 2", "The Wonderful Trinity")

def gear(c, x, y, r, ang, rgb, a, n=10):
    c.new_path(); c.save(); c.translate(x, y); c.rotate(ang)
    for i in range(n * 2):
        rr = r if i % 2 == 0 else r * 0.8; a0 = i * math.pi / n
        c.line_to(rr * math.cos(a0), rr * math.sin(a0)); c.line_to(rr * math.cos(a0 + math.pi / n), rr * math.sin(a0 + math.pi / n))
    c.close_path(); c.set_source_rgba(*rgb, a); c.fill(); c.arc(0, 0, r * 0.25, 0, 7); c.set_source_rgba(*PARCH, a); c.fill(); c.restore()

def s_p3(c, t, q, dur):
    parch_bg(c)
    ga = prog(t, q[1], 0.5) * (1 - prog(t, q[4], 0.5))
    if ga > 0:
        sl = prog(t, q[2], 6); spd = 1.4 * (1 - 0.85 * sl); ang = (t - q[1]) * spd if t < q[2] else (q[2] - q[1]) * 1.4 + (t - q[2]) * spd
        gear(c, 500, 330, 110, ang, INK, ga, 12); gear(c, 690, 330, 80, -ang * 1.37 + 0.2, (0.4, 0.3, 0.2), ga, 9)
        rnd = random.Random(3)
        for i in range(int(160 * sl)):
            c.new_path(); c.arc(rnd.uniform(400, 780), rnd.uniform(230, 440), 2.5, 0, 7); c.set_source_rgba(0.75, 0.6, 0.35, ga); c.fill()
        text(c, "FRICTION", 600, 520, 44, RED, ga, face=TITLE, bold=True, align='c')
        for i, s in enumerate(("danger", "exhaustion", "weather", "breakdowns", "error")):
            text(c, s, 1040, 220 + i * 50, 28, INK, ga * prog(t, q[2] + 0.8 * i, 0.4), italic=True, bold=True, align='c')
        fa = prog(t, q[3], 1.0)
        if fa > 0:
            rnd = random.Random(8)
            for k in range(14):
                x = (rnd.uniform(0, SW) + t * 25 * (1 + k % 3)) % (SW + 300) - 150
                g = cairo.RadialGradient(x, 330 + rnd.uniform(-200, 200), 0, x, 330, 220); g.add_color_stop_rgba(0, 0.8, 0.8, 0.8, 0.45 * fa * ga); g.add_color_stop_rgba(1, 0.8, 0.8, 0.8, 0)
                c.set_source(g); c.paint()
            quote_box(c, "A great part of the information obtained in War is contradictory, a still greater part is false.", "Clausewitz, Book I", ga * fa, y=60, size=32)
    ka = prog(t, q[4], 0.6) * (1 - prog(t, q[5], 0.6))
    if ka > 0:
        cam = GCam('europe', [(q[4], 31.0, 51.3, 7), (dur, 30.6, 51.1, 5)])
        c.push_group(); f = gbase(c, cam, t); dot(f, 'Kyiv', 1, BLUE, 9); label(f, 'Kyiv', 1, BLUE, size=26)
        pts = path_pts(f, [(30.2, 51.45), (30.25, 51.05), (30.35, 50.75)]); mv = prog(t, q[4], 3) * 0.95
        for k in range(26):
            x, y, ang = along(pts, max(0, mv - k * 0.035)); tank(c, x, y, RED, 1, 0.45)
        if t > q[4] + 3.5:
            for k in range(4):
                x, y, _ = along(pts, 0.2 + k * 0.2); explosion(c, x + 30, y, ((t - q[4]) * 0.7 + k * 0.25) % 1, 1, 26)
            text(c, "OUT OF FUEL", *f.S(30.8, 51.2), 26, RED, prog(t, q[4] + 3.5, 0.4), bold=True, halo=H)
            text(c, "~40-mile column", *f.S(28.9, 51.55), 26, RED, 1, bold=True, halo=H)
        c.pop_group_to_source(); c.paint_with_alpha(ka)
    da = prog(t, q[5], 0.5) * (1 - prog(t, q[6], 0.5))
    if da > 0:
        parch_bg(c, dark=True)
        for k in range(6):
            x, y = 200 + (k % 3) * 440, 220 + (k // 3) * 260; jam = math.sin(t * 15 + k) > 0.3
            panel(c, x - 170, y - 90, 340, 180, da, fill=(0.1, 0.12, 0.12), border=(0.5, 0.7, 0.6))
            if jam:
                rnd = random.Random(int(t * 15) + k)
                for i in range(40): c.new_path(); c.rectangle(x - 160 + rnd.uniform(0, 310), y - 80 + rnd.uniform(0, 160), 8, 3); c.set_source_rgba(0.8, 0.8, 0.8, da); c.fill()
            else: text(c, ["drone feed", "satellite", "signals", "social media", "radar", "reports"][k], x, y + 8, 26, (0.5, 1, 0.6), da, face="DejaVu Sans Mono", align='c')
        text(c, "MORE DATA, NEW FOG", SW / 2, 650 - 40, 36, (1, 0.9, 0.6), da, face=TITLE, bold=True, align='c')
    ma = prog(t, q[6], 0.5)
    if ma > 0:
        person(c, 300, 400, BLUE, ma, 1.8); text(c, "INTENT", 300, 260, 30, BLUE, ma, face=TITLE, bold=True, align='c')
        for k in range(3):
            x = 640 + k * 200; p = prog(t, q[6] + 1 + k * 0.4, 0.5); person(c, x, 420, (0.3, 0.45, 0.65), ma * p, 1.2)
            partial_line(c, [(380, 330), (x - 20, 360)], p, BLUE, ma * 0.6, 3, dash=[6, 6], arrow=True)
            partial_line(c, [(x, 470), (x + 40 * (k - 1), 580)], prog(t, q[6] + 3 + k * 0.3, 0.6), (0.2, 0.5, 0.25), ma, 5, arrow=True)
        text(c, "MISSION COMMAND", SW / 2, 640 - 30, 40, BLUE, ma * prog(t, q[6] + 2, 0.5), face=TITLE, bold=True, align='c')
    quote_box(c, "Everything is very simple in War, but the simplest thing is difficult.", "Clausewitz, Book I", prog(t, q[0] - 0.3, 0.5) * (1 - prog(t, q[1], 0.4)), size=42)
    card(c, t, "IDEA 3", "Friction and the Fog of War")

def wheel(c, t, a, hit, label_hub="CENTRE OF GRAVITY"):
    cx, cy = 640, 380; spokes = ["army", "capital", "alliance", "leader", "public opinion", "economy"]
    for i, s in enumerate(spokes):
        ang = i * math.pi / 3 - math.pi / 2; fall = hit * (1 + i * 0.1)
        x, y = cx + 220 * math.cos(ang), cy + 200 * math.sin(ang) + 200 * fall ** 2
        c.new_path(); c.set_source_rgba(*INK, a * (1 - hit)); c.set_line_width(4); c.move_to(cx, cy); c.line_to(x, y); c.stroke()
        panel(c, x - 80, y - 25, 160, 50, a * (1 - 0.6 * hit)); text(c, s, x, y + 8, 22, INK, a * (1 - 0.6 * hit), bold=True, align='c')
    c.new_path(); c.arc(cx, cy, 70, 0, 7); c.set_source_rgba(*RED, a * (1 - hit)); c.fill()
    text(c, "CoG", cx, cy + 10, 30, (1, 1, 1), a * (1 - hit), face=TITLE, bold=True, align='c')
    explosion(c, cx, cy, hit * 1.2, a, 110)

def s_p4(c, t, q, dur):
    parch_bg(c)
    wa = prog(t, q[1], 0.5) * (1 - prog(t, q[3], 0.5))
    if wa > 0:
        wheel(c, t, wa * prog(t, q[2], 0.5) if t > q[2] else 0, 0)
        if t < q[2] + 0.3:
            c.new_path(); c.arc(640, 380, 70, 0, 7); c.set_source_rgba(*RED, wa); c.fill(); text(c, "CoG", 640, 390, 30, (1, 1, 1), wa, face=TITLE, bold=True, align='c')
            for k in range(5):
                ph = ((t - q[1]) * 0.6 + k / 5) % 1; ang = k * 1.26
                partial_line(c, [(640 + 400 * math.cos(ang), 380 + 300 * math.sin(ang)), (640 + 90 * math.cos(ang), 380 + 90 * math.sin(ang))], ph, BLUE, wa, 6, arrow=True)
            text(c, "the whole weight of the attack", 640, 650 - 30, 32, BLUE, wa, italic=True, bold=True, align='c')
    ka = prog(t, q[3], 0.6) * (1 - prog(t, q[4], 0.6))
    if ka > 0:
        cam = GCam('europe2', [(q[3], 20.9, 43.75, 10.5), (dur, 20.9, 43.75, 10)])
        c.push_group(); f = gbase(c, cam, t)
        dot(f, 'Pristina', 1, INK, 7); label(f, 'Pristina', 1, INK, size=22, txt='Kosovo'); dot(f, 'Belgrade', 1, RED, 9, 1, t); label(f, 'Belgrade', 1, RED, size=26)
        rnd = random.Random(2)
        tb = q[3] + 4.5
        if t < tb:
            px, py = f.P('Pristina')
            for k in range(5): explosion(c, px + rnd.uniform(-90, 90), py + rnd.uniform(-60, 60), ((t - q[3]) * 0.6 + k / 5) % 1, 0.7, 22)
            text(c, "weeks of bombing, little effect", px, py + 80, 24, INK, prog(t, q[3] + 1, 0.5), italic=True, align='c', halo=H)
        else:
            bx, by = f.P('Belgrade')
            for k in range(7): explosion(c, bx + rnd.uniform(-120, 120), by + rnd.uniform(-80, 80), ((t - tb) * 0.8 + k / 7) % 1, 1, 30)
            text(c, "power grid · industry · leadership", bx, by + 60, 26, RED, prog(t, tb, 0.5), bold=True, align='c', halo=H)
            if t > tb + 4: stamp(c, "MILOŠEVIĆ YIELDS", 900, 560, prog(t, tb + 4, 0.4), (0.2, 0.5, 0.25), 36, p=prog(t, tb + 4, 0.4))
        year_badge(c, "1999", 1)
        c.pop_group_to_source(); c.paint_with_alpha(ka)
    ia = prog(t, q[4], 0.6) * (1 - prog(t, q[5], 0.6))
    if ia > 0:
        cam = GCam('mideast', [(q[4], 41.2, 35.4, 8), (dur, 41.2, 35.4, 7.5)])
        c.push_group(); f = gbase(c, cam, t)
        p = prog(t, q[4] + 1, 4)
        c.new_path()
        for k in range(40):
            ang = k / 40 * 6.283; r = (1 - p) * (180 + 30 * math.sin(ang * 3))
            x, y = f.S(41.0, 35.3); c.line_to(x + r * math.cos(ang) * 1.4, y + r * math.sin(ang))
        c.close_path(); c.set_source_rgba(0.1, 0.1, 0.1, 0.35); c.fill()
        for n in ('Mosul', 'Raqqa'):
            dot(f, n, 1, BLUE, 8); label(f, n, 1, BLUE, size=24)
        text(c, "“caliphate” territory", *f.S(39.5, 33.6), 26, INK, 1 - p, bold=True, halo=H)
        year_badge(c, "2017", 1)
        c.pop_group_to_source(); c.paint_with_alpha(ia)
    ba = prog(t, q[5], 0.6)
    if ba > 0:
        wheel(c, t, ba, 0)
        c.new_path(); c.set_source_rgba(*PARCH, ba); c.arc(640, 380, 72, 0, 7); c.fill()
        text(c, "Baghdad", 640, 390, 26, INK, ba, bold=True, align='c'); stamp(c, "FELL", 640, 300, prog(t, q[5] + 0.8, 0.4), RED, 30, p=prog(t, q[5] + 0.8, 0.4))
        text(c, "… but the real centre of gravity was the people's consent", SW / 2, 650 - 30, 30, RED, ba * prog(t, q[5] + 2, 0.5), italic=True, bold=True, align='c')
    quote_box(c, "the centre of power and movement, on which everything depends", "Clausewitz, Book VIII", prog(t, q[0] - 0.3, 0.5) * (1 - prog(t, q[1], 0.4)), size=42)
    card(c, t, "IDEA 4", "The Centre of Gravity")

def s_p5(c, t, q, dur):
    parch_bg(c)
    ga = prog(t, 3.6, 0.5) * (1 - prog(t, q[1], 0.5))
    if ga > 0:
        c.new_path(); c.set_source_rgba(*INK, ga); c.set_line_width(3); c.move_to(150, 560); c.line_to(1130, 560); c.move_to(150, 560); c.line_to(150, 180); c.stroke()
        text(c, "distance advanced →", 1120, 600, 22, INK, ga, italic=True, align='r'); text(c, "strength", 140, 170, 22, INK, ga, italic=True, align='l')
        p = prog(t, 4, 5); c.new_path(); c.move_to(150, 220)
        for i in range(int(100 * p) + 1):
            x = 150 + 9.8 * i; y = 220 + 0.0004 * (9.8 * i) ** 2 * 0.9 + 0.00 * i; c.line_to(x, y)
        c.set_source_rgba(*RED, ga); c.set_line_width(6); c.stroke()
        c.new_path(); c.set_dash([10, 8]); c.move_to(150, 400); c.line_to(1130, 400); c.set_source_rgba(*BLUE, ga); c.set_line_width(3); c.stroke(); c.set_dash([])
        text(c, "defender's strength", 1120, 390, 22, BLUE, ga, bold=True, align='r')
        cx = 150 + math.sqrt(180 / 0.00036); ca = prog(t, 7, 0.6) * ga
        c.new_path(); c.arc(cx, 400, 14, 0, 7); c.set_source_rgba(*GOLD, ca); c.fill()
        text(c, "CULMINATING POINT", cx, 470, 28, GOLD, ca, face=TITLE, bold=True, align='c')
    na = prog(t, q[1], 0.6) * (1 - prog(t, q[3], 0.6))
    if na > 0:
        cam = GCam('europe2', [(q[1], 30, 54.5, 20), (dur, 30, 54.5, 20)])
        c.push_group(); f = gbase(c, cam, t)
        pts = path_pts(f, ['Niemen', 'Smolensk', 'Borodino', 'Moscow']); adv = prog(t, q[1] + 1, 4)
        partial_line(c, pts, adv, (0.25, 0.25, 0.55), 1, 26)
        ret = prog(t, q[2], 6); rp = pts[::-1]
        if ret > 0:
            c.save(); c.translate(0, 30); partial_line(c, rp, ret, (0.1, 0.1, 0.1), 1, max(2, 24 * (1 - ret) + 2)); c.restore()
            rnd = random.Random(int(t * 10))
            for i in range(30): c.new_path(); c.arc(rnd.uniform(0, SW), rnd.uniform(0, SH), 2, 0, 7); c.set_source_rgba(1, 1, 1, 0.8); c.fill()
        for n in ('Niemen', 'Smolensk', 'Moscow'): dot(f, n, 1, INK, 6); label(f, n, 1, INK, size=22)
        men = int(lerp(422000, 100000, adv)) if ret <= 0 else int(lerp(100000, 10000, ret))
        panel(c, 860, 430, 360, 120, 1); text(c, f"{men:,}", 1040, 500, 52, (0.25, 0.25, 0.55) if ret <= 0 else RED, 1, face=TITLE, bold=True, align='c')
        text(c, "men in the main army", 1040, 535, 20, INK, 1, italic=True, align='c'); year_badge(c, "1812", 1)
        c.pop_group_to_source(); c.paint_with_alpha(na)
    da = prog(t, q[3], 0.5) * (1 - prog(t, q[4], 0.5))
    if da > 0:
        text(c, "DEFENCE: THE STRONGER FORM OF WAR", SW / 2, 160, 38, BLUE, da, face=TITLE, bold=True, align='c')
        for i, s in enumerate(("time", "terrain", "supplies close at hand")):
            text(c, s, 260 + i * 380, 380, 38, INK, da * prog(t, q[3] + 1 + i * 0.6, 0.4), italic=True, bold=True, align='c')
    ka = prog(t, q[4], 0.6)
    if ka > 0:
        cam = GCam('europe', [(q[4], 30.4, 51.4, 9.5), (dur, 30.4, 51.4, 9)])
        c.push_group(); f = gbase(c, cam, t); dot(f, 'Kyiv', 1, BLUE, 9); label(f, 'Kyiv', 1, BLUE, size=26)
        bx, by = f.S(29.5, 52.5); kx, ky = f.S(30.2, 50.75); p = prog(t, q[4] + 0.5, 2); r = prog(t, q[4] + 3, 2.5)
        xx, yy = lerp(bx, kx, p * (1 - r)), lerp(by, ky, p * (1 - r)); partial_line(c, [(bx, by), (xx, yy)], 1, RED, 1, 10, arrow=r <= 0)
        if r > 0: partial_line(c, [(kx, ky), (bx, by)], r, RED, 0.8, 4, dash=[10, 6], arrow=True)
        text(c, "Mar–Apr 2022: withdrawal from the north", *f.S(30.9, 51.0), 26, RED, prog(t, q[4] + 3, 0.5), bold=True, halo=H)
        c.pop_group_to_source(); c.paint_with_alpha(ka)
    card(c, t, "IDEA 5", "The Culminating Point")

def s_close(c, t, q, dur):
    parch_bg(c)
    la = prog(t, q[0], 0.5) * (1 - prog(t, q[6], 0.5))
    if la > 0:
        text(c, "CLAUSEWITZ'S LESSONS", SW / 2, 110, 46, INK, la, face=TITLE, bold=True, align='c')
        bullet_list(c, ["War serves policy: know your aim", "Balance passion, chance and reason", "Expect friction; train leaders to beat it",
                        "Find what truly holds the enemy together", "Know when to stop"], t, q[1:6], y0=200, dy=78, size=34, a=la)
    e = prog(t, q[6], 0.6)
    if e > 0:
        parch_bg(c, dark=True); c.set_source_rgba(0, 0, 0, 1 - e); c.paint()
        text(c, "“War is a mere continuation of policy by other means.”", SW / 2, 330, 40, (0.97, 0.88, 0.62), e, italic=True, align='c')
        text(c, "— Carl von Clausewitz, On War", SW / 2, 400, 28, (0.9, 0.8, 0.6), e * prog(t, q[6] + 2, 0.6), align='c')

SCENE_FN = {'open': s_open, 'p1': s_p1, 'p2': s_p2, 'p3': s_p3, 'p4': s_p4, 'p5': s_p5, 'close': s_close}
