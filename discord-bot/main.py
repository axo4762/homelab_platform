import discord
from dotenv import load_dotenv
import os
from minecraft import Minecraft

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

@client.event
async def on_ready():
  print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
  if message.author != client.user:
    if '$minecraft' in message.content.split(' ')[0].lower():
      command = message.content.replace('$minecraft ','')
      res = Minecraft().handler(command)
      await message.channel.send(f"> {message.content}\n```{res}```")
    elif '$help' in message.content.split(' ')[0].lower():
      await message.channel.send(
        '```I\'m Codsworth, the assistant in this server!\n'
        'You can run minecraft commands with $minecraft <command>\n\n'
        'Examples: \n'
        '  - $minecraft whitelist add <username> --> add a user to the whitelist\n'
        '  - $minecraft get stats --> get information about the server\n'
        '  - $minecraft get version --> get the server version\n'
        '  - $minecraft <command> --> any java support command - docs: https://minecraft.fandom.com/wiki/Commands```'
        )

client.run(TOKEN)