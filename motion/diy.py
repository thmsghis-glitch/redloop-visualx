"""Redloop DIY layer: paper, tape, scraps, marker annotations, handwriting."""
import sys, math, random, cairo, numpy as np, subprocess
sys.path.insert(0, "/home/claude/motion")
from redloop_motion import INK, RED, BG, width, text, font, loop_mark, caps, kinetic, wrap, disk, rrect
CW, CH = 1080, 1350
PAPER = (0.957, 0.937, 0.902); SCRAP = (0.99, 0.985, 0.97); POSTIT = (0.97, 0.91, 0.66)

def hand(ctx, x, y, s, size, col=RED, a=1.0, ang=0.0, fam="Caveat"):
    ctx.save(); ctx.translate(x, y); ctx.rotate(math.radians(ang))
    ctx.select_font_face(fam, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    ctx.set_source_rgba(*col, a); ctx.move_to(0, 0); ctx.show_text(s); w = ctx.text_extents(s).x_advance
    ctx.restore(); return w

def paper(ctx, seed=1):
    rnd = random.Random(seed)
    ctx.set_source_rgb(*PAPER); ctx.paint()
    ctx.set_line_width(1.2)
    for x in range(0, CW, 36):
        ctx.set_source_rgba(0.35, 0.45, 0.6, 0.07); ctx.move_to(x + .5, 0); ctx.line_to(x + .5, CH); ctx.stroke()
    for y in range(0, CH, 36):
        ctx.set_source_rgba(0.35, 0.45, 0.6, 0.07); ctx.move_to(0, y + .5); ctx.line_to(CW, y + .5); ctx.stroke()
    for _ in range(5):  # faint stains
        cx, cy, r = rnd.uniform(0, CW), rnd.uniform(0, CH), rnd.uniform(120, 300)
        g = cairo.RadialGradient(cx, cy, 0, cx, cy, r); g.add_color_stop_rgba(0, .55, .45, .3, .035); g.add_color_stop_rgba(1, .55, .45, .3, 0)
        ctx.set_source(g); ctx.paint()

def tape(ctx, x, y, w, h, ang, seed=0):
    rnd = random.Random(seed); ctx.save(); ctx.translate(x, y); ctx.rotate(math.radians(ang))
    ctx.new_path(); ctx.move_to(-w/2, -h/2)
    for i in range(7): ctx.line_to(-w/2 + w * (i + 1) / 7, -h/2 + rnd.uniform(-3, 3))
    for i in range(6): ctx.line_to(w/2 + rnd.uniform(-5, 5), -h/2 + h * (i + 1) / 6)
    for i in range(7): ctx.line_to(w/2 - w * (i + 1) / 7, h/2 + rnd.uniform(-3, 3))
    for i in range(6): ctx.line_to(-w/2 + rnd.uniform(-5, 5), h/2 - h * (i + 1) / 6)
    ctx.close_path(); ctx.set_source_rgba(0.93, 0.89, 0.78, 0.78); ctx.fill_preserve()
    ctx.set_source_rgba(0.6, 0.55, 0.45, 0.25); ctx.set_line_width(1); ctx.stroke(); ctx.restore()

def scrap(ctx, x, y, w, h, ang, color=SCRAP, seed=0, torn=True):
    rnd = random.Random(seed); ctx.save(); ctx.translate(x + w/2, y + h/2); ctx.rotate(math.radians(ang))
    def path(dx=0, dy=0):
        ctx.new_path(); ctx.move_to(-w/2 + dx, -h/2 + dy); ctx.line_to(w/2 + dx, -h/2 + dy); ctx.line_to(w/2 + dx, h/2 + dy)
        n = 28
        for i in range(n): ctx.line_to(w/2 - w * (i + 1) / n + dx, h/2 + dy + (rnd.uniform(-7, 5) if torn else 0))
        ctx.close_path()
    st = rnd.getstate()
    path(6, 10); ctx.set_source_rgba(0, 0, 0, 0.10); ctx.fill()
    rnd.setstate(st); path(); ctx.set_source_rgb(*color); ctx.fill()
    ctx.restore()

def wobble_pts(pts, amp, seed):
    rnd = random.Random(seed); return [(x + rnd.uniform(-amp, amp), y + rnd.uniform(-amp, amp)) for x, y in pts]

def stroke_smooth(ctx, pts, col=RED, w=7, a=0.92):
    ctx.set_source_rgba(*col, a); ctx.set_line_width(w); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.new_path(); ctx.move_to(*pts[0])
    for i in range(1, len(pts) - 1):
        mx, my = (pts[i][0] + pts[i+1][0]) / 2, (pts[i][1] + pts[i+1][1]) / 2
        ctx.curve_to(pts[i][0], pts[i][1], pts[i][0], pts[i][1], mx, my)
    ctx.line_to(*pts[-1]); ctx.stroke()

def marker_circle(ctx, cx, cy, rx, ry, seed=0, col=RED, w=7):
    rnd = random.Random(seed); pts = []; turns = 1.12; n = 40; a0 = rnd.uniform(0, 6.28)
    for i in range(n + 1):
        t = a0 + turns * 2 * math.pi * i / n; k = 1 + 0.06 * math.sin(i * 0.7 + seed) + rnd.uniform(-.02, .02)
        pts.append((cx + rx * k * math.cos(t), cy + ry * k * math.sin(t) * (1 + 0.04 * i / n)))
    stroke_smooth(ctx, pts, col, w)

def marker_line(ctx, x0, y0, x1, y1, seed=0, col=RED, w=7, bend=10):
    n = 8; pts = [(x0 + (x1-x0)*i/n, y0 + (y1-y0)*i/n + math.sin(i/n*math.pi) * bend) for i in range(n + 1)]
    stroke_smooth(ctx, wobble_pts(pts, 2.5, seed), col, w)

def marker_arrow(ctx, x0, y0, x1, y1, seed=0, col=RED, w=7, bend=-40):
    marker_line(ctx, x0, y0, x1, y1, seed, col, w, bend)
    ang = math.atan2(y1 - y0 - 0, x1 - x0); L = 30
    for d in (2.55, -2.55):
        marker_line(ctx, x1, y1, x1 + L * math.cos(ang + d), y1 + L * math.sin(ang + d), seed + 3, col, w, 0)

def strike(ctx, x0, x1, y, seed=0, col=RED, w=8):
    marker_line(ctx, x0 - 8, y + 6, x1 + 8, y - 4, seed, col, w, 4)

def header(ctx, ep, total, label, seed=0):
    loop_mark(ctx, 120, 128, 26, 8); caps(ctx, 170, 140, "REDLOOP", 26, INK)
    hand(ctx, CW - 300, 145, f"épisode {ep:02d} / {total:02d}", 46, INK, .75, -2)
    hand(ctx, 96, 222, label, 40, RED, 1, -1.5)

def finish(surf, path_png, path_jpg=None, seed=0):
    rng = np.random.default_rng(seed)
    a = np.frombuffer(surf.get_data(), np.uint8).reshape(CH, CW, 4).astype(np.int16)
    a[..., :3] += rng.normal(0, 5, (CH, CW, 1)).astype(np.int16)
    out = np.clip(a, 0, 255).astype(np.uint8)
    s2 = cairo.ImageSurface.create_for_data(bytearray(out.tobytes()), cairo.FORMAT_ARGB32, CW, CH); s2.write_to_png(path_png)
    if path_jpg: subprocess.run(["convert", path_png, "-quality", "90", path_jpg], check=True)
