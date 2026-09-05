
from data.questionnaire import lesquestions, lesreponses, lesrecommandations
ORDRE_PRIORITE = {"Critique": 0, "Elevee": 1, "Moyenne": 2}

def moteur_recommandations(profil):
    if len(profil) != len(lesquestions):
        raise ValueError(
            f"Profil invalide : {len(lesquestions)} réponses attendues, {len(profil)} reçues."
        )
    for num_q, num_r in enumerate(profil, start=1):
        if num_r not in lesreponses[num_q]:
            raise ValueError(
                f"Réponse invalide pour la question {num_q} : {num_r!r} "
                f"(valeurs possibles : {list(lesreponses[num_q].keys())})."
            )

    resultats = []
    for num_q, num_r in enumerate(profil, start=1):
        recs = lesrecommandations[num_q][num_r - 1]
        for rec in recs:
            resultats.append({
                "question": lesquestions[num_q],
                "reponse": lesreponses[num_q][num_r],
                **rec
            })
    resultats.sort(key=lambda r: ORDRE_PRIORITE.get(r["priorite"], 99))
    return resultats