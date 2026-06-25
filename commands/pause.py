from utils.draw import MusicUI


def setup(bot, get_player, card_prefix, _):

    @bot.command(name="пауза", help="Пауза")
    async def pause_cmd(ctx):
        player = get_player(ctx.guild.id)
        player.pause()
        await ctx.reply(embed=MusicUI.message("Пауза"))

    @bot.tree.command(name="пауза", description="Пауза")
    async def slash_pause(interaction):
        player = get_player(interaction.guild.id)
        player.pause()
        await interaction.response.send_message(embed=MusicUI.message("Пауза"))

    return pause_cmd
