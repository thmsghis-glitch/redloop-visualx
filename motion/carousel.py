import sys, math, os, subprocess; sys.path.insert(0, "/home/claude/motion")
from redloop_motion import *
CW, CH = 1080, 1350

def header(ctx, day, i, n):
    loop_mark(ctx, 126, 140, 28, 9); caps(ctx, 178, 152, "REDLOOP", 28, INK)
    s = f"{i:02d} / {n:02d}"; text(ctx, CW - MX - width(ctx, s, 28, "bold", 28*.15), 152, s, 28, INK, .45, "bold", 28*.15)
    # progress dots as a line
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_width(6)
    ctx.set_source_rgba(*INK, .1); ctx.move_to(MX, 220); ctx.line_to(CW - MX, 220); ctx.stroke()
    x1 = MX + (CW - 2*MX) * i / n; ctx.set_source_rgb(*RED); ctx.move_to(MX, 220); ctx.line_to(x1, 220); ctx.stroke(); disk(ctx, x1, 220, 9, RED)

def footer(ctx, last, day):
    label = f"JOUR {day:02d}"; w = width(ctx, label, 24, "bold", 24 * .2) + 66
    rrect(ctx, MX, 1222, w, 54, 27); ctx.set_source_rgb(*INK); ctx.fill(); disk(ctx, MX + 25, 1249, 7, RED); caps(ctx, MX + 42, 1257, label, 24, BG)
    if not last:
        s = "Glisse"; x = CW - MX - 70 - width(ctx, s, 30, "bold", 0)
        text(ctx, x, 1260, s, 30, INK, .6, "bold", 0)
        ctx.set_source_rgb(*RED); ctx.set_line_width(6); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.move_to(CW - MX - 50, 1249); ctx.line_to(CW - MX, 1249); ctx.move_to(CW - MX - 18, 1231); ctx.line_to(CW - MX, 1249); ctx.line_to(CW - MX - 18, 1267); ctx.stroke()

def bg(ctx):
    ctx.set_source_rgb(*BG); ctx.paint()
    ctx.save(); ctx.translate(1000, 1180); ctx.rotate(1.1); ctx.set_source_rgba(*INK, .04); ctx.set_line_width(60)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.new_path(); ctx.arc(0, 0, 420, 0, math.radians(300)); ctx.stroke(); ctx.restore()

def title_slide(tag, lines, sub=None, size=118):
    def f(ctx):
        lh = size * 1.08; sub_l = wrap(ctx, sub, 44, CW - 2*MX - 60, "text") if sub else []
        block = (100 if tag else 0) + len(lines) * lh + (50 + len(sub_l) * 62 if sub_l else 0)
        y = 300 + (900 - block) / 2 + size * 0.8
        if tag: caps(ctx, MX, y - size * 0.8 - 10, tag, 30, RED); y += 70
        kinetic(ctx, 99, lines, MX, y, size); y += (len(lines) - 1) * lh + 120
        for l in sub_l: text(ctx, MX, y, l, 44, INK, .7, "text", 0); y += 62
    return f

def prompt_slide(tag, prompt, note):
    def f(ctx):
        lines = wrap(ctx, prompt, 46, CW - 2*MX - 120, "text"); h = 210 + len(lines) * 66 + 30
        y0 = 300 + (860 - h - 110) / 2
        caps(ctx, MX, y0 - 40, tag, 30, RED)
        soft_shadow(ctx, MX, y0, CW - 2*MX, h, 40); rrect(ctx, MX, y0, CW - 2*MX, h, 40); ctx.set_source_rgb(*PAPER); ctx.fill()
        disk(ctx, MX + 86, y0 + 92, 36, INK); loop_mark(ctx, MX + 84, y0 + 94, 14, 6, 1, 1, RED, BG)
        text(ctx, MX + 142, y0 + 86, "Prompt à copier", 32, INK, 1, "bold", 0); text(ctx, MX + 142, y0 + 122, "ChatGPT, Claude, Gemini…", 26, INK, .5, "text", 0)
        ctx.set_source_rgba(*INK, .08); ctx.rectangle(MX + 50, y0 + 160, CW - 2*MX - 100, 2); ctx.fill()
        y = y0 + 236
        for l in lines: text(ctx, MX + 60, y, l, 46, INK, 1, "text", 0); y += 66
        text(ctx, MX, y0 + h + 90, note, 44, INK, .75, "accent")
    return f

def render(name, slides, day, outdir, jpgdir):
    os.makedirs(outdir, exist_ok=True); n = len(slides); files = []
    for i, fn in enumerate(slides, 1):
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, CW, CH); ctx = cairo.Context(s)
        bg(ctx); header(ctx, day, i, n); fn(ctx); footer(ctx, i == n, day)
        png = f"{outdir}/{name}_{i}.png"; s.write_to_png(png)
        subprocess.run(["convert", png, "-quality", "92", f"{jpgdir}/{name}_{i}.jpg"], check=True); files.append(png)
    return files

POST1 = [title_slide("", ["*Une~IA* gère", "ce compte."], "Objectif : 1 000 abonnés. Je montre tout, en direct.", 128),
         title_slide("LE PRINCIPE", ["L'IA propose,", "crée et *publie.*"], "Moi, je valide. Rien n'est caché."),
         title_slide("POINT DE DÉPART", ["Jour *zéro.*"], "0 abonné. 0 publication. 0 audience.", 140),
         title_slide("CE QUE JE MONTRE", ["Les tests.", "Les vrais chiffres.", "Les *échecs.*"], None, 104),
         title_slide("POUR QUI", ["Créateurs,", "boutiques,", "*TPE.*"], "Tous ceux qui veulent être vus sur Instagram."),
         title_slide("SUIS LE DÉFI", ["Rendez-vous", "au jour *30.*"], "Dis-moi en commentaire ce que tu veux que je teste.")]
POST3 = [title_slide("À SAUVEGARDER", ["*5 prompts*", "pour trouver", "30 idées de posts."], "En 10 minutes, avec n'importe quelle IA.", 108),
         prompt_slide("01 · LES SUJETS", "Tu es expert Instagram. Mon activité : [ton activité]. Donne-moi 10 sujets de posts qui répondent aux questions que mes clients se posent.", "Remplace [ton activité] par la tienne."),
         prompt_slide("02 · LES ACCROCHES", "Transforme ces 5 idées en accroches de 8 mots maximum, qui donnent envie de lire la suite : [tes idées]", "L'accroche fait presque tout."),
         prompt_slide("03 · LE RECYCLAGE", "Voici un de mes anciens posts : [texte]. Propose 5 angles différents pour en faire un nouveau post.", "Une bonne idée sert cinq fois."),
         prompt_slide("04 · LES ERREURS", "Quelles sont les 10 erreurs ou idées reçues les plus courantes dans mon secteur ? Fais-en 10 sujets de posts.", "On partage ce qui évite une erreur."),
         prompt_slide("05 · LE CALENDRIER", "Crée un calendrier de 30 jours : 3 carrousels, 2 reels et 2 stories par semaine, avec un sujet par jour.", "Trente jours de contenu d'un coup."),
         title_slide("À TOI", ["Lequel tu", "testes en", "*premier ?*"], "Dis-le en commentaire, et sauvegarde pour plus tard.")]

if __name__ == "__main__":
    J = "/home/claude/redloop-visualx/posts"
    a = render("post1", POST1, 0, "/home/claude/motion/out/c1", J)
    b = render("post3", POST3, 5, "/home/claude/motion/out/c3", J)
