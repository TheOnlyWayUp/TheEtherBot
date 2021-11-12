import discord, functions
from discord.ext import commands


class ehandler(commands.Cog):
    """The main error handler."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        """Error handler.

        Args:
            ctx (commands.Context): Provided by system.
            error (commands.CommandError): The error object.

        Raises:
            error: Raises error if undocumented.
        """
        # raise error
        # Command not found
        if isinstance(error, commands.CommandNotFound):
            await ctx.message.add_reaction("⁉️")
            message = "Command not found."
        # On cooldown
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.message.add_reaction("❌")
            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
        # User doesn't have permissions
        elif isinstance(error, commands.MissingPermissions):
            await ctx.message.add_reaction("🔐")
            message = "No permissions."
        elif isinstance(error, commands.BadArgument):
            await ctx.message.add_reaction("🤏")
            message = "Bad arguement."
        # Not enough args
        elif isinstance(error, commands.UserInputError):
            await ctx.message.add_reaction("🤏")
            message = f"Not all required arguements were passed, do `mp!help {ctx.message.content[2:]}`"
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.add_reaction("🤏")
            message = f"Not all required arguements were passed, do `mp!help {ctx.message.content[2:]}`"
        # Mentioned member not found
        elif isinstance(error, commands.MemberNotFound):
            await ctx.message.add_reaction("🤷‍♂️")
            message = "Couldn't find that member."
        # Fails not owner check
        elif isinstance(error, commands.errors.NotOwner):
            await ctx.message.add_reaction("🔐")
            message = "No permissions."
        else:
            message = "This is an undocumented error, it has been reported and will be patched in the next update."
            await ctx.send(embed=discord.Embed(title=message, color=0x992D22))
            raise error
        await ctx.send(embed=discord.Embed(title=message, color=0x992D22))


def setup(bot):
    bot.add_cog(ehandler(bot))
