import discord
import os
import io
import aiohttp
import random
from imgurpython import ImgurClient

frog_albums = {
  "$frog": os.environ['IMGUR_IMAGE_ALBUM_ID'],
  "$frogif": os.environ['IMGUR_GIF_ALBUM_ID']
}

imgur_client = ImgurClient(
  os.environ['IMGUR_CLIENT_ID'],
  os.environ['IMGUR_CLIENT_SECRET']
)
client = discord.Client()

@client.event
async def on_ready():
  print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message: discord.Message) -> None:
  if message.author != client.user and message.content in frog_albums:
    await try_send_image(message.channel, frog_albums[message.content])

async def try_send_image(channel: discord.TextChannel, imgur_album_id: str) -> None:
  images = imgur_client.get_album_images(imgur_album_id)
  image_index = random.randrange(len(images))
  image = images[image_index]
  # Grab image extension from MIME type
  image_type = image.type[6:]
  async with aiohttp.ClientSession() as session:
    async with session.get(image.link) as resp:
        if resp.status != 200:
            return await channel.send('Could not download file...')
        data = io.BytesIO(await resp.read())
        await channel.send(file=discord.File(data, f'cool_frog_{image_index}.{image_type}'))
      
client.run(os.environ['DISCORD_TOKEN'])