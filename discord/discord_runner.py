import discord
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
load_dotenv()
token = os.getenv("bot_token")
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('The bot is online, logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!weather"):
        city = message.content.split()[1]



client.run(token)