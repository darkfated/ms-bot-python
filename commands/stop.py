import discord

def setup(bot, get_player, card_prefix, _):
    @bot.command(name='стоп', help='!стоп — остановить и очистить очередь')
    async def stop_cmd(ctx):
        player = get_player(ctx.guild.id)
        await player.stop()
        embed = discord.Embed(title="🃏 Остановлено", description="Очередь очищена, бот отключен.")
        await ctx.reply(embed=embed)

    @bot.tree.command(name='стоп', description='Остановить плеер и очистить очередь')
    async def slash_stop(interaction: discord.Interaction):
        player = get_player(interaction.guild.id)
        await player.stop()
        embed = discord.Embed(title="🃏 Остановлено", description="Очередь очищена, бот отключен.")
        await interaction.response.send_message(embed=embed)

    return stop_cmd
