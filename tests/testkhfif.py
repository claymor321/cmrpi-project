import streamlit as st
from datetime import date
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

st.set_page_config(page_title="Audit Cybersécurité PME", page_icon="🔒", layout="centered")

# ============================================================
# DONNEES (questions, réponses, recommandations avec référence
# au guide CMRPI/AUSIM et justification)
# ============================================================

question1 = "Comment protegez-vous les postes de travail ?"
question2 = "Comment securisez-vous l'acces Internet et le Wi-Fi ?"
question3 = "Comment votre entreprise prepare-t-elle ses collaborateurs a reconnaitre et reagir face aux cybermenaces ?"
question4 = "Comment protegez-vous les echanges et transactions electroniques (messagerie, partage de fichiers, paiements en ligne) ?"
question5 = "Comment protegez-vous les donnees critiques ?"

reponses1 = {1: "A. Aucune protection", 2: "B. Antivirus uniquement", 3: "C. Antivirus + pare-feu",
             4: "D. Protection complete"}
rec11 = [{
             "recommandation": "Installer un antivirus assurant une protection contre les virus, vers, chevaux de Troie et autres logiciels malveillants",
             "priorite": "Critique", "guide": "3.3.1 Vecteurs d'attaques cybercriminelles",
             "justification": "Seule mesure de protection explicitement citée par le guide face aux malwares : « Installer un antivirus (logiciel qui protège un ordinateur contre les virus...) ». Son absence expose totalement le poste."},
         {"recommandation": "Configurer l'installation automatique des mises à jour de sécurité dès que possible",
          "priorite": "Critique", "guide": "3.1.7 Politique de mise à jour des systèmes et logiciels",
          "justification": "« Les attaquants exploitent ces vulnérabilités... longtemps après leur découverte et leur correction » : l'automatisation supprime le risque d'oubli d'un correctif critique."},
         {
             "recommandation": "Restreindre les droits d'installation et d'administration aux seuls utilisateurs autorisés",
             "priorite": "Elevee", "guide": "3.1.5 Les permissions d'accès",
             "justification": "« Il faut en principe éviter de donner le droit d'installation des programmes... aux utilisateurs non autorisés » — recommandation forte mais nuancée par « en principe »."},
         {"recommandation": "Interdire l'installation de logiciels non autorisés sur les postes de travail",
          "priorite": "Elevee", "guide": "3.1.1 Sécurité du poste de travail",
          "justification": "« Ne pas installer des logiciels sur le poste de travail » — règle de base énoncée simplement, sans qualificatif d'urgence absolue."}]
rec12 = [{
             "recommandation": "Paramétrer un verrouillage automatique de l'écran pour qu'aucune session ne reste ouverte sans surveillance",
             "priorite": "Elevee", "guide": "3.1.1 Sécurité du poste de travail",
             "justification": "« Ne pas laisser le poste de travail accessible avec la session ouverte » — directive claire visant à limiter les accès non autorisés en l'absence de l'utilisateur."},
         {
             "recommandation": "Restreindre l'usage des outils système (éditeur de registre, invite de commandes) et n'autoriser que les applications nécessaires à l'activité",
             "priorite": "Elevee", "guide": "3.1.5 Les permissions d'accès",
             "justification": "« Vous pouvez minimiser les risques d'intrusions en interdisant l'exécution de l'Explorateur Windows, des commandes MS-DOS et des outils de la base de registre » — mesure technique conseillée."},
         {
             "recommandation": "Attribuer à chaque utilisateur un espace de travail avec des droits d'accès adaptés à son activité",
             "priorite": "Elevee", "guide": "3.1.5 Les permissions d'accès",
             "justification": "« Un simple utilisateur possède son répertoire de travail... et des répertoires plus restreints appropriés à son activité » — principe standard de moindre privilège."},
         {
             "recommandation": "Sensibiliser l'ensemble du personnel ayant accès à des informations sensibles à la confidentialité des données",
             "priorite": "Critique", "guide": "3.4.3 Divulgation d'information",
             "justification": "« Il est impératif de sensibiliser et d'impliquer le personnel... » — le guide emploie explicitement le terme « impératif »."},
         {
             "recommandation": "Interdire la copie sur le poste de travail de fichiers provenant de sources douteuses (clé USB, pièce jointe email, etc.)",
             "priorite": "Critique", "guide": "3.1.2 Les virus, antivirus et firewall",
             "justification": "« Ne jamais copier sur le poste de travail des fichiers provenant de sources douteuses » — le guide utilise « jamais », vecteur d'infection direct."}]
rec13 = [{"recommandation": "Effectuer des sauvegardes régulières des documents importants", "priorite": "Critique",
          "guide": "3.1.1 Sécurité du poste de travail",
          "justification": "« Faire des sauvegardes régulières des documents importants » — mesure de base universellement critique face au risque de perte définitive de données."},
         {
             "recommandation": "Renouveler périodiquement les mots de passe des comptes utilisateurs (idéalement chaque mois)",
             "priorite": "Elevee", "guide": "3.1.4 L'authentification des utilisateurs",
             "justification": "« Le renouvellement périodique (mensuel si possible) du mot de passe » — présenté comme une consigne parmi d'autres, sans caractère absolu."},
         {"recommandation": "Interdire toute connexion avec un compte administrateur sur un poste non sécurisé",
          "priorite": "Critique", "guide": "3.1.4 L'authentification des utilisateurs",
          "justification": "« L'interdiction de se connecter avec des comptes administrateurs sur des postes non sécurisés » — le guide utilise le terme « interdiction »."}]
rec14 = [{
             "recommandation": "Bloquer automatiquement le système après un nombre défini de tentatives de connexion infructueuses",
             "priorite": "Elevee", "guide": "3.1.4 L'authentification des utilisateurs",
             "justification": "« La déconnexion et le blocage du système après un certain nombre de tentatives de connexion » — consigne standard de sécurisation de l'authentification."},
         {
             "recommandation": "Protéger les fichiers contenant les mots de passe système (mécanisme shadow sous Unix, base de registre protégée sous Windows)",
             "priorite": "Elevee", "guide": "3.1.5 Les permissions d'accès",
             "justification": "Mesure technique détaillée par le guide (mécanisme shadow, poledit et regedit) présentée comme apportant « un niveau minimal de sécurité »."}]

reponses2 = {1: "A. Wi-Fi paramètres par défaut", 2: "B. Wi-Fi protégé uniquement", 3: "C. Wi-Fi + HTTPS",
             4: "D. Politique complète"}
rec21 = [{"recommandation": "Ne jamais faire confiance à un réseau Wi-Fi public ne demandant aucun mot de passe",
          "priorite": "Critique", "guide": "3.2.2 Sécurité des connexions Wi-Fi (LAN/WLAN)",
          "justification": "« Ne faites jamais confiance aux réseaux de Wi-Fi public qui ne demandent pas de mots de passe » — formulation impérative absolue."},
         {"recommandation": "Désactiver la connexion automatique aux réseaux Wi-Fi inconnus", "priorite": "Elevee",
          "guide": "3.2.2 Sécurité des connexions Wi-Fi (LAN/WLAN)",
          "justification": "« Vérifiez si votre appareil est réglé pour se connecter automatiquement aux réseaux Wi-Fi inconnus. Si c'est le cas, désactivez cette fonction » — conseil pratique et concret."},
         {"recommandation": "Désactiver le Wi-Fi de l'appareil lorsqu'il n'est pas utilisé", "priorite": "Moyenne",
          "guide": "3.2.2 Sécurité des connexions Wi-Fi (LAN/WLAN)",
          "justification": "« Désactivez le Wi-Fi si vous ne l'utilisez pas. Cette mesure protégera vos données et vous aidera à économiser la batterie » — bénéfice présenté comme secondaire (confort + sécurité)."}]
rec22 = [{
             "recommandation": "Maintenir à jour le serveur web, le système de gestion de contenu (CMS) et l'ensemble de ses extensions",
             "priorite": "Critique", "guide": "3.2.3 Sécurité du site",
             "justification": "« Avoir la dernière version est votre assurance pour être sécurisé contre l'ensemble des failles récentes » — condition nécessaire face aux failles connues et répertoriées."},
         {"recommandation": "Chiffrer la connexion au site web au moyen d'un certificat SSL (accès en HTTPS)",
          "priorite": "Critique", "guide": "3.2.3 Sécurité du site",
          "justification": "« Il faut les protéger mieux que tout le reste... une contrainte légale » : le chiffrement SSL répond à une obligation, pas seulement une bonne pratique."},
         {"recommandation": "Ne jamais désactiver l'antivirus ou le pare-feu de l'entreprise", "priorite": "Critique",
          "guide": "3.2.1 Règles d'utilisation de l'internet",
          "justification": "« N'enlevez ou ne désactivez jamais les mesures de protection mises en place... (comme l'antivirus ou le pare-feu) »."},
         {"recommandation": "Mettre en place une authentification HTTP en protection complémentaire du serveur web",
          "priorite": "Moyenne", "guide": "3.2.3 Sécurité du site",
          "justification": "« L'authentification http est l'une des protections possibles pour votre serveur web » — présentée comme une option parmi d'autres, non obligatoire."}]
rec23 = [{
             "recommandation": "Utiliser un réseau privé virtuel (VPN) pour sécuriser les connexions à distance des collaborateurs nomades",
             "priorite": "Elevee", "guide": "3.1.6 Sécurité de l'accès à distance / VPN",
             "justification": "« Les VPN est une garantie de l'intégrité et la confidentialité des données échangées entre sites distants » — fortement recommandé pour tout accès nomade."},
         {
             "recommandation": "Protéger l'accès aux arborescences privées du site : seules les pages destinées au public doivent être visibles de l'extérieur",
             "priorite": "Critique", "guide": "3.2.3 Sécurité du site",
             "justification": "« L'accès aux arborescences privées de votre site doit être protégé » — formulation d'obligation."},
         {"recommandation": "Sauvegarder régulièrement le site web de l'entreprise", "priorite": "Critique",
          "guide": "3.2.3 Sécurité du site",
          "justification": "« Il est nécessaire de faire une sauvegarde régulière de votre site web. Ce backup aura une valeur inestimable si votre site web se fait attaquer »."}]
rec24 = [{
             "recommandation": "Vérifier régulièrement que la version du site et du serveur correspond à la dernière version publiée par l'éditeur",
             "priorite": "Elevee", "guide": "3.2.3 Sécurité du site",
             "justification": "« N'hésitez pas à vérifier constamment la version de votre site web et du serveur vis-à-vis de la dernière version publiée »."},
         {
             "recommandation": "Étendre la politique de sécurité à l'ensemble du réseau, réseau local (LAN) et réseau externe (WAN) inclus",
             "priorite": "Elevee", "guide": "3.1.3 Sécurité des serveurs",
             "justification": "« La politique de sécurité doit englober l'ensemble du réseau informatique » — mesure stratégique et organisationnelle plus que technique immédiate."},
         {"recommandation": "Chiffrer les données sensibles avant leur stockage sur le serveur", "priorite": "Critique",
          "guide": "3.2.3 Sécurité du site",
          "justification": "« Toutes les informations doivent être cryptées avant d'être stockées pour une meilleure protection en cas de subtilisation des données »."}]

reponses3 = {1: "A. Jamais formés", 2: "B. Sensibilisation occasionnelle", 3: "C. Sensibilisés régulièrement",
             4: "D. Formations régulières"}
rec31 = [{
             "recommandation": "Sensibiliser l'ensemble du personnel ayant accès à des informations sensibles à la valeur et à la confidentialité de ces données",
             "priorite": "Critique", "guide": "3.4.3 Divulgation d'information",
             "justification": "« Il est impératif de sensibiliser et d'impliquer le personnel... » (même justification que pour l'Axe 1)."},
         {
             "recommandation": "Apprendre aux collaborateurs à ne pas ouvrir de pièce jointe suspecte ou provenant d'un expéditeur inhabituel",
             "priorite": "Critique", "guide": "3.4.1 Menaces sur le courrier électronique",
             "justification": "« N'ouvrez pas les pièces jointes provenant de destinataires inconnus ou dont le titre ou le format paraissent incohérents » — vecteur d'infection majeur par email."}]
rec32 = [{"recommandation": "Exiger le signalement immédiat de tout incident d'infection par un virus",
          "priorite": "Critique", "guide": "3.1.2 Les virus, antivirus et firewall",
          "justification": "« Signaler tout incident d'infection de virus » — directive de réaction rapide indispensable pour limiter la propagation."},
         {
             "recommandation": "Établir une liste des personnes habilitées à connaître certaines informations sensibles selon le poste occupé",
             "priorite": "Moyenne", "guide": "3.4.3 Divulgation d'information",
             "justification": "« Il est possible de créer dans l'entreprise une liste des personnes habilitées à connaître de telles informations » — mesure facultative selon le guide."}]
rec33 = [{
             "recommandation": "Interdire formellement la divulgation d'informations personnelles ou professionnelles sur des forums ou réseaux sociaux",
             "priorite": "Critique", "guide": "3.4.3 Divulgation d'information",
             "justification": "« Il est important de ne jamais donner d'informations personnelles ou professionnelles sur des forums... ou réseaux sociaux »."},
         {
             "recommandation": "Former les collaborateurs à vérifier la cohérence entre l'expéditeur présumé d'un email et le contenu du message",
             "priorite": "Elevee", "guide": "3.4.1 Menaces sur le courrier électronique",
             "justification": "« Vérifiez la cohérence entre l'expéditeur présumé et le contenu du message et vérifiez son identité » — consigne standard de vigilance."}]
rec34 = [{
             "recommandation": "Former les collaborateurs à ne jamais répondre à un spam ni cliquer sur ses liens ou pièces jointes",
             "priorite": "Critique", "guide": "3.4.1 Menaces sur le courrier électronique",
             "justification": "Triple répétition du guide : « Ne jamais répondre à un spam... Ne jamais cliquer sur un lien html... Ne jamais cliquer sur la pièce jointe d'un spam »."},
         {
             "recommandation": "Former les collaborateurs à se méfier de tout lien reçu par email à caractère commercial suspect (tentative de phishing) et à le signaler à l'administrateur",
             "priorite": "Critique", "guide": "3.2.1 Règles d'utilisation de l'internet",
             "justification": "« Méfiez-vous. Les emails à consonance commerciale... sont souvent des tentatives de phishing. Supprimez l'email et contactez l'administrateur »."},
         {
             "recommandation": "Prévoir une procédure de réaction immédiate : déconnecter le poste infecté du réseau local",
             "priorite": "Critique", "guide": "3.1.2 Les virus, antivirus et firewall",
             "justification": "« En cas d'infection, déconnecter le poste de travail du réseau local » — mesure de confinement immédiat."}]

reponses4 = {1: "A. Aucune protection", 2: "B. Antivirus mail", 3: "C. Règles internes et accès contrôlés",
             4: "D. Mesures techniques et organisationnelles"}
rec41 = [{"recommandation": "Utiliser un logiciel antispam pour bloquer ou isoler les emails indésirables",
          "priorite": "Moyenne", "guide": "3.4.1 Menaces sur le courrier électronique",
          "justification": "« Utiliser un logiciel antispam pour bloquer ou déplacer les emails indésirables » — mesure de confort, sans qualificatif d'urgence dans le guide."},
         {
             "recommandation": "Vérifier la cohérence entre l'expéditeur présumé d'un email et le contenu du message avant toute action",
             "priorite": "Elevee", "guide": "3.4.1 Menaces sur le courrier électronique",
             "justification": "« L'identité d'un expéditeur n'étant en rien garantie : vérifiez la cohérence entre l'expéditeur présumé et le contenu du message »."},
         {"recommandation": "Ne pas ouvrir de pièce jointe suspecte ou provenant d'un expéditeur inconnu",
          "priorite": "Critique", "guide": "3.4.1 Menaces sur le courrier électronique",
          "justification": "Même justification que pour l'Axe 3 : vecteur d'infection majeur, formulé de manière impérative dans le guide."},
         {
             "recommandation": "Créer des mots de passe d'au moins 8 caractères combinant majuscules, minuscules, chiffres et caractères spéciaux",
             "priorite": "Critique", "guide": "3.4.2 Mot de passe",
             "justification": "« Créez des mots de passe comptant au moins huit caractères... Créez un mot de passe fort en incluant [majuscules, minuscules, chiffres, caractères spéciaux] » — base de toute sécurité d'accès."}]
rec42 = [
    {"recommandation": "Chiffrer les données pour limiter les risques d'interception et de surveillance des échanges",
     "priorite": "Elevee", "guide": "3.1.4 L'authentification des utilisateurs",
     "justification": "« Le cryptage des données pour rendre l'interception et la surveillance moins efficaces » — consigne parmi les règles d'authentification."},
    {
        "recommandation": "Centraliser le stockage et la gestion des fichiers via un système Web sécurisé, accessible en tout lieu",
        "priorite": "Elevee", "guide": "3.4.4 Envois, réceptions et partage sécurisés",
        "justification": "« Centraliser le stockage et la gestion des fichiers avec un système Web sécurisé, accessible en tout lieu... pour la protection hors site des données »."},
    {
        "recommandation": "Mettre en place des contrôles d'accès distincts pour séparer les fichiers privés des fichiers de production",
        "priorite": "Elevee", "guide": "3.4.4 Envois, réceptions et partage sécurisés",
        "justification": "« Mettre en place des contrôles et des autorisations d'accès pour sécuriser les fichiers privés et les séparer des fichiers de production »."},
    {"recommandation": "Adopter une politique de renouvellement des mots de passe tous les trois mois",
     "priorite": "Elevee", "guide": "3.4.2 Mot de passe",
     "justification": "« Votre entreprise devrait exiger ce changement tous les trois mois » — recommandation ferme mais conditionnelle (« devrait »)."}]
rec43 = [{"recommandation": "Surveiller et documenter les modalités de partage des fichiers de l'entreprise",
          "priorite": "Moyenne", "guide": "3.4.4 Envois, réceptions et partage sécurisés",
          "justification": "« Surveiller les modalités de partage des fichiers de l'entreprise » — mesure de suivi, sans qualificatif d'urgence."},
         {"recommandation": "Optimiser la configuration de l'antivirus pour la messagerie électronique",
          "priorite": "Moyenne", "guide": "3.4.1 Menaces sur le courrier électronique",
          "justification": "« Optimiser la configuration de son antivirus vis-à-vis de la messagerie électronique » — amélioration continue, non impérative."},
         {
             "recommandation": "Vérifier la présence d'un cadenas et du protocole HTTPS dans la barre d'adresse avant tout paiement en ligne",
             "priorite": "Elevee", "guide": "3.3.4 Escroquerie sur les moyens de paiement",
             "justification": "« Contrôlez la présence d'un cadenas dans la barre d'adresse... Assurez-vous que la mention [https] apparaît au début de l'adresse » — vérification systématique recommandée."},
         {
             "recommandation": "Ne jamais transmettre le code confidentiel de la carte bancaire, y compris par téléphone ou par email",
             "priorite": "Critique", "guide": "3.3.4 Escroquerie sur les moyens de paiement",
             "justification": "« De manière générale, ne transmettez jamais le code confidentiel de votre carte bancaire »."}]
rec44 = [{"recommandation": "Bloquer l'affichage des images et contenus externes dans les emails au format HTML",
          "priorite": "Moyenne", "guide": "3.4.1 Menaces sur le courrier électronique",
          "justification": "« Bloquer images et contenus externes dans les messages HTML » — mesure technique complémentaire, non prioritaire dans le guide."},
         {
             "recommandation": "Désactiver l'ouverture automatique des documents téléchargés et lancer une analyse antivirus avant toute ouverture",
             "priorite": "Elevee", "guide": "3.4.1 Menaces sur le courrier électronique",
             "justification": "« Désactivez l'ouverture automatique des documents téléchargés et lancez une analyse antivirus avant de les ouvrir »."},
         {
             "recommandation": "Configurer les logiciels et le navigateur pour qu'ils ne mémorisent pas les mots de passe saisis",
             "priorite": "Moyenne", "guide": "3.4.1 Menaces sur le courrier électronique",
             "justification": "« Configurez les logiciels, y compris votre navigateur web, pour qu'ils ne se \"souviennent\" pas des mots de passe choisis » — mesure d'hygiène numérique."},
         {
             "recommandation": "Envisager l'usage d'un gestionnaire de mots de passe pour renforcer la robustesse et l'unicité des mots de passe utilisés",
             "priorite": "Moyenne", "guide": "3.4.2 Mot de passe",
             "justification": "« Vous pourriez aussi envisager l'utilisation d'un gestionnaire de mots de passe » — le guide emploie un conditionnel, mesure facultative."},
         {
             "recommandation": "Privilégier, pour les paiements en ligne, la confirmation de commande par un code envoyé par SMS",
             "priorite": "Moyenne", "guide": "3.3.4 Escroquerie sur les moyens de paiement",
             "justification": "« Privilégiez la méthode impliquant l'envoi d'un code de confirmation de la commande par SMS » — recommandation, non une obligation."}]

reponses5 = {1: "A. Aucune sauvegarde", 2: "B. Sauvegardes manuelles", 3: "C. Sauvegardes automatiques",
             4: "D. Sauvegardes + chiffrement"}
rec51 = [{
             "recommandation": "Effectuer des sauvegardes régulières des données, quotidiennes ou hebdomadaires selon leur criticité",
             "priorite": "Critique", "guide": "3.5.1 Stockage, sauvegarde et restauration des données",
             "justification": "« Il est vivement conseillé d'effectuer des sauvegardes régulières (quotidiennes ou hebdomadaires) » — criticité renforcée par l'enjeu de perte définitive de données."},
         {"recommandation": "Veiller à la sécurité des fichiers contenant des données personnelles",
          "priorite": "Critique", "guide": "3.5.4 Collecte et tri des données personnelles",
          "justification": "Fait partie des « six règles d'or » imposées par la loi 09-08 relative au traitement des données personnelles — obligation légale."},
         {"recommandation": "Fixer une durée de conservation raisonnable pour les données personnelles collectées",
          "priorite": "Critique", "guide": "3.5.4 Collecte et tri des données personnelles",
          "justification": "Idem — règle d'or de la loi 09-08, obligation légale de conservation limitée dans le temps."},
         {"recommandation": "Chiffrer les données sensibles avant toute copie vers un service cloud",
          "priorite": "Critique", "guide": "3.5.2 Transfert des données et Cloud computing",
          "justification": "« Veillez à la confidentialité des données en... les chiffrant à l'aide d'un logiciel de chiffrement avant de les copier dans le cloud »."}]
rec52 = [
    {"recommandation": "Utiliser un support de sauvegarde externe dédié, conservé en dehors des locaux de l'entreprise",
     "priorite": "Elevee", "guide": "3.5.1 Stockage, sauvegarde et restauration des données",
     "justification": "« Un disque dur externe réservé exclusivement à cet usage... de préférence à l'extérieur de l'entreprise » pour éviter la perte simultanée de l'original et de la copie."},
    {
        "recommandation": "N'emporter en déplacement que du matériel dédié à la mission, contenant uniquement les données strictement nécessaires",
        "priorite": "Elevee", "guide": "3.5.3 Sécurité des données de la PME vs Mobilité",
        "justification": "« N'utilisez que du matériel... dédié à la mission, et ne contenant que les données nécessaires »."},
    {
        "recommandation": "Évaluer les risques (confidentialité, localisation, disponibilité, réversibilité contractuelle) avant toute sauvegarde sur une plateforme cloud",
        "priorite": "Elevee", "guide": "3.5.2 Transfert des données et Cloud computing",
        "justification": "« Soyez conscient que ces sites de stockage peuvent être la cible d'attaques informatiques et que ces solutions impliquent des risques spécifiques »."}]
rec53 = [{"recommandation": "Accorder une attention particulière à la durée de vie des supports de sauvegarde utilisés",
          "priorite": "Moyenne", "guide": "3.5.1 Stockage, sauvegarde et restauration des données",
          "justification": "« Il est nécessaire d'accorder une attention particulière à la durée de vie de ces supports » — mesure de maintenance secondaire par rapport à la sauvegarde elle-même."},
         {
             "recommandation": "Recourir à des spécialistes techniques et juridiques pour la rédaction de contrats cloud personnalisés, adaptés aux enjeux de l'entreprise",
             "priorite": "Moyenne", "guide": "3.5.2 Transfert des données et Cloud computing",
             "justification": "« N'hésitez pas à recourir à des spécialistes techniques et juridiques pour la rédaction des contrats personnalisés » — suggestion facultative du guide."},
         {
             "recommandation": "Assurer la confidentialité des données personnelles en en limitant l'accès aux seules personnes autorisées",
             "priorite": "Critique", "guide": "3.5.4 Collecte et tri des données personnelles",
             "justification": "Règle d'or de la loi 09-08 — obligation légale de confidentialité des données personnelles."}]
rec54 = [{
             "recommandation": "Lire attentivement les conditions générales d'utilisation avant de recourir à tout service cloud",
             "priorite": "Elevee", "guide": "3.5.2 Transfert des données et Cloud computing",
             "justification": "« Soyez vigilant en prenant connaissance des conditions générales d'utilisation de ces services »."},
         {
             "recommandation": "Définir un objectif précis et documenté pour chaque traitement de données personnelles réalisé",
             "priorite": "Critique", "guide": "3.5.4 Collecte et tri des données personnelles",
             "justification": "Dernière des « six règles d'or » de la loi 09-08 — obligation légale de finalité déterminée du traitement."}]

lesreponses = {1: reponses1, 2: reponses2, 3: reponses3, 4: reponses4, 5: reponses5}
lesquestions = {1: question1, 2: question2, 3: question3, 4: question4, 5: question5}
lesrecommandations = {1: [rec11, rec12, rec13, rec14], 2: [rec21, rec22, rec23, rec24], 3: [rec31, rec32, rec33, rec34],
                      4: [rec41, rec42, rec43, rec44], 5: [rec51, rec52, rec53, rec54]}

ORDRE_PRIORITE = {"Critique": 0, "Elevee": 1, "Moyenne": 2}

# Couleurs pour l'affichage Streamlit : fond clair + texte foncé de la même teinte
STYLE_PRIORITE = {
    "Critique": {"bg": "#FDEDEC", "border": "#C0392B", "texte": "#922B21", "badge": "#C0392B"},
    "Elevee": {"bg": "#FEF5E7", "border": "#E67E22", "texte": "#9C640C", "badge": "#E67E22"},
    "Moyenne": {"bg": "#FEF9E7", "border": "#B7950B", "texte": "#7D6608", "badge": "#B7950B"},
}
# Couleurs pour le PDF
COULEUR_PDF = {"Critique": colors.HexColor("#C0392B"), "Elevee": colors.HexColor("#E67E22"),
               "Moyenne": colors.HexColor("#B7950B")}
FOND_PDF = {"Critique": colors.HexColor("#FDEDEC"), "Elevee": colors.HexColor("#FEF5E7"),
            "Moyenne": colors.HexColor("#FEF9E7")}


def moteur_recommandations(profil):
    resultats = []
    for num_q, num_r in enumerate(profil, start=1):
        recs = lesrecommandations[num_q][num_r - 1]
        for rec in recs:
            resultats.append({
                "question": lesquestions[num_q],
                "reponse": lesreponses[num_q][num_r],
                **rec
            })
    resultats.sort(key=lambda r: ORDRE_PRIORITE.get(r["priorite"], 99))
    return resultats


# ============================================================
# SCORE DE CRITICITE GLOBALE
# ============================================================
# Chaque question est repondue par un indice 1 a 4 (1 = pire pratique,
# 4 = meilleure pratique). Avec 5 questions : score min = 5, score max = 20.
# On decoupe le score en 3 tranches : [5-10] [11-15] [16-20]

SCORE_MIN = 5
SCORE_MAX = 20

TRANCHES_SCORE = [
    {"borne_min": 5, "borne_max": 10, "niveau": "Critique", "couleur": "#C0392B",
     "message": "Niveau de securite tres insuffisant : des mesures urgentes doivent etre mises en oeuvre."},
    {"borne_min": 11, "borne_max": 15, "niveau": "Moyen", "couleur": "#E67E22",
     "message": "Niveau de securite intermediaire : des ameliorations sont necessaires sur plusieurs axes."},
    {"borne_min": 16, "borne_max": 20, "niveau": "Satisfaisant", "couleur": "#27AE60",
     "message": "Bon niveau de securite : maintenez et consolidez les bonnes pratiques en place."},
]


def calculer_score(profil):
    """Calcule le score total (5 a 20) et determine la tranche de criticite correspondante."""
    score_total = sum(profil)
    tranche = next(t for t in TRANCHES_SCORE if t["borne_min"] <= score_total <= t["borne_max"])
    return score_total, tranche


def domaines_a_risque(profil):
    """Identifie precisement, question par question, les domaines les plus faibles
    (reponse 1 ou 2) afin de cibler ou porter les efforts en priorite."""
    domaines = []
    for num_q, num_r in enumerate(profil, start=1):
        domaines.append({
            "num_q": num_q,
            "question": lesquestions[num_q],
            "reponse": lesreponses[num_q][num_r],
            "score": num_r,
        })
    domaines.sort(key=lambda d: d["score"])
    return domaines


# ============================================================
# ETAT DE SESSION
# ============================================================

if "etape" not in st.session_state:
    st.session_state.etape = "identification"  # identification -> questionnaire -> resultats
if "entreprise" not in st.session_state:
    st.session_state.entreprise = {}
if "profil" not in st.session_state:
    st.session_state.profil = [1, 1, 1, 1, 1]


def reset():
    st.session_state.etape = "identification"
    st.session_state.entreprise = {}
    st.session_state.profil = [1, 1, 1, 1, 1]


# ============================================================
# MODE TEST : chargement rapide des 3 profils pilotes
# (sert uniquement à valider les 3 tranches de score avant
# envoi à l'encadrant — n'a pas vocation à rester en production)
# ============================================================

PROFILS_TEST = {
    "PME vulnérable (Critique)": {
        "profil": [1, 1, 1, 1, 2],
        "nom": "PME Test - Vulnérable",
    },
    "PME intermédiaire (Moyen)": {
        "profil": [3, 2, 3, 2, 3],
        "nom": "PME Test - Intermédiaire",
    },
    "PME bien protégée (Satisfaisant)": {
        "profil": [4, 4, 3, 4, 4],
        "nom": "PME Test - Bien protégée",
    },
}

with st.sidebar:
    st.markdown("### 🧪 Mode test")
    st.caption("Charge directement un profil pilote et saute à l'écran des résultats.")
    for label, data in PROFILS_TEST.items():
        score_apercu = sum(data["profil"])
        if st.button(f"{label} — score {score_apercu}/20", key=f"test_{label}", use_container_width=True):
            st.session_state.entreprise = {
                "nom": data["nom"],
                "secteur": "Secteur de test",
                "taille": "PME",
                "email_contact": "test@gmail.com",
                "date_audit": date.today().isoformat(),
            }
            st.session_state.profil = data["profil"]
            st.session_state.etape = "resultats"
            st.rerun()
    st.divider()

# ============================================================
# TITRE
# ============================================================

st.title("🔒 Audit de cybersécurité pour PME")
st.caption("Questionnaire basé sur le guide CMRPI/AUSIM")

# ============================================================
# ETAPE 1 : IDENTIFICATION DE L'ENTREPRISE
# ============================================================

if st.session_state.etape == "identification":
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
        elif not email.strip():
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

# ============================================================
# ETAPE 2 : QUESTIONNAIRE (5 QUESTIONS)
# ============================================================

elif st.session_state.etape == "questionnaire":
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

# ============================================================
# ETAPE 3 : RESULTATS
# ============================================================

elif st.session_state.etape == "resultats":
    entreprise = st.session_state.entreprise
    profil = st.session_state.profil

    st.subheader("3. Rapport d'audit")
    st.markdown(
        f"""
        **Entreprise :** {entreprise['nom']}
        **Secteur :** {entreprise['secteur']} &nbsp;|&nbsp; **Taille :** {entreprise['taille']}
        **Contact :** {entreprise['email_contact']}
        **Date de l'audit :** {entreprise['date_audit']}
        """
    )
    st.divider()

    recos = moteur_recommandations(profil)

    # ============================================================
    # SCORE GLOBAL DE CRITICITE
    # ============================================================
    score_total, tranche = calculer_score(profil)
    pct = (score_total - SCORE_MIN) / (SCORE_MAX - SCORE_MIN)

    st.subheader("Score global de cybersécurité")
    st.markdown(
        f"""
        <div style="border:2px solid {tranche['couleur']}; border-radius:10px; padding:16px 20px; background-color:{tranche['couleur']}15;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:1.4em; font-weight:800; color:{tranche['couleur']};">{score_total} / {SCORE_MAX}</span>
                <span style="background-color:{tranche['couleur']}; color:#FFFFFF; font-weight:700; font-size:0.9em; padding:4px 14px; border-radius:14px;">
                    Niveau {tranche['niveau']}
                </span>
            </div>
            <div style="margin-top:6px; font-size:0.92em; color:#4A4A4A;">{tranche['message']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(pct)
    st.caption("Tranches : 5-10 Critique  •  11-15 Moyen  •  16-20 Satisfaisant")

    # Domaines/questions precis a l'origine du score (reponses faibles = 1 ou 2)
    domaines_faibles = [d for d in domaines_a_risque(profil) if d["score"] <= 2]
    if domaines_faibles:
        st.markdown("**⚠️ Domaines à l'origine du score (réponses les plus faibles) :**")
        for d in domaines_faibles:
            st.markdown(f"- **Q{d['num_q']}. {d['question']}** — réponse actuelle : *{d['reponse']}*")
    else:
        st.success("Aucun domaine critique isolé : toutes les réponses sont de bon niveau (≥ C).")

    st.divider()

    # Indicateurs synthétiques
    nb_critique = sum(1 for r in recos if r["priorite"] == "Critique")
    nb_elevee = sum(1 for r in recos if r["priorite"] == "Elevee")
    nb_moyenne = sum(1 for r in recos if r["priorite"] == "Moyenne")

    col1, col2, col3 = st.columns(3)
    col1.metric("🔴 Critique", nb_critique)
    col2.metric("🟠 Elevée", nb_elevee)
    col3.metric("🟡 Moyenne", nb_moyenne)

    st.divider()

    # Regrouper par question pour l'affichage
    for num_q in range(1, 6):
        num_r = profil[num_q - 1]
        recs_question = [r for r in recos if r["question"] == lesquestions[num_q]]

        with st.expander(f"Q{num_q}. {lesquestions[num_q]}  — Reponse :  {lesreponses[num_q][num_r]}", expanded=True):
            for r in recs_question:
                s = STYLE_PRIORITE.get(r["priorite"],
                                       {"bg": "#F2F3F4", "border": "#7F8C8D", "texte": "#2C3E50", "badge": "#7F8C8D"})
                st.markdown(
                    f"""
                    <div style="border-left:5px solid {s['border']}; border-radius:6px;
                                padding:12px 16px; margin-bottom:10px; background-color:{s['bg']};">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                            <span style="font-weight:700; color:#1C2833; font-size:1.02em;">{r['recommandation']}</span>
                            <span style="background-color:{s['badge']}; color:#FFFFFF; font-weight:700;
                                         font-size:0.78em; padding:3px 10px; border-radius:12px; white-space:nowrap; margin-left:10px;">
                                {r['priorite']}
                            </span>
                        </div>
                        <div style="font-size:0.85em; color:{s['texte']}; font-weight:600; margin-bottom:4px;">
                            📘 Réf. guide CMRPI/AUSIM : {r['guide']}
                        </div>
                        <div style="font-size:0.85em; color:#4A4A4A;"><b>Justification (texte du guide CMRPI/AUSIM) :</b> 
                            {r['justification']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.divider()


    # ============================================================
    # GENERATION DU PDF
    # ============================================================

    def generer_pdf_bytes(entreprise, profil):
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=A4,
            topMargin=2 * cm, bottomMargin=2 * cm, leftMargin=2 * cm, rightMargin=2 * cm
        )
        styles = getSampleStyleSheet()

        style_titre = ParagraphStyle("TitrePrincipal", parent=styles["Title"], fontSize=20, spaceAfter=6)
        style_soustitre = ParagraphStyle("SousTitre", parent=styles["Normal"], fontSize=10.5,
                                         textColor=colors.HexColor("#5D6D7E"), spaceAfter=3)
        style_question = ParagraphStyle("Question", parent=styles["Heading2"], fontSize=13,
                                        textColor=colors.HexColor("#1A5276"), spaceBefore=16, spaceAfter=4)
        style_reponse = ParagraphStyle("Reponse", parent=styles["Normal"], fontSize=10.5,
                                       textColor=colors.HexColor("#145A32"), spaceAfter=8, leftIndent=2)
        style_reco = ParagraphStyle("Reco", parent=styles["Normal"], fontSize=9.5, leading=13,
                                    textColor=colors.HexColor("#1C2833"), alignment=TA_JUSTIFY)
        style_meta = ParagraphStyle("Meta", parent=styles["Normal"], fontSize=8.3, leading=11,
                                    textColor=colors.HexColor("#5D6D7E"))

        story = []
        story.append(Paragraph("Rapport d'audit de cybersécurité", style_titre))
        story.append(Paragraph("Basé sur le guide CMRPI/AUSIM", style_soustitre))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#D5D8DC"), spaceAfter=10))

        story.append(Paragraph(f"<b>Entreprise :</b> {entreprise['nom']}", style_soustitre))
        story.append(
            Paragraph(f"<b>Secteur :</b> {entreprise['secteur']} &nbsp;|&nbsp; <b>Taille :</b> {entreprise['taille']}",
                      style_soustitre))
        story.append(Paragraph(f"<b>Contact :</b> {entreprise['email_contact']}", style_soustitre))
        story.append(Paragraph(f"<b>Date de l'audit :</b> {entreprise['date_audit']}", style_soustitre))
        story.append(Spacer(1, 0.5 * cm))

        # ---- Score global de criticite ----
        score_total, tranche = calculer_score(profil)
        couleur_score = colors.HexColor(tranche["couleur"])
        fond_score = colors.HexColor(tranche["couleur"])

        style_score = ParagraphStyle("Score", parent=styles["Heading1"], fontSize=18,
                                     textColor=couleur_score, spaceAfter=2)
        style_niveau = ParagraphStyle("Niveau", parent=styles["Normal"], fontSize=11,
                                      textColor=colors.white, alignment=1)
        style_message = ParagraphStyle("Message", parent=styles["Normal"], fontSize=9.5,
                                       textColor=colors.HexColor("#4A4A4A"), spaceAfter=4)

        tbl_score = Table(
            [[Paragraph(f"Score global : <b>{score_total} / {SCORE_MAX}</b>", style_score),
              Paragraph(f"Niveau {tranche['niveau']}", style_niveau)]],
            colWidths=[11.5 * cm, 4.3 * cm],
        )
        tbl_score.setStyle(TableStyle([
            ("BACKGROUND", (1, 0), (1, 0), couleur_score),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (1, 0), (1, 0), "CENTER"),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#D5D8DC")),
            ("LEFTPADDING", (0, 0), (0, 0), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(tbl_score)
        story.append(Paragraph(tranche["message"], style_message))
        story.append(Paragraph("Tranches : 5-10 Critique &nbsp;•&nbsp; 11-15 Moyen &nbsp;•&nbsp; 16-20 Satisfaisant",
                               style_meta))

        domaines_faibles = [d for d in domaines_a_risque(profil) if d["score"] <= 2]
        if domaines_faibles:
            story.append(Spacer(1, 0.15 * cm))
            story.append(Paragraph("<b>Domaines à l'origine du score :</b>", style_message))
            for d in domaines_faibles:
                story.append(
                    Paragraph(f"• Q{d['num_q']}. {d['question']} — réponse actuelle : {d['reponse']}", style_meta))

        story.append(Spacer(1, 0.5 * cm))

        for num_q in range(1, 6):
            num_r = profil[num_q - 1]
            story.append(Paragraph(f"Q{num_q}. {lesquestions[num_q]}", style_question))
            story.append(Paragraph(f"Réponse choisie : <b>{lesreponses[num_q][num_r]}</b>", style_reponse))

            for rec in lesrecommandations[num_q][num_r - 1]:
                couleur = COULEUR_PDF.get(rec["priorite"], colors.HexColor("#7F8C8D"))
                fond = FOND_PDF.get(rec["priorite"], colors.HexColor("#F2F3F4"))

                contenu_cellule = [
                    Paragraph(f"<b>{rec['recommandation']}</b>", style_reco),
                    Paragraph(f"📘 Réf. guide CMRPI/AUSIM : {rec['guide']}", style_meta),
                ]
                if rec.get("justification"):
                    contenu_cellule.append(Paragraph(rec["justification"], style_meta))

                tbl = Table(
                    [[contenu_cellule, Paragraph(f"<b>{rec['priorite']}</b>", style_reco)]],
                    colWidths=[13.5 * cm, 2.3 * cm],
                )
                tbl.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), fond),
                    ("LINEBEFORE", (0, 0), (0, 0), 3, couleur),
                    ("TEXTCOLOR", (1, 0), (1, 0), couleur),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (1, 0), (1, 0), "CENTER"),
                    ("LEFTPADDING", (0, 0), (0, 0), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (1, 0), (1, 0), 8),
                ]))
                story.append(tbl)
                story.append(Spacer(1, 0.25 * cm))

            story.append(Spacer(1, 0.3 * cm))

        doc.build(story)
        buffer.seek(0)
        return buffer


    pdf_buffer = generer_pdf_bytes(entreprise, profil)

    st.download_button(
        "📄 Télécharger le rapport (PDF)",
        data=pdf_buffer,
        file_name=f"rapport_{entreprise['nom'].replace(' ', '_')}.pdf",
        mime="application/pdf",
    )

    if st.button("🔄 Nouvel audit"):
        reset()
        st.rerun()

