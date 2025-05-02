![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![LLM](https://img.shields.io/badge/LLM-Mistral%20%7C%20Gemini-orange)
![Platform](https://img.shields.io/badge/Platform-Discord-blue)
![UNISTRA DS2E](https://img.shields.io/badge/UNISTRA-M1_DS2E-blue)

# 📄 CV Parser – Groupe 4 (Discord + LLM) ![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
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

| Modèle           | Statut | API utilisée                               |
|------------------|--------|--------------------------------------------|
| Mistral Small    | ✅ Testé | `https://api.mistral.ai/v1/chat/completions` |
| Gemini 1.5 Pro   | ✅ Testé | Google Generative AI SDK                   |

---

## 📦 Dépendances

```bash
pip install discord requests PyPDF2 google-generativeai


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

## 🧪 Exemple d'utilisation

Nous avons créé un CV fictif spécialement pour ce projet, disponible ici :  
📄 [CV Fictif](CV_Fictif.pdf)

Si l'on attache ce fichier `.pdf` à un message sur Discord en utilisant la commande : `!parse_cv`, le bot analysera le document et renverra un fichier `.json` contenant les données extraites.

Voici un exemple de résultat pouvant être obtenu avec notre programme :  
🧾📄 [CV Fictif Résultat](CV_Fictif_Resultat.json)

## 💬 Commande Discord

**Utilisation :**

Attachez un fichier `.pdf` contenant un CV à un message faisant appel à la commande : `!parse_cv`  
Le bot vous renverra un fichier `.json` contenant les données extraites.

##  👥 Contributeurs

Projet développé par le **Groupe 4** du **Master 1 DS2E**, composé de :

- Erleta Mziu  
- Noah Herwede  
- Marie Pierron  
- Quentin Bacher  
- Arnaud Kindbeiter  
- Laïfa Ahmed-Yahia
