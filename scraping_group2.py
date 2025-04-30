import difflib
import requests
from urllib.parse import urlencode

def get_token():


   url = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=/partenaire"
   payload = {
       "grant_type": "client_credentials",
       "client_id": "PAR_recuperateuroffressel_201263b93beec49e65d91dd35e577cc10da48c610f24e5185947ec13702f76fd",## RENTRER LE CLIENT ID DANS LES GUILLEMETS
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
       "distance": "30",
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


   zone = determine_zone_recherche(ville_input, communes)
   if zone:
       print(f"Recherche à proximité de : {zone['nom_corrige']}")
       offres = search_offres(token, zone["type"], zone["valeur"], mots_cles)
       print(f"{offres['resultats'][0] if offres['resultats'] else 'Aucune offre trouvée.'}")
       print(f"Nombre total d'offres : {len(offres['resultats'])}")
   else:
       print("Commune introuvable. Vérifiez l'orthographe.")






token = get_token()
communes = get_communes(token)




ville = input("Entrez le nom de la ville : ")
mots_cles = input("Entrez les mots-clés de l'offre : ")


recherche_offres(token, communes, ville, mots_cles)
