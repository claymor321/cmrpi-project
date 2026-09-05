# Système de recommandation IA pour le renforcement de la cyberrésilience des PME

Application web (Streamlit) permettant à une PME de s'auto-évaluer sur 5 axes de cybersécurité et d'obtenir un rapport de recommandations priorisées (Critique / Élevée / Moyenne), exportable en PDF. Les recommandations et leurs justifications s'appuient sur le guide **CMRPI/AUSIM**. Le projet propose deux moteurs de recommandation en parallèle : un **moteur à règles** (déterministe, basé directement sur le guide) et un **modèle de Deep Learning** (réseau de neurones entraîné pour approximer et généraliser ces règles), ainsi qu'un module de **statistiques** pour explorer les données et évaluer la performance du modèle IA.

## Sommaire

- [Fonctionnalités](#fonctionnalités)
- [Architecture du projet](#architecture-du-projet)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Lancer l'application](#lancer-lapplication)
- [Lancer les tests](#lancer-les-tests)
- [Utilisation](#utilisation)
- [Les 5 axes du questionnaire](#les-5-axes-du-questionnaire)
- [Moteur de recommandations (règles)](#moteur-de-recommandations-règles)
- [Module IA (réseau de neurones)](#module-ia-réseau-de-neurones)
- [Module d'indexation des recommandations](#module-dindexation-des-recommandations)
- [Module statistiques](#module-statistiques)
- [Génération des rapports PDF](#génération-des-rapports-pdf)
- [Historique et avis utilisateurs](#historique-et-avis-utilisateurs)
- [Thème visuel](#thème-visuel)
- [Stack technique](#stack-technique)
- [Limites connues et pistes d'amélioration](#limites-connues-et-pistes-damélioration)

## Fonctionnalités

- **Identification de l'entreprise** : nom, secteur d'activité et email de contact, avec validation du format.
- **Questionnaire en 5 axes** couvrant les principaux volets de la cybersécurité en entreprise (postes de travail, réseau, sensibilisation, échanges électroniques, protection des données).
- **Moteur de recommandations à règles** : pour chaque réponse donnée, génère une liste de recommandations classées par priorité (Critique / Élevée / Moyenne), chacune associée à une référence précise du guide CMRPI/AUSIM et à sa justification.
- **Moteur de recommandations IA** : un réseau de neurones (Keras/TensorFlow) prédit, pour chaque recommandation possible, son niveau de priorité (Absente / Moyenne / Élevée / Critique) à partir du profil de réponses — permet de comparer l'approche par règles et l'approche par apprentissage, et de généraliser à des profils partiellement renseignés.
- **Vérification automatique de compatibilité modèle ↔ questionnaire** : chaque modèle `.keras` est accompagné d'un fichier `.meta.json` contenant une signature (hash) du jeu de recommandations utilisé à l'entraînement. Au chargement, cette signature est comparée à celle calculée en direct depuis `data/questionnaire.py` ; en cas d'écart, l'application avertit ou bloque l'usage des prédictions.
- **Rapport interactif** : synthèse visuelle du nombre de recommandations par niveau de priorité (Critique / Élevée / Moyenne affichées côte à côte), détail par question ou par priorité selon le mode.
- **Export PDF** uniforme pour les deux rapports (questionnaire à règles et IA) : même charte graphique, mêmes informations d'entreprise en en-tête, mêmes couleurs par niveau de priorité.
- **Historique des audits IA** : chaque profil soumis est journalisé (entreprise, secteur, email, réponses) dans un fichier CSV consultable depuis l'application.
- **Recueil des avis utilisateurs** : formulaire de retour libre après consultation des recommandations IA, également journalisé et consultable.
- **Module statistiques** : exploration du volume et de la répartition des recommandations du guide (par question, par priorité) et évaluation de la performance du modèle IA (accuracy, précision, rappel, F1-score, matrice de confusion) sur l'ensemble des 1024 profils possibles.
- **Suite de tests automatisés** : 24 tests unitaires (`pytest`) couvrant la validation d'email, le calcul des scores de risque/maturité, le moteur de recommandations à règles et le module d'indexation.
- **Thème visuel personnalisé** (fond bleu nuit, accents turquoise) configuré via `.streamlit/config.toml`.

## Architecture du projet

```
.
├── app.py                            # Point d'entrée Streamlit, navigation et routing
├── requirements.txt                  # Dépendances Python
├── README.md
├── modeles_recommandations.keras     # Modèle IA entraîné, chargé par défaut par l'application
├── modeles_recommandations.keras.meta.json  # Métadonnées du modèle (signature, date d'entraînement)
├── historique_profils_ia.csv         # Historique des profils soumis via le module IA
├── historique_avis_ia.csv            # Avis / suggestions laissés par les utilisateurs (créé au premier avis soumis)
│
├── .streamlit/
│   └── config.toml                   # Thème visuel de l'application
│
├── core/
│   ├── etat_session.py               # Initialisation / réinitialisation de st.session_state
│   ├── validation.py                 # Validation du format de l'email
│   ├── moteur_recommandation.py      # Génère et trie les recommandations (approche à règles)
│   └── model_ia.py                   # Chargement / cache du modèle Keras, upload manuel, vérification de compatibilité
│
├── data/
│   ├── questionnaire.py              # Questions, réponses possibles et recommandations associées (source unique de vérité)
│   └── index_recommandations.py      # Indexation centralisée des recommandations (liste, classes, signature de version)
│
├── ML/
│   ├── ml.py                         # Script d'entraînement du modèle (dataset synthétique + réseau de neurones)
│   ├── modele_recommandations_optimise.keras  # Variante de modèle issue d'itérations d'entraînement
│   └── ml1.py                        # Page Streamlit "Recommandations IA" : formulaire, prédiction, PDF, historique, avis
│
├── statistique/
│   ├── score.py                      # Calcul de scores de risque / maturité par profil (utilisable hors Streamlit)
│   └── statique.py                   # Page Streamlit "Statistiques" : graphiques données + performance du modèle
│
├── pdf/
│   ├── generer_rapport.py            # Construction des rapports PDF (reportlab) — version règles et version IA
│   └── style_pdf.py                  # Constantes de style partagées (couleurs par priorité, fonds)
│
├── ui/
│   ├── identification.py             # Écran : formulaire d'identification de l'entreprise
│   ├── questionnaire_ui.py           # Écran : formulaire du questionnaire à règles
│   └── resultats.py                  # Écran : rapport du moteur à règles + export PDF
│
└── test/
    ├── test_validation.py            # Tests de la validation d'email
    ├── test_score.py                 # Tests des scores de risque, de maturité et de classification
    ├── test_moteur_recommandations.py # Tests du moteur de recommandations à règles
    └── test_index_recommandations.py # Tests de l'indexation et de la signature des recommandations
```

Le flux applicatif est piloté par `st.session_state.etape` (`"questionnaire"` → `"resultats"`) pour le parcours à règles, et par un onglet dédié pour le parcours IA (voir `app.py`).

## Prérequis

- Python 3.9 ou supérieur
- pip

## Installation

```bash
# Cloner ou récupérer le projet, puis se placer dans le dossier
cd CMRPI_PFA_cyber_audit

# (Recommandé) Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate      # Sous Windows : venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

## Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvre automatiquement dans le navigateur à l'adresse `http://localhost:8501`.

## Lancer les tests

```bash
pip install pytest
pytest test/ -v
```

24 tests couvrent la validation d'email, le calcul des scores de risque/maturité, le moteur de recommandations à règles et le module d'indexation des recommandations.

## Utilisation

1. **Identification** : renseigner le nom de l'entreprise, le secteur d'activité et un email de contact valide (obligatoire avant d'accéder au questionnaire ou au module IA).
2. Choisir un axe dans la barre latérale :
   - **📊 Statistique** : ne nécessite pas d'identification, accessible directement.
   - **📝 Questionnaire** : parcours classique à règles.
   - **🤖 Recommandations IA** : parcours basé sur le modèle de deep learning.
3. **Questionnaire (règles)** : répondre aux 5 questions (une réponse par axe), puis consulter le rapport détaillé par question et télécharger le PDF. Le bouton **Nouvel audit** réinitialise le parcours.
4. **Recommandations IA** : répondre au même questionnaire (pré-rempli si un profil existe déjà), le modèle prédit les recommandations pertinentes classées par priorité en 3 colonnes (Critique / Élevée / Moyenne), avec export PDF, possibilité de laisser un avis, et consultation de l'historique des audits et des avis précédents.

## Les 5 axes du questionnaire

| # | Axe |
|---|-----|
| 1 | Protection des postes de travail |
| 2 | Sécurisation de l'accès Internet et du Wi-Fi |
| 3 | Sensibilisation et formation des collaborateurs face aux cybermenaces |
| 4 | Sécurité des échanges et transactions électroniques (messagerie, partage de fichiers, paiements en ligne) |
| 5 | Protection des données critiques |

Chaque axe propose 4 niveaux de réponse (de « Aucune protection » à une protection complète/avancée). Le niveau choisi détermine le sous-ensemble de recommandations affichées pour cet axe (voir `data/questionnaire.py`).

## Moteur de recommandations (règles)

`core/moteur_recommandation.py` associe directement, pour chaque couple (question, réponse), la liste de recommandations codée en dur dans `data/questionnaire.py` (issue d'une lecture manuelle du guide CMRPI/AUSIM). Les recommandations sont ensuite triées par priorité (`Critique` > `Elevee` > `Moyenne`). C'est une approche 100 % déterministe et traçable : chaque recommandation affichée est justifiée par une citation du guide.

## Module IA (réseau de neurones)

- **Entraînement** (`ML/ml.py`) : génère un jeu de données synthétique couvrant les 4⁵ = 1024 profils de réponses possibles, construit les cibles à partir des mêmes règles que le moteur déterministe (avec un mécanisme de « bruit » forçant certains profils à haut risque en `Critique` pour renforcer l'apprentissage sur les cas graves), puis entraîne un réseau dense multi-sorties (une tête softmax à 4 classes — `Absente / Moyenne / Elevee / Critique` — par recommandation possible). Le script écrit également un fichier `.meta.json` contenant la signature du jeu de recommandations utilisé, pour permettre la vérification de compatibilité à l'inférence.
- **Inférence** (`ML/ml1.py`, page *Recommandations IA*) : charge le modèle `.keras` (par défaut `modeles_recommandations.keras`, ou upload manuel), prédit la classe de chaque recommandation pour le profil soumis, et n'affiche que celles dont la classe prédite n'est pas `Absente`.
- **Objectif** : montrer qu'un modèle de deep learning peut apprendre à retrouver — voire généraliser — les règles métier extraites manuellement du guide, ouvrant la voie à une évolution future vers un scoring plus nuancé (probabilités, profils partiels, etc.).

⚠️ **Point d'attention** : les prédictions du modèle sont positionnelles (l'index `i` de la sortie correspond à la `i`-ème recommandation de `LISTE_RECOS`, reconstruite à chaque lancement à partir de `data/questionnaire.py`). Toute modification de l'ordre ou du contenu des recommandations dans `data/questionnaire.py` **sans réentraînement du modèle** peut rendre les prédictions incohérentes avec les libellés affichés. Ce risque est aujourd'hui **atténué** par le mécanisme de signature décrit ci-dessous, mais reste à surveiller à chaque évolution du guide.

## Module d'indexation des recommandations

`data/index_recommandations.py` centralise la construction de la liste ordonnée des recommandations (`LISTE_RECOS`, `NOMS_RECOS`, `INDEX_RECO`) à partir de `data/questionnaire.py`, ainsi que les constantes partagées (`CLASSES`, `PRIORITES`, `NB_RECOS`). Ce module est importé aussi bien par le script d'entraînement (`ML/ml.py`) que par la page d'inférence (`ML/ml1.py`) et le module de statistiques (`statistique/statique.py`), garantissant que l'entraînement, l'inférence et l'évaluation du modèle utilisent toujours exactement le même ordre et le même contenu de recommandations.

Il calcule également `SIGNATURE_RECOS`, un hash SHA-256 du contenu et de l'ordre des recommandations, utilisé pour :
- taguer chaque modèle entraîné via son fichier `.meta.json` ;
- vérifier au chargement (`core/model_ia.py`) que le modèle utilisé correspond bien à la version courante de `data/questionnaire.py`, et avertir ou bloquer l'utilisateur en cas d'écart.

## Module statistiques

Accessible sans identification, avec deux onglets (`statistique/statique.py`) :

1. **📁 Données du questionnaire** : volume total de recommandations, répartition par question et par priorité (histogrammes empilés, camembert global).
2. **🤖 Performance du modèle IA** : évalue le modèle chargé sur l'ensemble des 1024 profils possibles vs. les règles du guide (vérité terrain), avec accuracy, précision, rappel, F1-score pondérés, matrice de confusion et rapport détaillé par classe.

Des fonctions de scoring indépendantes de l'interface sont également disponibles dans `statistique/score.py` (score de risque pondéré par question, score global, score de maturité, classification du niveau de risque, marge de progression vers le meilleur cas) — utilisables en ligne de commande via `python -m statistique.score`.

## Génération des rapports PDF

Le module `pdf/generer_rapport.py` (basé sur **ReportLab**) propose deux générateurs avec une charte graphique commune (`pdf/style_pdf.py` — couleurs et fonds par priorité) :

- `generer_pdf_bytes(entreprise, profil)` : rapport du **parcours à règles**, regroupé par question, avec la réponse choisie et le détail des recommandations associées.
- `generer_pdf_bytes_ia(entreprise, profil, recommandations)` : rapport du **parcours IA**, regroupé par niveau de priorité (Critique → Élevée → Moyenne), avec le même bloc d'informations d'entreprise (nom, secteur, taille, contact, date) que le rapport à règles pour une présentation uniforme.

Chaque recommandation est présentée avec son texte, sa référence au guide CMRPI/AUSIM et (pour le rapport à règles) sa justification textuelle. Les PDF sont générés en mémoire (`BytesIO`) et proposés directement au téléchargement, sans écriture sur disque côté serveur.

## Historique et avis utilisateurs

- `historique_profils_ia.csv` : journalise chaque profil soumis via le module IA (`horodatage, nom_entreprise, secteur, email_contact, Q1..Q5`), consultable dans un tableau depuis l'application.
- `historique_avis_ia.csv` : journalise les retours libres des utilisateurs après consultation des recommandations IA (`horodatage, nom_entreprise, email_contact, avis`), également consultable en tableau. Ce fichier est créé automatiquement lors du premier avis soumis s'il n'existe pas déjà.

⚠️ Ces fichiers contiennent des données à caractère personnel (email de contact) stockées en clair sur le disque local. À anonymiser ou chiffrer avant tout déploiement en production.

## Thème visuel

Le fichier `.streamlit/config.toml` définit une charte graphique sombre et technologique (fond bleu nuit `#081527`, accent turquoise `#2ED9C3`), reprise visuellement dans les cartes de recommandation (bordures et badges colorés par priorité) et dans les rapports PDF.

## Stack technique

- [Streamlit](https://streamlit.io/) — interface web
- [TensorFlow / Keras](https://www.tensorflow.org/) — modèle de recommandation par apprentissage
- [scikit-learn](https://scikit-learn.org/) — métriques d'évaluation du modèle
- [Matplotlib](https://matplotlib.org/) — visualisations statistiques
- [pandas](https://pandas.pydata.org/) — lecture/affichage de l'historique
- [ReportLab](https://www.reportlab.com/) — génération des PDF
- [NumPy](https://numpy.org/) — manipulation de tableaux (dataset, prédictions)
- [pytest](https://docs.pytest.org/) — tests automatisés
- Python standard (`re`, `datetime`, `csv`, `io`, `os`, `hashlib`, `json`)

## Limites connues et pistes d'amélioration

- **Champ « Taille »** actuellement figé à `"PME"` dans `ui/identification.py`, jamais saisi par l'utilisateur.
- **Deux modèles `.keras` présents dans le dépôt** (`modeles_recommandations.keras` à la racine, utilisé par défaut, et `ML/modele_recommandations_optimise.keras`, non chargé automatiquement) : à clarifier ou nettoyer pour éviter toute confusion sur la version de référence.
- **Historique CSV non versionné** : une évolution du schéma de colonnes (comme celle ajoutant `nom_entreprise`/`secteur`/`email_contact`) peut rendre les anciens fichiers illisibles par `pandas.read_csv` sans gestion explicite des formats mixtes.
- **Données personnelles en clair** dans les fichiers d'historique — à chiffrer ou anonymiser avant un déploiement réel.
- **Couverture de tests partielle** : le module IA (`ML/ml1.py`, `core/model_ia.py`) et la génération PDF (`pdf/generer_rapport.py`) ne sont pas encore couverts par des tests automatisés, contrairement au moteur à règles et au scoring.
