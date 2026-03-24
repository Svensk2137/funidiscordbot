from discord.ext.commands import is_owner
from dotenv import load_dotenv
import discord
import os

load_dotenv() # DISCORD_TOKEN
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DEBUG_GUILDS = [os.getenv("DEBUG_GUILDS"),os.getenv("JAGAD_GUILD")]
OWNER_ID = int(os.getenv("OWNER_ID"))

intents = discord.Intents.default()
intents.members = True
client = discord.Bot(intents=intents, debug_guilds=DEBUG_GUILDS, owner_id=OWNER_ID)

try:
	client.load_extension("error_handler")
	print("Loaded Error Handler")
except Exception as err:
	raise err

for file in os.listdir("cogs"):
	if file.endswith(".py"):
		try:
			client.load_extension(f"cogs.{file[:-3]}")
			print(f"Loaded cogs.{file[:-3]}")
		except Exception as err:
			raise err

@client.event
async def on_ready():
	print(f"Logged in as {client.user}")

@client.slash_command(name="ping", description="Latency")
async def ping(ctx: discord.ApplicationContext):
	await ctx.respond(f"Latency is {client.latency}")

@client.slash_command()
@is_owner()
async def reload_cogs(ctx: discord.ApplicationContext): # Commands dont work after reload, idk
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

client.run(DISCORD_TOKEN)
