import sys, os; sys.path.insert(0, "/home/claude/motion")
from notebook_kit import *
LBL = "épisode 01 · l'état du marché"; OUT = "/home/claude/motion/out/ep01"; J = "/home/claude/redloop-visualx/posts"
os.makedirs(OUT, exist_ok=True)
def save(p, i): p.render(f"{OUT}/ep01_{i}.png", f"{J}/ep01_{i}.jpg")

# 1
p = Page(101); header(p, LBL)
y, ws, sz = title(p, [("tout le monde", BLACK), ("vibe code.", BLACK)], 400, 116)
w = p.write(L, y + 200, "personne ne crée.", 100, RED, ang=-2.5)
note(p, ["j'ai regardé les chiffres."], y + 360, 58)
handle(p); glisse(p); save(p, 1)

# 2
p = Page(102); header(p, LBL)
y, ws, sz = title(p, [("le vibe coding,", BLACK), ("c'est quoi ?", BLACK)], 340, 104)
note(p, ["tu décris ton appli à une IA,", "elle écrit le code à ta place.", "pas besoin de savoir coder."], y + 150, 58)
def collins(t):
    p.write(30, 52, "DICTIONNAIRE COLLINS", 22, GREY, "Inter Display", True, 0, 0, 1, ctx=t, spacing=3)
    p.write(30, 112, "Mot de l'année 2025 :", 34, BLACK, "Inter", False, 0, 0, 1, ctx=t)
    p.write(30, 168, "« vibe coding »", 50, BLACK, "Inter Display", True, 0, 0, 1, ctx=t)
p.printed_scrap(L - 20, 900, 560, 210, -3, collins); p.tape(L + 260, 904, 140, 40, -6)
p.write(L + 560, 1180, "le mot de l'année.", 50, RED, "Caveat", True, 1, -4)
glisse(p); save(p, 2)

# 3
p = Page(103); header(p, LBL)
y, ws, sz = title(p, [("la vitrine", BLACK)], 330, 110)
yb, vx = doc_card(p, L - 40, 420, 760, 2, "RAPPORT LOVABLE · JUIN 2026", "Une des plateformes de vibe coding",
           [("Projets créés", "50 millions +"), ("Nouveaux projets", "≈ 1 million / sem."), ("Créateurs non techniques", "80 %")],
           "Chiffres de l'entreprise elle-même, non audités.")
p.write(L, yb + 140, "impressionnant…", 64, BLUE, "Caveat", True, 1, -2)
p.write(L + 380, yb + 230, "mais attends.", 70, RED, "Caveat", True, 1, -4)
glisse(p); save(p, 3)

# 4
p = Page(104); header(p, LBL)
y, ws, sz = title(p, [("l'envers", BLACK), ("du décor", RED)], 330, 110)
yb, vx = doc_card(p, L - 40, 560, 760, -2, "SONDAGE LOVABLE · 14 300+ UTILISATEURS", "Ce que rapporte ce qui a été créé",
           [("Ne gagnent encore rien", "60,5 %"), ("Revenu direct du produit", "10,7 %")],
           "Déclaratif, auprès des utilisateurs actifs.")
p.circle(L - 40 + vx + 70, 560 + 165 + 60 - 12, 95, 40, RED, 6, ctx=p.t)
p.write(L, yb + 140, "environ 1 sur 10", 74, RED, "Caveat", True, 1, -3)
p.write(L, yb + 220, "gagne vraiment de l'argent avec.", 54, BLUE, "Caveat", True, 1, -2)
glisse(p); save(p, 4)

# 5
p = Page(105); header(p, LBL)
y, ws, sz = title(p, [("créer,", BLACK), ("c'est pas", BLACK), ("lancer.", RED)], 360, 120)
note(p, ["les 50 millions comptent aussi", "les essais abandonnés", "au bout d'une heure."], y + 150, 54)
p.postit(560, 1000, 400, 230, 4, ["il manque :", "un public, une offre,", "de la confiance."], 46)
glisse(p); save(p, 5)

# 6
p = Page(106); header(p, LBL)
y, ws, sz = title(p, [("et derrière", BLACK), ("la façade ?", BLACK)], 340, 104)
yb, vx = doc_card(p, L - 40, 560, 760, 2, "VERACODE · TEST DE 100+ MODÈLES D'IA", "Code généré par IA",
           [("Avec une faille de sécurité connue", "45 %")],
           "Test en conditions de labo, pas un audit d'applis en ligne.", lab=26, val=40)
p.circle(L - 40 + vx + 50, 560 + 165 - 14, 80, 40, RED, 6, ctx=p.t)
note(p, ["un site « fait en 10 minutes »,", "c'est parfois tes clients", "qui paient l'addition."], yb + 150, 54)
glisse(p); save(p, 6)

# 7
p = Page(107); header(p, LBL)
y, ws, sz = title(p, [("l'IA a rendu", BLACK), ("la création", BLACK), ("facile.", BLACK)], 360, 112)
w = p.write(L, y + 190, "pas le business.", 104, RED, ang=-2.5)
note(p, ["c'est ce que je vais décortiquer,", "épisode après épisode."], y + 360, 54)
glisse(p); save(p, 7)

# 8
p = Page(108); header(p, LBL)
y, ws, sz = title(p, [("et toi ?", BLACK)], 330, 120)
under(p, 365, ws[0])
note(p, ["tu as déjà lancé un site", "qui n'a jamais vendu ?", "raconte en commentaire."], y + 190, 62)
p.postit(560, 980, 410, 250, 4, ["prochain épisode :", "les sites clé en main", "vides de sens"], 46)
handle(p); save(p, 8)
