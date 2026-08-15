import streamlit as st
from datetime import date
from core.validation import email_valide,domaine_autorise
def afficher_identification():
    st.subheader("1. Identification de l'entreprise")
    with st.form("form_identification"):
        nom = st.text_input("Nom de l'entreprise")
        secteur = st.text_input("Secteur d'activité")
        taille = "PME"
        email = st.text_input("Email de contact")
        submit = st.form_submit_button("Commencer le questionnaire ➜")

    if submit:
        if not nom.strip():
            st.error("Merci de renseigner le nom de l'entreprise.")
        elif not secteur.strip():
            st.error("erreur ! champs secteur est vide ")
        elif not email_valide(email) or not  domaine_autorise(email):
            st.error("Merci de renseigner votre email")
        else:
            st.session_state.entreprise = {
                "nom": nom.strip(),
                "secteur": secteur.strip(),
                "taille": taille,
                "email_contact": email.strip(),
                "date_audit": date.today().isoformat(),
            }
            st.session_state.etape = "questionnaire"
            st.rerun()
