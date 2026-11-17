import sys; sys.path.insert(0, "/home/claude/motion")
from diy_carousel import *
EP, TOT, DAY, N = 0, 9, 0, 7

def s1():
    s, c = base(EP, TOT, 11)
    y = title(c, ["On lance", "un business", "*en~direct.*"], 520, 136)
    hand(c, 640, 400, "pour de vrai.", 62, RED, 1, -7)
    marker_arrow(c, 760, 420, 700, 560, 1, RED, 6, -25)
    sub_scrap(c, "Avec une IA, de zéro, et les vrais chiffres. Rien de caché.", y + 90, 1.5, 3)
    footer(c, False, DAY); save(s, "post1_1", 1)

def s2():
    s, c = base(EP, TOT, 12); label(c, "le constat")
    y = title(c, ["Les réseaux", "sont pleins de", "*promesses.*"], 440, 120)
    promise(c, 110, y + 90, "Revenu 100 % passif", -3, 21)
    promise(c, 380, y + 230, "Sans aucune expérience", 2.5, 22)
    promise(c, 130, y + 370, "Résultats garantis", -1.5, 23)
    hand(c, 600, y + 470, "la plupart : faux.", 64, RED, 1, -5)
    footer(c, False, DAY); save(s, "post1_2", 2)

def s3():
    s, c = base(EP, TOT, 13); label(c, "notre objectif")
    y = title(c, ["Construire", "quelque chose", "de *concret.*"], 450, 124)
    sub_scrap(c, "Ensemble, étape par étape. Des actions, des résultats, des chiffres.", y + 90, -1.2, 5)
    postit(c, 640, y + 250, ["zéro théorie,", "promis."], 5, 320, 48, 8)
    footer(c, False, DAY); save(s, "post1_3", 3)

def s4():
    s, c = base(EP, TOT, 14); label(c, "ce que tu verras ici")
    y = title(c, ["Tout, même", "les *échecs.*"], 440, 110)
    check_list(c, ["Ce qu'on teste, et pourquoi", "Combien ça coûte, combien ça rapporte", "Ce qui marche, et ce qui rate", "Les décisions qu'on prend avec toi"], y + 90, 31)
    footer(c, False, DAY); save(s, "post1_4", 4)

def s5():
    s, c = base(EP, TOT, 15); label(c, "la méthode")
    y = title(c, ["Le trafic", "d'abord.", "Le produit", "*ensuite.*"], 440, 120)
    hand(c, 760, 470, "1", 90, RED, 1, 0); marker_circle(c, 784, 440, 44, 44, 3, RED, 6)
    hand(c, 760, 730, "2", 90, RED, 1, 0); marker_circle(c, 784, 700, 44, 44, 4, RED, 6)
    sub_scrap(c, "Pas de formation à vendre. Pas de business clé en main. On construit l'audience, puis on crée ce qu'elle demande.", y + 90, 1, 9, 38)
    footer(c, False, DAY); save(s, "post1_5", 5)

def s6():
    s, c = base(EP, TOT, 16); label(c, "point de départ")
    y = title(c, ["Jour *zéro.*"], 560, 170)
    postit(c, 140, y + 110, ["0 abonné", "0 produit", "0 €"], -4, 360, 58, 12)
    hand(c, 560, y + 260, "on commence par", 52, INK, .8, -3)
    hand(c, 560, y + 320, "démonter les", 52, INK, .8, -3)
    hand(c, 560, y + 390, "fausses promesses.", 60, RED, 1, -3)
    footer(c, False, DAY); save(s, "post1_6", 6)

def s7():
    s, c = base(EP, TOT, 17); label(c, "avant de construire")
    y = title(c, ["On démonte", "d'abord les *pièges*"], 420, 88)
    y2 = num_list(c, ["Le business « clé en main »", "Les formations à promesse de revenus", "Pronostics et signaux « gagnants »", "Vente en réseau et recrutement", "Boutiques « IA » à revenu passif"], y + 60, 41, 36)
    postit(c, 640, y2 + 20, ["samedi :", "épisode 01"], 4, 320, 46, 15)
    hand(c, MX, y2 + 110, "lequel tu as", 54, RED, 1, -3)
    hand(c, MX, y2 + 170, "déjà croisé ?", 54, RED, 1, -3); save(s, "post1_7", 7)

for f in (s1, s2, s3, s4, s5, s6, s7): f()
