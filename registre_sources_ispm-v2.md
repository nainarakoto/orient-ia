# REGISTRE DE TRAÇABILITÉ DES SOURCES — PROJET ORIENT'IA

Ce registre assure la transparence méthodologique, l'honnêteté scientifique et le respect éthique des sources utilisées dans le cadre de la construction de l'assistant d'orientation **ORIENT'IA**. Conformément aux exigences réglementaires de l'examen Master 2 (ISPM Madagascar), **aucune donnée non vérifiée n'est présentée comme officielle**.

---

## 1. INVENTAIRE SYSTÉMATIQUE DES SOURCES CONSULTÉES

| ID | Titre de la Source / Lien de Consultation | Statut | Date de Consultation | Données Extraites du Document | Limites, Biais et Incertitudes Identifiés |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **S01** | **Présentation Générale de l'ISPM**<br>`https://ispm-edu.com/presentation.php` | Officiel | 26 août 2026 | Cycle LMD (durée des études, stages, soutenances, types de diplômes), biographie complète du Recteur Professeur Raboanary J. Amédée, contacts téléphoniques et mail. | Contenu institutionnel généraliste. N'affiche pas le détail détaillé des matières créditées par unité d'enseignement. |
| **S02** | **Départements & Filières de l'ISPM**<br>`https://ispm-edu.com/filieres.php` | Officiel | 26 août 2026 | Descriptif des 5 départements et objectifs de formation de chacun des 16 parcours (IGGLIA, ESIIA, FIC, GCA, AEE, PIP, etc.). | Les fiches métiers associées aux filières manquent de fiches compétences détaillées. |
| **S03** | **Conditions d'accès en première année**<br>`https://ispm-edu.com/inscription.php` | Officiel | 26 août 2026 | Liste des pièces obligatoires pour le dossier de sélection en Licence, frais d'inscription du dossier (30 000 Ar), et cartographie obligatoire d'accès par série de Baccalauréat. | Les seuils de notes de Terminale pour la sélection finale des dossiers ne sont pas chiffrés publiquement. |
| **S04** | **Enquête Terrain (Étudiants et Diplômés)**<br>`Facebook / Google Forms` | Externe | 26 août 2026 | Réponses anonymisées de professionnels établis (métiers, adéquation des études) et d'étudiants actuels (parcours, satisfaction). | **Faible volume** (quelques centaines), **biais d'auto-sélection** (forte proportion d'informaticiens), et **biais de reconstruction** du passé chez les professionnels. |
| **S05** | **Étude CASPO (Chatbot-Assisted Study Program Orientation)**<br>`https://dl.gi.de/bitstreams/72d78fc9-46b3-46f8-89c0-a13debc388c8/download` | Externe | 26 août 2026 | Cadre méthodologique pour RAG éducatif (couplage Mixtral + RoBERTa), gestion des questions critiques d'utilisateurs et réduction du dropout universitaire. | Étude réalisée dans un contexte universitaire ouest-européen ; les facteurs d'orientation et d'abandon diffèrent des réalités socio-économiques malgaches. |
| **S06** | **Rapport d'implémentation de modèles hybrides RAG**<br>`ArXiv / Frontiers in Psychology` | Externe | 26 août 2026 | Intégration de modèles d'évaluation de similarité sémantique (scores BERT Similarity, BLEU, ROUGE) et métriques de validation d'experts. | Les évaluations sont hors-ligne et ne remplacent pas une validation fonctionnelle sur des profils d'utilisateurs réels. |

---

## 2. FIABILITÉ ET STATUT ADMINISTRATIVE DES DONNÉES (S01, S02, S03)

Les données relatives à l'offre de formation, aux dénominations de filières et aux contraintes logiques d'admission d'origine constituent des règles administratives rigides.
*   **Garde-fou technique** : En cas d'incohérence entre les prédictions d'un modèle d'apprentissage statistique et les prérequis formels de l'ISPM (ex: un modèle ML préconisant IGGLIA pour un titulaire de Bac littéraire A2), la couche d'IA symbolique (`verifier_prerequis`) impose un veto logique indiscutable.

---

## 3. TRAITEMENT DE L'INCERTITUDE ET GESTION DES REQUÊTES HORS-CORPUS

Pour être digne de confiance, l'assistant **ORIENT'IA** ne doit jamais inventer (halluciner) de réponse si l'information est absente de l'index ou si la demande relève d'une décision administrative discrétionnaire.

### Procédure de Fallback (Renvoyer vers l'administration officielle) :
Lorsque l'information n'existe pas ou requiert une approbation humaine officielle, l'assistant doit restituer la réponse type suivante :
> « L'information demandée n'est pas disponible dans les documents officiels actuels d'ORIENT'IA. Pour toute validation administrative officielle ou question spécifique, nous vous invitons à contacter directement l'administration de l'ISPM : »
> *   **Adresse physique** : Ambatomaro Antsobolo, Antananarivo, Madagascar
> *   **Téléphones** : +261 33 12 171 60 / +261 34 20 874 28 / +261 32 02 544 72
> *   **E-mail** : contact@ispm.education

---

## 4. BIAIS DE L'ENQUÊTE DE VALUATION (S04) ET ATTÉNUATION
Dans le cadre de l'enquête menée via le formulaire Facebook / Google Sheets, les biais majeurs suivants ont été répertoriés :
1.  **Le Biais d'Auto-Sélection** : Les utilisateurs qui répondent sur les réseaux sociaux sont massivement issus des filières informatiques technophiles de l'ISPM (IGGLIA/IMTICIA), entraînant un déséquilibre de données.
2.  **Le Biais de Reconstruction** : Les professionnels interrogés ont tendance à réévaluer positivement ou à simplifier rétrospectivement leur profil d'orientation initial à l'ISPM.
3.  **L'atténuation** : La validation croisée est effectuée sur le jeu d'entraînement synthétique (équilibré), et l'enquête réelle est conservée pour tester la capacité de robustesse du modèle face à ces déformations du monde réel.
