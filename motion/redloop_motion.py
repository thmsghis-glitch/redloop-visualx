"""Redloop motion identity v2 — shared engine for every Redloop reel.
Type: Inter Display ExtraBold (titres) + Lora Bold Italic (mots accent, rouge) + Inter (texte).
Palette: crème #F4EFE8, encre #14161B, rouge #E5322D. Signature: la boucle ouverte + le point."""
import cairo, math, subprocess, os, numpy as np, wave

W, H, FPS = 1080, 1920, 30
BG = (0xF4/255, 0xEF/255, 0xE8/255); INK = (0x14/255, 0x16/255, 0x1B/255)
RED = (0xE5/255, 0x32/255, 0x2D/255); WHITE = (1, 1, 1); PAPER = (0xFB/255, 0xF8/255, 0xF4/255)
DISPLAY = "Inter Display ExtraBold"; TEXT = "Inter"; ACCENT = "Lora"
MX = 96; LOGO_C = (126, 214); WIPE = 0.48
SUB = 4          # motion-blur sub-frames
GRAIN = 0.014

# ---------- easing ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, s, d): return clamp((t - s) / d) if d > 0 else float(t >= s)
def out_cubic(x): return 1 - (1 - x) ** 3
def out_quint(x): return 1 - (1 - x) ** 5
def out_expo(x): return 1 if x >= 1 else 1 - 2 ** (-10 * x)
def in_out_cubic(x): return 4*x*x*x if x < .5 else 1 - (-2*x + 2) ** 3 / 2
def in_out_quint(x): return 16*x**5 if x < .5 else 1 - (-2*x + 2) ** 5 / 2
def out_back(x, s=1.4): x -= 1; return 1 + (s + 1) * x**3 + s * x**2

# ---------- type ----------
STYLES = {"display": (DISPLAY, 0, 0), "accent": (ACCENT, 1, 1), "text": (TEXT, 0, 0),
          "medium": ("Inter", 0, 1), "bold": ("Inter Display", 0, 1)}
def font(ctx, size, style="display"):
    fam, it, bd = STYLES[style]
    ctx.select_font_face(fam, cairo.FONT_SLANT_ITALIC if it else cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if bd else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
def track_for(style, size): return -0.025 * size if style == "display" else (0.0 if style != "caps" else 0)
def glyphs(ctx, x, y, s, track):
    g = ctx.get_scaled_font().text_to_glyphs(x, y, s, False)
    return [(gl[0], gl[1] + i * track, gl[2]) for i, gl in enumerate(g)]
def tw(ctx, s, track=0.0): return ctx.text_extents(s).x_advance + track * max(0, len(s) - 1)
def text(ctx, x, y, s, size, col=INK, a=1.0, style="display", track=None):
    font(ctx, size, style); tr = track_for(style, size) if track is None else track
    ctx.set_source_rgba(*col, a); ctx.show_glyphs(glyphs(ctx, x, y, s, tr)); return x + tw(ctx, s, tr)
def caps(ctx, x, y, s, size=30, col=RED, a=1.0, n=None):
    s = s if n is None else s[:n]; return text(ctx, x, y, s, size, col, a, "bold", size * 0.2)
def width(ctx, s, size, style="display", track=None):
    font(ctx, size, style); return tw(ctx, s, track_for(style, size) if track is None else track)
def wrap(ctx, s, size, maxw, style="text"):
    out, cur = [], ""
    for w in s.split():
        t2 = (cur + " " + w).strip()
        if width(ctx, t2, size, style) > maxw and cur: out.append(cur); cur = w
        else: cur = t2
    out.append(cur); return out

# ---------- shapes ----------
def rrect(ctx, x, y, w, h, r):
    ctx.new_path(); ctx.arc(x+w-r, y+r, r, -math.pi/2, 0); ctx.arc(x+w-r, y+h-r, r, 0, math.pi/2)
    ctx.arc(x+r, y+h-r, r, math.pi/2, math.pi); ctx.arc(x+r, y+r, r, math.pi, 1.5*math.pi); ctx.close_path()
def soft_shadow(ctx, x, y, w, h, r, a=1.0, spread=36, strength=0.10):
    for i in range(10, 0, -1):
        k = i / 10; rrect(ctx, x - spread*k*0.5, y + spread*0.45 - spread*k*0.3, w + spread*k, h + spread*k, r + spread*k*0.5)
        ctx.set_source_rgba(*INK, strength * a * (1 - k) ** 2 * 0.35); ctx.fill()
def disk(ctx, cx, cy, r, col, a=1.0):
    if r <= 0: return
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 2*math.pi); ctx.set_source_rgba(*col, a); ctx.fill()
def loop_mark(ctx, cx, cy, r, lw, p=1.0, dot=1.0, col=RED, dotcol=INK, rot=0.0):
    a0 = math.radians(-40) + rot; sweep = math.radians(300)
    if p > 0:
        ctx.set_line_width(lw); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_source_rgb(*col)
        ctx.new_path(); ctx.arc_negative(cx, cy, r, a0, a0 - sweep * p); ctx.stroke()
    if dot > 0:
        ang = math.radians(-58) + rot; dr = r * 1.32
        disk(ctx, cx + dr*math.cos(ang), cy + dr*math.sin(ang), lw * 0.75 * dot, dotcol)

# ---------- persistent layers ----------
def background(ctx, T):
    ctx.set_source_rgb(*BG); ctx.paint()
    ctx.save(); ctx.translate(1010, 1660); ctx.rotate(T * 0.22)
    ctx.set_source_rgba(*INK, 0.04); ctx.set_line_width(64); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.new_path(); ctx.arc(0, 0, 480, 0, math.radians(300)); ctx.stroke(); ctx.restore()
def hud(ctx, T, total, day):
    loop_mark(ctx, *LOGO_C, 28, 9, rot=math.sin(T * 1.3) * 0.08)
    caps(ctx, 178, 226, "REDLOOP", 28, INK)
    label = f"JOUR {day:02d}"; w = width(ctx, label, 26, "bold", 26 * .2) + 70
    rrect(ctx, W - MX - w, 184, w, 58, 29); ctx.set_source_rgb(*INK); ctx.fill()
    disk(ctx, W - MX - w + 26, 213, 7 + 1.5 * math.sin(T * 5), RED)
    caps(ctx, W - MX - w + 44, 222, label, 26, BG)
    y = 298; x1 = MX + (W - 2*MX) * clamp(T / total)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_width(6)
    ctx.set_source_rgba(*INK, 0.10); ctx.move_to(MX, y); ctx.line_to(W - MX, y); ctx.stroke()
    ctx.set_source_rgb(*RED); ctx.move_to(MX, y); ctx.line_to(x1, y); ctx.stroke(); disk(ctx, x1, y, 9, RED)

def wipe_in(ctx, t):
    p1 = in_out_quint(prog(t, 0.0, WIPE * 0.75)); p2 = in_out_quint(prog(t, WIPE * 0.25, WIPE * 0.75))
    if p2 >= 1: return
    disk(ctx, *LOGO_C, 2500 * (1 - p2), RED); disk(ctx, *LOGO_C, 2500 * (1 - p1), INK)
def wipe_out(ctx, t, dur):
    p1 = in_out_quint(prog(t, dur - WIPE, WIPE * 0.75)); p2 = in_out_quint(prog(t, dur - WIPE * 0.75, WIPE * 0.75))
    if p1 <= 0: return
    disk(ctx, W/2, 1240, 2500 * p1, RED); disk(ctx, W/2, 1240, 2500 * p2, INK)

# ---------- kinetic headline ----------
def kinetic(ctx, t, lines, x, y, size, start=0.0, stagger=0.065, lh=1.08, col=INK):
    """*mot* = accent : Lora gras italique, rouge."""
    k = 0
    for li, line in enumerate(lines):
        cx = x; ly = y + li * size * lh
        for raw in line.split(" "):
            acc = raw.startswith("*"); word = raw.replace("*", "").replace("~", " ")
            style = "accent" if acc else "display"; sz = size * (1.06 if acc else 1)
            w = width(ctx, word, sz, style)
            p = prog(t, start + k * stagger, 0.6); e = out_back(p, 1.25) if p < 1 else 1
            if p > 0:
                ctx.save(); ctx.rectangle(cx - 30, ly - size * 1.0, w + 60, size * 1.32); ctx.clip()
                ctx.translate(cx, ly + (1 - e) * size * 1.05); ctx.rotate((1 - out_cubic(p)) * 0.12)
                text(ctx, 0, 0, word, sz, RED if acc else col, 1, style); ctx.restore()
            cx += w + width(ctx, " ", size, "display", 0) * 0.9; k += 1
    return start + k * stagger + 0.6

# ---------- scene rendering (motion blur + grain + push-in) ----------
_grain = None
def grain(i):
    global _grain
    if _grain is None:
        rng = np.random.default_rng(7)
        _grain = [(rng.standard_normal((H // 2, W // 2)) * 255 * GRAIN).repeat(2, 0).repeat(2, 1)[..., None] for _ in range(6)]
    return _grain[i % 6]

OUT, IN = 0.42, 0.32
def compose(ctx, T, t, dur, draw, total, day, hud_on, wipes, hud_in=False):
    """Soft transitions: the scene drifts up and dissolves, the next one rises in.
    The background and the header never move, so the cut feels continuous."""
    background(ctx, T)
    out_p = in_out_cubic(prog(t, dur - OUT, OUT)) if wipes[1] else 0.0
    in_p = out_cubic(prog(t, 0, IN)) if wipes[0] else 1.0
    if hud_on:
        ctx.push_group(); hud(ctx, T, total, day); ctx.pop_group_to_source()
        ctx.paint_with_alpha(in_p if hud_in else 1.0)
    ctx.push_group()
    s = 1 + 0.03 * in_out_cubic(clamp(t / dur))
    ctx.translate(W/2, 1000); ctx.scale(s, s); ctx.translate(-W/2, -1000)
    draw(ctx, t, dur)
    pat = ctx.pop_group()
    ctx.save(); ctx.translate(0, -110 * out_p + 60 * (1 - in_p)); ctx.set_source(pat)
    ctx.paint_with_alpha((1 - out_p) * in_p); ctx.restore()

def render_scene(path, dur, draw, T0, total, day, hud_on=True, wipes=(True, True), frame0=0, hud_in=False):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf)
    tmp = path[:-4] + ".part.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
        "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-tune", "grain",
        "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    for f in range(round(dur * FPS)):
        acc = np.zeros((H, W, 4), np.float32)
        for s in range(SUB):                       # 180° shutter
            t = (f + s / SUB * 0.5) / FPS
            compose(ctx, T0 + t, t, dur, draw, total, day, hud_on, wipes, hud_in); surf.flush()
            acc += np.frombuffer(surf.get_data(), np.uint8).reshape(H, W, 4)
        acc /= SUB; acc[..., :3] += grain(frame0 + f)
        p.stdin.write(np.clip(acc, 0, 255).astype(np.uint8).tobytes())
    p.stdin.close()
    if p.wait() != 0: raise RuntimeError("ffmpeg failed " + path)
    os.replace(tmp, path)

def still(path, t, dur, draw, T, total, day, hud_on=True):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf)
    compose(ctx, T, t, dur, draw, total, day, hud_on, (True, True)); surf.write_to_png(path)

# ---------- signature intro ----------
def intro(ctx, t, dur):
    p = in_out_quint(prog(t, 0.0, 0.62)); d = out_back(prog(t, 0.5, 0.4), 2.6)
    loop_mark(ctx, W/2, 860, 190, 52, p, d, rot=(1 - p) * -1.2)
    word = "REDLOOP"; size = 70; tr = size * 0.32
    total_w = width(ctx, word, size, "bold", tr); x = W/2 - total_w/2
    for i, ch in enumerate(word):
        q = out_quint(prog(t, 0.55 + i * 0.035, 0.45))
        if q > 0:
            ctx.save(); ctx.rectangle(x - 10, 1135, 120, 90); ctx.clip()
            text(ctx, x, 1205 + (1 - q) * 80, ch, size, INK, 1, "bold", 0); ctx.restore()
        x += width(ctx, ch, size, "bold", 0) + tr
    a = out_cubic(prog(t, 0.85, 0.4)); s = "une IA fait grandir ce compte"
    text(ctx, W/2 - width(ctx, s, 40, "accent")/2, 1285 + (1 - a) * 20, s, 40, RED, a, "accent")

# ---------- audio ----------
def soundtrack(path, total, cuts, ticks=(), bpm=104, sr=44100):
    n = int(total * sr); t = np.arange(n) / sr; out = np.zeros(n); rng = np.random.default_rng(3)
    def add(sig, at, g=1.0):
        i = int(at * sr); j = min(n, i + len(sig))
        if 0 <= i < n: out[i:j] += g * sig[:j - i]
    beat = 60 / bpm; start = 1.25
    kt = np.arange(int(.4*sr))/sr
    kick = np.sin(2*np.pi*np.cumsum(48 + 110*np.exp(-kt*32))/sr) * np.exp(-kt*7.5)
    ht = np.arange(int(.06*sr))/sr; hat = np.diff(rng.standard_normal(len(ht)+1)) * np.exp(-ht*80)
    ct = np.arange(int(.18*sr))/sr; clap = np.convolve(rng.standard_normal(len(ct)), np.ones(8)/8, "same")*np.exp(-ct*22)
    duck = np.ones(n); b = start; i = 0
    while b < total - 0.3:
        add(kick, b, 0.85); add(hat, b + beat/2, 0.10); add(hat, b + beat*0.75, 0.05)
        if i % 2 == 1: add(clap, b, 0.28)
        k0 = int(b*sr); k1 = min(n, k0 + int(.3*sr)); duck[k0:k1] = np.minimum(duck[k0:k1], 0.45 + 0.55*np.linspace(0, 1, k1-k0))
        b += beat; i += 1
    # bass + pad (Am – F – C – G), sidechained
    prog_ = [(110, 220, 261.6, 329.6), (87.3, 174.6, 220, 261.6), (130.8, 196, 261.6, 329.6), (98, 196, 246.9, 293.7)]
    env = np.clip(t/1.2, 0, 1) * np.clip((total - t)/1.0, 0, 1); bar = beat * 4
    for ci, ch in enumerate(prog_ * 8):
        s0 = start + ci * bar
        if s0 > total: break
        m = (t >= s0) & (t < s0 + bar); tt = t[m] - s0
        sig = 0.10*np.sin(2*np.pi*ch[0]*tt) + sum(0.025*np.sin(2*np.pi*f*tt + f)*(1+0.3*np.sin(2*np.pi*.5*tt)) for f in ch[1:])
        out[m] += sig * np.clip(tt/0.05, 0, 1)
    pre = (t < start); out[pre] += 0
    out *= duck * env + (1 - env) * 0
    # whoosh per cut (filtered noise, rising)
    wt = np.arange(int(.55*sr))/sr; nz = rng.standard_normal(len(wt))
    for w in (40, 20, 10): nz = np.convolve(nz, np.ones(w)/w, "same")
    sw = nz * 9 * np.sin(np.pi*wt/wt[-1])**3
    for c in cuts: add(sw, c - 0.35, 0.16)
    # intro sting: riser + pop
    st = np.arange(int(.7*sr))/sr
    add(np.sin(2*np.pi*np.cumsum(220 + 900*st**2)/sr) * np.sin(np.pi*st/st[-1])**2, 0.0, 0.16)
    pt = np.arange(int(.15*sr))/sr; pop = np.sin(2*np.pi*(660 + 400*np.exp(-pt*60))*pt) * np.exp(-pt*35)
    add(pop, 0.55, 0.5)
    tk = np.arange(int(.02*sr))/sr; tick = np.sin(2*np.pi*2400*tk)*np.exp(-tk*300)
    for x in ticks: add(tick, x, 0.08)
    out = np.tanh(out * 1.4); out = out / np.abs(out).max() * 0.85
    pcm = (np.repeat(out[:, None], 2, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as f: f.setnchannels(2); f.setsampwidth(2); f.setframerate(sr); f.writeframes(pcm.tobytes())

def assemble(files, audio, out):
    lst = out + ".txt"
    with open(lst, "w") as f:
        for s in files: f.write(f"file '{os.path.abspath(s)}'\n")
    v = out[:-4] + ".v.mp4"; tmp = out[:-4] + ".part.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", v], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", v, "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, out); os.remove(v)
