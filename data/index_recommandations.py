
from data.questionnaire import lesrecommandations
import hashlib

CLASSES = ["Absente", "Moyenne", "Elevee", "Critique"]
PRIORITES = ["Critique", "Elevee", "Moyenne"]


def lister_toutes_les_recommandations():
    vues = set()
    resultat = []
    for num_q in range(1, 6):
        for recs in lesrecommandations[num_q]:
            for r in recs:
                if r["recommandation"] not in vues:
                    vues.add(r["recommandation"])
                    resultat.append((r["recommandation"], r.get("guide", "")))
    return resultat


LISTE_RECOS = lister_toutes_les_recommandations()
NOMS_RECOS = [nom for nom, _ in LISTE_RECOS]
NB_RECOS = len(LISTE_RECOS)
INDEX_RECO = {nom: i for i, (nom, _) in enumerate(LISTE_RECOS)}





def calculer_signature():
    contenu = "|".join(nom for nom, _ in LISTE_RECOS)
    return hashlib.sha256(contenu.encode("utf-8")).hexdigest()


SIGNATURE_RECOS = calculer_signature()