import sys, math; sys.path.insert(0, "/home/claude/motion")
from notebook import *
GOLD = (0.88, 0.76, 0.45); CREAM = (0.97, 0.95, 0.90)

def header(p, L, ep):
    pts = [(L + 22 + 22*math.cos(math.radians(a)), 112 + 22*math.sin(math.radians(a))) for a in range(-40, -340, -12)]
    p.stroke(pts, RED, 6); p.c.set_source_rgba(*BLACK, .9); p.c.arc(L + 22 + 29*math.cos(math.radians(-58)), 112 + 29*math.sin(math.radians(-58)), 5, 0, 6.3); p.c.fill()
    p.write(L + 62, 128, "redloop", 40, BLACK, "Caveat", True, .6)
    p.write(700, 124, f"épisode {ep} · les pièges", 42, BLUE, "Caveat", True, .8, -1.5)

def glisse(p):
    w2 = p.write(860, 1288, "glisse", 46, RED, "Caveat", True, .8, -2)
    p.line(860 + w2 + 10, 1272, 860 + w2 + 60, 1268, RED, 5, 0); p.line(860 + w2 + 42, 1254, 860 + w2 + 62, 1268, RED, 5, 0, 4); p.line(860 + w2 + 42, 1284, 860 + w2 + 62, 1268, RED, 5, 0, 4)

# --- slide A : la promesse barrée ---
p = Page(21); L = 205; header(p, L, "01")
def ad(t):
    p.write(40, 64, "BUSINESS CLÉ EN MAIN", 30, GOLD, "Inter Display", True, 0, 0, 1, ctx=t, spacing=5)
    p.write(40, 170, "10 000 €/mois", 96, CREAM, "Inter Display", True, 0, 0, 1, ctx=t)
    p.write(40, 236, "sans expérience · 100 % passif", 34, CREAM, "Inter", False, 0, 0, .75, ctx=t)
p.printed_scrap(L - 40, 230, 700, 290, -3, ad, fill=(0.09, 0.09, 0.10))
p.tape(L - 20, 236, 130, 40, -28); p.tape(L + 640, 230, 130, 40, 24)
# strike on top layer
p.stroke([(L - 10, 418), (L + 220, 404), (L + 470, 396), (L + 600, 388)], RED, 12, ctx=p.t)
p.write(L + 470, 610, "vraiment ?", 76, RED, "Caveat", True, 1, -6)
p.arrow(L + 520, 560, L + 430, 470, RED, 6, -15)
p.write(L, 820, "Le business", 104, BLACK, ang=-1.5)
p.write(L, 940, "clé en main :", 104, BLACK, ang=-1.0)
w = p.write(L, 1075, "on a vérifié.", 108, RED, ang=-1.8)
p.line(L, 1110, L + w, 1098, RED, 6, 4)
p.write(L, 1200, "chiffres officiels à l'intérieur", 50, BLUE, "Caveat", True, 1, -1.5)
glisse(p); p.render("/home/claude/motion/out/diy/ep1_A.png")

# --- slide B : la preuve + verdict ---
p = Page(22); L = 205; header(p, L, "01")
p.write(L, 300, "ce qu'on a trouvé", 78, BLACK, ang=-1.5)
def doc(t):
    p.write(34, 58, "PLAINTE DE LA FTC · 2025", 24, (0.35, 0.35, 0.38), "Inter Display", True, 0, 0, 1, ctx=t, spacing=3)
    p.write(34, 92, "Boutiques Amazon « automatisées »", 30, BLACK, "Inter Display", True, 0, 0, 1, ctx=t)
    t.set_source_rgba(0, 0, 0, .15); t.rectangle(34, 112, 560, 2); t.fill()
    rows = [("Prix d'entrée", "39 000 – 65 000 €"), ("Sans aucun revenu", "21 %"), ("Revenu médian, à vie", "≈ 6 200 €"), ("Fermées par Amazon", "≈ 95 %")]
    for i, (a, b) in enumerate(rows):
        y = 170 + i * 62
        p.write(34, y, a, 30, (0.25, 0.25, 0.28), "Inter", False, 0, 0, 1, ctx=t)
        p.write(410, y, b, 32, BLACK, "Inter Display", True, 0, 0, 1, ctx=t)
    p.write(34, 430, "Montants convertis du dollar.", 22, (0.45, 0.45, 0.48), "Inter", False, 0, 0, 1, ctx=t)
p.printed_scrap(L - 50, 380, 720, 460, 2, doc)
p.tape(L + 300, 384, 150, 42, -4)
p.circle(L + 490, 668, 120, 44, RED, 6, ctx=p.t)
p.write(L + 10, 975, "tu paies 39 000 € et +,", 54, BLUE, "Caveat", True, 1, -2)
p.write(L + 10, 1040, "tu récupères env. 6 200 €.", 54, BLUE, "Caveat", True, 1, -2)
p.highlight(L + 6, 1026, L + 470, 44)
p.write(L + 10, 1130, "au PMU : 75 %…", 54, RED, "Caveat", True, 1, -2)
p.stamp(860, 1080, [("VERDICT", 30), ("À FUIR", 64)], -14)
glisse(p); p.render("/home/claude/motion/out/diy/ep1_B.png")
