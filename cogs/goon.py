import json
from pathlib import Path

import discord
from discord import default_permissions
from discord.ext import commands
import requests
import random
import os

# Gooning which is just rule 34 api

goon_key = os.getenv("GOON_KEY")

class Goon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    goon = discord.SlashCommandGroup("gooning", "command group for gooners", checks=[commands.is_nsfw().predicate])

    @goon.command(id=2137)
    async def search(self, ctx: discord.ApplicationContext, tags: str = ""):
        self.bot.dispatch("gooning_event", ctx.author)
        goon_tag = tags.replace(" ", "+")
        limit = 100
        if goon_tag.endswith("+"):
            goon_tag += "-ai_generated"
        else:
            goon_tag += "+-ai_generated"
        r = requests.get(url=f"https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&limit={limit}&tags={goon_tag}&json=1{goon_key}")
        try:
            rj = r.json()
        except:
            await ctx.respond("Nothin")
            return
        random_int = random.randint(0, len(rj)-1)
        rjp = rj[random_int]
        rjl = len(rj)
        rjpimage = rjp["file_url"]
        rjptags = rjp["tags"]
        if len(rjptags) > 1000:
            rjptags = "Too many fkin tags"
        message = f"Searched `{goon_tag.replace("+", " ")}`. Found: `{rjl}` (Max per query: {limit}). All tags: `{rjptags}`. Url: {rjpimage}"
        await ctx.respond(message)

    @goon.command(id=2137)
    async def tags(self, ctx: discord.ApplicationContext, term: str):
        self.bot.dispatch("gooning_event", ctx.author)
        r = requests.get(url=f"https://api.rule34.xxx/autocomplete.php?q={term}")
        rj = r.json()
        taglist = f"Searched {term}:\n"
        for e in rj:
            taglist += f"`{e['label']}`\n"
        await ctx.respond(taglist)

    @commands.Cog.listener()
    async def on_gooning_event(self, member: discord.Member):
        json_path = Path("./gooning_leaderboards.json")
        member_name = member.name
        if json_path.exists():
            with json_path.open("r") as f:
                leaderboard = json.load(f)
        else:
            leaderboard = {}

        current = leaderboard.get(member_name, 0)
        leaderboard[member_name] = current + 1

        with json_path.open("w") as z:
            json.dump(leaderboard, z, indent=2)
        print(f"{member.name} used the gooning command")

def setup(bot):
    bot.add_cog(Goon(bot))