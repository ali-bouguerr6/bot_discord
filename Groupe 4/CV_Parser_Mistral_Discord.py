"""
=============================================================================
                                  CV Parser
=============================================================================

Description:
-----------
Ce programme permet d'extraire automatiquement les informations d'un CV au format PDF et de les convertir en JSON structuré. Il utilise l’API Mistral AI pour analyser le texte du CV et générer un résultat cohérent et exploitable.

Le système est intégré à un bot Discord, qui offre une interface utilisateur simplifiée via la commande `!parse_cv`. Lorsqu’un utilisateur envoie un CV en pièce jointe à cette commande, le bot télécharge le fichier, en extrait le texte, l’analyse via l’API Mistral, et retourne un fichier JSON contenant les données extraites.

Cette solution facilite l'analyse de CV directement depuis Discord, sans nécessiter d’intervention manuelle ni d’interface utilisateur graphique.

Note sur le développement:
------------------------
Plusieurs versions préliminaires du programme ont été développées à l’aide d’expressions régulières pour extraire les informations clés. Cette méthode a rapidement montré ses limites : le code devenait inutilisable dès qu’un CV présentait une mise en page ou une structure différente.

L'approche retenue repose finalement sur l'intelligence artificielle (Mistral AI), qui permet une extraction beaucoup plus flexible et robuste, quels que soient le format ou la présentation du CV.

Packages requis:
--------------
- requests: pour communiquer avec l'API Mistral
- json: pour manipuler les données JSON
- pathlib: pour gérer les chemins de fichiers
- PyPDF2: pour extraire le texte des fichiers PDF
- re: pour les expressions régulières
- discord.py: pour la création du bot Discord

Installation des dépendances:
---------------------------
pip install requests PyPDF2 discord.py

Configuration requise:
-------------------
1. Créer un compte sur https://console.mistral.ai/
2. Générer une clé API dans votre compte Mistral
3. Remplacer la valeur de MISTRAL_API_KEY dans le code par votre clé API
4. Spécifier le token Discord dans BOT_TOKEN
5. Lancer le bot et utiliser la commande !parse_cv avec un fichier PDF attaché

Structure du JSON:
----------------
Le JSON généré contient les sections suivantes:
- prenom_nom: Nom complet de la personne
- email: Adresse email
- telephone: Numéro de téléphone
- linkedin: Nom d'utilisateur LinkedIn (si présent dans le CV)
- github: Nom d'utilisateur GitHub (si présent dans le CV)
- competences_techniques: Liste des compétences techniques (uniquement langages et logiciels)
- soft_skills: Liste des compétences personnelles (soft skills)
- langues: Liste des langues maîtrisées et leur niveau
- certifications: Liste des certifications (permis, langues, compétences)
- formation: Liste des formations avec titre, établissement, période, détails
- experience: Liste des expériences professionnelles avec titre, entreprise,
             lieu, période, détails

Validation:
---------
Le bot et son système d’analyse ont été testés avec succès sur plusieurs CV aux mises en page variées. Le programme s’adapte efficacement à différents formats et structures.
=============================================================================
"""

import discord
from discord.ext import commands
import os
import io
import tempfile
import requests
import json
import PyPDF2
import re
from pathlib import Path

# Configuration du bot Discord
BOT_TOKEN = "A MODIF"  # Remplacez par votre token Discord
COMMAND_PREFIX = "!"
MISTRAL_API_KEY = "A MODIF"  # Utilisez votre clé API Mistral
API_URL = "https://api.mistral.ai/v1/chat/completions"

# Intents pour le bot Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

@bot.event
async def on_ready():
    """Événement déclenché lorsque le bot est prêt et connecté"""
    print(f"{bot.user} est connecté à Discord!")
    print("------")

def extraire_texte_pdf(fichier_pdf):
    """
    Extrait le texte d'un fichier PDF
    
    Args:
        fichier_pdf (bytes): Contenu binaire du fichier PDF
        
    Returns:
        str: Texte extrait du PDF
    """
    try:
        texte = ""
        # Utiliser BytesIO pour lire les données binaires
        pdf_stream = io.BytesIO(fichier_pdf)
        lecteur_pdf = PyPDF2.PdfReader(pdf_stream)
        for page in lecteur_pdf.pages:
            texte += page.extract_text() + "\n"
        return texte
    except Exception as e:
        print(f"Erreur lors de l'extraction du texte du PDF: {e}")
        return None

def generer_json_avec_mistral(texte_cv):
    """
    Envoie le texte du CV à l'API Mistral pour générer directement le JSON
    
    Args:
        texte_cv (str): Texte du CV extrait du PDF
        
    Returns:
        str: JSON généré par Mistral
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MISTRAL_API_KEY}"
    }
    
    # Liste des compétences techniques et soft skills à rechercher pour aider le modèle
    liste_competences = """
    Exemples de compétences techniques à identifier (UNIQUEMENT les outils concrets et langages de programmation):
    
    # Langages de programmation
    Python, R, Java, C, C++, C#, JavaScript, TypeScript, PHP, Ruby, Swift, Kotlin, Go, Rust, SQL, Scala, Perl, Shell, Bash, PowerShell, MATLAB, VBA
    
    # Data Science et ML (outils uniquement)
    TensorFlow, PyTorch, Keras, Scikit-learn, Pandas, NumPy, SciPy, NLTK, spaCy, Matplotlib, Seaborn
    
    # Web et Frontend
    HTML, CSS, Bootstrap, React, Angular, Vue.js, jQuery, REST API, GraphQL, Node.js, Express
    
    # Bases de données
    MySQL, PostgreSQL, SQLite, Oracle, MongoDB, Redis, Elasticsearch, NoSQL, SQL Server, MariaDB
    
    # DevOps et Cloud
    AWS, Azure, GCP, Docker, Kubernetes, Git, GitHub, GitLab, CI/CD, Jenkins, Linux, Unix, Windows, MacOS
    
    # Bureautique et outils
    Microsoft Office, Microsoft 365, Office 365, Suite Office, Excel, Word, PowerPoint, Access, Outlook, OneNote, SharePoint, OneDrive, Teams, Microsoft Teams, Tableau, Power BI, SAP, Salesforce, Jira, Confluence, Trello, MS Project
    
    # Autres outils techniques
    LaTeX, RStudio, Jupyter, Orange, SAS, SPSS
    
    ATTENTION: N'inclus PAS les domaines de connaissances ou sujets théoriques comme compétences techniques.
    Par exemple, n'inclus PAS: Économie, Microéconomie, Macroéconomie, Comptabilité, Finance, Droit, Mathématiques, 
    Statistiques théoriques, Machine Learning théorique, etc. 
    
    Inclus UNIQUEMENT les outils et langages concrets que la personne sait utiliser.
    
    Exemples de soft skills à identifier:
    Communication, leadership, travail d'équipe, résolution de problèmes, gestion de projet, organisation, autonomie, adaptabilité, créativité, esprit critique, négociation, intelligence émotionnelle, gestion du temps, gestion du stress, écoute active, empathie, flexibilité, prise de décision, persuasion, présentation, prise de parole en public
    
    Exemples de certifications:
    Permis B, Permis BVA, TOEIC, TOEFL, IELTS, Cambridge Certificate, DELF, DALF, HSK, PIX, Google Analytics, Certification Microsoft, Certification AWS, Certification Azure, ITIL, PMP, PRINCE2
    """
    
    # Construire le prompt pour Mistral
    prompt = f"""
    Voici le texte complet d'un CV extrait d'un fichier PDF. Analyse-le et convertis-le directement en JSON avec la structure suivante:

    ```json
    {{
      "prenom_nom": "string",
      "email": "string",
      "telephone": "string",
      "linkedin": "string (seulement le nom d'utilisateur, pas l'URL complète, ou vide si non présent)",
      "github": "string (seulement le nom d'utilisateur, pas l'URL complète, ou vide si non présent)",
      "competences_techniques": [
        "compétence technique 1",
        "compétence technique 2"
      ],
      "soft_skills": [
        "soft skill 1",
        "soft skill 2"
      ],
      "langues": [
        "string (langue et niveau)"
      ],
      "certifications": [
        "string (certification 1)",
        "string (certification 2)"
      ],
      "formation": [
        {{
          "titre": "string (diplôme et spécialité)",
          "etablissement": "string (nom de l'école/université)",
          "periode": "string (dates de début et fin)",
          "details": [
            "string (enseignements, mentions, etc.)"
          ]
        }}
      ],
      "experience": [
        {{
          "titre": "string (intitulé du poste)",
          "entreprise": "string (nom de l'entreprise)",
          "lieu": "string (ville/pays ou télétravail)",
          "periode": "string (dates de début et fin)",
          "details": [
            "string (responsabilités, accomplissements)"
          ]
        }}
      ]
    }}
    ```

    Instructions spéciales:
    - Inclus TOUJOURS les champs "linkedin" et "github" dans le JSON, même s'ils sont vides ("").
    - Pour LinkedIn, si tu trouves une URL comme "linkedin.com/in/nom-utilisateur", n'inclus que "nom-utilisateur". Si tu trouves directement "/linkedin-innom-utilisateur", n'inclus que "nom-utilisateur".
    - Pour GitHub, si tu trouves une URL comme "github.com/nom-utilisateur", n'inclus que "nom-utilisateur". Si tu trouves directement "/githubnom-utilisateur", n'inclus que "nom-utilisateur".
    - Si aucun profil LinkedIn ou GitHub n'est mentionné dans le CV, laisse ces champs vides: "linkedin": "", "github": "".
    
    - IMPORTANT: Pour les compétences techniques, inclus UNIQUEMENT les langages de programmation, logiciels, et outils concrets.
      * Ne pas inclure dans cette section les domaines de connaissances théoriques comme l'économie, la finance, les mathématiques, etc.
      * Limite-toi aux compétences techniques concrètes et opérationnelles (langages, logiciels, frameworks, etc.)
      * Assure-toi d'inclure les outils de la suite Microsoft Office (Word, Excel, PowerPoint) et Microsoft 365 s'ils sont mentionnés dans le CV
    
    - Identifie et liste toutes les soft skills (compétences personnelles, interpersonnelles et transversales).
    
    - CERTIFICATIONS:
      * Recherche et inclus toutes les certifications mentionnées dans le CV.
      * Permis de conduire (B, BVA, etc.), certifications de langue (TOEIC, TOEFL, etc.), certifications informatiques (PIX, etc.)
      * Si aucune certification n'est mentionnée, laisse la liste vide: []
    
    - Tu dois ABSOLUMENT inclure les champs "competences_techniques", "soft_skills" et "certifications" dans le JSON final, même s'ils sont vides.

    {liste_competences}

    Texte du CV:
    {texte_cv}

    Retourne UNIQUEMENT le JSON sans aucun autre commentaire. Assure-toi que le format est valide.
    """
    
    # Préparer la requête pour l'API
    payload = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2  # Température plus basse pour respecter plus strictement le format demandé
    }
    
    try:
        # Envoyer la requête à l'API Mistral
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        # Extraire la réponse
        resultat = response.json()
        reponse_mistral = resultat["choices"][0]["message"]["content"]
        
        # Extraire uniquement le JSON de la réponse (au cas où Mistral ajoute des commentaires)
        json_pattern = r"```json\s*([\s\S]*?)\s*```|^\s*(\{[\s\S]*\})\s*$"
        match = re.search(json_pattern, reponse_mistral)
        
        if match:
            json_str = match.group(1) or match.group(2)
            
            # Vérifier que le JSON est valide
            try:
                json_obj = json.loads(json_str)
                
                # Post-traitement pour détecter Microsoft Office et ses composants
                if "competences_techniques" in json_obj:
                    # Liste des termes bureautiques à rechercher dans le texte du CV
                    bureautique_terms = [
                        "Microsoft Office", "MS Office", "Office", "Suite Office", 
                        "Microsoft 365", "Office 365", "M365", "O365",
                        "Excel", "Word", "PowerPoint", "PPT", "Access", "Outlook",
                        "OneNote", "SharePoint", "OneDrive", "Teams", "Microsoft Teams"
                    ]
                    
                    # Vérifier si ces termes sont dans le texte du CV mais pas dans les compétences
                    found_terms = set()
                    for term in bureautique_terms:
                        pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
                        if pattern.search(texte_cv):
                            # Normaliser le nom de la compétence (première lettre de chaque mot en majuscule)
                            normalized_term = ' '.join(word.capitalize() for word in term.split())
                            found_terms.add(normalized_term)
                    
                    # Ajouter les termes trouvés qui ne sont pas déjà dans les compétences
                    for term in found_terms:
                        if not any(comp.lower() == term.lower() for comp in json_obj["competences_techniques"]):
                            json_obj["competences_techniques"].append(term)
                
                # Vérifier que tous les champs requis sont présents, sinon les ajouter
                champs_requis = ["linkedin", "github", "competences_techniques", "soft_skills", "certifications"]
                for champ in champs_requis:
                    if champ not in json_obj:
                        if champ in ["linkedin", "github"]:
                            json_obj[champ] = ""
                        elif champ in ["competences_techniques", "soft_skills", "certifications"]:
                            json_obj[champ] = []
                
                return json.dumps(json_obj, ensure_ascii=False, indent=2)
            except json.JSONDecodeError as e:
                print(f"Erreur lors du décodage du JSON: {e}")
                print(f"JSON reçu: {json_str}")
                return None
        else:
            # Si Mistral n'a pas utilisé de balises de code, essayons de parser directement
            try:
                json_obj = json.loads(reponse_mistral)
                
                # Post-traitement pour détecter Microsoft Office et ses composants
                if "competences_techniques" in json_obj:
                    # Liste des termes bureautiques à rechercher dans le texte du CV
                    bureautique_terms = [
                        "Microsoft Office", "MS Office", "Office", "Suite Office", 
                        "Microsoft 365", "Office 365", "M365", "O365",
                        "Excel", "Word", "PowerPoint", "PPT", "Access", "Outlook",
                        "OneNote", "SharePoint", "OneDrive", "Teams", "Microsoft Teams"
                    ]
                    
                    # Vérifier si ces termes sont dans le texte du CV mais pas dans les compétences
                    found_terms = set()
                    for term in bureautique_terms:
                        pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
                        if pattern.search(texte_cv):
                            # Normaliser le nom de la compétence (première lettre de chaque mot en majuscule)
                            normalized_term = ' '.join(word.capitalize() for word in term.split())
                            found_terms.add(normalized_term)
                    
                    # Ajouter les termes trouvés qui ne sont pas déjà dans les compétences
                    for term in found_terms:
                        if not any(comp.lower() == term.lower() for comp in json_obj["competences_techniques"]):
                            json_obj["competences_techniques"].append(term)
                
                # Vérifier que tous les champs requis sont présents, sinon les ajouter
                champs_requis = ["linkedin", "github", "competences_techniques", "soft_skills", "certifications"]
                for champ in champs_requis:
                    if champ not in json_obj:
                        if champ in ["linkedin", "github"]:
                            json_obj[champ] = ""
                        elif champ in ["competences_techniques", "soft_skills", "certifications"]:
                            json_obj[champ] = []
                
                return json.dumps(json_obj, ensure_ascii=False, indent=2)
            except json.JSONDecodeError:
                print("Impossible d'extraire un JSON valide de la réponse Mistral")
                print(f"Réponse reçue: {reponse_mistral}")
                return None
    
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la communication avec l'API Mistral: {e}")
        return None

@bot.command(name="parse_cv")
async def parse_cv(ctx):
    """
    Commande pour traiter un CV PDF et le convertir en JSON
    Le CV doit être attaché au message comme pièce jointe
    """
    # Vérifier si un fichier est attaché au message
    if not ctx.message.attachments:
        await ctx.send("❌ Veuillez attacher un fichier PDF contenant le CV à analyser.")
        return
    
    attachment = ctx.message.attachments[0]
    
    # Vérifier si le fichier est au format PDF
    if not attachment.filename.lower().endswith('.pdf'):
        await ctx.send("❌ Le fichier doit être au format PDF.")
        return
    
    # Informer l'utilisateur que le traitement commence
    processing_msg = await ctx.send("⏳ Traitement du CV en cours... Veuillez patienter.")
    
    try:
        # Télécharger le fichier PDF
        pdf_content = await attachment.read()
        
        # Extraire le texte du PDF
        texte_cv = extraire_texte_pdf(pdf_content)
        if not texte_cv:
            await processing_msg.edit(content="❌ Impossible d'extraire le texte du PDF. Veuillez vérifier que le fichier est valide.")
            return
        
        # Générer le JSON avec Mistral
        await processing_msg.edit(content="⏳ Analyse du CV avec Mistral AI en cours...")
        json_str = generer_json_avec_mistral(texte_cv)
        if not json_str:
            await processing_msg.edit(content="❌ Erreur lors de la génération du JSON. Veuillez réessayer plus tard.")
            return
        
        # Créer un fichier temporaire pour stocker le JSON
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp_file:
            temp_file.write(json_str.encode('utf-8'))
            temp_path = temp_file.name
        
        # Envoyer le fichier JSON en réponse
        await processing_msg.edit(content="✅ Traitement terminé ! Voici le fichier JSON généré:")
        await ctx.send(file=discord.File(temp_path, f"{attachment.filename.rsplit('.', 1)[0]}.json"))
        
        # Supprimer le fichier temporaire
        os.unlink(temp_path)
        
    except Exception as e:
        await processing_msg.edit(content=f"❌ Une erreur est survenue lors du traitement: {str(e)}")

@bot.command(name="help_cv")
async def help_cv(ctx):
    """Affiche l'aide pour l'utilisation du bot CV Parser"""
    help_text = """
**🤖 Bot CV Parser - Aide**

Ce bot permet de convertir un CV au format PDF en un fichier JSON structuré.

**Commandes disponibles:**
• `!parse_cv` - Analyse un CV PDF et renvoie un fichier JSON structuré
  *Utilisation:* Joignez un fichier PDF à votre message et tapez `!parse_cv`
  
• `!help_cv` - Affiche ce message d'aide

**Fonctionnalités:**
• Extraction des informations personnelles (nom, email, téléphone)
• Détection des profils LinkedIn et GitHub
• Analyse des compétences techniques (langages, outils, etc.)
• Identification des soft skills
• Extraction des langues et certifications
• Liste des formations et expériences professionnelles

**Remarque:** Le traitement peut prendre quelques secondes, selon la taille du CV.
"""
    await ctx.send(help_text)

# Lancer le bot avec le token
bot.run(BOT_TOKEN)
