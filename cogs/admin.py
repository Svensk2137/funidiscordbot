from os import name

import discord
from datetime import datetime, timedelta, timezone

from discord import Forbidden
from discord.ext import commands


class Example(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	admingroup = discord.SlashCommandGroup("admin", "Some admin commands", default_member_permissions=discord.Permissions(administrator=True))
	renaming = admingroup.create_subgroup("rename", "Renaming shit :D")

	@admingroup.command()
	async def bulk_delete(self, ctx: discord.ApplicationContext, channel: discord.TextChannel = None):
		if channel == None:
			channel = ctx.channel

		await ctx.trigger_typing()

		now = datetime.now(timezone.utc)
		cutoff = now - timedelta(days=14)

		msgs = []
		async for m in channel.history(limit=100):
			if m.created_at >= cutoff:
				msgs.append(m)
			else: break
		await channel.delete_messages(msgs)
		await ctx.respond(f"Deleted {len(msgs)} messages", delete_after=2)

	@renaming.command(name="set_all")
	async def raname_all(self, ctx: discord.ApplicationContext, new_name: str):
		await ctx.defer()
		for u in ctx.guild.members:
			try:
				await u.edit(nick=new_name)
			except Forbidden as err: pass
		await ctx.respond("Finished", delete_after=2)

	@renaming.command(name="reset_all")
	async def rename_reset_all(self, ctx: discord.ApplicationContext):
		await ctx.defer()
		for u in ctx.guild.members:
			try:
				await u.edit(nick=None)
			except Forbidden as err: pass
		await ctx.respond("Finished", delete_after=2)

	@discord.user_command(name="Inform Israel")
	async def inform_israel(self, ctx: discord.ApplicationContext, user: discord.Member):
		await user.timeout(datetime.now(timezone.utc) + timedelta(days=5))
		namefortheloveofwhatsholypleasejustdonterrorfornoreason = user.nick
		if namefortheloveofwhatsholypleasejustdonterrorfornoreason is None:
			namefortheloveofwhatsholypleasejustdonterrorfornoreason = user.name
		await ctx.respond(f"Israel has been informed on {namefortheloveofwhatsholypleasejustdonterrorfornoreason} antisemitism")

def setup(bot):
	bot.add_cog(Example(bot))