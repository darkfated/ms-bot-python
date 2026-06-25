import discord


class MusicUI:

    @staticmethod
    def base(title: str, desc: str = ""):
        return discord.Embed(
            title=f"🎵 {title}",
            description=desc,
            color=discord.Color.blurple()
        )

    @staticmethod
    def now(track):
        if not track:
            return MusicUI.base(
                "Сейчас ничего не играет",
                "Используйте команду, чтобы добавить музыку"
            )

        title = getattr(track, "title", "Unknown")
        return MusicUI.base("Сейчас играет", f"**{title}**")

    @staticmethod
    def queue(items):
        if not items:
            return MusicUI.base("Очередь пуста")

        lines = []
        for i, t in enumerate(list(items)[:30], start=1):
            title = getattr(t, "title", "Unknown")
            lines.append(f"{i}. {title}")

        return MusicUI.base("Очередь", "\n".join(lines))

    @staticmethod
    def message(text: str):
        return MusicUI.base("Система", text)

    @staticmethod
    def help():

        embed = MusicUI.base(
            "Музыкальный бот",
            "Бот для воспроизведения музыки из YouTube.\n"
            "Поиск треков по названию или ссылке.\n\n"
            "📌 Большинство команд работают только в голосовом канале."
        )

        embed.add_field(
            name="▶️ Музыка",
            value=(
                "`%играть <название или ссылка>` - добавить трек в очередь\n"
                "`%сейчас` - что играет сейчас\n"
                "`%очередь` - список треков в очереди\n"
                "`%пропустить` - переключить трек\n"
                "`%стоп` - остановить музыку и выйти"
            ),
            inline=False
        )

        embed.add_field(
            name="⏯ Управление",
            value=(
                "`%пауза` - поставить на паузу\n"
                "`%продолжить` - возобновить воспроизведение\n"
                "`%повтор [вкл/выкл]` - зациклить очередь"
            ),
            inline=False
        )

        embed.add_field(
            name="🎭 Ситуации",
            value=(
                "Это плейлист, который можно сохранять и запускать.\n\n"
                "`%ситуация создать <имя>` - создать плейлист\n"
                "`%ситуация добавить <имя> <трек>` - добавить трек\n"
                "`%ситуация включить <имя>` - запустить плейлист\n"
                "`%ситуация список` - список всех плейлистов\n"
                "`%ситуация песни <имя>` - показать треки\n"
                "`%ситуация удалить <имя>` - удалить плейлист"
            ),
            inline=False
        )

        return embed

