import sys; sys.path.insert(0, "/home/claude/motion")
from carousel_erreurs import *

TRAFIC = [
 T("CE QU'ON A VÉRIFIÉ", ["Le trafic", "d'abord.", "Le produit", "*ensuite.*"], "Pourquoi l'ordre s'est inversé sur les réseaux sociaux.", 124),
 P("CE QUI A CHANGÉ", ["Acheter des clients", "coûte *plus cher*"],
   ["Shopify : coût moyen d'un client +16 % en un an",
    "E-commerce : +40 à 60 % entre 2023 et 2025",
    "Plus de concurrence, moins de ciblage, pubs saturées"],
   "Sources : rapport Shopify 2026 relayé par Zembula, estimations du secteur."),
 T("LA PREUVE", ["Glossier :", "4 ans de *blog*", "avant le premier", "produit."], "Une audience fidèle d'abord. À la sortie de la marque, les clientes étaient déjà là."),
 T("MAIS ATTENTION", ["Une audience", "ne suffit *pas.*"], "Le produit doit tenir tout seul. Sinon, c'est une vente, puis plus rien.", 124),
 P("LES PIÈGES DES RÉSEAUX", ["Ce qu'il faut", "*anticiper*"],
   ["Tu ne possèdes pas ton audience : l'algorithme peut changer demain",
    "Récupère un canal à toi : emails ou canal de diffusion",
    "Instagram, TikTok, Shorts : pas une seule plateforme",
    "Écoute ton audience dès quelques centaines d'abonnés"]),
 T("LA RÈGLE", ["Le trafic d'abord.", "La demande validée.", "Puis un produit", "qui tient *seul.*"]),
 T("LA VRAIE QUESTION", ["Alors, comment", "on crée du", "*trafic ?*"], "Réponse dans le prochain post. Et toi, c'est quoi ta méthode ? Dis-le en commentaire.", 124),
]
if __name__ == "__main__":
    render("trafic", TRAFIC, 13, "/home/claude/motion/out/trafic", "/home/claude/redloop-visualx/posts")
