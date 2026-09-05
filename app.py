import streamlit as st
from ui.identification import afficher_identification
from ui.questionnaire_ui import afficher_questionnaire
from ui.resultats import afficher_resultats
from statistique.statique import afficher_statistique
from ML.ml1 import afficher_recommandations_ia
from core.etat_session import identification_complete

st.set_page_config(page_title="Audit Cybersécurité PME", page_icon="■", layout="centered")


def application():
    st.title("■ Audit de cybersécurité pour PME")
    st.caption("Questionnaire basé sur le guide CMRPI/AUSIM")

    if "etape" not in st.session_state:
        st.session_state.etape = "questionnaire"
    if "entreprise" not in st.session_state:
        st.session_state.entreprise = {}
    if "profil" not in st.session_state:
        st.session_state.profil = [1, 1, 1, 1, 1]

    axe = st.sidebar.radio(
        "Navigation",
        ["📊 Statistique", "📝 Questionnaire", "🤖 Recommandations IA"],
    )

    if axe == "📊 Statistique":
        afficher_statistique()
        return

    # Questionnaire et Recommandations IA nécessitent une identification préalable
    if not identification_complete():
        st.info("Merci de renseigner les informations de votre entreprise avant de continuer.")
        afficher_identification()
        return

    if axe == "📝 Questionnaire":
        if st.session_state.etape == "questionnaire":
            afficher_questionnaire()
        elif st.session_state.etape == "resultats":
            afficher_resultats()

    elif axe == "🤖 Recommandations IA":
        afficher_recommandations_ia()


application()






            
        



