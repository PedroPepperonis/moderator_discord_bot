import asyncio
import re
import discord
from discord.ext import commands

from database.db import Database
from config import DATABASE_URL

db = Database(DATABASE_URL)


class Moderation(commands.Cog, name='модерация'):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        banned_words = db.get_banword(message.channel.id)
        banned_users = db.get_banned_users(message.channel.id)
        if not message.author.bot:
            for i in banned_words:
                if message.content.startswith(i[0]) or re.search(i[0], message.content):
                    await message.delete()
        for i in banned_users:
            if message.author.id == i[0]:
                await message.delete()

    @commands.command(name='add',
                      help='Запрет на использование слов или команд в текстовом канале в котором была прописана команда'
                           '\n(причину указывать необязательно)')
    @commands.has_permissions(administrator=True, manage_channels=True)
    async def add(self, context, word, *, reason='Просто бан'):
        if db.banword_exists(context.channel.id, word):
            embed = discord.Embed(
                title='Ошибка',
                description=f'Слово {word} уже запрещенно в канале {context.channel.name}',
                color=0xE02B2B
            )
            message = await context.send(embed=embed)
            await self.delete_messages(context, message, 4)
            return

        db.add_banword(context.guild.name, context.guild.id, context.channel.name, context.channel.id, word, reason)
        embed = discord.Embed(
            title='Успех',
            description=f'Теперь в {context.channel.name} запрещено использовать {word}',
            color=0xE02B2B
        )
        message = await context.send(embed=embed)
        await self.delete_messages(context, message, 4)

    @commands.command(name='delete', help='Удаляет слово из запрещенных', aliases=['del'])
    @commands.has_permissions(administrator=True, manage_channels=True)
    async def delete(self, context, word):
        if db.banword_exists(context.channel.id, word):
            db.delete_banword(context.channel.id, word)
            embed = discord.Embed(
                title='Успех',
                description=f'Слово {word} теперь снова можно использовать в {context.channel.name}',
                color=0x42F56C
            )
            message = await context.send(embed=embed)
            await self.delete_messages(context, message, 4)
            return

        embed = discord.Embed(
            title='Ошибка',
            description=f'Слова {word} нет в списке',
            color=0xE02B2B
        )
        message = await context.send(embed=embed)
        await self.delete_messages(context, message, 4)

    @commands.command(name='clear', help='Удаляет сообщения')
    @commands.has_permissions(administrator=True, manage_channels=True)
    async def clear(self, context, amount=5):
        await context.channel.purge(limit=int(amount)+1)

    @commands.command(name='block', help='Блок')
    @commands.has_permissions(manage_channels=True)
    async def block(self, context, member: discord.Member):
        await context.channel.set_permissions(member, send_messages=False)
        db.ban_user(context.guild.name, context.guild.id, context.channel.name, context.channel.id, member.id)
        embed = discord.Embed(
            title='Бан блять',
            description=f'Пользователю {member.display_name} теперь запрещено писать в {context.channel.name}',
            color=0xE02B2B
        )
        message = await context.send(embed=embed)
        await self.delete_messages(context, message, 10)

    @commands.command(name='unblock', help='Анблок')
    @commands.has_permissions(administrator=True, manage_channels=True)
    async def unblock(self, context, member: discord.Member):
        await context.channel.set_permissions(member, send_messages=True)
        db.unban_user(context.channel.id, member.id)
        embed = discord.Embed(
            title='Анбан блять',
            description=f'Пользователю {member.display_name} теперь разрешено писать в {context.channel.name}',
            color=0x42F56C
        )
        message = await context.send(embed=embed)
        await self.delete_messages(context, message, 10)

    @commands.command(name='list',
                      help='Список слов или команд запрещенных в текстовом канале в котором была прописана команда')
    async def list(self, context):
        banword_list = db.get_banword(context.channel.id)
        embed = discord.Embed(
            title=f'Список запрещенных слов в {context.channel.name}',
            description='\n'.join(f'{word[0]}' for word in banword_list),
            color=0xE02B2B
        )
        message = await context.send(embed=embed)
        await self.delete_messages(context, message, 10)

    @staticmethod
    async def delete_messages(context, message, time: int):
        await asyncio.sleep(time)
        await message.delete()
        await context.message.delete()


def setup(bot):
    bot.add_cog(Moderation(bot))
