import discord

def setup(bot, get_player, card_prefix, _):
    @bot.command(name='очередь', help='!очередь — показать очередь')
    async def queue_cmd(ctx):
        player = get_player(ctx.guild.id)
        items = []
        try:
            q_items = list(player.queue._queue)
            for i, it in enumerate(q_items, 1):
                items.append(f"{i}. {getattr(it,'title', 'unknown')}")
        except Exception:
            pass
        if not items:
            await ctx.reply(card_prefix("Очередь пуста."))
            return
        embed = discord.Embed(title="🃏 Очередь", description="\n".join(items[:50]))
        await ctx.reply(embed=embed)

    @bot.tree.command(name='очередь', description='Показать очередь')
    async def slash_queue(interaction):
        player = get_player(interaction.guild.id)
        items = []
        try:
            q_items = list(player.queue._queue)
            for i, it in enumerate(q_items, 1):
                items.append(f"{i}. {getattr(it,'title', 'unknown')}")
        except Exception:
            pass
        if not items:
            await interaction.response.send_message(card_prefix("Очередь пуста."))
            return
        embed = discord.Embed(title="🃏 Очередь", description="\n".join(items[:50]))
        await interaction.response.send_message(embed=embed)

    return queue_cmd
