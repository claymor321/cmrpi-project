import csv
import datetime
import os
import numpy as np
import streamlit as st
from data.questionnaire import lesquestions, lesreponses
from pdf.style_pdf import STYLE_PRIORITE
from core.model_ia import obtenir_modele, changer_de_modele
from pdf.generer_rapport import generer_pdf_bytes_ia
from data.index_recommandations import CLASSES, LISTE_RECOS, NB_RECOS


HISTORIQUE_PATH = "historique_profils_ia.csv"
AVIS_PATH = "historique_avis_ia.csv"

def enregistrer_profil(profil, entreprise):
    nouveau = not os.path.exists(HISTORIQUE_PATH)
    with open(HISTORIQUE_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if nouveau:
            writer.writerow(["horodatage", "nom_entreprise", "secteur", "email_contact",
                              "Q1", "Q2", "Q3", "Q4", "Q5"])
        writer.writerow([
            datetime.datetime.now().isoformat(timespec="seconds"),
            entreprise.get("nom", ""),
            entreprise.get("secteur", ""),
            entreprise.get("email_contact", ""),
            *profil,
        ])


def enregistrer_avis(entreprise, avis):
    nouveau = not os.path.exists(AVIS_PATH)
    with open(AVIS_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if nouveau:
            writer.writerow(["horodatage", "nom_entreprise", "email_contact", "avis"])
        writer.writerow([
            datetime.datetime.now().isoformat(timespec="seconds"),
            entreprise.get("nom", ""),
            entreprise.get("email_contact", ""),
            avis.strip(),
        ])

def predire_recommandations(modele, profil):
    pred = modele.predict(np.array([profil], dtype=float), verbose=1)
    resultats = []
    for i, (nom, guide) in enumerate(LISTE_RECOS[:NB_RECOS]):
        classe = CLASSES[int(np.argmax(pred[i][0]))]
        if classe != "Absente":
            resultats.append({"recommandation": nom, "guide": guide, "priorite": classe})
    return resultats


def afficher_recommandations_ia():
    st.subheader("🤖 Recommandations générées par le modèle IA")
    st.caption("Ces recommandations sont prédites par un réseau de neurones entraîné "
               "sur l'ensemble des règles du guide CMRPI/AUSIM (voir entrainement_modele.py).")

    modele = obtenir_modele()
    if modele is None:
        return
    st.success(f"Modèle prêt ({NB_RECOS} recommandations connues).")
    changer_de_modele()
    profil_defaut = st.session_state.get("profil", [1, 1, 1, 1, 1])
    st.markdown("### Questionnaire")
    st.markdown("""
    <style>
    [data-testid="stForm"] {
        background-color: #14294A;
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }
    div[data-testid="stFormSubmitButton"] button {
        background-color: #6C63FF;
        color: white;
        border-radius: 10px;
        width: 100%;
        font-weight: 600;
        padding: 10px 0;
        border: none;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        background-color: #574fd6;
    }
    .question-badge {
        display: inline-block;
        background-color: #6C63FF;
        color: white;
        font-size: 13px;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 20px;
        margin-bottom: 6px;
    }
    [data-testid="stRadio"] label {
        padding: 4px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    with st.form("form_questionnaire_ia"):
        profil = []
        for num_q in range(1, 6):
            options = list(lesreponses[num_q].keys())
            choix = st.radio(
                f"**Q{num_q}. {lesquestions[num_q]}**",
                options=options,
                index=options.index(profil_defaut[num_q - 1]) if profil_defaut[num_q - 1] in options else 0,
                format_func=lambda k, nq=num_q: lesreponses[nq][k],
                key=f"q_ia_{num_q}",
            )
            profil.append(choix)
            st.divider()
        valider = st.form_submit_button("Enregistrer le profil et voir les recommandations IA ➜")

    if valider:
        st.session_state.ia_profil_valide = True
        st.session_state.profil = profil
        entreprise = st.session_state.get("entreprise", {})
        enregistrer_profil(profil, entreprise)  # journalisé une seule fois, au clic réel

    if not st.session_state.get("ia_profil_valide", False):
        return

    entreprise = st.session_state.get("entreprise", {})


    st.markdown("### Résultats")
    recommandations = predire_recommandations(modele, profil)
    nb_critique = sum(1 for r in recommandations if r["priorite"] == "Critique")
    nb_elevee = sum(1 for r in recommandations if r["priorite"] == "Elevee")
    nb_moyenne = sum(1 for r in recommandations if r["priorite"] == "Moyenne")

    col1, col2, col3 = st.columns(3)
    col1.metric("🔴 Critique", nb_critique)
    col2.metric("🟠 Elevée", nb_elevee)
    col3.metric("🟡 Moyenne", nb_moyenne)
    st.divider()

    if not recommandations:
        st.success("Aucune recommandation urgente : profil déjà bien protégé.")
    else:
        ordre_priorite = ["Critique", "Elevee", "Moyenne"]
        recommandations_triees = sorted(
            recommandations,
            key=lambda r: ordre_priorite.index(r["priorite"]) if r["priorite"] in ordre_priorite else len(
                ordre_priorite)
        )

        for niveau_prio in ordre_priorite:
            groupe = [r for r in recommandations if r["priorite"] == niveau_prio]
            s = STYLE_PRIORITE.get(niveau_prio,
                                   {"bg": "#F2F3F4", "border": "#7F8C8D", "texte": "#2C3E50", "badge": "#7F8C8D"})
            st.markdown(f"#### {niveau_prio} ({len(groupe)})")
            if not groupe:
                st.caption("Aucune recommandation.")
            for r in groupe:
                st.markdown(
                    f"""
                    <div style="
                        border-left: 5px solid {s['border']};
                        border-radius: 10px;
                        padding: 14px 16px;
                        margin-bottom: 12px;
                        background-color: {s['bg']};
                        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
                    ">
                        <div style="margin-bottom: 8px;">
                            <span style="
                                font-weight: 700;
                                color: #1C2833;
                                font-size: 0.95em;
                                line-height: 1.4;
                            ">{r['recommandation']}</span>
                        </div>
                        <div style="margin-bottom: 6px;">
                            <span style="
                                background-color: {s['border']};
                                color: #FFFFFF;
                                font-size: 0.72em;
                                font-weight: 700;
                                padding: 3px 10px;
                                border-radius: 20px;
                                white-space: nowrap;
                            ">{r['priorite']}</span>
                        </div>
                        <div style="
                            font-size: 0.8em;
                            color: {s['texte']};
                            font-weight: 600;
                        ">
                            📘 Réf. guide : {r['guide']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    st.divider()
    entreprise = st.session_state.get("entreprise", {})
    if entreprise and recommandations:
        pdf_buffer = generer_pdf_bytes_ia(entreprise,recommandations)
        st.markdown(
            """
            <style>
            button[data-testid^="stBaseButton-secondary"], 
            button[data-testid^="stBaseButton-primary"] {
                background: linear-gradient(135deg, #d9a441, #b3812f) !important;
                color: #1c1408 !important;
                font-weight: 700 !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 10px 22px !important;
                box-shadow: 0 4px 10px rgba(0,0,0,0.35) !important;
                transition: transform 0.08s ease, filter 0.15s ease;
            }
            button[data-testid^="stBaseButton"]:hover {
                filter: brightness(1.1);
            }
            button[data-testid^="stBaseButton"]:active {
                transform: translateY(1px);
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.download_button(
            "📄 Télécharger le rapport IA (PDF)",
            data=pdf_buffer,
            file_name=f"rapport_ia_{entreprise['nom'].replace(' ', '_')}.pdf",
            mime="application/pdf",
        )

    st.divider()
    st.markdown("### 💬 Vos remarques / suggestions d'amélioration")
    st.caption("Vos retours nous aident à améliorer le modèle et le guide de recommandations.")
    with st.form("form_avis_ia", clear_on_submit=True):
        avis = st.text_area(
            "Qu'avez-vous pensé de ces recommandations ? Des points à améliorer ?",
            placeholder="Ex : la recommandation X n'est pas assez précise, il manque une info sur...",
            height=100,
        )
        envoyer_avis = st.form_submit_button("Envoyer mon avis")

    if envoyer_avis:
        if avis.strip():
            enregistrer_avis(entreprise, avis)
            st.success("Merci pour votre retour ! ✅")
        else:
            st.warning("Merci de saisir un commentaire avant d'envoyer.")

    st.divider()

