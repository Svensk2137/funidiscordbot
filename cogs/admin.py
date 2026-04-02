import discord
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from discord import Forbidden
from discord.ext import commands

# Some admin commands

class Example(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	admingroup = discord.SlashCommandGroup("admin", "Some admin commands", default_member_permissions=discord.Permissions(administrator=True))
	renaming = admingroup.create_subgroup("rename", "Renaming shit :D")

	@admingroup.command()
	async def bulk_delete(self, ctx: discord.ApplicationContext, amount: int = 100, channel: discord.TextChannel = None):
		if channel == None:
			channel = ctx.channel

		await ctx.trigger_typing()

		now = datetime.now(timezone.utc)
		cutoff = now - timedelta(days=14)

		msgs = []
		async for m in channel.history(limit=amount):
			if m.created_at >= cutoff:
				msgs.append(m)
			else: break
		await channel.delete_messages(msgs)
		await ctx.respond(f"Deleted {len(msgs)} messages", delete_after=2)

	@admingroup.command()
	async def goon_leaderboard(self, ctx: discord.ApplicationContext):
		await ctx.defer()
		json_path = Path("./gooning_leaderboards.json")
		if json_path.exists():
			with json_path.open("r") as f:
				leaderboard = json.load(f)
		else:
			leaderboard = {}

		await ctx.respond(leaderboard)

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

	@admingroup.command()
	async def make_pc_lagger_channel(self, ctx: discord.ApplicationContext, channel_name: str = None):
		await ctx.defer()
		channel = ctx.channel
		found_channel = False
		message = "Zoom out"
		if channel_name is not None:
			for c in ctx.guild.channels:
				if c.name == channel_name:
					channel = ctx.guild.get_channel(c.id)
					found_channel = True
					break

			if not found_channel:
				channel = await ctx.guild.create_text_channel(channel_name)

			message += f" in {channel.mention}"

		for i in range(200):
			await channel.send("-# 🇦🇮🇻🇬🇰🇾🇨🇰🇫🇰🇦🇺🇲🇸🇳🇿🇵🇳🇬🇸🇸🇭🇦🇨🇹🇦🇭🇲🇹🇨🇦🇮🇻🇬🇰🇾🇨🇰🇫🇰🇦🇺🇲🇸🇳🇿🇵🇳🇬🇸🇸🇭🇦🇨🇹🇦🇭🇲🇹🇨🇦🇮🇻🇬🇰🇾🇨🇰🇫🇰🇦🇺🇲🇸🇳🇿🇵🇳🇬🇸🇸🇭🇦🇨🇹🇦🇭🇲🇹🇨🇦🇮🇻🇬🇰🇾🇨🇰🇫🇰🇦🇺🇲🇸🇳🇿🇵🇳🇬🇸🇸🇭🇦🇨🇹🇦🇭🇲🇹🇨🇦🇮🇻🇬🇰🇾🇨🇰🇫🇰🇦🇺🇲🇸🇳🇿🇵🇳🇬🇸🇸🇭🇦🇨🇹🇦🇭🇲🇹🇨🇦🇮🇻🇬🇰🇾🇨🇰🇫🇰🇦🇺🇲🇸🇳🇿🇵🇳🇬🇸🇸🇭🇦🇨🇹🇦🇭🇲🇹🇨🇦🇮🇻🇬🇰🇾🇨🇰🇫🇰🇦🇺🇲🇸🇳🇿🇵🇳🇬🇸🇸🇭🇦🇨🇹🇦🇭🇲🇹🇨🇦🇮🇻🇬🇰🇾🇨🇰🇫🇰🇦🇺🇲🇸🇳🇿🇵🇳🇬🇸🇸🇭🇦🇨🇹🇦🇭🇲🇹🇨🇦🇮🇻🇬🇰🇾🇨🇰🇫🇰🇦🇺🇲🇸🇳🇿🇵🇳🇬🇸🇸🇭🇦🇨🇹🇦🇭🇲🇹🇨🇦🇮🇻🇬🇰🇾🇨🇰🇫🇰🇦🇺🇲🇸🇳🇿🇵🇳🇬🇸🇸🇭🇦🇨🇹🇦🇭🇲🇹🇨🇦🇮🇻🇬🇰🇾🇨🇰🇫🇰🇦🇺🇲🇸🇳🇿🇵🇳🇬🇸🇸🇭🇦🇨🇹🇦🇭🇲🇹🇨🇦🇮🇻🇬🇰🇾🇨🇰🇫🇰🇦🇺🇲🇸🇳🇿🇵🇳🇬🇸🇸🇭🇦🇨🇹🇦🇭🇲🇹🇨🇦🇮🇻🇬🇰🇾🇨🇰🇫🇰🇦🇺🇲🇸🇳🇿🇵🇳🇬🇸🇸🇭🇦🇨🇹🇦🇭🇲🇹🇨🇦🇮🇻🇬🇰🇾")
		await ctx.respond(message)

def setup(bot):
	bot.add_cog(Example(bot))