from dotenv import load_dotenv
import discord
import os

load_dotenv() # DISCORD_TOKEN

client = discord.Bot()

@client.event
async def on_ready():
	print(f"Logged in as {client.user}")

@client.slash_command(name="hello", description="Say hello")
async def hello(ctx: discord.ApplicationContext):
	await ctx.respond("Hello")

client.run(os.getenv("DISCORD_TOKEN"))
