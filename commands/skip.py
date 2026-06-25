from utils.draw import MusicUI


def setup(bot, get_player, card_prefix, _):

    @bot.command(name="пропустить", help="Пропустить трек")
    async def skip_cmd(ctx):
        player = get_player(ctx.guild.id)
        player.skip()
        await ctx.reply(embed=MusicUI.message("Пропущено"))

    @bot.tree.command(name="пропустить", description="Пропустить")
    async def slash_skip(interaction):
        player = get_player(interaction.guild.id)
        player.skip()
        await interaction.response.send_message(embed=MusicUI.message("Пропущено"))

    return skip_cmd
