import discord
from datetime import datetime, timedelta, timezone
from discord.ext import commands


class Example(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	admingroup = discord.SlashCommandGroup("admin", "Some admin commands", default_member_permissions=discord.Permissions(administrator=True))

	@admingroup.command()
	async def bulk_delete(self, ctx: discord.ApplicationContext, channel: discord.TextChannel = None):
		if channel == None:
			channel = ctx.channel

		now = datetime.now(timezone.utc)
		cutoff = now - timedelta(days=14)

		msgs = []
		async for m in channel.history(limit=100):
			if m.created_at >= cutoff:
				msgs.append(m)
			else: break
		await channel.delete_messages(msgs)
		await ctx.respond(f"Deleted {len(msgs)} messages", delete_after=2)


def setup(bot):
	bot.add_cog(Example(bot))