def setup(bot, get_player, card_prefix, _):
    @bot.command(name='пропустить', help='!пропустить — пропустить текущий трек')
    async def skip_cmd(ctx):
        player = get_player(ctx.guild.id)
        player.skip()
        await ctx.reply(card_prefix("Пропущено."))

    @bot.tree.command(name='пропустить', description='Пропустить текущий трек')
    async def slash_skip(interaction):
        player = get_player(interaction.guild.id)
        player.skip()
        await interaction.response.send_message(card_prefix("Пропущено."))

    return skip_cmd
