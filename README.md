#Partie I : Webscrapping  des offres d'alternance. 













# Partie 2 :  Webscrapping des offres de stage

## Introduction

Afin d’augmenter le volume et la diversité des offres d’emploi collectées, il a paru évident d’ouvrir la thématique aux **stages**. Cela permet d’obtenir plus de résultats, de couvrir un public plus large (étudiants, jeunes diplômés) et d’analyser les tendances du marché sur différents niveaux d’expérience.

---

## 1. Webscraping des stages sur Indeed

La première étape consiste à utiliser le package [`jobspy`](https://github.com/cullenwatson/JobSpy) pour scraper les offres de stage sur Indeed.  
Le mot-clé utilisé est **"stage"** ou sa traduction selon la langue et le pays ciblé :

- **France** : `stage` 
- **UK/USA** : `trainee`
- **Allemagne** : `praktikum`

Pour chaque recherche, un filtrage géographique est appliqué :
- **France** : les deux dernières recherches ciblent spécifiquement la France
- **UK** : ciblage sur le Royaume-Uni
- **USA** : ciblage sur les États-Unis
- **Allemagne** : ciblage sur l’Allemagne

L’objectif est d’obtenir un maximum d’offres pertinentes pour chaque zone géographique, en adaptant le mot-clé à la langue locale.

---

## 2. Webscraping des stages via Google Jobs

Dans un second temps, le même package `jobspy` est utilisé pour interroger **Google Jobs**.  
Google Jobs agrège des offres provenant de multiples plateformes, ce qui permet d’optimiser la couverture et la diversité des résultats.

La démarche reste similaire :
- Utilisation des mots-clés adaptés à chaque pays (`trainee`, `praktikum`, `stage`, etc.)
- Filtrage par pays (France, UK, USA, Allemagne)

Cela permet de croiser les résultats d’Indeed avec ceux de Google Jobs, pour maximiser les chances de trouver des offres variées et récentes.

---

## 3. Optimisation et perspectives

- **Optimisation** :  
  Les recherches sont pensées pour maximiser la pertinence (mot-clé adapté, filtrage géographique) et la diversité des sources.
- **Fusion des résultats** :  
  À ce stade, les résultats de chaque recherche (Indeed, Google Jobs) sont conservés séparément.  
  Une amélioration possible serait de fusionner les résultats par langue ou par pays, afin de faciliter l’analyse comparative et d’éviter les doublons.
- **Scalabilité** :  
  Le package `jobspy` permet d’étendre facilement la collecte à d’autres plateformes (Glassdoor, LinkedIn, etc.) ou à d’autres mots-clés.



