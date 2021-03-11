import discord
import asyncio
from discord.ext import commands
    
bot_commands = ('-p', '-q', '-n', '-leave', '-j', '-play', '-skip')

client = commands.Bot(command_prefix='!')

# ну тут все ясно
@client.event
async def on_ready():
    print('Опять работа? {0}'.format(client.user))

# очистка чата
@client.command()
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit = amount + 1)

# кик
"""
@client.command()
async def kick(ctx, member: discord.Member, *, reason = None):
    if (member == client.user):
        await ctx.send('Соси жопу')
    else:
        await member.kick(reason=reason)
        await ctx.send(f'{member} был кикнут с сервера по причине: {reason}')
"""

# channel id
"""
@client.command()
async def get_channel(ctx, *, given_name = None):
    channel = discord.utils.get(ctx.guild.channels, name=given_name)
    channel_name = channel.name
    await ctx.send(channel_name)
"""

# модерация чата (общение)
@client.listen('on_message')
async def on_chat_channel(message):
    if (message.channel.id == 702467354252279928):
        if message.content.startswith(bot_commands):
            print('{0.channel.name}: {0.author}: {0.content}'.format(message))
            
            await message.delete()
            
            msg = await message.channel.send('Пиши в музло!!!')
            
            await asyncio.sleep(6.0)
            await msg.delete()

        if message.author.id == 234395307759108106: # id бота 
            await message.delete()

# модерация чата (музыка)
@client.listen('on_message')
async def on_music_channel(message):
    if (message.channel.id == 698475260324085762):
        if (not(message.content.startswith(bot_commands)) and message.author.id != 234395307759108106): # id бота
            print('{0.channel.name}: {0.author}: {0.content}'.format(message))
            await message.delete()
                
@client.listen('on_message')
async def on_ping(member: discord.Member):
    member.kick()


client.run('ODE4NTA4Nzg3MDk4MzIwOTI3.YEZFtg.z-fiiIcfPUBR2AsoDb1ephFfWrw')

# 702467354252279928 чат
# 698475260324085762 музло