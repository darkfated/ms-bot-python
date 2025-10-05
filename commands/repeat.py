def setup(bot, get_player, card_prefix, _):
    @bot.command(name='повтор', help='!повтор [вкл/выкл] — переключить повтор')
    async def repeat_cmd(ctx, mode: str = None):
        player = get_player(ctx.guild.id)
        if mode is None:
            player.repeat = not player.repeat
        else:
            player.repeat = mode.lower() in ('вкл','on','да','true','1')
        await ctx.reply(card_prefix(f"Повтор {'включён' if player.repeat else 'выключен'}"))

    @bot.tree.command(name='повтор', description='Включить/выключить повтор')
    async def slash_repeat(interaction, mode: str = None):
        player = get_player(interaction.guild.id)
        if mode is None:
            player.repeat = not player.repeat
        else:
            player.repeat = mode.lower() in ('вкл','on','да','true','1')
        await interaction.response.send_message(card_prefix(f"Повтор {'включён' if player.repeat else 'выключен'}"))

    return repeat_cmd
