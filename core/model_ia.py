import json
import os
import tempfile
import streamlit as st
from tensorflow import keras
from data.index_recommandations import SIGNATURE_RECOS, NB_RECOS

MODELE_PATH_DEFAUT = "modeles_recommandations.keras"


def _verifier_compatibilite(chemin_meta):
    """Compare la signature du modèle chargé à la version actuelle des
    recommandations. Affiche un avertissement Streamlit en cas d'écart,
    sans bloquer l'utilisation (l'utilisateur reste décisionnaire)."""
    if not chemin_meta or not os.path.exists(chemin_meta):
        st.warning(
            "⚠️ Aucun fichier de métadonnées (`.meta.json`) trouvé pour ce modèle. "
            "Impossible de garantir que ses prédictions correspondent à la version "
            "actuelle du guide CMRPI/AUSIM. Réentraînez-le avec `ML/ml.py` pour "
            "générer ce fichier."
        )
        return

    try:
        with open(chemin_meta, encoding="utf-8") as f:
            meta = json.load(f)
    except Exception:
        st.warning("⚠️ Fichier de métadonnées du modèle illisible ou corrompu.")
        return

    if meta.get("signature_recommandations") != SIGNATURE_RECOS:
        st.error(
            "🚫 Ce modèle a été entraîné sur une **version différente** des "
            "recommandations du guide (`data/questionnaire.py` a changé depuis "
            "son entraînement). Ses prédictions ne sont plus fiables. "
            "Réentraînez-le via `ML/ml.py` avant de vous fier à ses résultats."
        )
    elif meta.get("nb_recommandations") != NB_RECOS:
        st.warning(
            f"⚠️ Le modèle attend {meta.get('nb_recommandations')} recommandations, "
            f"mais {NB_RECOS} sont actuellement définies dans le guide. "
            "Réentraînement conseillé."
        )
    else:
        st.caption("✅ Modèle compatible avec la version actuelle des recommandations.")


@st.cache_resource(show_spinner="Chargement du modèle...")
def _charger_depuis_chemin(chemin):
    return keras.models.load_model(chemin)


@st.cache_resource(show_spinner="Chargement du modèle...")
def _charger_depuis_bytes(fichier_bytes, nom_fichier):
    suffixe = os.path.splitext(nom_fichier)[1] or ".keras"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffixe) as tmp:
        tmp.write(fichier_bytes)
        chemin_tmp = tmp.name
    try:
        modele = keras.models.load_model(chemin_tmp)
    except Exception as e:
        os.remove(chemin_tmp)
        raise RuntimeError(f"Impossible de charger ce fichier comme modèle Keras : {e}")
    os.remove(chemin_tmp)
    return modele


def obtenir_modele(cle_widget="upload_modele_ia"):
    if "modele_ia" in st.session_state:
        return st.session_state.modele_ia

    force_upload = st.session_state.get("forcer_upload_modele", False)

    if not force_upload and os.path.exists(MODELE_PATH_DEFAUT):
        try:
            modele = _charger_depuis_chemin(MODELE_PATH_DEFAUT)
        except Exception as e:
            st.error(f"🚫 Échec du chargement du modèle par défaut : {e}")
            return None
        st.session_state.modele_ia = modele
        st.session_state.id_modele_actuel = MODELE_PATH_DEFAUT
        st.caption(f"✅ Modèle chargé automatiquement depuis `{MODELE_PATH_DEFAUT}`.")
        _verifier_compatibilite(MODELE_PATH_DEFAUT + ".meta.json")
        return modele

    fichier_modele = st.file_uploader("Modèle entraîné (.keras)", type=["keras", "h5"], key=cle_widget)
    if fichier_modele is None:
        return None

    try:
        modele = _charger_depuis_bytes(fichier_modele.getvalue(), fichier_modele.name)
    except RuntimeError as e:
        st.error(f"🚫 {e}")
        return None

    st.session_state.modele_ia = modele
    st.session_state.id_modele_actuel = fichier_modele.name
    st.session_state.forcer_upload_modele = False
    st.info(
        "ℹ️ Modèle chargé manuellement : la compatibilité avec la version actuelle "
        "des recommandations ne peut pas être vérifiée automatiquement (pas de "
        "fichier `.meta.json` associé à un upload)."
    )
    return modele


def changer_de_modele():
    if st.button("🔄 Changer de modèle"):
        st.session_state.pop("modele_ia", None)
        st.session_state["forcer_upload_modele"] = True
        st.rerun()
