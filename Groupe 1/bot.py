import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Importation des modules personnalisés
from commands.scrape_jobs import setup_scrape_command
from commands.extract_cv import setup_cv_command
from commands.match_cv_offer import setup_compare_command
from commands.generate_cover_letter import setup_letter_command
from utils.helper import UserData, user_data

# Configuration du bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Commandes synchronisées: {len(synced)}")
    except Exception as e:
        print(f"Erreur lors de la synchronisation des commandes: {e}")

# Configuration des commandes
def setup(bot):
    setup_scrape_command(bot)
    setup_cv_command(bot)
    setup_compare_command(bot)
    setup_letter_command(bot)

# Initialiser les commandes
setup(bot)

TOKEN = os.getenv("DISCORD_TOKEN")

print(f"Démarrage du bot avec le token: {'*' * len(TOKEN)}")  # Affiche des étoiles au lieu du token pour la sécurité
bot.run(TOKEN)
