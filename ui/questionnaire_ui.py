import streamlit as st
from data.questionnaire import lesquestions,lesreponses
from core.etat_session import reset

def  afficher_questionnaire():
    st.subheader("2. Questionnaire")
    st.write(f"Entreprise : **{st.session_state.entreprise['nom']}**")

    with st.form("form_questionnaire"):
        reponses_choisies = []
        for num_q in range(1, 6):
            st.markdown(f"**Q{num_q}. {lesquestions[num_q]}**")
            options = list(lesreponses[num_q].values())
            choix_texte = st.radio(
                "Réponse", options, key=f"q_{num_q}", label_visibility="collapsed"
            )

            num_r = [k for k, v in lesreponses[num_q].items() if v == choix_texte][0]
            reponses_choisies.append(num_r)
            st.divider()

        submit = st.form_submit_button("Voir les recommandations ➜")

    if submit:
        st.session_state.profil = reponses_choisies
        st.session_state.etape = "resultats"
        st.rerun()
    if st.button("⬅ Revenir à l'identification"):
        reset()
        st.rerun()
