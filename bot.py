import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Charger le token depuis le fichier .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
print(f"TOKEN récupéré : {TOKEN}")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user} !")

@bot.command(name="search_job")
async def search_job(ctx):
    await ctx.send("🔍 Recherche d'emploi en cours...")

    # Simulation de chaque groupe
    fake_cv = "Texte extrait du CV."
    fake_offre = {"titre": "Data Analyst", "description": "CDI - Paris", "url": "https://example.com"}
    pertinence = 8.5
    lettre = "Madame, Monsieur, je suis intéressé..."

    # Réponse utilisateur
    await ctx.send(f"**Offre :** {fake_offre['titre']} - {fake_offre['description']}")
    await ctx.send(f"📎 Lien : {fake_offre['url']}")
    await ctx.send(f"📈 Pertinence : {pertinence}/10")
    await ctx.send(f"📄 Lettre générée :\n```{lettre}```")

@bot.command(name='commandes')
async def help_command(ctx):
    help_message = """
    Voici les commandes disponibles :
    - `!search_job`: Recherche des offres d'emploi et génère une lettre de motivation.
    - `!status`: Affiche le statut actuel du bot.
    - `!ping`: Vérifie si le bot répond (retourne "Pong !").
    """
    await ctx.send(help_message)

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong !')

@bot.command(name='status')
async def status(ctx):
    status_message = f"Je suis {bot.user.name} et je suis présent sur {len(bot.guilds)} serveurs."
    await ctx.send(status_message)

@bot.command(name='clear')
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"{amount} messages ont été supprimés.")


# Lancer le bot
bot.run(TOKEN)
