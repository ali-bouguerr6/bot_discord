import discord
from discord import app_commands
from utils.helper import get_user_data

class OffreSelectionView(discord.ui.View):
    def __init__(self, offres):
        super().__init__(timeout=300)
        self.offres = offres
        
        # Créer un dropdown avec les offres
        select = OffreSelect(offres)
        self.add_item(select)

class OffreSelect(discord.ui.Select):
    def __init__(self, offres):
        options = [
            discord.SelectOption(label=f"{i+1}. {offre['titre']} - {offre['entreprise']}", value=str(i))
            for i, offre in enumerate(offres)
        ]
        super().__init__(placeholder="Sélectionner une offre pour l'analyser", options=options)
    
    async def callback(self, interaction: discord.Interaction):
        index = int(self.values[0])
        offre = self.view.offres[index]
        
        # Stockage de l'offre d'emploi sélectionnée
        user = get_user_data(interaction.user.id)
        user.job_offer = offre
        
        embed = discord.Embed(
            title="Offre sélectionnée",
            description=f"Vous avez sélectionné: {offre['titre']} - {offre['entreprise']}\n"
                      f"Pour comparer avec votre CV, utilisez la commande `/comparer_cv_offre`\n"
                      f"Pour générer une lettre de motivation, utilisez `/generer_lettre`",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

def setup_scrape_command(bot):
    @bot.tree.command(name="scrape", description="Rechercher des offres d'emploi")
    async def scrape(interaction: discord.Interaction, termes: str, lieu: str = None):
        await interaction.response.defer()
        
        try:
            # Ici, nous pouvons importer et utiliser le module de scraping développé par un collègue
            # from path.to.scraper import scrape_function
            # offres = scrape_function(termes, lieu)
            
            # Pour l'instant, utilisons des données simulées
            offres = [
                {"titre": f"Développeur {termes}", "entreprise": "TechCorp", "lieu": lieu or "Paris", "url": "https://exemple.com/job1"},
                {"titre": f"Ingénieur {termes}", "entreprise": "InnoSoft", "lieu": lieu or "Lyon", "url": "https://exemple.com/job2"},
                {"titre": f"Consultant {termes}", "entreprise": "ConseilTech", "lieu": lieu or "Marseille", "url": "https://exemple.com/job3"}
            ]
            
            # Création de la réponse
            embed = discord.Embed(title=f"Offres d'emploi pour '{termes}'", color=discord.Color.blue())
            
            for i, offre in enumerate(offres):
                embed.add_field(
                    name=f"{i+1}. {offre['titre']} - {offre['entreprise']}",
                    value=f"📍 {offre['lieu']}\n🔗 [Voir l'offre]({offre['url']})",
                    inline=False
                )
            
            # Ajout d'un bouton pour sélectionner une offre
            view = OffreSelectionView(offres)
            await interaction.followup.send(embed=embed, view=view)
            
        except Exception as e:
            print(f"Erreur lors du scraping: {e}")
            await interaction.followup.send(f"Une erreur s'est produite lors de la recherche d'offres: {e}", ephemeral=True)