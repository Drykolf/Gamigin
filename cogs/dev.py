from discord.ext import commands
from discord import HTTPException, Object
from typing import Literal, Optional

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Dev cog is ready!')
    
    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self,ctx: commands.Context, guilds: commands.Greedy[Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
        try:
            if not guilds:
                if spec == "~":
                    synced = await self.bot.tree.sync(guild=ctx.guild)
                elif spec == "*":
                    self.bot.tree.copy_global_to(guild=ctx.guild)
                    synced = await ctx.bot.tree.sync(guild=ctx.guild)
                elif spec == "^":
                    self.bot.tree.clear_commands(guild=ctx.guild)
                    await self.bot.tree.sync(guild=ctx.guild)
                    synced = []
                else:
                    synced = await ctx.bot.tree.sync()

                await ctx.send(
                    f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
                )
                return
            ret = 0
            for guild in guilds:
                try:
                    await self.bot.tree.sync(guild=guild)
                except HTTPException:
                    pass
                else:
                    ret += 1
            await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Dev(bot))