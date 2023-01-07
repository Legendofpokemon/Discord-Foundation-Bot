#install the following pip by typing the pypi below into your command prompt
#pip install discord.py

#Use discord developer portal to get your bot token
# as well as get the invite link making sure you enable
#app commands and bot scopes
#next paste your token in the .env file and follow instructions there


import discord
import os

from discord import app_commands
from dotenv import load_dotenv

load_dotenv()



class aclient(discord.Client): 
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def  on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await bot.sync()
            self.synced = True
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')



client = aclient()
bot = app_commands.CommandTree(client)


@bot.command(name="hello", description="sends user hello")
async def self(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}!")






client.run(os.getenv("TOKEN"))