import discord, db, datetime
from discord.ext import commands

bot = commands.Bot(
    command_prefix="mp!",
    description="Bot for The Ether Project's Discord. This is a testing bot only meant for pulling user information.",
)


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@bot.command(help="Get a user's common servers, playtimes and more.")
async def player(ctx, username):
    try:
        info = await db.returnServerJson(username)
        embedList = []
        em = discord.Embed(
            title=info["userinfo"]["name"],
            description=f"ID - {info['userinfo']['id']}",
            color=0x759851,
        )
        embedList.append(em)
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
                db.avg(
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
        await ctx.send("User not found.")


bot.run("OTA0Njg1NjI3NzA5MjA2NTQ5.YX_IJQ.dImIiqyH8QKq-auHbueNfxmeXA4")
