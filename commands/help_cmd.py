def setup(bot, get_player, card_prefix, _):
    @bot.command(name='помощь', help='!помощь — список команд')
    async def help_cmd(ctx):
        lines = []
        for cmd in sorted(bot.commands, key=lambda c: c.name):
            if getattr(cmd, "hidden", False):
                continue
            name = cmd.name
            desc = cmd.help or ""
            lines.append(f"**{name}** — {desc}")
        if not lines:
            await ctx.reply(card_prefix("Команды не найдены."))
            return
        for i in range(0, len(lines), 12):
            await ctx.reply(card_prefix("Список команд:\n" + "\n".join(lines[i:i+12])))

    @bot.tree.command(name='помощь', description='Показать список команд')
    async def slash_help(interaction):
        lines = []
        for cmd in sorted(bot.commands, key=lambda c: c.name):
            if getattr(cmd, "hidden", False):
                continue
            name = cmd.name
            desc = cmd.help or ""
            lines.append(f"**{name}** — {desc}")
        if not lines:
            await interaction.response.send_message(card_prefix("Команды не найдены."))
            return
        out = "\n".join(lines[:50])
        await interaction.response.send_message(card_prefix("Список команд:\n") + out)

    return help_cmd
