def setup(bot, get_player, card_prefix, _):
    @bot.command(name='пауза', help='!пауза — поставить на паузу')
    async def pause_cmd(ctx):
        player = get_player(ctx.guild.id)
        player.pause()
        await ctx.reply(card_prefix("Пауза."))

    @bot.tree.command(name='пауза', description='Поставить воспроизведение на паузу')
    async def slash_pause(interaction):
        player = get_player(interaction.guild.id)
        player.pause()
        await interaction.response.send_message(card_prefix("Пауза."))

    return pause_cmd
