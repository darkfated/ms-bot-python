from utils.draw import MusicUI


def setup(bot, get_player, card_prefix, _):

    @bot.command(name="очередь", help="Показать очередь")
    async def queue_cmd(ctx):
        player = get_player(ctx.guild.id)
        await ctx.reply(embed=MusicUI.queue(list(player.queue._queue)))

    @bot.tree.command(name="очередь", description="Очередь треков")
    async def slash_queue(interaction):
        player = get_player(interaction.guild.id)
        await interaction.response.send_message(embed=MusicUI.queue(list(player.queue._queue)))

    return queue_cmd
