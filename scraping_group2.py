import requests
import difflib
from urllib.parse import urlencode


class FranceTravailAPI:
   def __init__(self, client_id=None, client_secret=None):
       self.client_id = client_id or "PAR_monapplication_2467f1b7d6ed37ff4e9cae002054f0ee3cf2c000a17ca4bef29c7582d57a047c" ## RENTRER LE CLIENT ID DANS LES GUILLEMETS


       self.client_secret = client_secret or "1279149170b3d55082f4b59975f8b6b0b1ce4e425a18af21075c7c6953ba34b0" ## RENTRER LE CODE SECRET ENTRE LES GUILLEMETS


       self.token = self.get_token()
       self.communes = self.get_communes()


   def get_token(self):
       url = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=/partenaire"
       payload = {
           "grant_type": "client_credentials",
           "client_id": self.client_id,
           "client_secret": self.client_secret,
           "scope": "api_offresdemploiv2 o2dsoffre"
       }
       headers = {
           "Content-Type": "application/x-www-form-urlencoded"
       }
       response = requests.post(url, data=payload, headers=headers)
       response.raise_for_status()
       return response.json()["access_token"]


   def get_communes(self):
       url = "https://api.francetravail.io/partenaire/offresdemploi/v2/referentiel/communes"
       headers = {
           "Authorization": f"Bearer {self.token}",
           "Accept": "application/json"
       }
       response = requests.get(url, headers=headers)
       response.raise_for_status()
       return response.json()


   def find_commune_code(self, input_name):
       input_cleaned = input_name.upper().replace("-", " ").strip()
       noms_communes = [commune["libelle"] for commune in self.communes]
       best_match = difflib.get_close_matches(input_cleaned, noms_communes, n=1, cutoff=0.6)


       if best_match:
           for commune in self.communes:
               if commune["libelle"] == best_match[0]:
                   return {
                       "nom_corrige": best_match[0],
                       "code_insee": commune["code"],
                       "code_postal": commune["codePostal"],
                       "departement": commune["codeDepartement"]
                   }
       return None


   def determine_zone_recherche(self, ville_input):
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
           commune_info = self.find_commune_code(ville_input)
           if commune_info:
               return {
                   "type": "commune",
                   "valeur": commune_info["code_insee"],
                   "nom_corrige": commune_info["nom_corrige"]
               }
       return None


   def search_offres(self, zone_type, zone_code, mots_cles):
       url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
       params = {
           "motsCles": mots_cles,
           "distance": "40",  # rayon par défaut à 40km
           "sort": "0",  # trie par pertinence
           "offresPartenaires": "true"
       }


       if zone_type == "commune":
           params["commune"] = zone_code
       elif zone_type == "departement":
           params["departement"] = zone_code


       full_url = f"{url}?{urlencode(params)}"
       print("URL de la requête : ", full_url)


       headers = {
           "Authorization": f"Bearer {self.token}",
           "Accept": "application/json"
       }
       response = requests.get(url, headers=headers, params=params)
       response.raise_for_status()
       return response.json()


   def recherche_offres(self, ville_input, mots_cles):


       try:
           zone = self.determine_zone_recherche(ville_input)
           if not zone:
               return {"erreur": "Commune introuvable. Vérifiez l'orthographe."}


           offres = self.search_offres(zone["type"], zone["valeur"], mots_cles)
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






#Exemple de comment utiliser mais surement différent pour discord
#mais l'objet étant une classe, l'intégration dans discord devrait être facile.
if __name__ == "__main__":
   api = FranceTravailAPI()
   ville = input("Entrez le nom de la ville : ")
   mots_cles = input("Entrez les mots-clés de l'offre : ")
  
   resultats = api.recherche_offres(ville, mots_cles)
   print(resultats)

