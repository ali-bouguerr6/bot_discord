# 🔍 France Travail API - Recherche d'Offres d’Emploi
![image](https://github.com/user-attachments/assets/afe664a4-3661-42a6-b155-0b003ab2cd33)

Le groupe 2 a développé un outil Python permettant de **chercher des offres d’emploi** en utilisant l’API de France Travail. Il gère l'authentification, la géolocalisation par ville (y compris les erreurs de frappe), et renvoie des résultats d’offres d’emploi de manière structurée.

---

## 🚀 Fonctionnalités principales

- Authentification OAuth2 pour accéder à l’API.
- Récupération automatique des **codes INSEE** pour les villes saisies.
- Recherche intelligente avec tolérance aux fautes (ex : `Renne` → `Rennes`).
- Gestion des cas particuliers comme **Paris** ou **Lyon** (avec découpage par arrondissement).
- Nettoyage des descriptions d'offres (formatage lisible).
- Gestion des erreurs réseau et d’authentification.

---

## 🛠 Prérequis

Avant d’utiliser ce script, vous devez :

1. Avoir un compte sur [France Travail IO](https://www.francetravail.io/).
2. Créer une **application partenaire** dans votre espace personnel.
3. Récupérer les identifiants suivants :
   - `Client ID`
   - `Client Secret`
4. Renseigner ces identifiants dans le fichier Python (`__init__` de la classe `FranceTravailAPI`).

---

## 👥 Équipe
Ce projet a été réalisé par :
- Dalia Azzoug
- Thomas Meresse
- Jeancy Candela Nisharize
- Lucie MATT 
- Essi BALLOGOU 
- Lenny LEPETIT 
