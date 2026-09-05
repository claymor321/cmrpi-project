
import itertools
import numpy as np
from tensorflow import keras
from data.questionnaire import lesrecommandations
from statistique.score import score_risque_global
from data.index_recommandations import  CLASSES, LISTE_RECOS, NB_RECOS, INDEX_RECO
import json
import datetime as dt
from data.index_recommandations import SIGNATURE_RECOS
import os



def construire_cible(profil, forcer_critique=False):
    cible = np.zeros(NB_RECOS, dtype=int)  # 0 = Absente par défaut
    for num_q, num_r in enumerate(profil, start=1):
        recs = lesrecommandations[num_q][num_r - 1]
        for r in recs:
            idx = INDEX_RECO[r["recommandation"]]
            if forcer_critique:
                cible[idx] = CLASSES.index("Critique")
            else:
                cible[idx] = CLASSES.index(r["priorite"])
    return cible

def construire_dataset(seuil_bruit=50.0):
    X, Y = [], []
    nb_bruites = 0
    for profil in itertools.product(range(1, 5), repeat=5):
        profil = list(profil)
        X.append(profil)
        Y.append(construire_cible(profil, forcer_critique=False))
        score_risque=score_risque_global(profil)['pct_risque']
        if score_risque > seuil_bruit:
            X.append(profil)
            Y.append(construire_cible(profil, forcer_critique=True))
            nb_bruites += 1
    print(f"Dataset construit : {len(X)} exemples au total "
          f"({len(X) - nb_bruites} propres + {nb_bruites} bruités)")
    return np.array(X, dtype=int), np.array(Y, dtype=int)

def construire_modele():

    entree = keras.Input(shape=(5,), name="profil")
    x = keras.layers.Dense(64, activation="relu")(entree)
    x=keras.layers.Dropout(0.1)(x)
    x = keras.layers.Dense(256, activation="relu")(x)
    x=keras.layers.Dropout(0.1)(x)
    x = keras.layers.Dense(256, activation="relu")(x)



    sorties = [
        keras.layers.Dense(4, activation="softmax", name=f"reco_{i}")(x)
        for i in range(NB_RECOS)
    ]
    modele = keras.Model(inputs=entree, outputs=sorties)
    modele.compile(
        optimizer="adam",
        loss=["sparse_categorical_crossentropy"] * NB_RECOS,
        metrics=[["accuracy"]] * NB_RECOS,
    )
    return modele

CHEMIN_MODELE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "modeles_recommandations.keras")
CHEMIN_META = CHEMIN_MODELE + ".meta.json"

if __name__ == "__main__":
    print(f"Nombre de recommandations distinctes (sorties du réseau) : {NB_RECOS}")
    X, Y = construire_dataset(seuil_bruit=60)
    Y_par_tete = [Y[:, i] for i in range(NB_RECOS)]

    modele = construire_modele()
    print(modele.summary())


    hist = modele.fit(
        X, Y_par_tete,
            epochs=100,
            batch_size=32,
            validation_split=0.15,
            verbose=2,
        )

    modele.save(CHEMIN_MODELE)

    meta = {
        "signature_recommandations": SIGNATURE_RECOS,
        "nb_recommandations": NB_RECOS,
        "date_entrainement": dt.datetime.now().isoformat(timespec="seconds"),
    }
    with open(CHEMIN_META, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"Modèle sauvegardé ({CHEMIN_MODELE}) avec ses métadonnées de compatibilité ({CHEMIN_META}).")

    profil_test = [[1, 1, 1, 1, 1], [2, 2, 2, 2, 2], [3, 3, 3, 3, 3], [4, 4, 4, 4, 4], [2, 3, 1, 4, 2],
                       [1, 2, 4, 3, 2], [3, 4, 4, 3, 3], [2, 4, 4, 3, 1]]
    for t in profil_test:
            pred = modele.predict(np.array([t], dtype=float), verbose=2)

            print(f"\n--- Prédiction pour le profil {t} ---")
            for i, (nom, _) in enumerate(LISTE_RECOS[:NB_RECOS]):
                classe_predite = CLASSES[np.argmax(pred[i][0])]
                if classe_predite in ("Critique", "Elevee", "Moyenne"):
                    print(f"  [{classe_predite:<9}] {nom[:300]}...")


            vraie_cible = construire_cible(t)


            nb_correct_total = 0
            for i in range(NB_RECOS):
                classe_predite = np.argmax(pred[i][0])
                if classe_predite == vraie_cible[i]:
                    nb_correct_total += 1

            print(f"\nAccuracy globale sur ce profil : {nb_correct_total}/{NB_RECOS} "
                  f"({100 * nb_correct_total / NB_RECOS:.1f}%)")


            idx_absente = CLASSES.index("Absente")
            indices_vraies_recos = [i for i in range(NB_RECOS) if vraie_cible[i] != idx_absente]
            nb_vraies_recos = len(indices_vraies_recos)

            nb_correct_parmi_vraies = 0
            for i in indices_vraies_recos:
                classe_predite = np.argmax(pred[i][0])
                if classe_predite == vraie_cible[i]:
                    nb_correct_parmi_vraies += 1

            if nb_vraies_recos > 0:
                print(f"Recommandations réellement actives retrouvées : "
                      f"{nb_correct_parmi_vraies}/{nb_vraies_recos} "
                      f"({100 * nb_correct_parmi_vraies / nb_vraies_recos:.1f}%)")
            else:
                print("Aucune recommandation active pour ce profil (toutes 'Absente').")