import sys, math; sys.path.insert(0, "/home/claude/motion")
from notebook import *
L = 205; MAXW = 1080 - L - 60
GOLD = (0.88, 0.76, 0.45); CREAM = (0.97, 0.95, 0.90); GREY = (0.35, 0.35, 0.38)

def header(p, label):
    pts = [(L + 22 + 22*math.cos(math.radians(a)), 112 + 22*math.sin(math.radians(a))) for a in range(-40, -340, -12)]
    p.stroke(pts, RED, 6); p.c.set_source_rgba(*BLACK, .9); p.c.arc(L + 22 + 29*math.cos(math.radians(-58)), 112 + 29*math.sin(math.radians(-58)), 5, 0, 6.3); p.c.fill()
    w = p.width(label, 42, "Caveat", True); p.write(1080 - 60 - w, 124, label, 42, BLUE, "Caveat", True, .8, -1.5)

def handle(p, txt="@redloopx"):
    p.write(L, 1288, txt, 46, BLUE, "Caveat", True, .9, -2)

def glisse(p):
    w2 = p.write(860, 1288, "glisse", 46, RED, "Caveat", True, .8, -2)
    p.line(860 + w2 + 10, 1272, 860 + w2 + 60, 1268, RED, 5, 0); p.line(860 + w2 + 42, 1254, 860 + w2 + 62, 1268, RED, 5, 0, 4); p.line(860 + w2 + 42, 1284, 860 + w2 + 62, 1268, RED, 5, 0, 4)

def title(p, lines, y, size=110, gap=1.12, maxw=MAXW):
    """lines: list of (text, colour). Auto-shrinks to fit; returns (y_after, widths)."""
    sz = size
    while max(p.width(t, sz) for t, _ in lines) > maxw and sz > 50: sz -= 4
    ws = []
    for i, (t, col) in enumerate(lines):
        ws.append(p.write(L, y + i * sz * gap, t, sz, col, ang=p.rnd.uniform(-2, -0.6)))
    return y + (len(lines) - 1) * sz * gap, ws, sz

def note(p, lines, y, size=56, col=BLUE, x=L, gap=1.15, bold=True):
    for i, t in enumerate(lines): p.write(x, y + i * size * gap, t, size, col, "Caveat", bold, 1.0, -1.2)
    return y + (len(lines) - 1) * size * gap

def under(p, y, w, col=RED, twice=False):
    p.line(L, y, L + w, y - 12, col, 7, 4)
    if twice: p.line(L + 20, y + 22, L + w - 30, y + 10, col, 5, 3)

def ad(p, x, y, w, h, ang, kicker, big, small):
    def f(t):
        p.write(36, 60, kicker, 28, GOLD, "Inter Display", True, 0, 0, 1, ctx=t, spacing=4)
        p.write(36, 60 + 0.9 * h * 0.42, big, int(h * 0.27), CREAM, "Inter Display", True, 0, 0, 1, ctx=t)
        p.write(36, h - 36, small, 30, CREAM, "Inter", False, 0, 0, .75, ctx=t)
    p.printed_scrap(x, y, w, h, ang, f, fill=(0.09, 0.09, 0.10))
