from utils.draw import MusicUI
from utils.checks import user_in_voice
from music.yt_utils import YTDLSource
import discord


def setup(bot, get_player, card_prefix, MAX_QUEUE_SIZE):

    @bot.command(name='играть', help='Добавить трек')
    async def play_cmd(ctx, *, query: str):

        if not user_in_voice(ctx):
            await ctx.reply(embed=MusicUI.message("Войди в голосовой канал"))
            return

        player = get_player(ctx.guild.id)

        if player.queue.qsize() >= MAX_QUEUE_SIZE:
            await ctx.reply(embed=MusicUI.message("Очередь переполнена"))
            return

        await player.join_voice(ctx.author.voice.channel)

        async with ctx.channel.typing():
            source = await YTDLSource.create_source(query, loop=bot.loop)

        if not source:
            await ctx.reply(embed=MusicUI.message("Не удалось загрузить трек"))
            return

        await player.queue.put(source)
        await ctx.reply(embed=MusicUI.message(f"Добавлено: {source.title}"))

    @bot.tree.command(name="play", description="Добавить трек")
    async def play_slash(interaction: discord.Interaction, query: str):

        user = interaction.user

        if not getattr(user, "voice", None) or not user.voice.channel:
            await interaction.response.send_message(embed=MusicUI.message("Войди в голосовой канал"))
            return

        player = get_player(interaction.guild.id)

        if player.queue.qsize() >= MAX_QUEUE_SIZE:
            await interaction.response.send_message(embed=MusicUI.message("Очередь переполнена"))
            return

        await player.join_voice(user.voice.channel)

        await interaction.response.defer()

        source = await YTDLSource.create_source(query, loop=bot.loop)

        if not source:
            await interaction.followup.send(embed=MusicUI.message("Не удалось загрузить"))
            return

        await player.queue.put(source)
        await interaction.followup.send(embed=MusicUI.message(f"Добавлено: {source.title}"))

    return play_cmd
