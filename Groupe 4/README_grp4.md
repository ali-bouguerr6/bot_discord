# 📄 CV Parser – Groupe 4 (Discord + LLM)

Ce projet Discord permet d’extraire automatiquement les informations d’un CV PDF et de les convertir en JSON structuré. Deux versions sont proposées : une avec **Mistral AI**, l’autre avec **Gemini (Google)**. Les deux ont été testées et donnent des résultats cohérents. Le bot est conçu pour être utilisé directement sur un serveur Discord avec la commande `!parse_cv`.


## 🔍 Objectif

 **Groupe 4 – Extraction des informations du CV**  
 Lire un fichier PDF envoyé sur Discord, extraire le contenu pertinent, le structurer et le transmettre au groupe 5.


## 🤖 Pourquoi un LLM ?
Nous avons tenté une approche basée sur des regex. Résultat : peu fiable, fragile à la mise en page, difficile à maintenir.
L’utilisation de LLMs permet une extraction plus intelligente, plus résistante au bruit, et plus adaptable à l’avenir.

## ⚙️ Fonctionnalités

- Lecture de fichiers PDF (même avec mises en page variées)
- Utilisation de LLM (Mistral ou Gemini)
- JSON structuré avec les sections :
  - `prenom_nom`, `email`, `telephone`, `linkedin`, `github`
  - `competences_techniques`, `soft_skills`, `langues`, `certifications`
  - `formation`, `experience`
- Résultat prêt pour un système de matching, ATS, ou base de données RH
- Fonctionne sur Discord avec les pièces jointes

---

## 🧠 Modèles utilisés

| Modèle | Statut | API utilisée |
|--------|--------|--------------|
| Mistral Small | ✅ Testé | `https://api.mistral.ai/v1/chat/completions` |
| Gemini 1.5 Pro | ✅ Testé | Google Generative AI SDK |

---

## 📦 Dépendances

```bash
pip install discord requests PyPDF2 google-generativeai
```

## 🧪 Exemple de JSON généré
```
{
  "prenom_nom": "Eleonore VERNE",
  "email": "eleonore.verne@marine-analytics.com",
  "telephone": "+377 98 76 54 32",
  "linkedin": "eleonore-verne",
  "github": "eleonoreverne",
  "competences_techniques": [
    "Python", "R", "Tableau", "SQL", "MATLAB", "Azure"
  ],
  "soft_skills": [
    "Leadership", "Innovation", "Résolution de problèmes", "Communication"
  ],
  "langues": [
    "Français (Natif)", "Anglais (C1)", "Espagnol (B2)", "Japonais (B1)"
  ],
  "certifications": [
    "Yacht Master", "Data Science Professional (DSP-M278X93)"
  ],
  "formation": [
    {
      "titre": "Master Intelligence Artificielle et Politiques Publiques",
      "etablissement": "Sciences Po Paris",
      "periode": "Sept. 2023 – Juin 2025",
      "details": [
        "Principaux enseignements: Deep Learning, Gouvernance des données, Éthique de l’IA, Politiques environnementales, Modélisation prédictive."
      ]
    },
    {
      "titre": "Licence Mathématiques Appliquées et Sciences Sociales",
      "etablissement": "Université Côte d’Azur",
      "periode": "Sept. 2020 – Juin 2023",
      "details": [
        "Statistiques avancées, Économétrie, Analyse de données, Simulation stochastique, Mention Très Bien"
      ]
    }
  ],
  "experience": [
    {
      "titre": "Data Scientist Junior",
      "entreprise": "Marine Analytics Monaco",
      "lieu": "Monaco",
      "periode": "Juin 2022 – Déc. 2022",
      "details": [
        "Optimisation de trajets maritimes, réduction de l’empreinte carbone, tableaux de bord interactifs"
      ]
    },
    {
      "titre": "Stage en Data Analytics",
      "entreprise": "Azur Innovations",
      "lieu": "Nice, France",
      "periode": "Mai 2021 – Août 2021",
      "details": [
        "Analyse des données touristiques, visualisation, prévision d’affluence, tourisme durable"
      ]
    }
  ]
}
```
## 💬 Commande Discord

Utilisation :

Attachez un fichier .pdf contenant un CV à un message

Tapez la commande : !parse_cv

Le bot vous renverra un fichier .json contenant les données extraites.

##  👥 Contributeurs

Projet développé par le Groupe 4 du Master 1 DS2E
Merci à tous les testeurs et reviewers ✨

