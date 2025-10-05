import discord

def setup(bot, get_player, card_prefix, _):
    try:
        bot.remove_command('resume')
    except Exception:
        pass

    @bot.command(name='продолжить', aliases=['resume'], help='!продолжить — возобновить воспроизведение')
    async def resume_cmd(ctx):
        player = get_player(ctx.guild.id)
        player.resume()
        await ctx.reply(card_prefix("Возобновление воспроизведения."))

    @bot.tree.command(name='продолжить', description='Возобновить воспроизведение')
    async def slash_resume(interaction: discord.Interaction):
        player = get_player(interaction.guild.id)
        player.resume()
        await interaction.response.send_message(card_prefix("Возобновление воспроизведения."))

    return resume_cmd
