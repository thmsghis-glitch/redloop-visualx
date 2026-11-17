import sys, math, subprocess; sys.path.insert(0, "/home/claude/motion")
from diy import *
from carousel_erreurs import fit, MAXW
from redloop_motion import MX, WHITE, PAPER as CARD

def base(ep, total, seed):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, CW, CH); c = cairo.Context(s); paper(c, seed)
    loop_mark(c, 120, 128, 26, 8); caps(c, 170, 140, "REDLOOP", 26, INK)
    hand(c, CW - 290, 146, f"épisode {ep:02d} / {total:02d}", 46, INK, .75, -2)
    return s, c

def label(c, s, y=300, ang=-1.5): hand(c, MX, y, s, 50, RED, 1, ang)

def title(c, lines, y, size=118, ang=-1.0):
    sz = fit(c, lines, size); c.save(); c.translate(MX, y); c.rotate(math.radians(ang))
    kinetic(c, 99, lines, 0, 0, sz); c.restore(); return y + (len(lines) - 1) * sz * 1.08

def sub_scrap(c, txt, y, ang=1.2, seed=0, fs=42):
    lines = wrap(c, txt, fs, MAXW - 120, "text"); h = 70 + len(lines) * fs * 1.4
    scrap(c, MX - 10, y, MAXW - 40, h, ang, SCRAP, seed)
    tape(c, MX + 60, y + 4, 130, 44, -12, seed + 1)
    c.save(); c.translate(MX + 40, y + 70); c.rotate(math.radians(ang))
    for i, l in enumerate(lines): text(c, 0, i * fs * 1.4, l, fs, INK, .85, "text", 0)
    c.restore(); return y + h

def postit(c, x, y, lines, ang=3, w=380, fs=44, seed=0):
    h = 60 + len(lines) * fs * 1.15; scrap(c, x, y, w, h, ang, POSTIT, seed, torn=False)
    for i, l in enumerate(lines): hand(c, x + 30, y + 62 + i * fs * 1.15, l, fs, INK, .9, ang)

def footer(c, last, day):
    hand(c, MX, 1268, f"jour {day:02d}", 44, INK, .7, -2)
    if not last:
        w = hand(c, CW - MX - 190, 1268, "glisse", 46, RED, 1, -2)
        x0 = CW - MX - 180 + w; marker_line(c, x0, 1252, x0 + 70, 1248, 2, RED, 6, 0)
        marker_line(c, x0 + 48, 1230, x0 + 72, 1248, 3, RED, 6, 0); marker_line(c, x0 + 48, 1268, x0 + 72, 1248, 4, RED, 6, 0)

def checkbox(c, x, y, seed):
    pts = wobble_pts([(x, y), (x + 40, y - 2), (x + 42, y + 40), (x + 1, y + 42), (x, y)], 2, seed)
    stroke_smooth(c, pts, INK, 4, .8)
    stroke_smooth(c, wobble_pts([(x + 6, y + 20), (x + 18, y + 36), (x + 52, y - 12)], 2, seed + 1), RED, 7)

def check_list(c, items, y, seed=0, fs=40):
    rows = [wrap(c, it, fs, MAXW - 190, "medium") for it in items]
    h = 70 + sum(len(r) * fs * 1.35 + 34 for r in rows)
    scrap(c, MX - 10, y, MAXW - 20, h, -1, SCRAP, seed); tape(c, CW / 2, y + 2, 170, 46, 4, seed + 2)
    yy = y + 80
    for i, r in enumerate(rows):
        checkbox(c, MX + 30, yy - 34, seed + i * 7)
        for j, l in enumerate(r): text(c, MX + 110, yy + j * fs * 1.35, l, fs, INK, 1, "medium", 0)
        yy += len(r) * fs * 1.35 + 34
    return y + h

def num_list(c, items, y, seed=0, fs=40):
    rows = [wrap(c, it, fs, MAXW - 190, "medium") for it in items]
    h = 70 + sum(len(r) * fs * 1.35 + 30 for r in rows)
    scrap(c, MX - 10, y, MAXW - 20, h, 1, SCRAP, seed); tape(c, MX + 80, y + 2, 150, 44, -10, seed + 2)
    yy = y + 80
    for i, r in enumerate(rows):
        marker_circle(c, MX + 52, yy - 14, 26, 26, seed + i, RED, 5)
        hand(c, MX + 40, yy + 2, str(i + 1), 46, RED, 1, 0)
        for j, l in enumerate(r): text(c, MX + 110, yy + j * fs * 1.35, l, fs, INK, 1, "medium", 0)
        yy += len(r) * fs * 1.35 + 30
    return y + h

def promise(c, x, y, txt, ang, seed):
    font(c, 40, "bold"); w = width(c, txt, 40, "bold", 0) + 70
    scrap(c, x, y, w, 96, ang, INK, seed, torn=False)
    c.save(); c.translate(x + w / 2, y + 48); c.rotate(math.radians(ang))
    text(c, -w / 2 + 35, 14, txt, 40, (0.88, 0.76, 0.45), 1, "bold", 0)
    strike(c, -w / 2 + 25, w / 2 - 25, 0, seed, RED, 9); c.restore()
    tape(c, x + 10, y + 10, 80, 34, -35, seed + 5)
    return w

def save(s, name, seed):
    finish(s, f"/home/claude/motion/out/diy/{name}.png", f"/home/claude/redloop-visualx/posts/{name}.jpg", seed)
