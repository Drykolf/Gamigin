import asyncio
import os
import discord
from discord.ext import commands, tasks
import settings
from itertools import cycle

#Bot setup
intents: discord.Intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
bot = commands.Bot(command_prefix=settings.PREFIX, intents=intents)
bot_status = cycle(["Probando...", "Testing..."])

@tasks.loop(seconds=60)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(bot_status)))
@bot.event
async def on_ready() -> None:
    print(f'Logged in as {bot.user}')
    change_status.start()
    
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            
async def main():
    async with bot:
        await load()
        await bot.start(settings.TOKEN)

asyncio.run(main())