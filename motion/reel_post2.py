import sys, math; sys.path.insert(0, "/home/claude/motion")
from redloop_motion import *

DAY = 2
PROMPT = "Tu es expert Instagram. Mon compte est géré par une IA, de 0 à 1000 abonnés, pour créateurs et petites entreprises. Donne-moi 3 idées de premier post."
POST1 = cairo.ImageSurface.create_from_png("/home/claude/motion/out/c1/post1_1.png")
CPS = 44; TYPE0 = 0.9

def s_hook(ctx, t, d):
    caps(ctx, MX, 600, "LE TEST DU JOUR", 30, RED, 1, int(max(0, t - .3) / .025))
    kinetic(ctx, t, ["J'ai demandé", "à *une~IA* de", "trouver mon", "premier post."], MX, 760, 118, 0.45)

def s_prompt(ctx, t, d):
    caps(ctx, MX, 470, "MON PROMPT", 30, RED, 1, int(max(0, t - .3) / .025))
    a = out_quint(prog(t, 0.25, 0.6)); y0 = 530 + (1 - a) * 120; cw = W - 2*MX
    lines = wrap(ctx, PROMPT, 48, cw - 120, "text"); h = 230 + len(lines) * 68 + 40
    soft_shadow(ctx, MX, y0, cw, h, 44, a); rrect(ctx, MX, y0, cw, h, 44); ctx.set_source_rgba(*PAPER, a); ctx.fill()
    ctx.save(); ctx.translate(0, y0)
    disk(ctx, MX + 88, 98, 38, INK, a); loop_mark(ctx, MX + 86, 100, 15, 6, 1, 1, RED, BG)
    text(ctx, MX + 146, 92, "Redloop", 34, INK, a, "bold", 0); text(ctx, MX + 146, 130, "écrit à l'IA…", 28, INK, .5*a, "text", 0)
    ctx.set_source_rgba(*INK, .08*a); ctx.rectangle(MX + 50, 170, cw - 100, 2); ctx.fill()
    chars = int(max(0, t - TYPE0) * CPS); y = 250; shown = 0; cur = (MX + 60, y)
    for l in lines:
        if shown >= chars: break
        part = l[:chars - shown]; end = text(ctx, MX + 60, y, part, 48, INK, 1, "text", 0)
        cur = (end, y); shown += len(l) + 1; y += 68
    done = chars >= len(PROMPT)
    if not done or int(t * 2.4) % 2 == 0:
        ctx.set_source_rgb(*RED); ctx.rectangle(cur[0] + 6, cur[1] - 40, 5, 52); ctx.fill()
    ctx.restore()
    # AI thinking bubble
    q = out_back(prog(t, TYPE0 + len(PROMPT)/CPS + 0.2, 0.45), 1.6)
    if q > 0:
        by = y0 + h + 50; ctx.save(); ctx.translate(MX + 40, by); ctx.scale(q, q)
        rrect(ctx, 0, 0, 220, 96, 48); ctx.set_source_rgb(*INK); ctx.fill()
        for i in range(3):
            disk(ctx, 62 + i * 48, 48 - 10 * max(0, math.sin(t * 9 - i * .8)), 12, RED if i == 1 else BG)
        ctx.restore()

def s_three(ctx, t, d):
    caps(ctx, MX, 600, "SA RÉPONSE", 30, RED, 1, int(max(0, t - .3) / .025))
    kinetic(ctx, t, ["Elle m'a donné"], MX, 740, 96, 0.4)
    # digit roll 1 → 2 → 3
    r = in_out_quint(prog(t, 0.75, 0.9)) * 2; size = 560; x0, base = MX - 18, 1330
    ctx.save(); ctx.rectangle(x0 - 20, base - size * .78, 420, size * .86); ctx.clip()
    for i, dgt in enumerate("123"):
        off = (i - r) * size * 0.82
        if abs(off) < size: text(ctx, x0, base + off, dgt, size, RED, 1, "display")
    ctx.restore()
    kinetic(ctx, t, ["*idées.*"], MX + 400, 1320, 150, 1.4)

def idea(n, lines):
    def f(ctx, t, d):
        s = out_back(prog(t, 0.25, 0.5), 2.0)
        if s > 0:
            disk(ctx, MX + 50, 640, 50 * s, RED)
            if s > .5: text(ctx, MX + 50 - width(ctx, str(n), 56)/2, 660, str(n), 56, WHITE)
        caps(ctx, MX + 128, 652, f"IDÉE {n} SUR 3", 30, INK, .55, int(max(0, t - .35) / .025))
        kinetic(ctx, t, lines, MX, 860, 112, 0.5)
    return f

def s_choice(ctx, t, d):
    caps(ctx, MX, 520, "MON CHOIX", 30, RED, 1, int(max(0, t - .3) / .025))
    kinetic(ctx, t, ["J'ai pris", "la *n°1.*"], MX, 670, 118, 0.4)
    q = out_back(prog(t, 0.9, 0.7), 1.3)
    if q > 0:
        sc = 0.5; w, h = 1080 * sc, 1350 * sc; cx, cy = W/2 + 60, 1250 + (1 - q) * 500
        ctx.save(); ctx.translate(cx, cy); ctx.rotate(math.radians(-5 * q + 2 * (1 - q)))
        soft_shadow(ctx, -w/2, -h/2, w, h, 24, q, 60, .16); rrect(ctx, -w/2, -h/2, w, h, 24); ctx.clip()
        ctx.scale(sc, sc); ctx.set_source_surface(POST1, -540, -675); ctx.paint(); ctx.restore()
        caps(ctx, MX, 1700, "MON PREMIER POST", 26, INK, .55 * q)

def s_outro(ctx, t, d):
    caps(ctx, MX, 520, "SUIS LE DÉFI", 30, RED, 1, int(max(0, t - .3) / .025))
    kinetic(ctx, t, ["Dis-moi ce", "que je *teste*", "ensuite."], MX, 670, 112, 0.35)
    a = out_cubic(prog(t, 1.15, 0.5)); y = 1150
    caps(ctx, MX, y, "ABONNÉS", 26, INK, .55 * a)
    s = "0 / 1 000"; text(ctx, W - MX - width(ctx, s, 34, "bold", 0), y + 2, s, 34, INK, a, "bold", 0)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_width(20)
    ctx.set_source_rgba(*INK, .09 * a); ctx.move_to(MX, y + 60); ctx.line_to(W - MX, y + 60); ctx.stroke()
    disk(ctx, MX, y + 60, 34 * a * (1 + .35 * (0.5 + 0.5*math.sin(t*6))), RED, .25 * a); disk(ctx, MX, y + 60, 16 * a, RED)
    b = out_back(prog(t, 1.6, 0.6), 1.5)
    if b > 0:
        ctx.save(); ctx.translate(W/2, 1430); ctx.scale(b, b)
        rrect(ctx, -300, -62, 600, 124, 62); ctx.set_source_rgb(*INK); ctx.fill()
        s = "Suis le défi"; text(ctx, -width(ctx, s, 46, "bold", 0)/2 - 24, 16, s, 46, BG, 1, "bold", 0)
        loop_mark(ctx, 210, 0, 18, 7, 1, 1, RED, BG); ctx.restore()

SCENES = [(intro, 1.95, False, False, True), (s_hook, 3.3, True, True, True), (s_prompt, 6.0, True, True, True),
          (s_three, 2.9, True, True, True),
          (idea(1, ["Jour 0 :", "*zéro* abonné,", "voici le plan."]), 2.7, True, True, True),
          (idea(2, ["Ce que l'IA", "ne sait *pas*", "faire."]), 2.7, True, True, True),
          (idea(3, ["Mes *prédictions*", "pour le jour 30."]), 2.7, True, True, True),
          (s_choice, 3.0, True, True, True), (s_outro, 3.6, True, True, False)]
TOTAL = sum(s[1] for s in SCENES)

if __name__ == "__main__":
    out = "/home/claude/motion/out"; os.makedirs(out, exist_ok=True)
    if sys.argv[1] == "stills":
        T0 = 0
        for i, (fn, d, h, wi, wo) in enumerate(SCENES):
            tt = float(sys.argv[2]) if len(sys.argv) > 2 else d - WIPE - .05
            still(f"{out}/v2_{i}.png", tt, d, fn, T0 + tt, TOTAL, DAY, h); T0 += d
    else:
        T0 = 0; files = []; cuts = []; f0 = 0
        p_start = SCENES[0][1] + SCENES[1][1]
        ticks = [p_start + TYPE0 + i / CPS * 3 for i in range(len(PROMPT) // 3)]
        for i, (fn, d, h, wi, wo) in enumerate(SCENES):
            f = f"{out}/v2_scene_{i}.mp4"; render_scene(f, d, fn, T0, TOTAL, DAY, h, (wi, wo), f0, hud_in=(i == 1))
            files.append(f); T0 += d; f0 += round(d * FPS); cuts.append(T0)
        soundtrack(f"{out}/v2_music.wav", TOTAL, cuts[:-1], ticks)
        assemble(files, f"{out}/v2_music.wav", f"{out}/reel_post2_v2.mp4"); print("total", TOTAL)
