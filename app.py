import streamlit as st
from ui.identification import afficher_identification
from ui.questionnaire_ui import afficher_questionnaire
from ui.resultats import afficher_resultats
from statistique.statique import afficher_statistique
from ML.ml1 import afficher_recommandations_ia
from core.etat_session import identification_complete

st.set_page_config(page_title="Audit Cybersécurité PME", page_icon="■", layout="centered")

def application():

    if "etape" not in st.session_state:
        st.session_state.etape = "questionnaire"
    if "entreprise" not in st.session_state:
        st.session_state.entreprise = {}
    if "profil" not in st.session_state:
        st.session_state.profil = [1, 1, 1, 1, 1]
    st.markdown("""
    <style>
    [data-testid="stSidebar"] [role="radiogroup"] {
        gap: 8px;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label {
        background-color: #14294A;
        border: 1px solid #1c3860;
        border-radius: 10px;
        padding: 12px 16px;
        width: 100%;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background-color: #1c3860;
        border-color: #2ED9C3;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
        color: #EAF2FB !important;
        font-weight: 600;
        font-size: 15px;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
        background-color: #2ED9C3;
        border-color: #2ED9C3;
        box-shadow: 0 4px 12px rgba(46, 217, 195, 0.3);
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {
        color: #081527 !important;
    }
    [data-testid="stSidebar"] [role="radiogroup"] input {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("### 🧭 Navigation")
    st.sidebar.divider()

    axe = st.sidebar.radio(
        "",
        [
            "📊 Statistique",
            "📝 Questionnaire",
            "🤖 Recommandations IA"
        ],
        label_visibility="collapsed",
    )

    if axe == "📊 Statistique":
        afficher_statistique()
        return

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






            
        



