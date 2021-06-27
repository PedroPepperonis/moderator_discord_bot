from asyncio import sleep
import discord
from discord.ext import commands

from database.db import Database
from config import DATABASE_URL

db = Database(DATABASE_URL)


class Moderation(commands.Cog, name='модерация'):
    def __init__(self, bot):
        self.bot = bot
        self.word = []

    @commands.Cog.listener()
    async def on_message(self, message):
        result = db.get_ban_word(message.channel.id)
        for i in result:
            if message.content.startswith(i[0]) or message.content.find(i[0]):
                await message.delete()

    @commands.command(name='add',
                      help='Запрет на использование слов или команд в текстовом канале в котором была прописана команда'
                           '\n(причину указывать необязательно)')
    @commands.has_permissions(administrator=True)
    async def add(self, context, word, *, reason='Просто бан'):
        if db.banword_exists(context.channel.id, word):
            embed = discord.Embed(
                title='Ошибка',
                description=f'Слово {word} уже запрещенно в канале {context.channel.name}',
                color=0xE02B2B
            )
            message = await context.send(embed=embed)
            await sleep(4)
            await message.delete()
            await context.message.delete()
            return

        db.add_ban_word(context.guild.name, context.guild.id, context.channel.name, context.channel.id, word, reason)
        embed = discord.Embed(
            title='Успех',
            description=f'Теперь в {context.channel.name} запрещено использовать {word}',
            color=0xE02B2B
        )
        message = await context.send(embed=embed)
        await sleep(4)
        await message.delete()
        await context.message.delete()

    @commands.command(name='delete', help='Удаляет слово из запрещенных', aliases=['del'])
    @commands.has_permissions(administrator=True)
    async def delete(self, context, word):
        if db.banword_exists(context.channel.id, word):
            db.delete_ban_word(context.channel.id, word)
            embed = discord.Embed(
                title='Успех',
                description=f'Слово {word} теперь снова можно использовать в {context.channel.name}',
                color=0x42F56C
            )
            message = await context.send(embed=embed)
            await sleep(4)
            await message.delete()
            await context.message.delete()
            return

        embed = discord.Embed(
            title='Ошибка',
            description=f'Слова {word} нет в списке',
            color=0xE02B2B
        )
        message = await context.send(embed=embed)
        await sleep(4)
        await message.delete()
        await context.message.delete()

    @commands.command(name='clear', help='Удаляет сообщения')
    @commands.has_permissions(administrator=True)
    async def clear(self, context, amount=5):
        await context.channel.purge(limit=int(amount)+1)

    @commands.command(name='list',
                      help='Список слов или команд запрещенных в текстовом канале в котором была прописана команда')
    async def list(self, context):
        banword_list = db.get_ban_word(context.channel.id)
        embed = discord.Embed(
            title=f'Список запрещенных слов в {context.channel.name}',
            description='\n'.join(f'{word[0]}' for word in banword_list),
            color=0xE02B2B
        )
        message = await context.send(embed=embed)
        await sleep(10)
        await message.delete()
        await context.message.delete()


def setup(bot):
    bot.add_cog(Moderation(bot))
