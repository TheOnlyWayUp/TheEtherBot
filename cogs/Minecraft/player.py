import discord, functions, datetime
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
file = discord.File("logo.png", filename="image.png")

class Player(commands.Cog):
    """All commands related to Player Information."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help="Get a user's common servers, playtimes and more.",
        cooldown_after_parsing=True,
        usage="<player username>"
    )
    @commands.cooldown(1, 5, BucketType.user)
    async def player(self, ctx, username):
        try:
            info = await functions.returnUserJson(username)
            embedList = []
            em = discord.Embed(
                title=info["userinfo"]["name"],
                description=f"ID - {info['userinfo']['id']}",
                color=0x759851,
            )
            file = discord.File("logo.png", filename="image.png", file=file)
            em.set_thumbnail(url="attachment://image.png")
            await ctx.send(embed=em)
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
                    functions.avg(
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


def setup(bot):
    bot.add_cog(Player(bot))
