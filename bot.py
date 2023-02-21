import discord
from discord import app_commands
import os
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


@bot.command(name="hello", description="Says hello to you")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}")

client.run(os.getenv("TOKEN"))

