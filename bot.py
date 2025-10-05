import os, importlib, logging, sys
from pathlib import Path
import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils.errors import on_command_error as handle_command_error

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX', '!')
MAX_QUEUE_SIZE = int(os.getenv('MAX_QUEUE_SIZE', '50'))

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("music-bot")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

players = {}

def get_player(guild_id: int):
    if guild_id not in players:
        from music.player import MusicPlayer
        players[guild_id] = MusicPlayer(bot, guild_id)
        logger.info("Created MusicPlayer for guild %s", guild_id)
    return players[guild_id]

def card_prefix(text: str) -> str:
    return f"🃏 {text}"

@bot.event
async def on_ready():
    logger.info("Bot ready: %s (id=%s)", bot.user, bot.user.id)
    try:
        await bot.tree.sync()
        logger.info("Slash commands synced")
    except Exception:
        logger.exception("Slash sync failed")

@bot.event
async def on_voice_state_update(member: discord.Member, before, after):
    if member == bot.user:
        guild = member.guild
        pl = players.get(guild.id)
        if pl:
            if before.channel is not None and after.channel is None:
                await pl.stop()
            elif before.channel is not None and after.channel is not None and before.channel != after.channel:
                await pl.stop()

@bot.event
async def on_command_error(ctx, error):
    try:
        await handle_command_error(ctx, error)
    except Exception:
        logger.exception("Error in handle_command_error")
        try:
            await ctx.reply(card_prefix("Произошла ошибка при обработке команды — проверьте логи."))
        except Exception:
            pass

commands_path = Path(__file__).parent / "commands"
for file in commands_path.iterdir():
    if file.is_file() and file.suffix == ".py" and file.stem != "__init__":
        mod_name = f"commands.{file.stem}"
        try:
            module = importlib.import_module(mod_name)
            if hasattr(module, "setup"):
                module.setup(bot, get_player, card_prefix, MAX_QUEUE_SIZE)
                logger.info("Loaded module %s", mod_name)
        except Exception:
            logger.exception("Failed to load %s", mod_name)

if TOKEN is None:
    logger.error("DISCORD_TOKEN not set")
else:
    bot.run(TOKEN)
