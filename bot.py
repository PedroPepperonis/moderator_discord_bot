import discord
import asyncio
from discord.ext import commands
    
bot_commands = ('-p', '-q', '-n', '-leave', '-j', '-play', '-skip')

client = commands.Bot(command_prefix='!')

# ну тут все ясно
@client.event
async def on_ready():
    print('Опять работа? {0}'.format(client.user))

# тестовая комманда
@client.command(aliases = ['ping'])
async def _ping(ctx):
    await ctx.send('pong')

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
# модерация чата
@client.listen('on_message')
async def on_message(message):
    if message.author == client.user:
        return

    if (message.channel.id == 702467354252279928):
        if message.content.startswith(bot_commands):
            await message.delete()
            print('Удалено сообщение {0.author}: {0.content}'.format(message))
            msg = await message.channel.send('Пиши в музло')
            await asyncio.sleep(10.0)
            await msg.delete()
        if message.author.id == 234395307759108106:
            await message.delete()

    if (message.channel.id == 698475260324085762):
        while True:
            if message.content.startswith(bot_commands):
                break
            if message.author.id == 234395307759108106:
                break
            else:
                print('Удалено сообщение {0.author}: {0.content}'.format(message))
                await message.delete()

client.run('ODE4NTA4Nzg3MDk4MzIwOTI3.YEZFtg.NYNzHi6h51lzJsxlrfq0OZrkFmU')

# 702467354252279928 чат
# 698475260324085762 музло