import discord, pyfade, os, functions
from termcolor import cprint
from discord.ext import commands

bot = commands.Bot(
    commands.when_mentioned_or("mp!"),
    intents=discord.Intents.all(),
    description="Meant for the Ether Project. Manages queries to database from Discord and general administrative tasks.",
    case_inensitive=True,
)


@bot.event
async def on_ready():
    r = """
 ______ _          ___     _                 __                        
(_) |  | |        / (_)   | |             /|/  \           o           
    |  | |   _    \__  _|_| |   _  o _     |___/ o _   __    _  __  _|_
    |  |/ \ |/    /     | |/ \ |/  /  |   _|     /  | /  \ ||/ /     | 
 (_/\_/|   ||__  /\___/ |_|   ||__/   |_   |    /   |_\__//||__\___/ |_
                                                          /|           
                                                          \|           

    """
    c = "𝕄𝕣𝔹𝕣𝕦𝕙, 𝕊𝕚𝕘𝕟𝕒𝕞, ℤ𝕤𝕖, 𝕋𝕙𝕖𝕆𝕟𝕝𝕪𝕎𝕒𝕪𝕌𝕡"
    print(pyfade.Fade.Vertical(pyfade.Colors.purple_to_red, r))
    print(
        f"""                                             - Made by {pyfade.Fade.Vertical(pyfade.Colors.green_to_yellow, c)}."""
    )


# def bin2text(s): return "".join([chr(int(s[i:i+8],2)) for i in xrange(0,len(s),8)])


import discord
from discord.ext import commands


class MyNewHelp(commands.MinimalHelpCommand):

    # async def send_pages(self):
    #     destination = self.get_destination()
    #     for page in self.paginator.pages:
    #         emby = discord.Embed(title="The Ether Project | Help", description=page)
    #         totals = await functions.returnTotals()
    #         emby.set_footer(text=f"{totals['servers']} Servers, {totals['players']} Players.")
    #         await destination.send(embed=emby)

    async def send_pages(self):
        halp = discord.Embed(
            title="The Ether Project | Help",
            description="Uh, yeah don't harass people lol.",
        )
        totals = await functions.returnTotals()
        halp.add_field(name="__Servers__", value=totals["servers"], inline=True)
        halp.add_field(name="__Players__", value=totals["players"], inline=True)
        cogs_desc = ""
        file = discord.File("logo.png", filename="image.png")
        halp.set_thumbnail(url="attachment://image.png")
        halp.set_footer(icon_url="attachment://image.png")
        for x in bot.cogs:
            cogs_desc += "{} - {}".format(x, bot.cogs[x].__doc__) + "\n"
        halp.add_field(
            name="Cogs", value=cogs_desc[0 : len(cogs_desc) - 1], inline=False
        )
        await self.get_destination().send(embed=halp, file=file)

    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command))
        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
        channel = self.get_destination()
        await channel.send(embed=embed)


bot.help_command = MyNewHelp()


bot.load_extension("jishaku")


all_categories = [category for category in os.listdir("./cogs")]
print(all_categories)
for category in all_categories:
    for filename in os.listdir(f"./cogs/{category}"):
        if filename.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{category}.{filename[:-3]}")
                cprint(f"Loaded {filename}", "green")
            except Exception as e:
                cprint(f"Unable to load {filename} due to {e}", "red")
                continue
        else:
            continue

    # paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
    # paginator.add_reaction("⏮️", "first")
    # paginator.add_reaction("⏪", "back")
    # paginator.add_reaction("🔐", "lock")
    # paginator.add_reaction("⏩", "next")
    # paginator.add_reaction("⏭️", "last")
    # await paginator.run(embedList)


bot.run("OTA0Njg1NjI3NzA5MjA2NTQ5.YX_IJQ.dImIiqyH8QKq-auHbueNfxmeXA4")
