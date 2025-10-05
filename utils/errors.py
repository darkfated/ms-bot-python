import logging
from discord.ext import commands
logger = logging.getLogger(__name__)

async def on_command_error(ctx, error):
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            try:
                await ctx.reply(f"🃏 Отсутствует аргумент: {error.param.name}")
            except Exception:
                pass
        elif isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CommandInvokeError):
            try:
                await ctx.reply(f"🃏 Ошибка при выполнении команды: {error.original}")
            except Exception:
                logger.exception("reply failed")
        else:
            try:
                await ctx.reply(f"🃏 Произошла ошибка: {error}")
            except Exception:
                logger.exception("reply failed")
    except Exception:
        logger.exception("Error in on_command_error")
