import discord
from discord import app_commands
from music.yt_utils import YTDLSource
from utils.checks import user_in_voice

def setup(bot, get_player, card_prefix, MAX_QUEUE_SIZE):
    @bot.command(name='ситуация', help='Управление музыкальными подборками (плейлистами)')
    async def situation_cmd(ctx, action: str = None, name: str = None, *, query: str = None):
        if action is None:
            await ctx.reply(card_prefix("Использование: !ситуация <создать|добавить|включить|выключить|список|песни|удалить> ..."))
            return

        action = action.lower()
        player = get_player(ctx.guild.id)

        if action == 'создать':
            if not name:
                await ctx.reply(card_prefix("Укажи имя: !ситуация создать <имя>"))
                return
            ok = await player.create_situation(name)
            await ctx.reply(card_prefix(f"Ситуация **{name}** создана." if ok else "Не удалось создать (возможно, уже существует)."))
            return

        if action == 'добавить':
            if not name or not query:
                await ctx.reply(card_prefix("Использование: !ситуация добавить <имя> <ссылка/запрос>"))
                return
            async with ctx.channel.typing():
                src = await YTDLSource.create_source(query)
                if src is None:
                    await ctx.reply(card_prefix("Не удалось загрузить трек."))
                    return
                ok = await player.add_to_situation(name, src)
                await ctx.reply(card_prefix(f"Добавлено в ситуацию **{name}**: **{src.title}**" if ok else "Не удалось добавить (нет такой ситуации)."))
                return

        if action == 'включить':
            if not name:
                await ctx.reply(card_prefix("Укажи имя: !ситуация включить <имя>"))
                return
            if not user_in_voice(ctx):
                await ctx.reply(card_prefix("Ты должен находиться в голосовом канале."))
                return
            try:
                await player.join_voice(ctx.author.voice.channel)
            except Exception as e:
                await ctx.reply(card_prefix(f"Не удалось подключиться: {e}"))
                return
            ok = await player.start_situation(name)
            await ctx.reply(card_prefix(f"Ситуация **{name}** включена." if ok else "Не удалось включить (нет такой ситуация или она пуста)."))
            return

        if action == 'выключить':
            await player.stop_situation()
            await ctx.reply(card_prefix("Ситуация выключена. Очередь очищена."))
            return

        if action == 'список':
            names = player.list_situations()
            if not names:
                await ctx.reply(card_prefix("Ситуаций нет."))
                return
            embed = discord.Embed(title="🃏 Ситуации", description="\n".join(f"- {n}" for n in names))
            await ctx.reply(embed=embed)
            return

        if action == 'песни':
            if not name:
                await ctx.reply(card_prefix("Укажи имя: !ситуация песни <имя>"))
                return
            tracks = player.get_situation_tracks(name)
            if not tracks:
                await ctx.reply(card_prefix("Треков нет или такой ситуации нет."))
                return
            desc = "\n".join(f"{i+1}. {t.title}" for i, t in enumerate(tracks[:50]))
            embed = discord.Embed(title=f"🃏 Треки ситуации {name}", description=desc)
            await ctx.reply(embed=embed)
            return

        if action == 'удалить':
            if not name:
                await ctx.reply(card_prefix("Укажи имя: !ситуация удалить <имя>"))
                return
            ok = await player.delete_situation(name)
            await ctx.reply(card_prefix(f"Ситуация **{name}** удалена." if ok else "Не удалось удалить (возможно, нет такой ситуации)."))
            return

        await ctx.reply(card_prefix("Неизвестное действие. Использование: создать, добавить, включить, выключить, список, песни, удалить"))

    class SituationGroup(app_commands.Group):
        def __init__(self):
            super().__init__(name="ситуация", description="Управление ситуациями")

        @app_commands.command(name="создать", description="Создать ситуацию")
        async def create(self, interaction: discord.Interaction, name: str):
            player = get_player(interaction.guild.id)
            ok = await player.create_situation(name)
            await interaction.response.send_message(card_prefix(f"Ситуация **{name}** создана." if ok else "Не удалось создать (возможно, уже существует)."))

        @app_commands.command(name="добавить", description="Добавить трек в ситуацию")
        async def add(self, interaction: discord.Interaction, name: str, query: str):
            await interaction.response.defer()
            player = get_player(interaction.guild.id)
            src = await YTDLSource.create_source(query)
            if src is None:
                await interaction.followup.send(card_prefix("Не удалось загрузить трек."))
                return
            ok = await player.add_to_situation(name, src)
            await interaction.followup.send(card_prefix(f"Добавлено в ситуацию **{name}**: **{src.title}**" if ok else "Не удалось добавить (нет такой ситуации)."))

        @app_commands.command(name="включить", description="Включить ситуацию")
        async def start(self, interaction: discord.Interaction, name: str):
            user = interaction.user
            if not getattr(user, "voice", None) or not getattr(user.voice, "channel", None):
                await interaction.response.send_message(card_prefix("Вы должны находиться в голосовом канале."))
                return
            player = get_player(interaction.guild.id)
            try:
                await player.join_voice(user.voice.channel)
            except Exception as e:
                await interaction.response.send_message(card_prefix(f"Не удалось подключиться: {e}"))
                return
            ok = await player.start_situation(name)
            await interaction.response.send_message(card_prefix(f"Ситуация **{name}** включена." if ok else "Не удалось включить (нет такой ситуация или она пуста)."))

        @app_commands.command(name="выключить", description="Выключить текущую ситуацию")
        async def stop(self, interaction: discord.Interaction):
            player = get_player(interaction.guild.id)
            await player.stop_situation()
            await interaction.response.send_message(card_prefix("Ситуация выключена. Очередь очищена."))

        @app_commands.command(name="список", description="Показать ситуации")
        async def list_cmd(self, interaction: discord.Interaction):
            player = get_player(interaction.guild.id)
            names = player.list_situations()
            if not names:
                await interaction.response.send_message(card_prefix("Ситуаций нет."))
                return
            embed = discord.Embed(title="🃏 Ситуации", description="\n".join(f"- {n}" for n in names))
            await interaction.response.send_message(embed=embed)

        @app_commands.command(name="песни", description="Показать песни ситуации")
        async def songs(self, interaction: discord.Interaction, name: str):
            player = get_player(interaction.guild.id)
            tracks = player.get_situation_tracks(name)
            if not tracks:
                await interaction.response.send_message(card_prefix("Треков нет или такой ситуации нет."))
                return
            desc = "\n".join(f"{i+1}. {t.title}" for i, t in enumerate(tracks[:50]))
            embed = discord.Embed(title=f"🃏 Треки ситуации {name}", description=desc)
            await interaction.response.send_message(embed=embed)

        @app_commands.command(name="удалить", description="Удалить ситуацию")
        async def delete_cmd(self, interaction: discord.Interaction, name: str):
            player = get_player(interaction.guild.id)
            ok = await player.delete_situation(name)
            await interaction.response.send_message(card_prefix(f"Ситуация **{name}** удалена." if ok else "Не удалось удалить (возможно, нет такой ситуации)."))

    bot.tree.add_command(SituationGroup())
    return situation_cmd
