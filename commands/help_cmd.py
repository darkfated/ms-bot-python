from utils.draw import MusicUI


def setup(bot, get_player, card_prefix, _):

    @bot.command(name="инфо", help="Показать список команд")
    async def help_cmd(ctx):
        await ctx.reply(embed=MusicUI.help())

    @bot.tree.command(name="инфо", description="Показать список команд")
    async def slash_help(interaction):
        await interaction.response.send_message(embed=MusicUI.help())

    return help_cmd
