import discord
from discord.ext import commands


class Gangshit(commands.Cog):  # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot):  # this is a special method that is called when the cog is loaded
        self.bot = bot

    @discord.slash_command()  # we can also add application commands
    async def list_guilds(self, ctx):
        await ctx.respond(self.bot.guilds)

def setup(bot):  # this is called by Pycord to setup the cog
    bot.add_cog(Gangshit(bot))  # add the cog to the bot