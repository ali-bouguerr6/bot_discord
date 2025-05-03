import discord
from discord import app_commands
from utils.helper import get_user_data, check_user_prerequisites

def setup_compare_command(bot):
    @bot.tree.command(name="comparer_cv_offre", description="Comparer votre CV avec la fiche de poste")
    async def comparer_cv_offre(interaction: discord.Interaction):
        await interaction.response.defer()
        
        # Vérifier que l'utilisateur a téléchargé un CV et sélectionné une offre
        error_message = check_user_prerequisites(interaction.user.id, need_cv=True, need_job_offer=True)
        if error_message:
            await interaction.followup.send(error_message, ephemeral=True)
            return
        
        try:
            user = get_user_data(interaction.user.id)
            
            # Ici, nous pouvons appeler la fonction de comparaison développée par un collègue
            # from path.to.cv_job_matcher import compare_cv_job
            # resultats = compare_cv_job(user.cv_text, user.job_offer)
            
            # Simulation de résultats en attendant la fonction réelle
            correspondance = 78  # pourcentage de correspondance
            points_forts = ["Excellente expérience en Python", "Bonne formation académique"]
            points_amelioration = ["Expérience en cloud computing limitée", "Pas de certification mentionnée"]
            conseils = ["Mettre en avant vos projets personnels", "Détailler davantage votre expérience en développement web"]
            
            # Création de la réponse
            embed = discord.Embed(
                title=f"Comparaison CV vs Offre: {user.job_offer['titre']}",
                description=f"Taux de correspondance: **{correspondance}%**",
                color=discord.Color.blue()
            )
            
            embed.add_field(name="📈 Points forts", value="\n".join([f"✅ {p}" for p in points_forts]), inline=False)
            embed.add_field(name="🔍 Points à améliorer", value="\n".join([f"❗ {p}" for p in points_amelioration]), inline=False)
            embed.add_field(name="💡 Conseils", value="\n".join([f"- {c}" for c in conseils]), inline=False)
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            print(f"Erreur lors de la comparaison CV/offre: {e}")
            await interaction.followup.send(f"Une erreur s'est produite lors de la comparaison: {e}", ephemeral=True)
