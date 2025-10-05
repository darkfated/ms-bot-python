import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from music.yt_utils import YTDLSource
from utils.checks import user_in_voice


def setup(bot, get_player, card_prefix, MAX_QUEUE_SIZE):
    @bot.command(name='играть', help='!play <запрос или ссылка> — добавить трек в очередь')
    async def play_cmd(ctx: commands.Context, *, query: str):
        if not user_in_voice(ctx):
            await ctx.reply(card_prefix("Вы должны находиться в голосовом канале, чтобы использовать эту команду."))
            return

        player = get_player(ctx.guild.id)

        try:
            qsize = player.queue.qsize()
        except Exception:
            qsize = 0
        if qsize >= MAX_QUEUE_SIZE:
            await ctx.reply(card_prefix(f"Очередь уже доверху (макс {MAX_QUEUE_SIZE})."))
            return

        try:
            await player.join_voice(ctx.author.voice.channel)
        except Exception as e:
            await ctx.reply(card_prefix(f"Не удалось подключиться к голосовому каналу: {e}"))
            return

        async with ctx.channel.typing():
            try:
                source = await YTDLSource.create_source(query, loop=bot.loop)
            except Exception as e:
                source = None
                print(f"[play] create_source exception: {e}")

        if source is None:
            await ctx.reply(card_prefix("Не удалось загрузить аудио по данной ссылке или запросу."))
            return

        await player.queue.put(source)
        await ctx.reply(card_prefix(f"Добавлено в очередь: **{source.title}**"))

    @app_commands.command(name="play", description="Проиграть трек или добавить в очередь")
    @app_commands.describe(query="Название или ссылка на трек")
    async def play_slash(interaction: discord.Interaction, query: str):
        user = interaction.user
        if not getattr(user, "voice", None) or not getattr(user.voice, "channel", None):
            await interaction.response.send_message(card_prefix("Вы должны находиться в голосовом канале."))
            return

        player = get_player(interaction.guild.id)

        try:
            qsize = player.queue.qsize()
        except Exception:
            qsize = 0
        if qsize >= MAX_QUEUE_SIZE:
            await interaction.response.send_message(card_prefix(f"Очередь уже доверху (макс {MAX_QUEUE_SIZE})."))
            return

        try:
            await player.join_voice(user.voice.channel)
        except Exception as e:
            await interaction.response.send_message(card_prefix(f"Не удалось подключиться: {e}"))
            return

        await interaction.response.defer()
        try:
            source = await YTDLSource.create_source(query, loop=bot.loop)
        except Exception as e:
            source = None
            print(f"[play_slash] create_source exception: {e}")

        if source is None:
            await interaction.followup.send(card_prefix("Не удалось загрузить трек."))
            return

        await player.queue.put(source)
        await interaction.followup.send(card_prefix(f"Добавлено в очередь: **{source.title}**"))

    bot.tree.add_command(play_slash)

    return play_cmd
