import io

import discord, requests
from wand.image import Image
from discord import SlashCommandGroup
from discord.ext import commands

# ImageMagick based commands

class ImageMagick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    image = SlashCommandGroup("image", "ImageMagick tooling")

    async def _get_image_data(self, ctx: discord.ApplicationContext, file: discord.Attachment = None, url: str = None):
        """
        Returns tuple (image_bytes, filename) or (None, None) if nothing found.
        """
        if file is not None:
            image_data = await file.read()
            filename = file.filename
            return image_data, filename

        if url is not None:
            image_data = requests.get(url).content
            filename = url + ".jpg"
            return image_data, filename

        # find last image attachment in recent history
        last_attachment = None
        async for m in ctx.channel.history(limit=10):
            for attachment in m.attachments:
                if attachment.height is not None and attachment.width is not None:
                    last_attachment = attachment
                    break
            if last_attachment:
                break

        if last_attachment is None:
            return None, None

        image_data = requests.get(last_attachment.url).content
        filename = last_attachment.url
        filename = filename.split("?", 1)[0]
        filename = filename.split("/", 6)[-1]
        return image_data, filename

    @image.command()
    async def resize(self, ctx: discord.ApplicationContext, scale: float, file: discord.Attachment = None, url: str = None):
        await ctx.defer()
        image_data, filename = await self._get_image_data(ctx, file=file, url=url)
        if image_data is None:
            await ctx.respond("Nothin")
            return

        with Image(blob=image_data) as i:
            i.resize(int(i.width * scale), int(i.height * scale))
            processed_bytes = i.make_blob()
            await ctx.respond(file=discord.File(io.BytesIO(processed_bytes), filename=f"resized-{filename}"))

def setup(bot):
    bot.add_cog(ImageMagick(bot))