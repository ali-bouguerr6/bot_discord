#fichier python groupe 2 pour le scraping
#Création de la base pour récupérer les offres
import requests
import difflib
from urllib.parse import urlencode

def get_token():
   url = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=/partenaire"
   payload = {
       "grant_type": "client_credentials",
       "client_id": "", ## RENTRER LE CLIENT ID DANS LES GUILLEMETS
       "client_secret": "", ## RENTRER LE CODE SECRET ENTRE LES GUILLEMETS
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



def search_offres(token, code_insee, mots_cles):
   url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
   params = {"motsCles": mots_cles,
             "distance": "50", 
             "sort": "0", 
             "offresPartenaires" : "true",
             "commune" : code_insee}


   full_url = f"{url}?{urlencode(params)}"
   print("URL de la requête : ", full_url)


   headers = {
       "Authorization": f"Bearer {token}",
       "Accept": "application/json"
   }
   response = requests.get(url, headers=headers, params=params)
   response.raise_for_status()
   return response.json()


token = get_token()
communes = get_communes(token)

ville = input("Entrez le nom de la ville : ")
mots_cles = input("Entrez les mots-clés de l'offre : ")

resultat = find_commune_code(ville, communes)


if resultat:
   print(f"Recherche à proximité de : {resultat['nom_corrige']}")
   offres = search_offres(token, resultat["code_insee"], mots_cles)
   print(f"{offres['resultats'][0] if offres['resultats'] else 'Aucune offre trouvée.'}")
else:
   print("Commune introuvable. Vérifiez l'orthographe.")