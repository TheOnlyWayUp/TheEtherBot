import discord, functions
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

file = discord.File("logo.png", filename="image.png")
class Server(commands.Cog):
    """All commands related to servers."""

    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(
        help="Finds the hostname, or tries to.", cooldown_after_parsing=True,
        usage="<ip here>"
    )
    @commands.cooldown(1, 5, BucketType.user)
    async def hostname(self, ctx, *, ip):
        hostname = await functions.returnHostname(ip)
        if hostname is None:
            await ctx.send("Couldn't find a hostname in the db.")
        else:
            e = discord.Embed(
                title=hostname, description=f"Found a hostname for {ip}, nice."
            )
            e.set_thumbnail(url="attachment://image.png")
            await ctx.send(embed=e, file=file)

    @commands.command(
        help="Return information about a server from the Database.",
        cooldown_after_parsing=True,
        usage="<ip here>"
    )
    @commands.cooldown(1, 5, BucketType.user)
    async def server(self, ctx, ip):
        info = await functions.returnServerJson(ip)
        if not info:
            await ctx.send("Server not in DB.")
            return
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
        e.set_thumbnail(url="attachment://image.png")
        await ctx.send(embed=e, file=file)

    @commands.command(
        help="Ping a server and show current information about a server.",
        cooldown_after_parsing=True,
        usage="<ip here>",
    )
    @commands.cooldown(1, 5, BucketType.user)
    async def ping(self, ctx, *, ip):
        try:
            info = await functions.returnPingJson(ip)
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
            e.set_thumbnail(url="attachment://image.png")
            await ctx.send(embed=e, file=file)
        except Exception as e:
            await ctx.send(f"Failed - {e}.")


def setup(bot):
    bot.add_cog(Server(bot))
