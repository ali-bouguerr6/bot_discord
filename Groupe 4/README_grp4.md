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
Voir l'exemple déposer dans le dossier "Groupe 4"
```
## 💬 Commande Discord

Utilisation :

Attachez un fichier .pdf contenant un CV à un message

[Cv fictif d'exemple si nécessaire ](CV_Fictif.pdf))

Tapez la commande : !parse_cv

Le bot vous renverra un fichier .json contenant les données extraites.

##  👥 Contributeurs

Projet développé par le Groupe 4 du Master 1 DS2E
Merci à tous les testeurs et reviewers ✨

