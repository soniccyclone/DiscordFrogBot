import discord
import os
import io
import aiohttp
import random
from imgurpython import ImgurClient

imgur_client = ImgurClient(
  os.environ['IMGUR_CLIENT_ID'],
  os.environ['IMGUR_CLIENT_SECRET']
)
client = discord.Client()

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg == "$frog":
    channel = message.channel
    images = imgur_client.get_album_images(os.environ['IMGUR_IMAGE_ALBUM_ID'])
    image_index = random.randrange(len(images))
    image = images[image_index]
    async with aiohttp.ClientSession() as session:
      async with session.get(image.link) as resp:
          if resp.status != 200:
              return await channel.send('Could not download file...')
          data = io.BytesIO(await resp.read())
          await channel.send(file=discord.File(data, f'cool_frog_pic{image_index}.png'))
  elif msg == "$frogif":
    channel = message.channel
    images = imgur_client.get_album_images(os.environ['IMGUR_GIF_ALBUM_ID'])
    image_index = random.randrange(len(images))
    image = images[image_index]
    async with aiohttp.ClientSession() as session:
      async with session.get(image.link) as resp:
          if resp.status != 200:
              return await channel.send('Could not download file...')
          data = io.BytesIO(await resp.read())
          await channel.send(file=discord.File(data, f'cool_frog_gif{image_index}.gif'))
      
client.run(os.environ['DISCORD_TOKEN'])



