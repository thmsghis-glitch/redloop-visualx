import sys, math; sys.path.insert(0, "/home/claude/motion")
from redloop_motion import *

DAY = 2
PROMPT = "Tu es expert Instagram. Mon compte est géré par une IA, de 0 à 1000 abonnés, pour créateurs et petites entreprises. Donne-moi 3 idées de premier post."

def s_hook(ctx, t, d):
    tag(ctx, t, "LE TEST DU JOUR", MX, 560, 0.35)
    kinetic(ctx, t, ["J'ai demandé", "à *une* *IA* de", "trouver mon", "premier post."], MX, 720, 108, 0.5)

def s_prompt(ctx, t, d):
    tag(ctx, t, "MON PROMPT", MX, 470, 0.35)
    a = out_back(prog(t, 0.35, 0.5), 1.2)
    y0 = 530 + (1 - a) * 80; h = 640
    ctx.save(); ctx.translate(0, 14); rrect(ctx, MX, y0, W - 2*MX, h, 40); ctx.set_source_rgba(*INK, 0.08 * a); ctx.fill(); ctx.restore()
    rrect(ctx, MX, y0, W - 2*MX, h, 40); ctx.set_source_rgba(*WHITE, a); ctx.fill()
    # chat header
    rrect(ctx, MX + 50, y0 + 50, 74, 74, 37); ctx.set_source_rgba(*RED, a); ctx.fill()
    text(ctx, MX + 66, y0 + 100, "IA", 32, WHITE, a)
    text(ctx, MX + 150, y0 + 100, "Nouvelle conversation", 34, INK, 0.55 * a, False)
    lines = wrap(ctx, PROMPT, 50, W - 2*MX - 120, False)
    chars = int(max(0, t - 0.8) * 44); y = y0 + 220; shown = 0
    for l in lines:
        if shown >= chars: break
        part = l[:chars - shown]; end = text(ctx, MX + 60, y, part, 50, INK, 1, False)
        shown += len(l) + 1; cur = (end, y); y += 70
    if chars and (int(t * 2.5) % 2 == 0 or shown < len(PROMPT)):
        ctx.set_source_rgb(*RED); ctx.rectangle(cur[0] + 6, cur[1] - 42, 6, 54); ctx.fill()

def s_three(ctx, t, d):
    tag(ctx, t, "SA RÉPONSE", MX, 560, 0.35)
    kinetic(ctx, t, ["Elle m'a donné"], MX, 690, 84, 0.45)
    s = out_back(prog(t, 0.8, 0.55), 2.0)
    if s > 0:
        ctx.save(); ctx.translate(MX + 170, 1180); ctx.scale(s, s)
        text(ctx, -170, 0, "3", 560, RED); ctx.restore()
    kinetic(ctx, t, ["idées."], MX + 400, 1175, 130, 1.0)

def idea(n, lines):
    def f(ctx, t, d):
        tag(ctx, t, f"IDÉE {n}", MX + 140, 640, 0.35)
        s = out_back(prog(t, 0.3, 0.45), 2.2)
        if s > 0:
            ctx.new_path(); ctx.arc(MX + 52, 628, 52 * s, 0, 2*math.pi); ctx.set_source_rgb(*RED); ctx.fill()
            if s > 0.6: text(ctx, MX + 36, 650, str(n), 60, WHITE)
        kinetic(ctx, t, lines, MX, 820, 100, 0.55)
    return f

def s_choice(ctx, t, d):
    tag(ctx, t, "MON CHOIX", MX, 600, 0.35)
    kinetic(ctx, t, ["J'ai pris", "la *n°1.*", "C'était mon", "premier post."], MX, 760, 110, 0.45)

def s_outro(ctx, t, d):
    tag(ctx, t, "SUIS LE DÉFI", MX, 520, 0.3)
    kinetic(ctx, t, ["Dis-moi ce que", "je *teste* ensuite."], MX, 660, 92, 0.4)
    a = out_cubic(prog(t, 1.2, 0.5)); y = 1060
    text(ctx, MX, y, "ABONNÉS", 30, INK, 0.6 * a, True, 4)
    font(ctx, 30); s = "0 / 1000"; text(ctx, W - MX - tw(ctx, s) - 10, y, s, 30, INK, a, True, 2)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_width(22)
    ctx.set_source_rgba(*INK, 0.1 * a); ctx.move_to(MX, y + 60); ctx.line_to(W - MX, y + 60); ctx.stroke()
    pulse = 1 + 0.25 * math.sin(t * 6)
    ctx.set_source_rgba(*RED, a); ctx.new_path(); ctx.arc(MX, y + 60, 20 * pulse, 0, 2*math.pi); ctx.fill()
    b = out_back(prog(t, 1.7, 0.6), 1.6)
    if b > 0:
        ctx.save(); ctx.translate(W/2, 1420); ctx.scale(b, b); loop_mark(ctx, 0, 0, 80, 24, 1, 1); ctx.restore()

SCENES = [  # (draw, dur, hud, wipe_in, wipe_out)
    (intro, 1.9, False, False, True),
    (s_hook, 3.3, True, True, True),
    (s_prompt, 5.4, True, True, True),
    (s_three, 2.4, True, True, True),
    (idea(1, ["Jour 0 :", "*0* abonné,", "voici le plan."]), 2.7, True, True, True),
    (idea(2, ["Ce que l'IA", "ne sait *pas*", "faire."]), 2.7, True, True, True),
    (idea(3, ["Mes *prédictions*", "pour le jour 30."]), 2.6, True, True, True),
    (s_choice, 2.6, True, True, True),
    (s_outro, 3.4, True, True, False),
]
TOTAL = sum(s[1] for s in SCENES)

if __name__ == "__main__":
    out = "/home/claude/motion/out"; os.makedirs(out, exist_ok=True)
    if sys.argv[1] == "stills":
        T0 = 0
        for i, (fn, d, h, wi, wo) in enumerate(SCENES):
            still(f"{out}/still_{i}.png", d - WIPE - 0.05, fn, T0 + d - 0.5, TOTAL, DAY, h); T0 += d
        still(f"{out}/still_intro_mid.png", 0.8, intro, 0.8, TOTAL, DAY, False)
    else:
        T0 = 0; files = []; cuts = []
        for i, (fn, d, h, wi, wo) in enumerate(SCENES):
            f = f"{out}/scene_{i}.mp4"; render_scene(f, d, fn, T0, TOTAL, DAY, h, (wi, wo)); files.append(f)
            T0 += d; cuts.append(T0)
        soundtrack(f"{out}/music.wav", TOTAL, cuts[:-1])
        assemble(files, f"{out}/music.wav", f"{out}/reel_post2.mp4")
        print("total", TOTAL)
