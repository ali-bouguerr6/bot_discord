# Classe pour stocker temporairement les données de l'utilisateur
class UserData:
    def __init__(self):
        self.cv_text = None
        self.job_offer = None
        self.cv_file_name = None
        self.cv_analysis = None

# Dictionnaire global pour stocker les données des utilisateurs (user_id -> UserData)
user_data = {}

def get_user_data(user_id):
    """
    Récupère les données de l'utilisateur, crée une nouvelle entrée si nécessaire
    """
    if user_id not in user_data:
        user_data[user_id] = UserData()
    return user_data[user_id]

def check_user_prerequisites(user_id, need_cv=True, need_job_offer=True):
    """
    Vérifie si l'utilisateur a téléchargé un CV et/ou sélectionné une offre d'emploi
    Retourne un message d'erreur si les conditions ne sont pas remplies, None sinon
    """
    if user_id not in user_data:
        return "Veuillez d'abord télécharger votre CV et/ou sélectionner une offre d'emploi"
    
    user = user_data[user_id]
    
    if need_cv and not user.cv_text:
        return "Veuillez d'abord télécharger votre CV avec `/analyser_cv`"
    
    if need_job_offer and not user.job_offer:
        return "Veuillez d'abord sélectionner une offre d'emploi avec `/scrape`"
    
    return None
