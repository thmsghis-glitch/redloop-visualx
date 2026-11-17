"""Realistic notebook page renderer (top-down photo look)."""
import cairo, math, random, numpy as np, subprocess
from scipy.ndimage import gaussian_filter
W, H = 1080, 1350
BLACK = (0.10, 0.10, 0.12); RED = (0.84, 0.16, 0.14); BLUE = (0.12, 0.20, 0.55)

def noise(shape, sigma, seed):
    r = np.random.default_rng(seed).standard_normal(shape)
    n = gaussian_filter(r, sigma); return n / (n.std() + 1e-9)

class Page:
    grid = 0.68
    def __init__(self, seed=1, full=True):
        self.seed = seed; self.rnd = random.Random(seed); self.full = full
        # page geometry: full bleed by default, else a notebook on a desk
        self.px0, self.py0, self.px1, self.py1 = (0, 0, W, H) if full else (70, 34, 1050, 1318)
        self.ink = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); self.c = cairo.Context(self.ink)
        self.top = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); self.t = cairo.Context(self.top)  # objects above paper (post-its, tape, rings)

    # ---------- handwriting ----------
    def write(self, x, y, s, size, col=BLACK, fam="Permanent Marker", bold=False, jitter=1.0, ang=0.0, alpha=0.95, ctx=None, spacing=0.0):
        c = ctx or self.c; rnd = self.rnd
        c.save(); c.translate(x, y); c.rotate(math.radians(ang))
        c.select_font_face(fam, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
        cx = 0.0
        for ch in s:
            sz = size * (1 + rnd.uniform(-0.05, 0.05) * jitter); c.set_font_size(sz)
            adv = c.text_extents(ch).x_advance
            c.save(); c.translate(cx, rnd.uniform(-2.2, 2.2) * jitter * size / 60)
            c.rotate(math.radians(rnd.uniform(-3.5, 3.5) * jitter))
            c.set_source_rgba(*col, alpha * rnd.uniform(0.86, 1.0)); c.move_to(0, 0); c.show_text(ch); c.restore()
            cx += adv * rnd.uniform(0.97, 1.02) + spacing
        c.restore(); return cx

    def width(self, s, size, fam="Permanent Marker", bold=False):
        self.c.select_font_face(fam, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
        self.c.set_font_size(size); return self.c.text_extents(s).x_advance

    # ---------- marker strokes ----------
    def stroke(self, pts, col=RED, w=8, alpha=0.9, ctx=None, passes=2):
        c = ctx or self.c; rnd = self.rnd
        for p in range(passes):
            q = [(x + rnd.uniform(-1.5, 1.5), y + rnd.uniform(-1.5, 1.5)) for x, y in pts]
            c.set_source_rgba(*col, alpha * (0.75 if p else 1)); c.set_line_width(w * (0.85 if p else 1))
            c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
            c.new_path(); c.move_to(*q[0])
            for i in range(1, len(q) - 1):
                mx, my = (q[i][0] + q[i+1][0]) / 2, (q[i][1] + q[i+1][1]) / 2
                c.curve_to(q[i][0], q[i][1], q[i][0], q[i][1], mx, my)
            c.line_to(*q[-1]); c.stroke()

    def line(self, x0, y0, x1, y1, col=RED, w=8, bend=6, n=10, **k):
        pts = [(x0 + (x1-x0)*i/n, y0 + (y1-y0)*i/n + math.sin(i/n*math.pi)*bend + self.rnd.uniform(-1.5, 1.5)) for i in range(n+1)]
        self.stroke(pts, col, w, **k)

    def circle(self, cx, cy, rx, ry, col=RED, w=7, **k):
        a0 = self.rnd.uniform(0, 6.28); pts = []
        for i in range(46):
            t = a0 + 2.15 * math.pi * i / 45; kk = 1 + 0.07 * math.sin(i * 0.6) + self.rnd.uniform(-.015, .015)
            pts.append((cx + rx * kk * math.cos(t), cy + ry * kk * math.sin(t) + i * 0.25))
        self.stroke(pts, col, w, **k)

    def arrow(self, x0, y0, x1, y1, col=RED, w=7, bend=-30):
        self.line(x0, y0, x1, y1, col, w, bend)
        a = math.atan2(y1 - y0, x1 - x0)
        for d in (2.6, -2.5): self.line(x1, y1, x1 + 34 * math.cos(a + d), y1 + 34 * math.sin(a + d), col, w, 0, 4)

    def highlight(self, x0, y, x1, h=46, col=(1.0, 0.86, 0.25)):
        c = self.c
        for k in range(3):
            c.set_source_rgba(*col, 0.22); c.set_line_width(h * (1 - k * 0.08)); c.set_line_cap(cairo.LINE_CAP_BUTT)
            c.move_to(x0 + self.rnd.uniform(-4, 4), y + self.rnd.uniform(-3, 3)); c.line_to(x1 + self.rnd.uniform(-6, 6), y - 3 + self.rnd.uniform(-3, 3)); c.stroke()

    # ---------- objects on top ----------
    def postit(self, x, y, w, h, ang, lines, size=50, col=(0.98, 0.90, 0.48)):
        t = self.t; t.save(); t.translate(x + w/2, y + h/2); t.rotate(math.radians(ang))
        for i in range(14, 0, -1):  # soft shadow, stronger at curled corner
            t.set_source_rgba(0, 0, 0, 0.012 * (15 - i)); t.rectangle(-w/2 + 4 + i * .3, -h/2 + 8 + i * .6, w + i * .6, h + i * 1.2); t.fill()
        g = cairo.LinearGradient(0, -h/2, 0, h/2); g.add_color_stop_rgb(0, *col); g.add_color_stop_rgb(1, col[0]*.95, col[1]*.93, col[2]*.88)
        t.set_source(g); t.move_to(-w/2, -h/2); t.line_to(w/2, -h/2); t.line_to(w/2, h/2 - 24); t.curve_to(w/2 - 4, h/2 - 6, w/2 - 30, h/2, w/2 - 40, h/2); t.line_to(-w/2, h/2); t.close_path(); t.fill()
        t.set_source_rgba(1, 1, 1, .25); t.rectangle(-w/2, -h/2, w, 26); t.fill()  # glue strip sheen
        for i, l in enumerate(lines): self.write(-w/2 + 26, -h/2 + 70 + i * size * 1.12, l, size, BLACK, "Caveat", True, 0.8, 0, 0.9, ctx=t)
        t.restore()

    def tape(self, x, y, w, h, ang):
        t = self.t; rnd = self.rnd; t.save(); t.translate(x, y); t.rotate(math.radians(ang))
        t.new_path(); t.move_to(-w/2, -h/2)
        for i in range(8): t.line_to(-w/2 + w*(i+1)/8, -h/2 + rnd.uniform(-2, 2))
        for i in range(6): t.line_to(w/2 + rnd.uniform(-6, 6), -h/2 + h*(i+1)/6)
        for i in range(8): t.line_to(w/2 - w*(i+1)/8, h/2 + rnd.uniform(-2, 2))
        for i in range(6): t.line_to(-w/2 + rnd.uniform(-6, 6), h/2 - h*(i+1)/6)
        t.close_path(); t.set_source_rgba(0.95, 0.93, 0.86, 0.55); t.fill_preserve(); t.set_source_rgba(1, 1, 1, .18); t.set_line_width(2); t.stroke()
        t.restore()

    def printed_scrap(self, x, y, w, h, ang, draw, fill=(0.985, 0.98, 0.965)):
        t = self.t; t.save(); t.translate(x + w/2, y + h/2); t.rotate(math.radians(ang))
        for i in range(10, 0, -1): t.set_source_rgba(0, 0, 0, .014 * (11 - i)); t.rectangle(-w/2 + 3, -h/2 + 6 + i*.5, w + i*.4, h + i); t.fill()
        t.set_source_rgb(*fill); t.rectangle(-w/2, -h/2, w, h); t.fill()
        t.translate(-w/2, -h/2); draw(t); t.restore()

    def stamp(self, cx, cy, lines, ang=-12, size=64, col=RED):
        ss = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(ss)
        c.translate(cx, cy); c.rotate(math.radians(ang))
        c.select_font_face("Inter Display", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ws = []
        for i, (txt, sz) in enumerate(lines):
            c.set_font_size(sz); ws.append(c.text_extents(txt).x_advance + 0.18 * sz * (len(txt) - 1))
        bw = max(ws) + 70; bh = sum(sz for _, sz in lines) * 1.25 + 50
        c.set_source_rgba(*col, 0.9); c.set_line_width(7); c.rectangle(-bw/2, -bh/2, bw, bh); c.stroke()
        c.set_line_width(3); c.rectangle(-bw/2 + 11, -bh/2 + 11, bw - 22, bh - 22); c.stroke()
        y = -bh/2 + 30
        for (txt, sz), w in zip(lines, ws):
            c.set_font_size(sz); x = -w/2; y += sz * 1.05
            for ch in txt:
                c.move_to(x, y); c.show_text(ch); x += c.text_extents(ch).x_advance + 0.18 * sz
            y += sz * 0.2
        # wear: punch tiny holes
        c.identity_matrix(); c.set_operator(cairo.OPERATOR_CLEAR); rnd = random.Random(self.seed + 77)
        for _ in range(2600):
            c.arc(cx + rnd.gauss(0, bw * .45), cy + rnd.gauss(0, bh * .6), rnd.uniform(0.6, 2.6), 0, 6.3); c.fill()
        self.t.set_source_surface(ss, 0, 0); self.t.paint_with_alpha(0.88)

    # ---------- composite ----------
    def render(self, path_png, path_jpg=None):
        s = self.seed; Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
        # desk: warm dark wood-ish felt
        desk = np.zeros((H, W, 3), np.float32); base = np.array([0.20, 0.17, 0.15])
        grain = noise((H, W), 1.0, s) * 0.025 + noise((H, W), (2, 60), s + 1) * 0.03
        desk[:] = base; desk += grain[..., None]
        # page
        inpage = (X >= self.px0) & (X <= self.px1) & (Y >= self.py0) & (Y <= self.py1)
        paper = np.empty((H, W, 3), np.float32); paper[:] = np.array([0.965, 0.948, 0.905])
        fib = noise((H, W), 0.7, s + 2) * 0.012 + noise((H, W), 4, s + 3) * 0.010 + noise((H, W), 40, s + 4) * 0.012
        paper += fib[..., None]
        # printed grid (5mm squares) + margin line
        g = np.zeros((H, W), np.float32); step = 34
        gx = ((X - self.px0) % step) < 1.4; gy = ((Y - self.py0) % step) < 1.4
        g[gx | gy] = 1.0; g = gaussian_filter(g, 0.5) * (0.85 + 0.15 * noise((H, W), 30, s + 5))
        paper -= g[..., None] * np.array([0.10, 0.07, 0.03]) * 1.4 * getattr(self, 'grid', 1.0)
        margin = np.abs(X - (self.px0 + 150)) < 1.5
        paper[margin] = paper[margin] * 0.75 + np.array([0.85, 0.35, 0.35]) * 0.25
        # ink layer absorbed into paper
        ink = np.frombuffer(self.ink.get_data(), np.uint8).reshape(H, W, 4).astype(np.float32) / 255
        a = ink[..., 3:4]; rgb = np.where(a > 0, ink[..., 2::-1] / np.maximum(a, 1e-4), 0)
        absorb = np.clip(1 - 0.18 * np.abs(noise((H, W), 0.8, s + 6)), 0.6, 1)[..., None]
        a2 = gaussian_filter(a[..., 0], 0.6)[..., None] * absorb
        paper = paper * (1 - a2) + (paper * rgb) * a2  # multiply-like ink
        # page shadow on desk
        m = gaussian_filter(inpage.astype(np.float32), 14); sh = np.roll(np.roll(m, 10, 0), 8, 1)
        desk *= (1 - 0.55 * sh[..., None] * (1 - inpage[..., None]))
        img = np.where(inpage[..., None], paper, desk)
        # spiral binding: holes + rings
        if not self.full: img = self._spiral(img)
        # objects on top
        top = np.frombuffer(self.top.get_data(), np.uint8).reshape(H, W, 4).astype(np.float32) / 255
        ta = top[..., 3:4]; trgb = np.where(ta > 0, top[..., 2::-1] / np.maximum(ta, 1e-4), 0)
        img = img * (1 - ta) + trgb * ta
        # lighting: soft key light top-left, vignette, slight warmth
        light = 1.04 - 0.10 * ((X / W) * 0.6 + (Y / H) * 0.4) - 0.10 * (((X - W/2) / W) ** 2 + ((Y - H/2) / H) ** 2)
        img *= light[..., None]
        img += np.random.default_rng(s + 9).normal(0, 0.012, (H, W, 1))
        img = np.clip(img, 0, 1)
        out = (img * 255).astype(np.uint8)
        from PIL import Image; Image.fromarray(out).save(path_png)
        if path_jpg: Image.fromarray(out).save(path_jpg, quality=90)

    def _spiral(self, img):
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
        x = self.px0 + 26
        for y in range(self.py0 + 40, self.py1 - 20, 46):
            c.set_source_rgba(0.12, 0.10, 0.09, 1); c.arc(x, y, 9, 0, 2 * math.pi); c.fill()   # punched hole showing desk
            g = cairo.LinearGradient(x - 40, y - 10, x + 6, y + 6); g.add_color_stop_rgb(0, .35, .35, .37); g.add_color_stop_rgb(.5, .85, .85, .87); g.add_color_stop_rgb(1, .4, .4, .42)
            c.set_source(g); c.set_line_width(6); c.set_line_cap(cairo.LINE_CAP_ROUND)
            c.move_to(x - 2, y + 2); c.curve_to(x - 30, y - 6, x - 46, y - 2, x - 44, y + 10); c.stroke()
        a = np.frombuffer(surf.get_data(), np.uint8).reshape(H, W, 4).astype(np.float32) / 255
        aa = a[..., 3:4]; rgb = np.where(aa > 0, a[..., 2::-1] / np.maximum(aa, 1e-4), 0)
        # shading near binding
        X = np.arange(W)[None, :, None]; shade = 1 - 0.10 * np.exp(-(X - self.px0) / 60.0) * (X >= self.px0)
        img = img * shade
        return img * (1 - aa) + rgb * aa
