import requests
import difflib
from urllib.parse import urlencode




def get_token():


   url = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=/partenaire"
   payload = {
       "grant_type": "client_credentials",
       "client_id": "PAR_recuperateuroffressel_201263b93beec49e65d91dd35e577cc10da48c610f24e5185947ec13702f76fd", ## RENTRER LE CLIENT ID DANS LES GUILLEMETS
       "client_secret": "1200839c51315a11b6619dcbab857711dc67f6591696feddc6169c191590f158", ## RENTRER LE CODE SECRET ENTRE LES GUILLEMETS
       "scope": "api_offresdemploiv2 o2dsoffre"
   }
   headers = {
       "Content-Type": "application/x-www-form-urlencoded"
   }
   response = requests.post(url, data=payload, headers=headers)
   response.raise_for_status()
   return response.json()["access_token"]




def get_communes(token):
   url = "https://api.francetravail.io/partenaire/offresdemploi/v2/referentiel/communes"
   headers = {
       "Authorization": f"Bearer {token}",
       "Accept": "application/json"
   }
   response = requests.get(url, headers=headers)
   response.raise_for_status()
   return response.json()




def find_commune_code(input_name, communes):
   input_cleaned = input_name.upper().replace("-", " ").strip()


   noms_communes = [commune["libelle"] for commune in communes]
   best_match = difflib.get_close_matches(input_cleaned, noms_communes, n=1, cutoff=0.6)
   print(best_match)


   if best_match:
       for commune in communes:
           if commune["libelle"] == best_match[0]:
               print(commune["libelle"])
               return {
                   "nom_corrige": best_match[0],
                   "code_insee": commune["code"],
                   "code_postal": commune["codePostal"],
                   "departement": commune["codeDepartement"]
               }
   return None




def determine_zone_recherche(ville_input, communes):


   villes_specifiques = {
       "PARIS": "75",
       "LYON": "69"
   }
   ville_upper = ville_input.upper().strip()
  
   if ville_upper in villes_specifiques:
       return {
           "type": "departement",
           "valeur": villes_specifiques[ville_upper],
           "nom_corrige": ville_upper
       }
   else:
       commune_info = find_commune_code(ville_input, communes)
       if commune_info:
           return {
               "type": "commune",
               "valeur": commune_info["code_insee"],
               "nom_corrige": commune_info["nom_corrige"]
           }
   return None




def search_offres(token, zone_type, zone_code, mots_cles):
   url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
   params = {
       "motsCles": mots_cles,
       "distance": "40", 
       "sort": "0", 
       "offresPartenaires": "true"
    
   }


   if zone_type == "commune":
       params["commune"] = zone_code
   elif zone_type == "departement":
       params["departement"] = zone_code


   full_url = f"{url}?{urlencode(params)}"
   print("URL de la requête : ", full_url)


   headers = {
       "Authorization": f"Bearer {token}",
       "Accept": "application/json"
   }
   response = requests.get(url, headers=headers, params=params)
   response.raise_for_status()
   return response.json()




def recherche_offres(token, communes, ville_input, mots_cles):
   try:
       zone = determine_zone_recherche(ville_input, communes)
       if not zone:
           return {"erreur": "Commune introuvable. Vérifiez l'orthographe."}


       offres = search_offres(token, zone["type"], zone["valeur"], mots_cles)
       if not offres.get("resultats"):
           return {"message": f"Aucune offre trouvée pour '{mots_cles}' à {zone['nom_corrige']}."}


       resultats_utiles = []
       for offre in offres["resultats"]:
           resultat = {
               "titre": offre.get("intitule", "Titre non renseigné"),
               "entreprise": offre.get("entreprise", {}).get("nom", "Entreprise non précisée"),
               "lieu": offre.get("lieuTravail", {}).get("libelle", "Lieu non précisé"),
               "date": offre.get("dateCreation", "Date non renseignée"),
               "contrat": offre.get("typeContratLibelle", "Non précisé"),
               "salaire": offre.get("salaire", {}).get("libelle", "Non précisé"),
               "dureeTravail": offre.get("dureeTravailLibelle", "Non précisé"),
               "description": offre.get("description", "Aucune description disponible."),
               "competences": [comp.get("libelle", "") for comp in offre.get("competences", [])],
               "lien": offre.get("origineOffre", {}).get("urlOrigine", "Lien indisponible")
           }
           resultats_utiles.append(resultat)


       return {
           "ville": zone["nom_corrige"],
           "zone_type": zone["type"],
           "zone_valeur": zone["valeur"],
           "nombre_offres": len(resultats_utiles),
           "offres": resultats_utiles
       }


   except requests.exceptions.RequestException as e:
       return {"erreur": f"Erreur réseau ou problème API : {e}"}
   except Exception as e:
       return {"erreur": f"Erreur inattendue : {str(e)}"}




token = get_token()
communes = get_communes(token)




ville = input("Entrez le nom de la ville : ")
mots_cles = input("Entrez les mots-clés de l'offre : ")


print(recherche_offres(token, communes, ville, mots_cles))