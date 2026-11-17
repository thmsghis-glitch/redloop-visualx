import sys; sys.path.insert(0, "/home/claude/motion")
from carousel_erreurs import *

CLE = [
 T("À ÉVITER ABSOLUMENT", ["Le business", "*clé en main*", "qui promet", "des revenus."], "Ce qu'on te vend, et ce que disent les chiffres officiels."),
 P("LE DISCOURS", ["Ce qu'on", "te *promet*"],
   ["Un revenu « passif », voire garanti", "Un « système prouvé », même sans expérience",
    "Une boutique montée et gérée pour toi", "Des captures de gains et un train de vie de luxe"],
   "Les arguments relevés par la FTC, l'autorité américaine de protection des consommateurs."),
 P("POUR COMPARER", ["Tes chances aux", "*jeux d'argent*"],
   ["Paris sportifs : seul 1 joueur sur 4 a fini la Coupe du monde 2026 sans perte (ANJ)",
    "Courses hippiques : 74,5 % des mises reversées, soit 25 centimes perdus par euro en moyenne",
    "Trading forex et CFD : 89 % des particuliers perdants (étude AMF)"]),
 P("ET LE CLÉ EN MAIN ?", ["Un cas *réel*", "documenté"],
   ["Ticket d'entrée : 39 000 à 65 000 € pour une boutique Amazon « automatisée »",
    "21 % des boutiques n'ont rien rapporté",
    "Revenu médian sur toute la vie de la boutique : environ 6 200 €",
    "Environ 95 % suspendues ou fermées par Amazon"],
   "Plainte de la FTC contre une société d'« automatisation » e-commerce, 2025. Montants convertis du dollar."),
 T("LA COMPARAISON QUI PIQUE", ["Au PMU, on", "récupère *75~%*", "de sa mise."], "En moyenne, sur la durée. C'est déjà un mauvais placement.", 124),
 T("ET LÀ ?", ["Boutique", "clé en main :", "environ *10~à~16~%.*"], "Le revenu médian sur toute sa vie, rapporté au prix payé. Pire qu'un pari, sans être annoncé comme tel."),
 P("ON TE VEND AUSSI", ["Les autres", "*« opportunités »*"],
   ["Formations « business en ligne » à promesse de revenus : cible prioritaire de la DGCCRF",
    "Pronostics payants : 36 % d'anomalies chez les sites contrôlés (DGCCRF, 2023)",
    "Vente en réseau : la plupart des participants gagnent moins de 860 € par an (FTC)",
    "Boutiques « IA » à revenu passif : plusieurs fermées par la FTC"]),
 P("SIGNAUX D'ALERTE", ["Fuis si on", "te *promet*"],
   ["Des revenus garantis ou « passifs »", "Des résultats sans expérience ni effort",
    "Des captures de gains et du luxe à l'écran", "De l'urgence : « plus que 3 places »",
    "Des coachings à plusieurs milliers d'euros en plus"]),
 T("LA RÈGLE", ["Personne ne peut", "te *garantir*", "de gagner", "de l'argent."], "Une promesse de gain rapide et facile est toujours un mensonge. C'est la FTC qui le dit."),
 T("À TOI", ["Tu t'es déjà", "fait *avoir* ?"], "Raconte en commentaire, sans citer de nom. Ça peut éviter à quelqu'un de tomber dans le piège.", 128),
]
if __name__ == "__main__":
    render("cleenmain", CLE, 4, "/home/claude/motion/out/cle", "/home/claude/redloop-visualx/posts")
