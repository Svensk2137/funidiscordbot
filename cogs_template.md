Use this for adding cogs brother

```
import discord
from discord.ext import commands


class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def hello(self, ctx: discord.ApplicationContext):
        await ctx.respond("Hi, this is a slash command from a cog!")


def setup(bot):
    bot.add_cog(Example(bot))
```