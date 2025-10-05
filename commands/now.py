import discord

def setup(bot, get_player, card_prefix, _):
    @bot.command(name='сейчас', help='!сейчас — показать текущий трек')
    async def now_cmd(ctx):
        player = get_player(ctx.guild.id)
        if player.current:
            embed = discord.Embed(title="🃏 Сейчас играет", description=f"**{player.current.title}**")
            await ctx.reply(embed=embed)
        else:
            await ctx.reply(card_prefix("Сейчас ничего не играет."))

    @bot.tree.command(name='сейчас', description='Показать текущий трек')
    async def slash_now(interaction):
        player = get_player(interaction.guild.id)
        if player.current:
            embed = discord.Embed(title="🃏 Сейчас играет", description=f"**{player.current.title}**")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(card_prefix("Сейчас ничего не играет."))

    return now_cmd
