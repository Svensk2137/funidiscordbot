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
		await ctx.trigger_typing()
		message = "Renaming...\n"
		msg = await ctx.respond(f"```{message}```")
		for u in ctx.guild.members:
			try:
				await u.edit(nick=new_name)
				message += f"Changed `{u.name}` to `{u.nick}`\n"
			except Forbidden as err:
				message += f"Failed to change `{u.name}` with `{err}`\n"
			await msg.edit(content=f"```{message}```")
		message += "Finished"
		await msg.edit(content=f"```{message}```")

	@renaming.command(name="reset_all")
	async def rename_reset_all(self, ctx: discord.ApplicationContext):
		await ctx.trigger_typing()
		message = "Renaming...\n"
		msg = await ctx.respond(f"```{message}```")
		for u in ctx.guild.members:
			try:
				await u.edit(nick=None)
				message += f"Reset nickname for `{u.name}`\n"
			except Forbidden as err:
				message += f"Failed to reset nickname for `{u.name}`\n"
			await msg.edit(content=f"```{message}```")
		message += "Finished"
		await msg.edit(content=f"```{message}```")


def setup(bot):
	bot.add_cog(Example(bot))