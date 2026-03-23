from dotenv import load_dotenv
import discord
import os

load_dotenv() # DISCORD_TOKEN

client = discord.Bot()

client.load_extension("cogs.greetings")

@client.event
async def on_ready():
	print(f"Logged in as {client.user}")

@client.slash_command(name="ping", description="Latency")
async def ping(ctx: discord.ApplicationContext):
	await ctx.respond(f"Latency is {client.latency}")

client.run(os.getenv("DISCORD_TOKEN"))
