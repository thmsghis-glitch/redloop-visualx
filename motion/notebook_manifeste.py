import sys; sys.path.insert(0, "/home/claude/motion")
from notebook_kit import *
LBL = "épisode 00 · l'intro"; OUT = "/home/claude/motion/out/nb"; J = "/home/claude/redloop-visualx/posts"
import os; os.makedirs(OUT, exist_ok=True)
def save(p, i): p.render(f"{OUT}/manifeste_{i}.png", f"{J}/manifeste_{i}.jpg")

# 1
p = Page(31); header(p, LBL)
y, ws, sz = title(p, [("je vais faire", BLACK), ("le point sur", BLACK), ("le business", BLACK), ("en ligne.", BLACK)], 400, 112)
w = p.write(L, y + 190, "Sérieusement.", 104, RED, ang=-2.5); under(p, y + 225, w, twice=True)
note(p, ["sans bullshit, promis."], y + 360, 58)
glisse(p); save(p, 1)

# 2
p = Page(32); header(p, LBL)
ad(p, L - 40, 230, 720, 300, -3, "FORMATION · PLACES LIMITÉES", "Ton business IA", "lancé en un week-end · 100 % passif")
p.tape(L - 10, 236, 130, 40, -28); p.tape(L + 650, 230, 130, 40, 24)
p.stroke([(L - 20, 445), (L + 250, 432), (L + 520, 424), (L + 640, 418)], RED, 12, ctx=p.t)
y, ws, sz = title(p, [("partout, on te", BLACK), ("promet que", BLACK), ("c'est facile.", RED)], 720, 108)
under(p, y + 35, ws[-1])
note(p, ["(spoiler : non.)"], y + 160, 58, RED)
glisse(p); save(p, 2)

# 3
p = Page(33); header(p, LBL)
y, ws, sz = title(p, [("la mise", BLACK), ("en scène", RED)], 330, 112)
def call(t):
    p.write(30, 52, "RÉEL · COLD CALL", 24, GREY, "Inter Display", True, 0, 0, 1, ctx=t, spacing=3)
    p.write(30, 108, "« Vous êtes le meilleur", 36, BLACK, "Inter Display", True, 0, 0, 1, ctx=t)
    p.write(30, 152, "plombier de la ville ? »", 36, BLACK, "Inter Display", True, 0, 0, 1, ctx=t)
    p.write(30, 210, "→ signé en 2 minutes", 30, GREY, "Inter", False, 0, 0, 1, ctx=t)
p.printed_scrap(L - 30, 560, 560, 250, -4, call); p.tape(L + 240, 563, 140, 40, -5)
def pod(t):
    p.write(30, 52, "PODCAST", 24, GREY, "Inter Display", True, 0, 0, 1, ctx=t, spacing=3)
    p.write(30, 108, "« Comment j'ai bâti", 36, BLACK, "Inter Display", True, 0, 0, 1, ctx=t)
    p.write(30, 152, "un empire à 1 M€ »", 36, BLACK, "Inter Display", True, 0, 0, 1, ctx=t)
p.printed_scrap(L + 250, 860, 520, 200, 3, pod); p.tape(L + 510, 862, 130, 40, 6)
p.write(L - 10, 1150, "c'est du montage.", 64, RED, "Caveat", True, 1, -3)
p.arrow(L + 420, 1110, L + 330, 820, RED, 6, -20)
glisse(p); save(p, 3)

# 4
p = Page(34); header(p, LBL)
y, ws, sz = title(p, [("la réalité", BLACK), ("du terrain ?", BLACK), ("beaucoup moins", BLACK), ("glamour.", RED)], 380, 108)
under(p, y + 35, ws[-1])
p.highlight(L - 6, y + 238, L + 470, 52)
note(p, ["et je vais te la montrer,", "chiffres à l'appui."], y + 190, 62)
p.postit(640, 960, 330, 190, 4, ["une source", "par chiffre."], 54)
glisse(p); save(p, 4)

# 5
p = Page(35); header(p, LBL)
y, ws, sz = title(p, [("le programme", BLACK)], 330, 104)
items = ["l'état du marché", "le brouillard des promesses", "les pièges, un par un", "ce que l'IA ne fait pas", "les vraies bases"]
yy = 500
for i, t in enumerate(items, 1):
    p.write(L, yy, f"{i}.", 60, RED, "Caveat", True, .8); p.write(L + 60, yy, t, 60, BLUE, "Caveat", True, 1, -1); yy += 92
w = p.write(L + 60, yy + 40, "… et après ?", 74, RED, "Caveat", True, 1, -3)
p.circle(L + 60 + w / 2, yy + 18, w / 2 + 40, 62, RED, 6)
note(p, ["épisode après épisode,", "sans brûler les étapes."], yy + 190, 50, BLACK, bold=False)
glisse(p); save(p, 5)

# 6
p = Page(36); header(p, LBL)
y, ws, sz = title(p, [("pas de formation", BLACK), ("à vendre.", BLACK), ("pas de gourou.", BLACK)], 380, 104)
note(p, ["juste moi, mon carnet,", "des sources,", "et une IA pour vérifier."], y + 190, 62)
p.stamp(800, 1040, [("ZÉRO", 34), ("PROMESSE", 58)], -12)
glisse(p); save(p, 6)

# 7
p = Page(37); header(p, LBL)
y, ws, sz = title(p, [("abonne-toi", RED), ("si tu veux", BLACK), ("y voir clair.", BLACK)], 400, 112)
under(p, 400 + 30, ws[0])
note(p, ["et dis-moi en commentaire", "quelle promesse t'a déjà", "fait rêver."], y + 180, 58)
p.postit(600, 1030, 380, 230, 4, ["prochain épisode :", "l'état du marché"], 50)
save(p, 7)
