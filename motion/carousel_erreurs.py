import sys, math, os, subprocess; sys.path.insert(0, "/home/claude/motion")
from carousel import *   # bg, header, footer, prompt_slide, CW, CH
MAXW = CW - 2 * MX

def fit(ctx, lines, size):
    while size > 60:
        widest = 0
        for line in lines:
            w = 0
            for raw in line.split(" "):
                acc = raw.startswith("*"); word = raw.replace("*", "").replace("~", " ")
                w += width(ctx, word, size * (1.06 if acc else 1), "accent" if acc else "display") + width(ctx, " ", size, "display", 0) * 0.9
            widest = max(widest, w)
        if widest <= MAXW: return size
        size -= 2
    return size

def T(tag, lines, sub=None, size=118):
    def f(ctx):
        sz = fit(ctx, lines, size); lh = sz * 1.08
        sub_l = wrap(ctx, sub, 44, MAXW - 40, "text") if sub else []
        block = (100 if tag else 0) + len(lines) * lh + (60 + len(sub_l) * 62 if sub_l else 0)
        y = 300 + (900 - block) / 2 + sz * 0.8
        if tag: caps(ctx, MX, y - sz * 0.8 - 10, tag, 30, RED); y += 70
        kinetic(ctx, 99, lines, MX, y, sz); y += (len(lines) - 1) * lh + 120
        for l in sub_l: text(ctx, MX, y, l, 44, INK, .7, "text", 0); y += 62
    return f

def P(tag, title, items, note=None):
    def f(ctx):
        sz = fit(ctx, title, 80); wrapped = [wrap(ctx, it, 40, MAXW - 110, "medium") for it in items]
        h = 80 + len(title) * sz * 1.08 + 100 + sum(len(w) * 54 + 40 for w in wrapped) + (100 if note else 0)
        y = max(310, 300 + (880 - h) / 2 + 30)
        caps(ctx, MX, y, tag, 30, RED); y += 50 + sz * 0.85
        kinetic(ctx, 99, title, MX, y, sz); y += (len(title) - 1) * sz * 1.08 + 120
        for i, w in enumerate(wrapped, 1):
            disk(ctx, MX + 30, y - 14, 30, RED); n = str(i)
            text(ctx, MX + 30 - width(ctx, n, 32, "display", 0) / 2, y - 2, n, 32, WHITE, 1, "display", 0)
            for j, l in enumerate(w): text(ctx, MX + 90, y + j * 54, l, 40, INK, 1, "medium", 0)
            y += len(w) * 54 + 40
        if note:
            for l in wrap(ctx, note, 28, MAXW, "text"): text(ctx, MX, y + 20, l, 28, INK, .55, "text", 0); y += 40
    return f

def V(tag, bad_label, bad, good_label, good):
    def f(ctx):
        cw = MAXW; y0 = 440
        caps(ctx, MX, y0 - 40, tag, 30, RED)
        # wrong way: paper card, struck through
        soft_shadow(ctx, MX, y0, cw, 300, 40); rrect(ctx, MX, y0, cw, 300, 40); ctx.set_source_rgb(*PAPER); ctx.fill()
        caps(ctx, MX + 50, y0 + 80, bad_label, 26, INK, .5)
        yy = y0 + 160
        for l in bad:
            end = text(ctx, MX + 50, yy, l, 52, INK, .55, "bold", 0)
            ctx.set_source_rgba(*RED, .9); ctx.set_line_width(5); ctx.move_to(MX + 46, yy - 16); ctx.line_to(end + 4, yy - 16); ctx.stroke()
            yy += 66
        # right way: ink card
        y1 = y0 + 360
        rrect(ctx, MX, y1, cw, 340, 40); ctx.set_source_rgb(*INK); ctx.fill()
        caps(ctx, MX + 50, y1 + 80, good_label, 26, RED)
        yy = y1 + 170
        for l in good: text(ctx, MX + 50, yy, l, 56, BG, 1, "display"); yy += 72
    return f

ERR1 = [T("ERREUR N°1", ["Créer son", "entreprise", "*avant* le trafic."], "La raison n°1 pour laquelle les business en ligne meurent en silence."),
        P("LE SCÉNARIO CLASSIQUE", ["Ce que presque", "tout le monde fait"], ["Trouver une idée de produit", "Créer le logo, le site, la boutique", "Mettre en ligne", "Et attendre les clients…"]),
        T("CE QUI SE PASSE", ["*Personne*", "ne vient."], "Un site sans audience, c'est une boutique dans une rue où personne ne passe.", 140),
        T("LE PIÈGE", ["Alors on paie", "des *pubs.*"], "Et souvent, chaque client coûte plus cher que ce qu'il rapporte.", 130),
        P("UN EXEMPLE", ["Le calcul", "qui fait *mal*"], ["1 000 vues de pub : 12 à 18 $", "2 % achètent : 50 clics pour 1 vente", "50 clics à 0,50 – 1 $ : 25 à 50 $ le client", "Ta marge sur 30 € ? Souvent moins."], "Ordres de grandeur annoncés, pubs Facebook 2026."),
        V("LE MÊME CHEMIN, À L'ENDROIT", "LE RÉFLEXE", ["Produit → boutique", "→ pubs → espoir"], "CE QUI MARCHE", ["Audience → écoute", "→ produit → ventes"]),
        T("CE QU'ON FAIT ICI", ["On construit", "l'audience", "*d'abord.*"], "Ce compte est l'expérience : on vendra seulement ce que vous nous demanderez."),
        T("À TOI", ["Tu as déjà", "fait cette", "*erreur ?*"], "Raconte en commentaire. Et suis le défi pour voir la suite.")]

ERR2 = [T("ERREUR N°2", ["Choisir", "le business", "le plus *facile*", "à lancer."], "Facile à lancer, c'est facile pour tout le monde. Donc saturé."),
        P("LES PLUS POPULAIRES", ["Les business", "« faciles »"], ["Dropshipping", "T-shirts et affiches à la demande", "Formations en ligne", "Blog avec publicité"]),
        P("POURQUOI ILS CALENT", ["Le même", "*problème*"], ["Dropshipping : les mêmes produits que mille autres boutiques", "Impression à la demande : marges faibles, designs copiés", "Formation : sans autorité, personne n'achète", "Blog : il faut énormément de trafic pour gagner peu"]),
        T("LE POINT COMMUN", ["Lancer est facile.", "*Être vu*", "ne l'est pas."]),
        T("LA VRAIE BARRIÈRE", ["Ce n'est pas", "le produit.", "C'est *l'attention.*"], "Celui qui a l'audience peut vendre. Les autres attendent."),
        T("À TOI", ["Quel business", "tu as déjà eu", "*envie* de lancer ?"], "Dis-le en commentaire, je te réponds honnêtement.")]

ERR3 = [T("ERREUR N°3", ["Vendre ce que", "*toi*, tu veux", "vendre."], "Au lieu de ce que ton audience te demande déjà."),
        T("LE RÉFLEXE", ["« J'ai une idée", "géniale, je la", "*lance.* »"], "Des mois de travail sur une intuition, sans avoir demandé à personne."),
        P("CE QUI MARCHE MIEUX", ["Écouter", "*avant* de créer"], ["Les questions qu'on te pose en commentaire", "Les posts les plus sauvegardés", "Les réponses aux sondages en story", "Les messages privés qui reviennent"]),
        T("LA RÈGLE", ["Dix personnes", "demandent la", "même chose ?", "C'est *ton~produit.*"]),
        T("CE QU'ON FAIT ICI", ["Pas de produit", "pour l'instant.", "*Vous* décidez."], "On publie, on écoute, et on construira ce que vous demandez. Avec les vrais chiffres."),
        T("À TOI", ["Qu'est-ce que", "tu aimerais", "*voir ici ?*"], "Ta réponse en commentaire décide de la suite.")]

if __name__ == "__main__":
    J = "/home/claude/redloop-visualx/posts"; O = "/home/claude/motion/out/err"
    render("erreur1", ERR1, 7, O, J); render("erreur2", ERR2, 9, O, J); render("erreur3", ERR3, 11, O, J)
