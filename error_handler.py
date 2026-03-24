import discord
from discord.ext import commands


class Error_handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond("Command on cooldown.")
        elif isinstance(error, commands.NotOwner):
            await ctx.respond("Owner only command")
        else:
            try:
                await ctx.respond(error)
            except: pass
            raise error

def setup(bot):
    bot.add_cog(Error_handler(bot))