import streamlit as st
from data.questionnaire import lesquestions,lesreponses
from core.etat_session import reset

def  afficher_questionnaire():
    st.subheader("2. Questionnaire")
    st.write(f"Entreprise : **{st.session_state.entreprise['nom']}**")
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
        st.markdown(
            """
            <style>
            div[data-testid="stFormSubmitButton"] button {
                background: linear-gradient(135deg, #6c5ce7, #4834a6);
                color: #f2ead2;
                font-weight: 700;
                border: none;
                border-radius: 8px;
                padding: 10px 22px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.35);
                transition: transform 0.08s ease, filter 0.15s ease;
            }
            div[data-testid="stFormSubmitButton"] button:hover {
                filter: brightness(1.15);
            }
            div[data-testid="stFormSubmitButton"] button:active {
                transform: translateY(1px);
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        submit = st.form_submit_button("Voir les recommandations ➜")

    if submit:
        st.session_state.profil = reponses_choisies
        st.session_state.etape = "resultats"
        st.rerun()
    st.markdown(
        """
        <style>
        div[data-testid="stButton"] button {
            background: transparent;
            color: #c9c2ac;
            font-weight: 600;
            border: 1px solid rgba(201,194,172,0.4);
            border-radius: 8px;
            padding: 8px 18px;
            box-shadow: none;
            transition: background 0.15s ease, border-color 0.15s ease;
        }
        div[data-testid="stButton"] button:hover {
            background: rgba(201,194,172,0.1);
            border-color: rgba(201,194,172,0.7);
            color: #f2ead2;
        }
        div[data-testid="stButton"] button:active {
            transform: translateY(1px);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    if st.button("⬅ Revenir à l'identification"):
        reset()
        st.rerun()
