import discord, functions, datetime
from discord.ext import commands

# from discord_slash import SlashCommand, SlashContext

bot = commands.Bot(
    command_prefix="mp!",
    description="Bot for The Ether Project's Discord. This is a testing bot only meant for pulling user information.",
)
# slash = SlashCommand(bot)


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


# @slash.slash(name="Player", help="Get a user's common servers, playtimes and more.")
@bot.slash_command(
    help="Get a user's common servers, playtimes and more.",
    guild_ids=[903777611082260521],
)
async def player(ctx, username):
    try:
        info = await dbFunctions.returnUserJson(username)
        embedList = []
        em = discord.Embed(
            title=info["userinfo"]["name"],
            description=f"ID - {info['userinfo']['id']}",
            color=0x759851,
        )
        await ctx.respond(embed=em)
        em = discord.Embed(
            title="Common Servers",
            description="A list of servers this user has been seen on, and common servers.",
            color=0x4C7F99,
        )
        em.add_field(
            name="\u200B",
            value="__Common servers__\n" + "\n".join(info["servers"]),
            inline=False,
        )
        em.add_field(
            name="\u200B",
            value="__All Instances__\n"
            + "\n".join(
                [
                    f"{list(time.keys())[0]} - {list(time.values())[0]}"
                    for time in info["utctime"]
                ]
            ),
            inline=False,
        )
        embedList.append(em)
        em = discord.Embed(
            title="Estimated Time to be Online",
            description="We estimate that this user will be online at "
            + str(
                dbFunctions.avg(
                    [
                        datetime.datetime.utcfromtimestamp(time / 1000)
                        for time in info["times"]
                    ]
                )
            )
            + " UTC",
            color=0x938FAD,
        )
        embedList.append(em)
        for embed in embedList:
            await ctx.send(embed=embed)
    except:
        await ctx.respond("User not found.")


@bot.command(help="Finds the hostname, or tries to.")
async def hostname(ctx, *, ip):
    hostname = await dbFunctions.returnHostname(ip)
    if hostname is None:
        await ctx.send("Couldn't find a hostname in the db.")
    else:
        await ctx.send(hostname)


@bot.command(help="Return information about a server from the Database.")
async def server(ctx, *, ip):
    info = await dbFunctions.returnServerJson(ip)
    print(info)
    e = discord.Embed(
        title=f"{info['ip']['hostname']}:{info['ip']['port']}",
        description="If you're unable to find information here, try pinging the server instead.",
        color=0x759851,
    )
    e.add_field(name="MOTD", value=info["motd"], inline=False)
    e.add_field(
        name="Players",
        value=f"{info['players']['online']}/{info['players']['max']}",
        inline=False,
    )
    e.add_field(name="Version", value=info["version"], inline=False)
    await ctx.send(embed=e)


@bot.command(help="Ping a server and show current information about a server.")
async def ping(ctx, *, ip):
    info = await dbFunctions.returnPingJson(ip)
    print(info)
    e = discord.Embed(
        title=f"{info['ip']['hostname']}:{info['ip']['port']}",
        description="Server Pinged.",
        color=0x759851,
    )
    e.add_field(name="MOTD", value=info["motd"], inline=False)
    e.add_field(
        name="Players",
        value=f"{info['players']['online']}/{info['players']['max']}"
        + "\n"
        + info["players"]["players"],
        inline=False,
    )
    e.add_field(name="Version", value=info["version"], inline=False)
    await ctx.send(embed=e)


bot.run("OTA0Njg1NjI3NzA5MjA2NTQ5.YX_IJQ.dImIiqyH8QKq-auHbueNfxmeXA4")
