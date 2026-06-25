from utils.draw import MusicUI


def setup(bot, get_player, card_prefix, _):

    @bot.command(name="повтор", help="Повтор")
    async def repeat_cmd(ctx, mode: str = None):
        player = get_player(ctx.guild.id)

        if mode is None:
            player.repeat = not player.repeat
        else:
            player.repeat = mode.lower() in ("вкл", "on", "1", "true")

        await ctx.reply(embed=MusicUI.message(f"Повтор {'вкл' if player.repeat else 'выкл'}"))

    @bot.tree.command(name="повтор", description="Повтор")
    async def slash_repeat(interaction, mode: str = None):
        player = get_player(interaction.guild.id)

        if mode is None:
            player.repeat = not player.repeat
        else:
            player.repeat = mode.lower() in ("вкл", "on", "1", "true")

        await interaction.response.send_message(
            embed=MusicUI.message(f"Повтор {'вкл' if player.repeat else 'выкл'}")
        )

    return repeat_cmd
