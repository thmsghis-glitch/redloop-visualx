"""Redloop motion identity: shared engine for every Redloop reel."""
import cairo, math, subprocess, os, numpy as np, wave

W, H, FPS = 1080, 1920, 30
BG = (0xF4/255, 0xEF/255, 0xE8/255)
INK = (0x14/255, 0x16/255, 0x1B/255)
RED = (0xE5/255, 0x32/255, 0x2D/255)
WHITE = (1, 1, 1)
FONT = "Poppins"
MX = 90                 # left margin
LOGO_C = (128, 214)     # mini logo centre
WIPE = 0.42             # wipe duration (s)

# ---------- easing ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, start, dur): return clamp((t - start) / dur) if dur > 0 else float(t >= start)
def out_cubic(x): return 1 - (1 - x) ** 3
def out_expo(x): return 1 if x >= 1 else 1 - 2 ** (-10 * x)
def in_out_cubic(x): return 4*x*x*x if x < .5 else 1 - (-2*x + 2) ** 3 / 2
def out_back(x, s=1.7): x -= 1; return 1 + (s + 1) * x**3 + s * x**2

# ---------- primitives ----------
def font(ctx, size, bold=True):
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)

def tw(ctx, s): return ctx.text_extents(s).x_advance

def text(ctx, x, y, s, size, col=INK, a=1, bold=True, spacing=0):
    font(ctx, size, bold); ctx.set_source_rgba(*col, a)
    if spacing:
        for ch in s:
            ctx.move_to(x, y); ctx.show_text(ch); x += tw(ctx, ch) + spacing
        return x
    ctx.move_to(x, y); ctx.show_text(s); return x + tw(ctx, s)

def loop_mark(ctx, cx, cy, r, lw, p=1.0, dot=1.0, col=RED, dotcol=INK):
    """Signature loop: open arc + escaping dot. p = draw progress, dot = dot scale."""
    a0 = math.radians(-40); sweep = math.radians(300)
    if p > 0:
        ctx.set_line_width(lw); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_source_rgb(*col)
        ctx.new_path(); ctx.arc_negative(cx, cy, r, a0, a0 - sweep * p); ctx.stroke()
    if dot > 0:
        ang = math.radians(-58); dr = r * 1.32
        ctx.set_source_rgb(*dotcol); ctx.new_path()
        ctx.arc(cx + dr * math.cos(ang), cy + dr * math.sin(ang), lw * 0.75 * dot, 0, 2*math.pi); ctx.fill()

def rrect(ctx, x, y, w, h, r):
    ctx.new_path(); ctx.arc(x+w-r, y+r, r, -math.pi/2, 0); ctx.arc(x+w-r, y+h-r, r, 0, math.pi/2)
    ctx.arc(x+r, y+h-r, r, math.pi/2, math.pi); ctx.arc(x+r, y+r, r, math.pi, 1.5*math.pi); ctx.close_path()

# ---------- persistent layers ----------
def background(ctx, T):
    ctx.set_source_rgb(*BG); ctx.paint()
    # slow rotating echo of the loop, bottom right
    ctx.save(); ctx.translate(980, 1640); ctx.rotate(T * 0.25)
    ctx.set_source_rgba(*INK, 0.045); ctx.set_line_width(70); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.new_path(); ctx.arc(0, 0, 470, 0, math.radians(300)); ctx.stroke(); ctx.restore()

def hud(ctx, T, total, day, a=1):
    loop_mark(ctx, *LOGO_C, 30, 10)
    text(ctx, 182, 228, "REDLOOP", 30, INK, a, True, 3)
    # day pill
    label = f"JOUR {day:02d}"; font(ctx, 28); w = tw(ctx, label) + 44 + 2*len(label)
    rrect(ctx, W - MX - w, 182, w, 60, 30); ctx.set_source_rgba(*INK, a); ctx.fill()
    text(ctx, W - MX - w + 22, 223, label, 28, BG, a, True, 2)
    # global progress (the "loop timer")
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_width(8)
    ctx.set_source_rgba(*INK, 0.12); ctx.move_to(MX, 300); ctx.line_to(W - MX, 300); ctx.stroke()
    ctx.set_source_rgb(*RED); ctx.move_to(MX, 300); ctx.line_to(MX + (W - 2*MX) * clamp(T / total), 300); ctx.stroke()

def wipe_in(ctx, t):
    """Red disk shrinks back into the logo dot."""
    p = prog(t, 0, WIPE)
    if p >= 1: return
    r = 2400 * (1 - in_out_cubic(p))
    ctx.set_source_rgb(*RED); ctx.new_path(); ctx.arc(*LOGO_C, r, 0, 2*math.pi); ctx.fill()

def wipe_out(ctx, t, dur):
    """Red disk grows from the centre-bottom to fill the frame."""
    p = prog(t, dur - WIPE, WIPE)
    if p <= 0: return
    r = 2400 * in_out_cubic(p)
    ctx.set_source_rgb(*RED); ctx.new_path(); ctx.arc(W/2, 1150, r, 0, 2*math.pi); ctx.fill()

# ---------- kinetic text ----------
def kinetic(ctx, t, lines, x, y, size, start=0.0, stagger=0.07, lh=1.16, col=INK):
    """lines: list of strings; *word* = red highlight with drawn underline."""
    font(ctx, size); space = tw(ctx, " "); k = 0; marks = []
    for li, line in enumerate(lines):
        cx = x; ly = y + li * size * lh
        for raw in line.split(" "):
            hl = raw.startswith("*"); word = raw.strip("*").replace("~", " ")
            p = out_cubic(prog(t, start + k * stagger, 0.5))
            font(ctx, size); w = tw(ctx, word)
            if p > 0:
                ctx.save(); ctx.rectangle(cx - 20, ly - size * 1.05, w + 40, size * 1.35); ctx.clip()
                text(ctx, cx, ly + (1 - p) * size * 0.9, word, size, RED if hl else col, 1)
                ctx.restore()
            if hl:
                if marks and marks[-1][4] == (li, k - 1): marks[-1] = (marks[-1][0], cx + w, ly, marks[-1][3], (li, k))
                else: marks.append((cx, cx + w, ly, start + k * stagger + 0.35, (li, k)))
            cx += w + space; k += 1
    for (x0, x1, ly, s, _) in marks:   # hand-drawn underline
        p = out_expo(prog(t, s, 0.45))
        if p > 0:
            ctx.set_source_rgb(*RED); ctx.set_line_width(size * 0.09); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.new_path(); ctx.move_to(x0, ly + size * 0.2)
            ctx.curve_to(x0 + (x1-x0)*.3, ly + size*.28, x0 + (x1-x0)*.7, ly + size*.12, x0 + (x1 - x0) * p, ly + size * 0.2)
            ctx.stroke()
    return start + k * stagger + 0.5

def tag(ctx, t, s, x, y, start=0.0, col=RED):
    n = int(clamp((t - start) / 0.025, 0, len(s)))
    if n: text(ctx, x, y, s[:n], 32, col, 1, True, 6)

def wrap(ctx, s, size, maxw, bold=True):
    font(ctx, size, bold); out = []; cur = ""
    for w in s.split():
        test = (cur + " " + w).strip()
        if tw(ctx, test) > maxw and cur: out.append(cur); cur = w
        else: cur = test
    out.append(cur); return out

# ---------- scene renderer ----------
def render_scene(path, dur, draw, T0, total, day, hud_on=True, wipe=(True, True)):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf)
    ctx.set_antialias(cairo.ANTIALIAS_BEST)
    tmp = path[:-4] + ".part.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                          "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    n = round(dur * FPS)
    for f in range(n):
        t = f / FPS; T = T0 + t
        ctx.save(); background(ctx, T)
        if hud_on: hud(ctx, T, total, day)
        draw(ctx, t, dur); ctx.restore()
        if wipe[1]: wipe_out(ctx, t, dur)
        if wipe[0]: wipe_in(ctx, t)
        surf.flush(); p.stdin.write(bytes(surf.get_data()))
    p.stdin.close()
    if p.wait() != 0: raise RuntimeError("ffmpeg failed: " + path)
    os.replace(tmp, path)

def still(path, dur_t, draw, T, total, day, hud_on=True):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf)
    background(ctx, T)
    if hud_on: hud(ctx, T, total, day)
    draw(ctx, dur_t, 99); surf.write_to_png(path)

# ---------- signature intro ----------
def intro(ctx, t, dur):
    p = in_out_cubic(prog(t, 0.0, 0.6)); d = out_back(prog(t, 0.5, 0.35), 2.4)
    loop_mark(ctx, W/2, 860, 190, 52, p, d)
    a = out_cubic(prog(t, 0.55, 0.35))
    font(ctx, 64); s = "REDLOOP"; w = sum(tw(ctx, c) + 14 for c in s) - 14
    text(ctx, W/2 - w/2, 1200 + (1 - a) * 30, s, 64, INK, a, True, 14)
    a2 = out_cubic(prog(t, 0.75, 0.35)); font(ctx, 34, False); s2 = "Une IA fait grandir ce compte"
    text(ctx, W/2 - tw(ctx, s2)/2, 1268, s2, 34, INK, 0.6 * a2, False)

# ---------- audio ----------
def soundtrack(path, total, cuts, bpm=100, sr=44100):
    n = int(total * sr); t = np.arange(n) / sr; out = np.zeros(n)
    beat = 60 / bpm
    def add(sig, at):
        i = int(at * sr); j = min(n, i + len(sig))
        if i < n: out[i:j] += sig[:j - i]
    kt = np.arange(int(0.35 * sr)) / sr
    kick = np.sin(2*np.pi*np.cumsum(45 + 90*np.exp(-kt*28))/sr) * np.exp(-kt*9) * 0.9
    rng = np.random.default_rng(1)
    ht = np.arange(int(0.05 * sr)) / sr
    hat = np.diff(rng.standard_normal(len(ht) + 1)) * np.exp(-ht * 90) * 0.12
    b = 1.1  # music starts after the intro sting
    while b < total - 0.2:
        add(kick, b); add(hat, b + beat/2); b += beat
    # pad: Am9 soft chord
    env = np.clip(t / 1.5, 0, 1) * np.clip((total - t) / 1.2, 0, 1)
    for f in (110, 164.8, 196, 246.9, 261.6):
        out += 0.035 * np.sin(2*np.pi*f*t) * (0.8 + 0.2*np.sin(2*np.pi*0.2*t + f)) * env
    # whoosh on each cut
    wt = np.arange(int(0.5 * sr)) / sr
    noise = rng.standard_normal(len(wt))
    k = 60; noise = np.convolve(noise, np.ones(k)/k, mode="same") * 6
    sw = noise * np.sin(np.pi * wt / wt[-1]) ** 2 * 0.22
    for c in cuts: add(sw, max(0, c - 0.3))
    # intro sting: rising tone + pop
    st = np.arange(int(0.9*sr))/sr
    add(np.sin(2*np.pi*np.cumsum(300 + 500*st)/sr) * np.sin(np.pi*st/st[-1])**2 * 0.18, 0.05)
    pt = np.arange(int(0.12*sr))/sr
    add(np.sin(2*np.pi*880*pt) * np.exp(-pt*40) * 0.35, 0.68)
    out = out / max(1e-6, np.abs(out).max()) * 0.8
    pcm = (np.repeat(out[:, None], 2, axis=1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())

def assemble(scene_files, audio, out):
    lst = out + ".txt"
    with open(lst, "w") as f:
        for s in scene_files: f.write(f"file '{os.path.abspath(s)}'\n")
    tmp_v = out[:-4] + ".v.mp4"; tmp = out[:-4] + ".part.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", tmp_v], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp_v, "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, out); os.remove(tmp_v)
