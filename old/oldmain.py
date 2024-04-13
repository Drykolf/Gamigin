import utils.settings as settings
import discord
from old.responses import get_response
from discord.ext import commands


#Bot setup
intents: discord.Intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
#client:Client = Client(intents=intents)
bot = commands.Bot(command_prefix=settings.PREFIX, intents=intents)

#Message functionality
@bot.command()
async def test(ctx, *args):
    arguments = ', '.join(args)
    await ctx.send(f'{len(args)} arguments: {arguments}')
@bot.command()
async def info(ctx, *, member: discord.Member=None):
    """Tells you some info about the member."""
    if member is None:
        member = ctx.message.author
    msg = discord.Embed(title="User Info", 
                          description=f"Here's {member.name}'s info",
                          color=discord.Color.green(),
                          timestamp=ctx.message.created_at)
    msg.add_field(name="ID", value=member.id)
    #msg = f'{member} joined on {member.joined_at} and has {len(member.roles)} roles.'
    await ctx.send(embed=msg)

@info.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('I could not find that member...')
#bot.add_command(info)
#starting app
@bot.event
async def on_ready() -> None:
    print(f'Logged in as {bot.user}')

#Handle incomming messages

''' 
#Main entry point
def main() -> None:
    bot.run(token=settings.TOKEN)
    
if __name__ == '__main__':
    main()'''