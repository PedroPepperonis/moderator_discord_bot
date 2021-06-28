import os
import platform
import random

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot

from config import BOT_TOKEN, BOT_PREFIX, STATUSES


intents = discord.Intents.default()

bot = Bot(command_prefix=BOT_PREFIX, intents=intents)
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'Discord.py API version {discord.__version__}')
    print(f'Python version {platform.python_version()}')
    print(f'Running on: {platform.system()} {platform.release()} ({os.name})')
    print(' ')
    status_task.start()


@tasks.loop(minutes=1.0)
async def status_task():
    await bot.change_presence(activity=discord.Game(random.choice(STATUSES)))


if __name__ == '__main__':
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            extension = file[:-3]
            try:
                bot.load_extension(f'cogs.{extension}')
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f'{type(e).__name__}: {e}'
                print(f'Failed to load extension {extension}\n{exception}')


@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)


@bot.event
async def on_command_completion(context):
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    print(
        f"Executed {executed_command} command in {context.guild.name} {context.channel.name} "
        f"(ID: {context.message.guild.id}) by {context.message.author} (ID: {context.message.author.id})")


@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours %= 24
        embed = discord.Embed(
            title='Не так быстро',
            description='Пока ты не можешь использовать эту комманду',
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title='Ошибка',
            description='У вас нет доступа к данной комманде',
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title='Ошибка',
            description=str(error).capitalize(),
            color=0xE02B2B
        )
        await context.send(embed=embed)
    raise error

bot.run(BOT_TOKEN)
