from utils.draw import MusicUI


def setup(bot, get_player, card_prefix, _):

    @bot.command(name="продолжить", help="Продолжить")
    async def resume_cmd(ctx):
        player = get_player(ctx.guild.id)
        player.resume()
        await ctx.reply(embed=MusicUI.message("Продолжено"))

    @bot.tree.command(name="продолжить", description="Продолжить")
    async def slash_resume(interaction):
        player = get_player(interaction.guild.id)
        player.resume()
        await interaction.response.send_message(embed=MusicUI.message("Продолжено"))

    return resume_cmd
