import discord
from discord import app_commands
import aiohttp
import asyncio
import PyPDF2
import tempfile
import os
from utils.helper import get_user_data

def setup_cv_command(bot):
    @bot.tree.command(name="analyser_cv", description="Extraire des informations d'un CV au format PDF")
    async def analyser_cv(interaction: discord.Interaction):
        await interaction.response.send_message("Veuillez téléverser votre CV au format PDF", ephemeral=True)
        
        # Fonction pour vérifier que le message suivant contient un CV
        def check(message):
            return message.author == interaction.user and message.attachments and message.attachments[0].filename.endswith('.pdf')
        
        try:
            # Attendre que l'utilisateur envoie un fichier PDF
            message = await bot.wait_for('message', check=check, timeout=60.0)
            attachment = message.attachments[0]
            
            # Télécharger le fichier PDF
            async with aiohttp.ClientSession() as session:
                async with session.get(attachment.url) as resp:
                    if resp.status != 200:
                        await interaction.followup.send("Erreur lors du téléchargement du fichier", ephemeral=True)
                        return
                    
                    pdf_data = await resp.read()
                    
            # Traitement du PDF pour extraire le texte
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                temp_file.write(pdf_data)
                temp_path = temp_file.name
            
            with open(temp_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                cv_text = ""
                for page in pdf_reader.pages:
                    cv_text += page.extract_text()
            
            # Supprimer le fichier temporaire
            os.unlink(temp_path)
            
            # Ici, nous pouvons appeler la fonction d'analyse de CV développée par un collègue
            # from path.to.cv_analyzer import analyze_cv
            # cv_analysis = analyze_cv(cv_text)
            
            # Stockage des données du CV
            user = get_user_data(interaction.user.id)
            user.cv_text = cv_text
            user.cv_file_name = attachment.filename
            
            # Simulation d'analyse en attendant la fonction réelle
            competences = ["Python", "Java", "SQL", "Machine Learning"]
            experiences = ["Développeur chez XYZ (2 ans)", "Stage chez ABC (6 mois)"]
            formation = ["Master en Informatique - Université XYZ"]
            
            # Stocker l'analyse simulée
            user.cv_analysis = {
                "competences": competences,
                "experiences": experiences,
                "formation": formation
            }
            
            # Création de la réponse
            embed = discord.Embed(title=f"Analyse de votre CV: {attachment.filename}", color=discord.Color.green())
            embed.add_field(name="Compétences identifiées", value="\n".join([f"- {c}" for c in competences]), inline=False)
            embed.add_field(name="Expériences professionnelles", value="\n".join([f"- {e}" for e in experiences]), inline=False)
            embed.add_field(name="Formation", value="\n".join([f"- {f}" for f in formation]), inline=False)
            
            await interaction.followup.send(embed=embed)
            
        except asyncio.TimeoutError:
            await interaction.followup.send("Délai d'attente dépassé. Veuillez réessayer la commande.", ephemeral=True)
        except Exception as e:
            print(f"Erreur lors de l'analyse du CV: {e}")
            await interaction.followup.send(f"Une erreur s'est produite lors de l'analyse du CV: {e}", ephemeral=True)
