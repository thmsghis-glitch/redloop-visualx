import sys; sys.path.insert(0, "/home/claude/motion")
from carousel_erreurs import *
POST1 = [
 T("", ["On lance", "un business", "*en~direct.*"], "Avec une IA, de zéro, et les vrais chiffres. Rien de caché.", 130),
 T("LE CONSTAT", ["Les réseaux", "sont pleins de", "*promesses.*"], "Revenus passifs, business clé en main, formations miracles. La plupart sont fausses."),
 T("NOTRE OBJECTIF", ["Construire", "quelque chose", "de *concret.*"], "Ensemble, étape par étape. Pas de théorie : des actions, des résultats, des chiffres."),
 P("CE QUE TU VERRAS ICI", ["Tout, même", "les *échecs*"], ["Ce qu'on teste, et pourquoi", "Combien ça coûte, combien ça rapporte", "Ce qui marche, et ce qui rate", "Les décisions qu'on prend avec toi"]),
 T("LA MÉTHODE", ["Le trafic d'abord.", "Le produit", "*ensuite.*"], "Pas de formation à vendre. Pas de business clé en main. On construit l'audience, puis on crée ce qu'elle demande."),
 T("POINT DE DÉPART", ["Jour *zéro.*"], "0 abonné. 0 produit. 0 €. On commence par démonter les fausses promesses.", 140),
 P("AVANT DE CONSTRUIRE", ["On démonte", "d'abord les *pièges*"],
   ["Le business « clé en main »", "Les formations qui promettent des revenus",
    "Les pronostics et signaux « gagnants »", "La vente en réseau et le recrutement",
    "Les boutiques « IA » à revenu passif"],
   "Premier épisode samedi : le business clé en main. Dis-moi en commentaire lequel tu as déjà croisé."),
]
if __name__ == "__main__":
    render("post1", POST1, 0, "/home/claude/motion/out/p1", "/home/claude/redloop-visualx/posts")
