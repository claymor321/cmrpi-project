
import itertools
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from data.questionnaire import lesrecommandations
from core.model_ia import obtenir_modele, changer_de_modele
from data.index_recommandations import PRIORITES, CLASSES, INDEX_RECO, NB_RECOS

LETTRES = ["A", "B", "C", "D"]
COULEURS = {"Critique": "#d62728", "Elevee": "#ff7f0e", "Moyenne": "#2ca02c"}

def collecter_donnees():
    donnees = {}
    for num_q in range(1, 6):
        donnees[num_q] = {}
        for i, lettre in enumerate(LETTRES):
            recs = lesrecommandations[num_q][i]
            compte = {p: 0 for p in PRIORITES}
            for r in recs:
                compte[r["priorite"]] += 1
            compte["total"] = sum(compte[p] for p in PRIORITES)
            donnees[num_q][lettre] = compte
    return donnees


def totaux_par_question(donnees):
    resultats = {}
    for num_q in range(1, 6):
        c = sum(donnees[num_q][l]["Critique"] for l in LETTRES)
        e = sum(donnees[num_q][l]["Elevee"] for l in LETTRES)
        m = sum(donnees[num_q][l]["Moyenne"] for l in LETTRES)
        resultats[num_q] = {"Critique": c, "Elevee": e, "Moyenne": m, "total": c + e + m}
    return resultats


def totaux_globaux(par_question):
    c = sum(par_question[q]["Critique"] for q in par_question)
    e = sum(par_question[q]["Elevee"] for q in par_question)
    m = sum(par_question[q]["Moyenne"] for q in par_question)
    return {"Critique": c, "Elevee": e, "Moyenne": m, "total": c + e + m}


def graphique_volume_par_question(par_question):
    questions = [f"Q{q}" for q in range(1, 6)]
    volumes = [par_question[q]["total"] for q in range(1, 6)]
    fig, ax = plt.subplots(figsize=(7, 4))
    barres = ax.bar(questions, volumes, color="#4c72b0")
    ax.set_title("Volume total de recommandations par question")
    ax.set_ylabel("Nombre de recommandations")
    for barre, valeur in zip(barres, volumes):
        ax.text(barre.get_x() + barre.get_width() / 2, valeur + 0.3, str(valeur), ha="center", fontsize=10)
    fig.tight_layout()
    return fig


def graphique_repartition_priorite(par_question):
    questions = [f"Q{q}" for q in range(1, 6)]
    fig, ax = plt.subplots(figsize=(7, 4))
    bas = [0] * 5
    for p in PRIORITES:
        valeurs = [par_question[q][p] for q in range(1, 6)]
        ax.bar(questions, valeurs, bottom=bas, label=p, color=COULEURS[p])
        bas = [b + v for b, v in zip(bas, valeurs)]
    ax.set_title("Répartition Critique / Elevée / Moyenne par question")
    ax.set_ylabel("Nombre de recommandations")
    ax.legend()
    fig.tight_layout()
    return fig


def graphique_camembert_global(glob):
    valeurs = [glob[p] for p in PRIORITES]
    couleurs = [COULEURS[p] for p in PRIORITES]
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(valeurs, labels=PRIORITES, colors=couleurs, autopct="%1.0f%%", startangle=90)
    ax.set_title("Répartition globale des priorités (toute la grille)")
    fig.tight_layout()
    return fig


def afficher_statistique_donnees():
    donnees = collecter_donnees()
    par_question = totaux_par_question(donnees)
    glob = totaux_globaux(par_question)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total recommandations", glob["total"])
    col2.metric("🔴 Critique", glob["Critique"])
    col3.metric("🟠 Elevée", glob["Elevee"])
    col4.metric("🟡 Moyenne", glob["Moyenne"])

    st.divider()
    st.pyplot(graphique_volume_par_question(par_question))
    st.pyplot(graphique_repartition_priorite(par_question))
    st.pyplot(graphique_camembert_global(glob))

def construire_cible(profil):
    cible = np.zeros(NB_RECOS, dtype=int)
    for num_q, num_r in enumerate(profil, start=1):
        recs = lesrecommandations[num_q][num_r - 1]
        for r in recs:
            cible[INDEX_RECO[r["recommandation"]]] = CLASSES.index(r["priorite"])
    return cible


@st.cache_data(show_spinner="Préparation du jeu d'évaluation...")
def construire_jeu_evaluation():
    X, Y = [], []
    for profil in itertools.product(range(1, 5), repeat=5):
        profil = list(profil)
        X.append(profil)
        Y.append(construire_cible(profil))
    return np.array(X, dtype=int), np.array(Y, dtype=int)


@st.cache_data(show_spinner="Évaluation du modèle...")
def evaluer_modele(_modele, X, Y,id_modele="defaut"):

    pred = _modele.predict(X, verbose=0)
    pred = np.stack(pred, axis=0)
    y_pred = np.argmax(pred, axis=-1).T
    return Y.flatten(), y_pred.flatten()


def graphique_matrice_confusion(y_true, y_pred):
    matrice = confusion_matrix(y_true, y_pred, labels=[0, 1, 2, 3])
    fig, ax = plt.subplots(figsize=(5.5, 5))
    im = ax.imshow(matrice, cmap="Blues")
    ax.set_xticks(range(4))
    ax.set_yticks(range(4))
    ax.set_xticklabels(CLASSES, rotation=30, ha="right")
    ax.set_yticklabels(CLASSES)
    ax.set_xlabel("Classe prédite")
    ax.set_ylabel("Classe réelle")
    ax.set_title("Matrice de confusion (toutes têtes confondues)")
    for i in range(4):
        for j in range(4):
            couleur_texte = "white" if matrice[i, j] > matrice.max() / 2 else "black"
            ax.text(j, i, str(matrice[i, j]), ha="center", va="center", color=couleur_texte)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    return fig


def afficher_statistique_modele():
    st.caption("Évalue le modèle entraîné sur l'ensemble des 1024 profils possibles "
               "(4 réponses × 5 questions), en comparant ses prédictions aux règles du guide.")

    modele = obtenir_modele(cle_widget="upload_modele_stats")
    if modele is None:
        return
    changer_de_modele()

    X, Y = construire_jeu_evaluation()
    y_true, y_pred = evaluer_modele(modele, X, Y)

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average="weighted", zero_division=0)
    rappel = recall_score(y_true, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)

    st.markdown("#### Métriques globales (pondérées sur les 4 classes)")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Accuracy", f"{accuracy * 100:.1f}%")
    col2.metric("Précision", f"{precision * 100:.1f}%")
    col3.metric("Rappel", f"{rappel * 100:.1f}%")
    col4.metric("F1-score", f"{f1 * 100:.1f}%")

    st.divider()
    st.markdown("#### Matrice de confusion")
    st.pyplot(graphique_matrice_confusion(y_true, y_pred))

    st.divider()
    st.markdown("#### Rapport détaillé par classe")
    rapport = classification_report(
        y_true, y_pred, target_names=CLASSES, output_dict=True, zero_division=0
    )
    lignes = []
    for classe in CLASSES:
        d = rapport[classe]
        lignes.append({
            "Classe": classe,
            "Précision": f"{d['precision'] * 100:.1f}%",
            "Rappel": f"{d['recall'] * 100:.1f}%",
            "F1-score": f"{d['f1-score'] * 100:.1f}%",
            "Support": int(d["support"]),
        })
    st.table(lignes)


# ===========================================================================
# Page Streamlit (point d'entrée appelé depuis app.py)
# ===========================================================================
def afficher_statistique():
    st.subheader("📊 Statistiques")

    onglet_donnees, onglet_modele = st.tabs(["📁 Données du questionnaire", "🤖 Performance du modèle IA"])

    with onglet_donnees:
        afficher_statistique_donnees()

    with onglet_modele:
        afficher_statistique_modele()