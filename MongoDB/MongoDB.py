#install this pypi to connect to MongoDB
#python3 -m pip install motor

import discord
import os

from discord import app_commands
from dotenv import load_dotenv

#added from base-code
import motor.motor_asyncio
from random import randint

load_dotenv()

#connect to mongodb with motor
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODBTOKEN")) #paste mongodb token in the .env file
db = client["Bots"]
collection = db["Levels"]

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

#level system
@client.event
async def on_message(message):
    if message.author.id == client.user.id: #checks if user is bot, if it is bot then do nothing
        return
    else: 
        member = message.author.id #gets message authors id
        xp = randint(1, 20) # random number bewtween 1 and 20
        if await collection.find_one({"_id" : member}) == None: #checks if id is in database
            await collection.insert_one({"_id" : member, "xp" : 0, "level" : 1}) #add new user data in not found
            print(f"{message.author} added to database")
        else: 
            newxp = await collection.find_one({"_id" : member}) #checks for usersdata
            currxp = newxp["xp"] #gets users xp
            nowxp = currxp + xp #users xp plus random xp from message
            await collection.update_one({"_id" : member}, {"$set" : {"xp" : nowxp}}, upsert=True) #updates usersdata with new xp
        
        lvl = await collection.find_one({"_id" : member}) # gets user data
        start_lvl = lvl["level"] # gets users level
        next_lvl = start_lvl + 1 # checks what the next level is

        if currxp >= round(5 * (start_lvl ** 4/5)): # how much xp till next level

            #updates users data when required amount of xp is reached
            await collection.update_one({"_id" : member}, {"$set" : {"level" : next_lvl}}, upsert=True) 
            await message.channel.send(next_lvl) #lets user know they reached the next level



#check what level you are
@bot.command(name="level", description="Check what level you are")
async def self(interaction: discord.Interaction):
    lvl = await collection.find_one({"_id" : interaction.user.id}) # retrives users data
    mylvl = lvl["level"] #finds users level

    await interaction.response.send_message(f"{interaction.user.mention} are level {mylvl}") #sends users level

#Check how much xp you have and how far you are from the next level
@bot.command(name="xp", description="Check how much xp your have")
@app_commands.checks.cooldown(1, 60, key=lambda i: (i.guild_id, i.user.id)) #60 second cool down on command
async def xp(interaction: discord.Interaction):
    xp = await collection.find_one({"_id" : interaction.user.id}) #gets users data
    myxp = xp["xp"] #gets users xp
    lvl = xp["level"] #gets users level

    to_next_lvl = round(5 * (lvl ** 4/5)) #xp for next leve
    next_lvl = to_next_lvl - myxp #xp till next level

    #sends users cerrent xp and xp needed for next level  
    await interaction.response.send_message(f"{interaction.user.mention} you have {myxp} xp and are {next_lvl} xp away from the next next level") 

#checks for app command error in the xp command
#send cool down message to user
@xp.error
async def on_xp_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(str(error), ephemeral=True)


#original commmand
@bot.command(name="hello", description="sends user hello")
async def self(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}!")

client.run(os.getenv("TOKEN"))
