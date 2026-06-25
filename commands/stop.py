from utils.draw import MusicUI


def setup(bot, get_player, card_prefix, _):

    @bot.command(name="стоп", help="Стоп")
    async def stop_cmd(ctx):
        player = get_player(ctx.guild.id)
        await player.stop()
        await ctx.reply(embed=MusicUI.message("Остановлено"))

    @bot.tree.command(name="стоп", description="Стоп")
    async def slash_stop(interaction):
        player = get_player(interaction.guild.id)
        await player.stop()
        await interaction.response.send_message(embed=MusicUI.message("Остановлено"))

    return stop_cmd
