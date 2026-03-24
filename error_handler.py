import discord
from discord.ext import commands


class Error_handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond("Command on cooldown.", delete_after=5, ephemeral=True)
        elif isinstance(error, commands.NotOwner):
            await ctx.respond("Owner only command", delete_after=5, ephemeral=True)
        elif isinstance(error, discord.Forbidden):
            await ctx.respond(error, delete_after=5, ephemeral=True)
        else:
            try:
                await ctx.respond(error, delete_after=5, ephemeral=True)
            except: pass
            raise error

def setup(bot):
    bot.add_cog(Error_handler(bot))