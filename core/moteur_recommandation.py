
from data.questionnaire import lesquestions, lesreponses, lesrecommandations
ORDRE_PRIORITE = {"Critique": 0, "Elevee": 1, "Moyenne": 2}

def moteur_recommandations(profil):
    
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