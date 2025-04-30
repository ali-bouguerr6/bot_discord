#fichier python groupe 2 pour le scraping
#Création de la base pour récupérer les offres
import requests

def get_token():
    url = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=/partenaire"
    payload = {
        "grant_type": "client_credentials",
        "client_id": "PAR_scraping_a866f085dcff12a371d96a7baab5f5f0aa1944d66b9302bf91a193ef838feb71",
        "client_secret": "2f93b4aef7e854d72aa85727e1b2cbd4c6d84f1331ec1afae1620b3148062d14",
        "scope": "api_offresdemploiv2 o2dsoffre"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=payload, headers=headers)
    response.raise_for_status()
    return response.json()["access_token"]

def search_offres(token, code_insee, mots_cles):
    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
    params = {
        "motsCles": mots_cles,
        "distance": "50",
        "sort": "0",
        "offresPartenaires": "true",
        "commune": code_insee
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

token = get_token()

code_insee = input("Entrez le code INSEE de la ville : ")
mots_cles = input("Entrez les mots-clés de l'offre : ")

print(search_offres(token, code_insee, mots_cles))

#test
#test 5