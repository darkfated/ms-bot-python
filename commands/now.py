from utils.draw import MusicUI


def setup(bot, get_player, card_prefix, _):

    @bot.command(name="сейчас", help="Показать текущий трек")
    async def now_cmd(ctx):
        player = get_player(ctx.guild.id)
        await ctx.reply(embed=MusicUI.now(player.current))

    @bot.tree.command(name="сейчас", description="Текущий трек")
    async def slash_now(interaction):
        player = get_player(interaction.guild.id)
        await interaction.response.send_message(embed=MusicUI.now(player.current))

    return now_cmd
