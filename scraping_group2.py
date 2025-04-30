import requests
import difflib
from urllib.parse import urlencode
import re
import pprint




class FranceTravailAPI:
   def __init__(self, client_id=None, client_secret=None):
       self.client_id = client_id or "PAR_scrappinggroupe2_fa66652706eede69dc3a6d6b16ae9b2aac8e7c0d80ba202f3da9c32233837ba4"
       self.client_secret = client_secret or "dcd274a3f37e29e40f0998e8f65ac5da2598b42acad3d762e437db0af747a315"
      
       try:
           self.token = self.get_token()
           self.communes = self.get_communes()
       except Exception as e:
           print(f"Erreur d'initialisation : {str(e)}")
           raise


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
      
       try:
           response = requests.post(url, data=payload, headers=headers)
          
           if response.status_code != 200:
               if response.status_code == 401:
                   error_msg = "Erreur d'authentification: vérifiez vos identifiants"
               elif response.status_code == 429:
                   error_msg = "Trop de requêtes envoyées à l'API"
               else:
                   error_msg = f"Erreur HTTP {response.status_code}: {response.text}"
               raise Exception(error_msg)
              
           data = response.json()
           if "access_token" not in data:
               raise Exception("Token non trouvé dans la réponse")
              
           return data["access_token"]
          
       except requests.exceptions.ConnectionError:
           raise Exception("Impossible de se connecter au serveur d'authentification")
       except requests.exceptions.Timeout:
           raise Exception("Délai d'attente dépassé lors de l'authentification")
       except requests.exceptions.RequestException as e:
           raise Exception(f"Erreur lors de la requête d'authentification: {str(e)}")
       except ValueError:
           raise Exception("Réponse non-JSON reçue")


   def get_communes(self):
       url = "https://api.francetravail.io/partenaire/offresdemploi/v2/referentiel/communes"
       headers = {
           "Authorization": f"Bearer {self.token}",
           "Accept": "application/json"
       }
      
       try:
           response = requests.get(url, headers=headers)
          
           if response.status_code != 200:
               if response.status_code == 401:
                   raise Exception("Token d'authentification invalide ou expiré")
               else:
                   raise Exception(f"Erreur HTTP {response.status_code}: {response.text}")
                  
           return response.json()
          
       except requests.exceptions.RequestException as e:
           raise Exception(f"Erreur lors de la récupération des communes: {str(e)}")


   def find_commune_code(self, input_name):
       if not input_name or not isinstance(input_name, str):
           return None
      
       input_cleaned = input_name.upper().replace("-", " ").strip()
  
       try:
           noms_communes = [commune["libelle"] for commune in self.communes]
           best_match = difflib.get_close_matches(input_cleaned, noms_communes, n=1, cutoff=0.6)


           if best_match:
               for commune in self.communes:
                   if commune["libelle"] == best_match[0]:
                       return {
                           "nom_corrige": best_match[0],
                           "code_insee": commune["code"]
                       }
           return None
      
       except Exception as e:
           print(f"Erreur lors de la recherche de code commune pour '{input_name}': {str(e)}")
           return None


   def determine_zone_recherche(self, ville_input):
       if not ville_input:
           return None
      
       villes_specifiques = {
           "PARIS": "75",
           "LYON": "69"
       }
  
       try:
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
              
       except Exception as e:
           print(f"Erreur lors de la détermination de la zone pour '{ville_input}': {str(e)}")
           return None


   def search_offres(self, zone_type, zone_code, mots_cles):
       if not zone_type or zone_type not in ["commune", "departement"]:
           raise ValueError(f"Type de zone invalide: {zone_type}")
          
       if not zone_code:
           raise ValueError("Code de zone obligatoire")
          
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


       headers = {
           "Authorization": f"Bearer {self.token}",
           "Accept": "application/json"
       }
      
       try:
           response = requests.get(url, headers=headers, params=params)
          
           if response.status_code != 200:
               if response.status_code == 401:
                   raise Exception("Token d'authentification expiré")
               elif response.status_code == 404:
                   raise Exception("Ressource non trouvée")
               elif response.status_code == 429:
                   raise Exception("Trop de requêtes. Veuillez réessayer plus tard")
               else:
                   raise Exception(f"Erreur HTTP {response.status_code}: {response.text}")
                  
           return response.json()
          
       except requests.exceptions.ConnectionError:
           raise Exception("Impossible de se connecter au serveur")
       except requests.exceptions.Timeout:
           raise Exception("Délai d'attente dépassé")
       except requests.exceptions.RequestException as e:
           raise Exception(f"Erreur réseau: {str(e)}")


   def nettoyer_description(self, description):
       if not description:
           return "Aucune description disponible."
          
       # Remplace les sauts de ligne par un espace
       cleaned = re.sub(r'\n', ' ', description)
      
       # Remplace les espaces multiples par un seul
       cleaned = re.sub(r'\s+', ' ', cleaned)
      
       # Enlève les espaces avant la ponctuation
       cleaned = re.sub(r'\s+([.,;:!?])', r'\1', cleaned)
      
       return cleaned.strip()


   def recherche_offres(self, ville_input, mots_cles):
       try:
           if not ville_input:
               return {"erreur": "Ville obligatoire"}
              
           if not mots_cles:
               print("Avertissement: recherche sans mots-clés")
              
           zone = self.determine_zone_recherche(ville_input)
           if not zone:
               return {"erreur": "Commune introuvable. Vérifiez l'orthographe."}


           try:
               offres = self.search_offres(zone["type"], zone["valeur"], mots_cles)
              
               if not offres.get("resultats"):
                   return {"message": f"Aucune offre trouvée pour '{mots_cles}' à {zone['nom_corrige']}."}


               resultats_utiles = []
               for offre in offres["resultats"]:
                   try:
                       resultat = {
                           "titre": offre.get("intitule", "Titre non renseigné"),
                           "entreprise": offre.get("entreprise", {}).get("nom", "Entreprise non précisée"),
                           "lieu": offre.get("lieuTravail", {}).get("libelle", "Lieu non précisé"),
                           "contrat": offre.get("typeContratLibelle", "Type de contrat non précisé"),
                           "description": self.nettoyer_description(offre.get("description"))
                       }
                       resultats_utiles.append(resultat)
                   except Exception as e:
                       print(f"Erreur sur une offre: {str(e)}")
                       continue


               return {
                   "ville": zone["nom_corrige"],
                   "nombre_offres": len(resultats_utiles),
                   "offres": resultats_utiles
               }
              
           except Exception as e:
               if "Token d'authentification expiré" in str(e):
                   print("Token expiré. Tentative de renouvellement...")
                   try:
                       self.token = self.get_token()
                       return self.recherche_offres(ville_input, mots_cles)
                   except Exception as token_error:
                       return {"erreur": f"Impossible de renouveler le token: {str(token_error)}"}
               else:
                   return {"erreur": f"Erreur lors de la recherche: {str(e)}"}


       except requests.exceptions.RequestException as e:
           return {"erreur": f"Problème de connexion: {str(e)}"}
          
       except Exception as e:
           return {"erreur": f"Erreur inattendue: {str(e)}"}


# Exemple d'utilisation
if __name__ == "__main__":
   try:
       api = FranceTravailAPI()
       ville = input("Entrez le nom de la ville : ")
       mots_cles = input("Entrez les mots-clés de l'offre : ")
      
       resultats = api.recherche_offres(ville, mots_cles)
      
       if "erreur" in resultats:
           print(f"Erreur : {resultats['erreur']}")
       elif "message" in resultats:
           print(resultats["message"])
       else:
           print(f"\nRésultats pour '{mots_cles}' à {resultats['ville']} ({resultats['nombre_offres']} offres trouvées) :\n")
          
           for i, offre in enumerate(resultats["offres"], 1):
               print(f"Offre {i}/{resultats['nombre_offres']}:")
               print(f"Titre: {offre['titre']}")
               print(f"Entreprise: {offre['entreprise']}")
               print(f"Lieu: {offre['lieu']}")
               print(f"Contrat: {offre['contrat']}")
               print(f"Description:\n{offre['description']}")
               print("\n" + "-"*50 + "\n")
   except Exception as e:
       print(f"Erreur d'initialisation de l'API: {str(e)}")
       print("Vérifiez que vous avez bien renseigné votre client_id et client_secret.")


#pour bien voir la structure du dictionnaire
pprint.pprint(resultats)