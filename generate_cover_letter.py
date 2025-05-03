import discord
from discord import app_commands
import io
from utils.helper import get_user_data, check_user_prerequisites

def setup_letter_command(bot):
    @bot.tree.command(name="generer_lettre", description="Générer une lettre de motivation basée sur votre CV et l'offre d'emploi")
    async def generer_lettre(interaction: discord.Interaction):
        await interaction.response.defer()
        
        # Vérifier que l'utilisateur a téléchargé un CV et sélectionné une offre
        error_message = check_user_prerequisites(interaction.user.id, need_cv=True, need_job_offer=True)
        if error_message:
            await interaction.followup.send(error_message, ephemeral=True)
            return
        
        try:
            user = get_user_data(interaction.user.id)
            
            # Ici, nous pouvons appeler la fonction de génération de lettre développée par un collègue
            # from path.to.letter_generator import generate_letter
            # lettre = generate_letter(user.cv_text, user.job_offer)
            
            # Simulation de lettre de motivation en attendant la fonction réelle
            lettre = f"""
Objet : Candidature pour le poste de {user.job_offer['titre']} chez {user.job_offer['entreprise']}

Madame, Monsieur,

Actuellement à la recherche de nouvelles opportunités professionnelles, je me permets de vous adresser ma candidature pour le poste de {user.job_offer['titre']} au sein de votre entreprise.

Mon expérience en développement logiciel et mes compétences techniques correspondent aux exigences mentionnées dans votre offre. J'ai notamment travaillé sur des projets similaires qui m'ont permis de développer une expertise pertinente pour ce poste.

Je suis particulièrement intéressé(e) par {user.job_offer['entreprise']} en raison de sa réputation d'innovation et de ses valeurs qui correspondent à ma vision professionnelle.

Je serais ravi(e) de pouvoir échanger avec vous lors d'un entretien pour vous présenter plus en détail mon parcours et ma motivation.

Je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.

[Votre nom]
            """
            
            # Création de la réponse avec la lettre de motivation
            embed = discord.Embed(
                title=f"Lettre de motivation pour: {user.job_offer['titre']}",
                description="Voici votre lettre de motivation générée. Vous pouvez la télécharger ci-dessous.",
                color=discord.Color.green()
            )
            
            # Création d'un fichier texte contenant la lettre
            with io.StringIO() as file:
                file.write(lettre)
                file.seek(0)
                
                # Conversion en bytes pour l'envoi
                bytes_io = io.BytesIO(file.getvalue().encode('utf-8'))
                
                # Envoi du fichier avec l'embed
                file_discord = discord.File(bytes_io, filename=f"Lettre_Motivation_{user.job_offer['entreprise']}.txt")
                await interaction.followup.send(embed=embed, file=file_discord)
                
        except Exception as e:
            print(f"Erreur lors de la génération de la lettre: {e}")
            await interaction.followup.send(f"Une erreur s'est produite lors de la génération de la lettre: {e}", ephemeral=True)