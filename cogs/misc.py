from discord.ext import commands
from discord import Embed, Member

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        print('Misc cog is ready!')
    @commands.command()
    async def info(self, ctx, *, member: Member):
        """Tells you some info about the member."""
        msg = f'{member} joined on {member.joined_at} and has {len(member.roles)} roles.'
        await ctx.send(msg)

    @info.error
    async def info_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('I could not find that member...')
    @commands.command()
    async def ping(self, ctx):
        '''This is a test command to check the bot latency'''
        bot_latency = round(self.bot.latency*1000)
        await ctx.send(f'Pong! {bot_latency}')
    
    @commands.command()
    async def embed(self, ctx):
        '''This is a test command for the embed messages'''
        embedMsg = Embed(title="Hello World!", description="This is a test", color=0x00ff00)
        embedMsg.set_author(name=f'Requested by {ctx.author.mention}', icon_url=ctx.author.avatar)
        embedMsg.set_thumbnail(url=ctx.author.guild.icon)
        embedMsg.set_image(url=ctx.guild.icon)
        embedMsg.add_field(name="Field Name", value="Field Value", inline=False)
        embedMsg.set_footer(text="This is the footer", icon_url=ctx.author.avatar)
        await ctx.send(embed=embedMsg)

async def setup(bot):
    await bot.add_cog(Misc(bot))