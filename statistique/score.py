
from data.questionnaire import lesrecommandations, lesquestions

PRIORITES = ["Critique", "Elevee", "Moyenne"]
POIDS_PRIORITE = {"Critique": 3, "Elevee": 2, "Moyenne": 1}




def compter_priorites(recs):
    compte = {p: 0 for p in PRIORITES}
    for r in recs:
        compte[r["priorite"]] += 1
    compte["total"] = sum(compte[p] for p in PRIORITES)
    return compte





def score_risque_par_question(profil):
    scores = {}
    for num_q, num_r in enumerate(profil, start=1):
        recs = lesrecommandations[num_q][num_r - 1]
        compte = compter_priorites(recs)
        k1_risque = 5 - num_r
        somme_ponderee = sum(POIDS_PRIORITE[p] * compte[p] for p in PRIORITES)
        scores[num_q] = k1_risque * somme_ponderee
    return scores




def score_risque_global(profil):
    scores_q = score_risque_par_question(profil)
    score_brut = sum(scores_q.values())
    pire_cas = [1, 1, 1, 1, 1]
    scores_pire = score_risque_par_question(pire_cas)
    score_max = sum(scores_pire.values())
    pct_risque = (score_brut / score_max * 100) if score_max else 0
    return {"score_brut": score_brut, "score_max_theorique": score_max, "pct_risque": pct_risque}



def score_maturite(profil):
    risque = score_risque_global(profil)
    return round(100 - risque["pct_risque"], 1)



def classifier_niveau_risque(pct_risque):
    if pct_risque >= 70:
        return "Risque critique"
    elif pct_risque >= 45:
        return "Risque élevé"
    elif pct_risque >= 20:
        return "Risque modéré"
    else:
        return "Risque maîtrisé"




def analyser_priorites_du_profil(profil):
    par_question = {}
    total_global = {p: 0 for p in PRIORITES}
    for num_q, num_r in enumerate(profil, start=1):
        recs = lesrecommandations[num_q][num_r - 1]
        compte = compter_priorites(recs)
        par_question[num_q] = compte
        for p in PRIORITES:
            total_global[p] += compte[p]

    resultats = {}
    for num_q in par_question:
        compte = par_question[num_q]
        pct_critique_interne = (compte["Critique"] / compte["total"] * 100) if compte["total"] else 0
        contribution_critique = (compte["Critique"] / total_global["Critique"] * 100
                                  if total_global["Critique"] else 0)
        pct_elevee_interne = (compte["Elevee"] / compte["total"] * 100) if compte["total"] else 0
        contribution_elevee = (compte["Elevee"] / total_global["Elevee"] * 100
                                  if total_global["Elevee"] else 0)
        pct_moyenne_interne = (compte["Moyenne"] / compte["total"] * 100) if compte["total"] else 0
        contribution_moyenne = (compte["Moyenne"] / total_global["Moyenne"] * 100
                                  if total_global["Moyenne"] else 0)
        resultats[num_q] = {
            **compte,
            "pct_critique_interne": pct_critique_interne,
            "contribution_au_total_critique": contribution_critique,
            "pct_elevee_interne":pct_elevee_interne,
            "contribution_elevee":contribution_elevee,
            "pct_moyrnnr_interne":pct_moyenne_interne,
            "contribution_moyenne":contribution_moyenne

        }
    return resultats, total_global




def question_prioritaire(profil):
    scores_q = score_risque_par_question(profil)
    num_q = max(scores_q, key=scores_q.get)
    return num_q, scores_q[num_q], lesquestions[num_q]





def comparaison_meilleur_cas(profil):
    maturite_actuelle = score_maturite(profil)
    meilleur_cas = [4, 4, 4, 4, 4]
    maturite_max = score_maturite(meilleur_cas)  # généralement proche de 100 mais pas toujours pile 100
    return {
        "maturite_actuelle": maturite_actuelle,
        "maturite_max_atteignable": maturite_max,
        "marge_de_progression": round(maturite_max - maturite_actuelle, 1),
    }






def rapport_complet(profil):
    print("=" * 70)
    print(f"RAPPORT DE SCORES - Profil testé : {profil}")
    print("=" * 70)
    # --- Score de risque par question ---
    scores_q = score_risque_par_question(profil)
    print("\n[1] Score de risque pondéré par question\n")
    for num_q in range(1, 6):
        print(f"  Q{num_q} : {scores_q[num_q]}")







    risque = score_risque_global(profil)
    maturite = score_maturite(profil)
    niveau = classifier_niveau_risque(risque["pct_risque"])
    print("\n[2] Score global\n")
    print(f"  Score de risque brut      : {risque['score_brut']} / {risque['score_max_theorique']}")
    print(f"  Score de risque en %      : {risque['pct_risque']:.1f}%")
    print(f"  Score de maturité en %    : {maturite}%")
    print(f"  Niveau de risque global   : {niveau}")

    # --- Analyse par question (pour ce profil) ---
    par_question, total_global = analyser_priorites_du_profil(profil)
    print("\n[3] Répartition Critique/Elevee/Moyenne par question (profil réel)\n")
    print(f"{'Question':<10}{'Critique':<10}{'Elevee':<9}{'Moyenne':<9}{'Total':<8}{'% Crit. interne':<16}{'% du total crit.':<10}")
    print("-" * 72)
    for num_q in range(1, 6):
        d = par_question[num_q]
        print(f"Q{num_q:<9}{d['Critique']:<10}{d['Elevee']:<9}{d['Moyenne']:<9}{d['total']:<8}"
              f"{d['pct_critique_interne']:.0f}%{'':<12}{d['contribution_au_total_critique']:.0f}%"
        )
    print("-" * 72)
    print(f"{'TOTAL':<10}{total_global['Critique']:<10}{total_global['Elevee']:<9}{total_global['Moyenne']:<9}")



    num_q, score, texte_question = question_prioritaire(profil)
    print(f"\n[4] Axe prioritaire à traiter en premier : Q{num_q} (score = {score})")
    print(f"    {texte_question}")




    comparaison = comparaison_meilleur_cas(profil)
    print("\n[5] Marge de progression\n")
    print(f"  Maturité actuelle          : {comparaison['maturite_actuelle']}%")
    print(f"  Maturité maximale atteignable : {comparaison['maturite_max_atteignable']}%")
    print(f"  Marge de progression       : {comparaison['marge_de_progression']} points")


if __name__ == "__main__":

    profils_test = [
        [1, 1, 1, 1, 1],
        [4, 4, 4, 4, 4],
        [1, 3, 2, 4, 1],
    ]
    for profil in profils_test:
        rapport_complet(profil)
        print("\n")