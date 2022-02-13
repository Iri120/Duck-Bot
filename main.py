  # WHAT IS DUCK: Gahee, Mekdim, Naoto and Iris
# Duck-inspired discord bot

import os
import discord
from discord.ext import commands
import datetime

TOKEN = 'OTQyMTE3Mjg0NTM5OTQ5MDU3.Ygf1GA.JSixbrrn2WNrrW6oI8F_mYdzck8'
DISCORD_GUILD = 'Duck Timer'

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
client = commands.Bot(command_prefix = '!', intents = intents)   # Instance of a client
users = []

# Runs when bot is ready to be used
@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client) + '...')

  for guild in client.guilds:
    if guild.name == DISCORD_GUILD:
      break

  print(
    f'{client.user} is connected to the following guild:\n'
    f'{guild.name}(id: {guild.id})'
  )
  members = '\n - '.join([member.name for member in guild.members])
  print(f'\nGuild Members:\n - {members}')

# Returns seconds -> hours and minutes into a string
def convert_time(seconds):
  result = ""
  second_value = seconds % (24 * 3600)
  hours = second_value // 3600
  second_value %= 3600
  minutes = second_value // 60
  second_value %= 60

  if hours > 0:
    result += (str(hours) + " hour(s) ")

  if minutes > 0:
    result += (str(minutes) + " minute(s) ")

  if hours == 0 and minutes == 0:
    result += (str(seconds) + " second(s) ")

  return result

def search_user(users, user_name):
  user_numbers = len(users)
  for i in range(user_numbers):
    if users[i]["user_name"] == user_name:
      return users[i]["start_time"], i
  else:
    return -1, -1

# Checks when a member enters into the voice channel and leaves 
@client.event
async def on_voice_state_update(member, before, after):
    
  if before.channel != after.channel:
      
    bot_room = client.get_channel(942158062586826904)
    announceChannelIds = [942108183479058445]
    current_time = datetime.datetime.now()

    # Print message when user joins channel
    if after.channel is not None and after.channel.id in announceChannelIds:
      await bot_room.send("Welcome " + member.name + "! What's quacking? :smile:")
      dic = {}
      dic["user_name"] = member.name
      dic["start_time"] = current_time
      users.append(dic)

    # Print message when user leaves channel
    if before.channel is not None and before.channel.id in announceChannelIds:
      await bot_room.send("Goodbye " + member.name +  ", quack ya later! :wave:")
      
      # Calculates how long user has been in the voice channel
      user_start_time, user_index = search_user(users, member.name)
      if user_index >=0:
        tdatetime = datetime.datetime.strptime(str(user_start_time), '%Y-%m-%d %H:%M:%S.%f')

        time_elapsed = current_time - tdatetime 
        seconds =  time_elapsed.seconds
        time_str = convert_time(seconds)

        await bot_room.send("Bye " + member.name + "! You've been quacking in this voicecall for "+ time_str)
        users.pop(user_index)
      else:
          print("I could not find a user.")
      
# -------------------------------------------------------------------------------
@client.command()
async def hello(ctx):
  await ctx.send("QUACK")

# pass_context: we need this to when communicating to the voice part of our bot
@client.command(pass_context = True)
async def join(ctx):      # ctx lets you send and recieve messages
  # If user is in vc, it will get the vc id, and will join it
  if (ctx.author.voice):
    channel = ctx.message.author.voice.channel
    await channel.connect()
    await ctx.send("Quack! Any grapes? :grapes:")

  # If we're not in a vc, tell user that you're not in a vc
  else:
    await ctx.send("Please join a quack channel! You must be in a quack channel to run this command!")

# Make discord bot leave a vc
@client.command(pass_content = True)

async def leave(ctx):
  # If the bot is in a voice channel, it will disconnect and send a message
  if (ctx.voice_client):
    await ctx.guild.voice_client.disconnect()
    await ctx.send("Quack! Going to buy some grapes. Goodbye :duck:")
  else:
    await ctx.send("I am not in a voice channel :scream:")

# Handles invalid commands
@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound): 
    await ctx.send("That's not an valid command Mr. Bill :woozy_face:")
  else:
    error

client.run(TOKEN)