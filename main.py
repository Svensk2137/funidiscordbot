from dotenv import load_dotenv
import discord
from discord import application_command
import os

load_dotenv() # DISCORD_TOKEN
DEBUG_GUILDS = [os.getenv("DEBUG_GUILDS")]

client = discord.Bot(debug_guilds=DEBUG_GUILDS)


for file in os.listdir("cogs"):
	if file.endswith(".py"):
		client.load_extension(f"cogs.{file[:-3]}")

@client.event
async def on_ready():
	print(f"Logged in as {client.user}")

@client.slash_command(name="ping", description="Latency")
async def ping(ctx: discord.ApplicationContext):
	await ctx.respond(f"Latency is {client.latency}")

@client.slash_command()
async def reload_cogs(ctx: discord.ApplicationContext):
	message = "Reloading cogs...\n"
	msg = await ctx.respond(f"```{message}```")
	for file in os.listdir("cogs"):
		if file.endswith(".py"):
			try:
				client.reload_extension(f"cogs.{file[:-3]}")
				message += f"Reload cogs.{file[:-3]}    Success\n"
				await msg.edit(content=f"```{message}```")
			except:
				message += f"Reload cogs.{file[:-3]}    Fail\n"
				await msg.edit(content=f"```{message}```")
	message += "Finished"
	await msg.edit(content=f"```{message}```")

client.run(os.getenv("DISCORD_TOKEN"))
