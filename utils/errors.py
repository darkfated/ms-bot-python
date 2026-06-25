import logging
from discord.ext import commands

logger = logging.getLogger(__name__)


async def on_command_error(ctx, error):

    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("🎵 Не хватает аргумента")

        elif isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.CommandInvokeError):
            await ctx.reply("🎵 Ошибка выполнения команды")

        else:
            await ctx.reply(f"🎵 Ошибка: {error}")

    except Exception:
        logger.exception("error handler failed")
