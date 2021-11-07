import config, discord, asyncio, aiohttp, os, termcolor
from discord.ext import commands

bot = commands.Bot(commands.when_mentioned_or(config.prefix), description=config.description, case_insensitive=True, strip_after_prefix=True)

async def req(link):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
            return await resp.json()

async def api(type, query)
def stcheck():
    def predicate(ctx):
            return ctx.author.guild_permissions.administrator is True
    return commands.check(predicate)

def modcheck():
    def predicate(ctx):
            return ctx.author.guild_permissions.administrator is True or ctx.author.guild_permissions.kick_members is True
    return commands.check(predicate)

all_categories = list(os.listdir("./cogs"))
for category in all_categories:
    for filename in os.listdir(f"./cogs/{category}"):
        if filename.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{category}.{filename[:-3]}")
                termcolor.cprint(f"Loaded {filename}", "green")
            except Exception as e:
                termcolor.cprint(f"Unable to load {filename} due to {e}", "red")
                continue
        else:
            continue

