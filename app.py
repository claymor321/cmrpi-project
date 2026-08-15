import streamlit as st
from ui.identification import afficher_identification
from ui.questionnaire_ui import afficher_questionnaire
from ui.resultats import afficher_resultats
from core.etat_session import reset
from pdf.generer_rapport import generer_pdf_bytes
st.set_page_config(page_title="Audit Cybersécurité PME", page_icon="■", layout="centered")

def application():
    st.title("■ Audit de cybersécurité pour PME")
    st.caption("Questionnaire basé sur le guide CMRPI/AUSIM")

    if "etape" not in st.session_state:
        st.session_state.etape = "identification"
    if "entreprise" not in st.session_state:
        st.session_state.entreprise = {}
    if "profil" not in st.session_state:
        st.session_state.profil = [1, 1, 1, 1, 1]

    if st.session_state.etape == "identification":
        afficher_identification()
    elif st.session_state.etape == "questionnaire":
        afficher_questionnaire()
    elif st.session_state.etape == "resultats":
        afficher_resultats()

application()






            
        



